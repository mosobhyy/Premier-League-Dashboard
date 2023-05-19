"""import packages"""
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import pandas as pd
import sys

import sys
sys.path.append('../')

from utils.data import *

from utils.interactivity import *

""" define app """
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)

server = app.server

# set app title
app.title = 'Premier League'


content = html.Div(id="page-content")

""" define app layout """
app.layout = html.Div([dcc.Location(id="url"), content],
                      style={'color': '#566A7F'},
                      className='bg-light')

""" interactivity """
interactive(app)


if __name__ == "__main__":
    app.run_server(debug=False)
