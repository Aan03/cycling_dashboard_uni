# Statistics page

import dash_bootstrap_components as dbc
from dash import dcc
import app2  # barcharts
import app3  # linecharts
import app4  # choropleths


def all_boroughs():
    """Return a dropdown widget to select the borough."""
    return dcc.Dropdown(
        id="dropdown_borough",
        options=app2.borough_names.loc[:, "name"],
        value="All Boroughs",
        clearable=False)


def stats_layout():
    """Define the statistic page layout."""
    return dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(app4.app4_layout(), width="100%", align="evenly",),
        ]),
        dbc.Row(children=[
            dbc.Col(all_boroughs(), width="100%"),
        ]),
        dbc.Row(children=[
                dbc.Col(
                    (app2.app2_layout()),
                    md=4,
                    xs=12,
                    sm=12,
                    align="evenly",
                ),
                dbc.Col(
                    (app3.app3_layout()),
                    md=8,
                    xs=12,
                    sm=12,
                    align="evenly",
                ),
                ]
                ),
    ], fluid=True
    )
