# Line Charts Reports

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

import os
data_dir = os.path.abspath(os.path.dirname(__file__))
in_dir = data_dir + "/data"
borough_names = pd.read_csv((f'{in_dir}/{"boroughs.csv"}'))
cycle_parking_data = pd.read_csv((f'{in_dir}/{"cycle_parking_data.csv"}'))

borough_names['name'] = borough_names['name'].replace(
    ['City of Westminster', "Lewishaw", "Wandworth"],
    ['Westminster', "Lewisham", "Wandsworth"])


def random_dates(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')


start = pd.to_datetime('2020-01-01')
end = pd.to_datetime('2023-01-01')

df_report_dates = pd.DataFrame(random_dates(start, end, 60000),
                               columns=['REPORT_DATE'])

df = pd.DataFrame(cycle_parking_data, columns=["FEATURE_ID", "BOROUGH"])
df_random_FEATURE_ID = df.sample(n=60000, replace=True, ignore_index=True)
Reports_df = pd.concat([df_report_dates, df_random_FEATURE_ID], axis=1)
Reports_df['BOROUGH'] = df['BOROUGH'].replace(
    ['Kingston upon Thames', 'Richmond upon Thames'],
    ['Kingston Upon Thames', 'Richmond Upon Thames'])

Reports_df['date'] = pd.to_datetime(Reports_df['REPORT_DATE']).dt.date
Reports_df['time'] = pd.to_datetime(Reports_df['REPORT_DATE']).dt.time
Reports_df['date'] = pd.to_datetime(Reports_df['date'])

# Set time of day based on your specified time frames
Reports_df.loc[Reports_df.set_index('REPORT_DATE').index.indexer_between_time(
    '4:00', '11:59'), 'd_time'] = 'Morning'
Reports_df.loc[Reports_df.set_index('REPORT_DATE').index.indexer_between_time(
    '12:00', '16:59'), 'd_time'] = 'Afternoon'
Reports_df.loc[Reports_df.set_index('REPORT_DATE').index.indexer_between_time(
    '17:00', '19:59'), 'd_time'] = 'Evening'
Reports_df.loc[Reports_df.set_index('REPORT_DATE').index.indexer_between_time(
    '20:00', '3:59'), 'd_time'] = 'Night'

Reports_df["Count"] = 1
borough_names.loc["name"] = [0, "All Boroughs"]
borough_names['name'] = borough_names['name'].replace(['Westminster'],
                                                      ['City of Westminster'])
Reports_df['BOROUGH'] = Reports_df['BOROUGH'].replace(['Westminster'],
                                                      ['City of Westminster'])


def app3_layout():
    return dbc.Container(children=[
        html.Div(lang="en", children=[
            html.H4('Investigating Theft Reports'),
            dcc.Dropdown(
                id="dropdown_year",
                options=[2022, 2021, 2020],
                value=2022,
                clearable=False,
                className="dbc",
                ),
            dbc.Checklist([
                {
                    "label": 'All Day',
                    "value": "All Day"
                },
                {
                    "label": 'Morning',
                    "value": "Morning",
                },
                {
                    "label": 'Afternoon',
                    "value": "Afternoon",
                },
                {
                    "label": 'Evening',
                    "value": "Evening",
                },
                {
                    "label": 'Night',
                    "value": "Night",
                }
            ],  id="tick_times",
                value=['All Day'],
                inline=True
            ),
            dcc.Graph(id="report_graph")]),
        html.Div(lang="en", children=[
                     html.P(
                        "Morning: 4:00AM-11:59AM | "
                        "Afternoon: 12:00PM-16:59PM |"
                        "Evening: 17:00PM-19:59PM "
                        "| Night: 20:00PM-3:59AM")
        ]),
    ])


firstyearpd = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
secondyearpd = pd.date_range(start="2021-01-01", end="2021-12-31", freq="D")
thirdyearpd = pd.date_range(start="2022-01-01", end="2022-12-31", freq="D")


@dash.callback(
    Output("report_graph", "figure"), 
    Input("dropdown_borough", "value"),
    Input("dropdown_year", "value"),
    Input("tick_times", "value"))
def update_report_chart(dropdown_borough, dropdown_year, tick_times):
    if dropdown_year == 2020:
        display_dates = firstyearpd
    elif dropdown_year == 2021:
        display_dates = secondyearpd
    elif dropdown_year == 2022:
        display_dates = thirdyearpd

    plot_df = pd.DataFrame(display_dates, columns=['Date'])

    if len(tick_times) > 0:
        for x in tick_times:
            if x == "All Day":
                if dropdown_borough == "All Boroughs":
                    temp_df = (Reports_df[Reports_df.date.dt.year == dropdown_year])
                    temp_df = temp_df.groupby(by="date")['Count'].sum()
                    temp_df = temp_df.to_frame().reset_index()
                    temp_df = temp_df.set_index('date')
                    temp_df = temp_df.reindex(display_dates, fill_value=0)
                    temp_df = temp_df.reset_index()
                    plot_df[x] = temp_df["Count"]
                else:
                    temp_df = (Reports_df[Reports_df.date.dt.year == dropdown_year])
                    temp_df = temp_df.loc[temp_df['BOROUGH'] == dropdown_borough]
                    temp_df = temp_df.groupby(by="date")['Count'].sum()
                    temp_df = temp_df.to_frame().reset_index()
                    temp_df = temp_df.set_index('date').reindex(display_dates,fill_value=0)
                    temp_df = temp_df.reset_index()
                    plot_df[x] = temp_df["Count"]
            else:
                if dropdown_borough == "All Boroughs":
                    temp_df = Reports_df.loc[(Reports_df['d_time'] == x)]
                    temp_df = temp_df.sort_values('date')
                    temp_df = temp_df.groupby(by="date")['Count'].sum()
                    temp_df = temp_df.to_frame().reset_index()
                    temp_df = temp_df.set_index('date').reindex(display_dates,fill_value=0)
                    temp_df = temp_df.reset_index()
                    display_count = temp_df["Count"]
                    plot_df[x] = display_count
                else:
                    temp_df = Reports_df.loc[(Reports_df['BOROUGH'] == dropdown_borough)
                                 & (Reports_df['d_time'] == x)].sort_values('date')
                    temp_df = temp_df.groupby(by="date")['Count'].sum()
                    temp_df = temp_df.to_frame().reset_index()
                    temp_df = temp_df.set_index('date').reindex(display_dates,fill_value=0)
                    temp_df = temp_df.reset_index()
                    plot_df[x] = temp_df["Count"]

    plot_df = pd.melt(plot_df, id_vars='Date', value_vars=plot_df.columns)
    plot_df.rename(columns={"variable": "Time of Day",
                            "value": "Number of Reports"}, inplace=True)

    fig = px.line(plot_df, x='Date', y='Number of Reports', color='Time of Day'
                  )

    fig.update_layout(title="Number of & Time of Reports in<br>" +
                      dropdown_borough + ":", showlegend=True)
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    fig.update_layout(title_x=0.5)

    return fig
