# Choropleth

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import pyproj
import area
from area import area

in_dir = "multi_page_app/data"
borough_names = pd.read_csv((f'{in_dir}/{"boroughs.csv"}'))
cycle_parking_data = pd.read_csv((f'{in_dir}/{"cycle_parking_data.csv"}'))
borough_count = pd.read_csv((f'{in_dir}/{"borough_count.csv"}'))
gdf_boroughpoly = gpd.read_file(f'{in_dir}/{"borough_geometry.geojson"}')

borough_names['name'] = borough_names['name'].replace(['Lewishaw', "Wandworth"
                                                       ], ["Lewisham",
                                                           "Wandsworth"])


gdf_boroughpoly['name'] = gdf_boroughpoly['name'].replace(['Wandworth',
                                                          "Lewishaw"],
                                                          ['Wandsworth',
                                                          "Lewisham"])

gdf_boroughpoly.crs = "EPSG:27700"  # original crs of cleaned geodata
gdf_boroughpoly["area"] = gdf_boroughpoly.geometry.area / 1000**2

# Convert df so true and false are 1 and 0

ft = {False: 0, True: 1}
cycle_parking_data['PRK_COVER'] = cycle_parking_data['PRK_COVER'].replace(ft)
cycle_parking_data['PRK_SECURE'] = cycle_parking_data['PRK_SECURE'].replace(ft)
cycle_parking_data['PRK_LOCKER'] = cycle_parking_data['PRK_LOCKER'].replace(ft)

# Convert df structure
df_grouped_COVER = cycle_parking_data.groupby(by="BOROUGH")['PRK_COVER'].sum(
).to_frame()

df_grouped_SECURE = cycle_parking_data.groupby(by="BOROUGH")['PRK_SECURE'].sum(
).to_frame()

df_grouped_LOCKER = cycle_parking_data.groupby(by="BOROUGH")['PRK_LOCKER'].sum(
).to_frame()


borough_count_alpha = borough_count.sort_values('name')
borough_count_alpha.rename(columns={'name': 'BOROUGH', 'count': 'Total'},
                           inplace=True)
df_grouped = df_grouped_COVER.merge(
    df_grouped_SECURE, how='left', left_on="BOROUGH",
    right_on="BOROUGH").merge(
        df_grouped_LOCKER, how='left', left_on="BOROUGH",
        right_on="BOROUGH").merge(
            borough_count_alpha, how='right', left_on="BOROUGH",
            right_on="BOROUGH")

df_grouped = pd.concat([df_grouped], axis=1)
df_grouped['PRK_COVER_PROP'] = df_grouped['PRK_COVER'] / df_grouped['Total']
df_grouped['PRK_SECURE_PROP'] = df_grouped['PRK_SECURE'] / df_grouped['Total']
df_grouped['PRK_LOCKER_PROP'] = df_grouped['PRK_LOCKER'] / df_grouped['Total']

max_cover_prop = df_grouped.max()['PRK_COVER_PROP']
max_secured_prop = df_grouped.max()['PRK_SECURE_PROP']
max_locker_prop = df_grouped.max()['PRK_LOCKER_PROP']

df_grouped['BOROUGH'] = df_grouped['BOROUGH'].replace(["Westminster"],
                                                      ["City of Westminster"])
df_grouped['BOROUGH'] = df_grouped['BOROUGH'].replace(
    ['Kingston upon Thames', "Richmond upon Thames"], ['Kingston Upon Thames',
                                                       "Richmond Upon Thames"])
df_grouped = df_grouped.sort_values('BOROUGH').reset_index()
gdf_boroughpoly = gdf_boroughpoly.sort_values('name').reset_index()
df_grouped = df_grouped.drop('index', axis=1)
gdf_boroughpoly = gdf_boroughpoly.drop('index', axis=1)

gdf_boroughpoly.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

df_grouped['PRK_COVER_DENS'] = df_grouped['PRK_COVER'] / gdf_boroughpoly[
    "area"]
df_grouped['PRK_SECURE_DENS'] = df_grouped['PRK_SECURE'] / gdf_boroughpoly[
    "area"]
df_grouped['PRK_LOCKER_DENS'] = df_grouped['PRK_LOCKER'] / gdf_boroughpoly[
    "area"]
max_cover_dens = df_grouped.max()['PRK_COVER_DENS']
max_secured_dens = df_grouped.max()['PRK_SECURE_DENS']
max_locker_dens = df_grouped.max()['PRK_LOCKER_DENS']

df_grouped['TOTAL_DENS'] = df_grouped['Total'] / gdf_boroughpoly["area"]
max_total_dens = df_grouped.max()['TOTAL_DENS']

all_options = {
    'Density': ["Locker", "Secured", "Cover", "All bike racks"],
    'Proportion': ["Locker", "Secured", "Cover"]
}


def app4_layout():
    return html.Div([
        html.H4(
            'Density distribution and proportion of bike racks in all boroughs'
            ),
        html.P("Select a rack type:"),
        dbc.RadioItems(id='rack_type', inline=True),
        html.P(""),
        html.P(
         "Proportion (number/total number) or Density (number/(Area in km^2)):"
            ),
        dcc.Dropdown(
            id="prop_or_density",
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            value="Density",          
        ),
        dcc.Graph(id="choropleth_graph", style={"margin": "auto"}),
    ], lang="en")


@dash.callback(
    Output('rack_type', 'options'),
    Input('prop_or_density', 'value'))
def set_button_options(prop_or_density):
    return [{'label': i, 'value': i} for i in all_options[prop_or_density]]


@dash.callback(
    Output('rack_type', 'value'),
    Input('rack_type', 'options'))
def set_initial_button_value(available_options):
    return available_options[0]['value']


@dash.callback(
    Output("choropleth_graph", "figure"), 
    Input("rack_type", "value"),
    Input("prop_or_density", "value"))
def display_choropleth(rack_type, prop_or_density):
    if prop_or_density == "Proportion":

        if rack_type == "Locker":
            selected_density = 'PRK_LOCKER_PROP'
            max = max_locker_prop
            title = "Proportion of racks" + '<br>' + "that are lockers"  
        elif rack_type == "Cover":
            selected_density = 'PRK_COVER_PROP'
            max = max_cover_prop
            title = "Proportion of racks" + '<br>' + "that have a cover"
        elif rack_type == "Secured":
            selected_density = 'PRK_SECURE_PROP'
            max = max_secured_prop
            title = "Proportion of racks" + '<br>' + "that are secured"

    elif prop_or_density == "Density":
        if rack_type == "Locker":
            selected_density = 'PRK_LOCKER_DENS'
            max = max_locker_dens
            title = "Density of racks" + '<br>' + "that are lockers"
        elif rack_type == "Cover":
            selected_density = 'PRK_COVER_DENS'
            max = max_cover_dens
            title = "Density of racks" + '<br>' + "that have a cover"
        elif rack_type == "Secured":
            selected_density = 'PRK_SECURE_DENS'
            max = max_secured_dens
            title = "Density of racks" + '<br>' + "that are secured"
        elif rack_type == "All bike racks":
            selected_density = 'TOTAL_DENS'
            max = max_total_dens
            title = "Density of all <br> bike racks"

    fig = px.choropleth(df_grouped, geojson=gdf_boroughpoly,
                        color=selected_density,
                        locations="BOROUGH", featureidkey="properties.name",
                        projection="mercator",
                        hover_name="BOROUGH", custom_data=['BOROUGH',
                                                           selected_density],
                        range_color=[0, max])

    fig.update_traces(hovertemplate="<br>".join(["%{customdata[0]}",
                      str(prop_or_density) + ":" + "%{customdata[1]:.4f}"]),
                      marker_line_width=1)
    fig.update_geos(
        fitbounds="locations", showframe=False,
        visible=False)
    fig.update_layout(margin=dict(l=60, r=60, t=50, b=50),
                      dragmode=False,
                      coloraxis_colorbar=dict(title=title))

    return fig
