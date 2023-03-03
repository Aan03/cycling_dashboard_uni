import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc

import map_app
import stats  # statistics dashboard

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MINTY, "custom.css"])

server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Map", href="/"), id="map-link"),
        dbc.NavItem(dbc.NavLink("Statistics", href="/statistics"),
                    id="stats-link"),
    ],
    brand="Cycle Parking Dashboard",
    brand_href="/",
    sticky=True,
    color="primary",
    dark=True,
    id="navbar_main"
)

app.layout = html.Div(lang="en", children=[
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(lang='en', id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/statistics':
        return stats.stats_layout()
    elif pathname == '/':
        return map_app.map_app_layout()
    else:
        return '404 Page Not Found'


if __name__ == '__main__':

    app.run_server(debug=True)  # , host='0.0.0.0')
