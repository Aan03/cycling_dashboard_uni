import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import geopandas as gpd

gdf = gpd.read_file('multi_page_app/data/cycle_parking.json')
df1 = gdf[['FEATURE_ID', 'BOROUGH', 'PRK_COVER', 'PRK_SECURE', 'PRK_LOCKER']]
geoms = gdf['geometry'].tolist()
long_center = 0
lat_center = 0
long_list = []
lat_list = []
for geom in geoms:
    long_list.append(geom.x)
    lat_list.append(geom.y)
    long_center += geom.x
    lat_center += geom.y
df1['lat'] = lat_list
df1['long'] = long_list
lat_center /= len(geoms)
long_center /= len(geoms)

map_layout = dict(
    autosize=True,
    responsive=True,
    # height="100vh",
    # font=dict(color="#191A1A"),
    # titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    hovermode="closest",
    # plot_bgcolor='#fffcfc',
    # paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    mapbox=dict(
        style="open-street-map",
        center=dict(
            lon=long_center,
            lat=lat_center
        ),
        zoom=9.5,
    )
)


def map_app_layout():
    title = "Map showing location of all bike racks in London"
    return dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(html.H1(title),
                    width="100%", align="centre", md=10, xs=8, sm=8),
            dbc.Col(html.H5("Filter Racks"),
                    align="centre", width="100%", md=1, xs=1, sm=1),
        ]),
        dbc.Row(children=[
            dbc.Col(dcc.Graph(id='main_map', style={'height': '85vh'}),
                    width="auto", align="centre", md=10, xs=8, sm=8),
            dbc.Col(dbc.Checklist(
                [{
                    'label': 'Covered',
                    'value': 'COVER',
                },
                    {
                    'label': 'Secure',
                    'value': 'SECURE',
                },
                    {
                    'label': 'Locker',
                    'value': 'LOCKER',
                }],
                id='selection',
                value=[]), align="centre", width="100%", md=1, xs=1, sm=1)
                ])
                ], fluid=True)


@dash.callback(Output("main_map", "figure"),
               Input("selection", "value"))
def update_df(selection):
    df2 = df1
    if len(selection) > 0:
        for x in selection:
            if x == "COVER":
                df2 = (df2.loc[df2['PRK_COVER'] == "TRUE"])
            if x == "SECURE":
                df2 = (df2.loc[df2['PRK_SECURE'] == "TRUE"])
            if x == "LOCKER":
                df2 = (df2.loc[df2['PRK_LOCKER'] == "TRUE"])
    hov = "ID: {}, Borough: {}, Covered: {}, Secure: {}, Is a bike locker: {} "
    figure = {"data": [{"type": "scattermapbox",
                        "lat": list(df2.lat),
                        "lon": list(df2.long),
                        "hoverinfo": "text",
                        "hovertext": [
                                [
                                    hov.format(i, j, k, l, m)
                                ]
                                for i, j, k, l, m in zip(df2.FEATURE_ID,
                                                         df2.BOROUGH,
                                                         df2.PRK_COVER,
                                                         df2.PRK_SECURE,
                                                         df2.PRK_LOCKER)
                            ],
                        "mode": "markers",
                        "marker": {
                                "size": 5,
                                "opacity": 0.7,
                                "color": '#FF0000'
                            }
                        }],
              "layout": map_layout}

    return figure