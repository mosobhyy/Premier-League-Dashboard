"""import packages"""
from dash import html, dcc
from utils.home_figures import *

""" Home Page """
home_page = html.Div(className="content", children=[
        html.Img(src='assets/premier-league-logo.png', style={"width": "60rem"}),

        # Champions
        html.Div(className='default-div', children=[
            html.Br(),
            html.H4('Premier League Champions'),
            html.Br(),
            html.Hr(),
            html.Br(),
            html.Div(id='champions')  
        ], style={'text-align':'center',}),

        # Figures

        # Champions 
        html.Div(className='default-div', children=[
            dcc.Graph(figure=champions_figure),
        ], style={'width': '55%'}),

        # Champions By City
        html.Div(className='default-div', children=[
            dcc.Graph(figure=champions_by_city_figure),
        ], style={'width': '40%'}),

        # Goals Count per Minute
        html.Div(className='default-div', children=[
            dcc.Graph(figure=goals_per_minute_figure),
        ], style={'width': '100%'}),
        
        # Goals Count per Minute over Seasons
        html.Div(className='default-div', children=[
            dcc.Graph(figure=goals_per_minute_season_figure),
        ], style={'width': '100%'}),

        # Clubs Scored and Conceded Goals
        html.Div(className='default-div', children=[
            dcc.Graph(figure=scored_conceded_goals_figure),
        ], style={'width': '50%'}),

        # # Top 10 Scorers
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=top_10_scorers_figure),
        # ], style={'width': '48%'}),

        # # Top 10 assist makers
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=top_10_assist_makers_figure),
        # ], style={'width': '48%'}),

        html.Div([
            # Top 10 Scorers
            html.Div(className='default-div', children=[
                dcc.Graph(figure=top_10_scorers_figure),
            ], style={'width': '125%'}),

            # Top 10 assist makers
            html.Div(className='default-div', children=[
                dcc.Graph(figure=top_10_assist_makers_figure),
            ], style={'width': '125%'}),

        ], style={'width': '40%', 'display': 'inline-block'}),

        # Top 10 Contributors
        html.Div(className='default-div', children=[
            dcc.Graph(figure=top_10_contributors_figure),
        ], style={'width': '100%'}),

    ],)