# Barcharts

import dash
from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from multi_page_app.app4 import df_grouped


in_dir = "multi_page_app/data"
borough_names = pd.read_csv((f'{in_dir}/{"boroughs.csv"}'))
cycle_parking_data = pd.read_csv((f'{in_dir}/{"cycle_parking_data.csv"}'))


borough_names['name'] = borough_names['name'].replace(
    ["Lewishaw", "Wandworth"], ["Lewisham", "Wandsworth"]
    )

df_grouped = (df_grouped)
london_total = (df_grouped["Total"].sum())

PRK_COVER_count = int((df_grouped["PRK_COVER"]).sum())
PRK_SECURE_count = int((df_grouped["PRK_SECURE"]).sum())
PRK_LOCKER_count = int((df_grouped["PRK_LOCKER"]).sum())

borough_names.loc["name"] = [0, "All Boroughs"]


def app2_layout():
    return dbc.Container(fluid=True, children=[html.Div(lang="en", children=[
        html.H4('Types of Bike Racks in London Boroughs'),
        dbc.RadioItems(
            id='quant_percent',
            options=["Quantity", "Percentage out of total"],
            value="Quantity",
            inline=True,
        ),
        dcc.Graph(id="bar_graph")]
        ),
    ],

    )


@dash.callback(
    Output("bar_graph", "figure"),
    Input("dropdown_borough", "value"),
    Input("quant_percent", "value"))
def update_bar_chart(BOROUGH, quant_percent):
    if quant_percent == "Quantity":
        if BOROUGH == "All Boroughs":
            y_data = [PRK_COVER_count, PRK_SECURE_count,
                      PRK_LOCKER_count, london_total]
        else:
            # Counting the number of each type of rack
            cover = df_grouped.loc[df_grouped['BOROUGH'] ==
                                   BOROUGH, "PRK_COVER"].item()
            secured = df_grouped.loc[df_grouped['BOROUGH'] ==
                                     BOROUGH, "PRK_SECURE"].item()
            locker = df_grouped.loc[df_grouped['BOROUGH'] ==
                                    BOROUGH, "PRK_LOCKER"].item()
            total = df_grouped.loc[df_grouped['BOROUGH'] ==
                                   BOROUGH, "Total"].item()
            y_data = [cover, secured, locker, total]
        title_final = ("Type of & Total Quantity<br>of Bike Racks in<br>" + 
                       BOROUGH + ":<br>")
        y_axis_label = "Quantity of Bike Racks"
        x_labels = ["Covered", "Secured", "Locker", "Total"]

    elif quant_percent == "Percentage out of total":
        if BOROUGH == "All Boroughs":
            y_data = [PRK_COVER_count/london_total,
                      PRK_SECURE_count/london_total,
                      PRK_LOCKER_count/london_total]
        else:
            cover_percent = df_grouped.loc[df_grouped['BOROUGH'] == BOROUGH,
                                           "PRK_COVER_PROP"].item() * 100
            secured_percent = df_grouped.loc[df_grouped['BOROUGH'] == BOROUGH,
                                             "PRK_SECURE_PROP"].item() * 100
            locker_percent = df_grouped.loc[df_grouped['BOROUGH'] == BOROUGH,
                                            "PRK_LOCKER_PROP"].item() * 100
            y_data = [cover_percent, secured_percent, locker_percent]

        title_final = ("Percentage Make-up of<br>Different Bike Racks in<br>" +
                       BOROUGH + ":<br>")
        y_axis_label = "Percentage (%)"
        x_labels = ["Covered", "Secured", "Locker"]

    fig = px.bar(x=x_labels,
                 y=y_data,
                 title=title_final,
                 text=y_data,
                 labels=dict(x="Types of Bike Racks", y=y_axis_label))
    fig.update_xaxes(type='category')
    fig.update_layout(title_x=0.5)

    if quant_percent == "Quantity":
        if BOROUGH == "All Boroughs":
            fig.update_traces(texttemplate='%{text}', textposition='outside',
                              hovertemplate=("%{text}"))
            fig.update_yaxes(range=[0, (max(y_data) + 2000)])
        else:
            fig.update_traces(texttemplate='%{text}', textposition='outside',
                              hovertemplate=("%{text}"))
            fig.update_yaxes(range=[0, (max(y_data) + 500)])
    elif quant_percent == "Percentage out of total":
        fig.update_traces(texttemplate='%{text:.4f}%', textposition='outside',
                          hovertemplate=("%{text:.4f}%"))
        fig.update_yaxes(range=[0, max(y_data) + 0.5])

    return fig