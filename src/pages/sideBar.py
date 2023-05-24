"""import packages"""
from dash import html
import dash_bootstrap_components as dbc

""" Sidebar """
sidebar = html.Div(
    [
        html.Div(
            [
                html.A(href='/',
                    style={"display": "flex", "align-items": "center", 
                           "text-decoration": "none", "color": "darkslateblue"},
                    children=[
                        html.Img(src='assets/premier-league.png', style={"width": "3rem"}),
                        html.H4("Premier League", style={"margin-top": "10px"}),
                    ])
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/home",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Matches"),
                    ],
                    href="/matches",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)