"""import packages"""
from dash import html

""" Landing Page """
landing_page = html.Div(className='landing-page', children=[
    html.A(href='/home', className='btn-outline', children=[
            html.Span(children=['Dashboard']),
        ])
])