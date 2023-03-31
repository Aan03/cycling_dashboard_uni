# Statistics page
from dash import dcc, Dash
import dash_bootstrap_components as dbc
import main_flask_app.dash_app_cycling.bar_charts as bar_charts  # barcharts
import main_flask_app.dash_app_cycling.line_charts as line_charts  # linecharts
import main_flask_app.dash_app_cycling.choropleths as choropleths  # choropleth


def create_dash_app(flask_app):
    """Creates Dash as a route in Flask

    :param flask_app: A confired Flask app
    :return dash_app: A configured Dash app registered to the Flask app
    """
    # Register the Dash app to a route '/dashboard/' on a Flask app
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/dash_app/",
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1",
            }
        ],
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    def all_boroughs():
        """Return a dropdown widget to select the borough."""
        return dcc.Dropdown(
            id="dropdown_borough",
            options=bar_charts.borough_names.loc[:, "name"],
            value="All Boroughs",
            clearable=False)

    def stats_layout():
        """Define the statistic page layout."""
        return dbc.Container(children=[
            dbc.Row(children=[
                dbc.Col(choropleths.app4_layout(), width="100%",
                        align="evenly"),
            ]),
            dbc.Row(children=[
                dbc.Col(all_boroughs(), width="100%"),
            ]),
            dbc.Row(children=[
                    dbc.Col(
                        (bar_charts.app2_layout()),
                        md=4,
                        xs=12,
                        sm=12,
                        align="evenly",
                    ),
                    dbc.Col(
                        (line_charts.app3_layout()),
                        md=8,
                        xs=12,
                        sm=12,
                        align="evenly",
                    ),
                    ]
                    ),
        ], fluid=True
        )

    dash_app.layout = stats_layout()
    return dash_app
