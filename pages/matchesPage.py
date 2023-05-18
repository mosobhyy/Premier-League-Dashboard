from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data import *

home_team_scorers = html.Div(
                        className="column-secondary",
                        children=[
                            html.Div(id='home-team-scorers'),
                        ])


away_team_scorers = html.Div(
                        className="column-secondary",
                        children=[
                            html.Div(id='away-team-scorers'),
                        ])

scoreboard = html.Div(
    className="container",
    children=[
        html.Div(
            className="match",
            children=[
                html.Div(
                    className="match-header",
                    children=[
                        html.Div(
                            className="match-tournament",
                            children=[
                                html.Img(
                                    src="https://assets.codepen.io/285131/pl-logo.svg"
                                ),
                                "English Premier League",
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="match-content",
                    children=[
                        home_team_scorers,
                        html.Div(
                            className="column-primary",
                            children=[
                                html.Div(
                                    className="team team--home",
                                    children=[
                                        html.Div(
                                            className="team-logo",
                                            children=[
                                                html.Img(
                                                    id="home-team-logo",
                                                )
                                            ],
                                        ),
                                        html.H2(
                                            id="home-team-name",
                                            className="team-name",
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="column-primary",
                            children=[
                                html.Div(
                                    className="match-details",
                                    children=[
                                        html.Div(
                                            className="match-score",
                                            children=[
                                                html.Span(
                                                    id='home-team-score',
                                                    className="match-score-number",
                                                ),
                                                html.Span(
                                                    className="match-score-divider",
                                                    children=":",
                                                ),
                                                html.Span(
                                                    id='away-team-score',
                                                    className="match-score-number",
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="column-primary",
                            children=[
                                html.Div(
                                    className="team team--away",
                                    children=[
                                        html.Div(
                                            className="team-logo",
                                            children=[
                                                html.Img(
                                                    id="away-team-logo",

                                                )
                                            ],
                                        ),
                                        html.H2(
                                            id="away-team-name",
                                            className="team-name",
                                        ),
                                    ],
                                )
                            ],
                        ),
                        away_team_scorers,
                    ],
                ),
                html.Div(
                    className="match-footer",
                    children=[
                        html.Div([
                            html.Img(src='assets/clock-icon.png', style={'width': '8%',
                                                                    'display': 'inline-block'}), 
                            html.Span(id='clock', style={'margin': '10px'})
                        ]),

                        html.Div([
                            html.Img(src='assets/field-icon.png', style={'width': '10%',
                                                                    'display': 'inline-block'}), 
                            html.Span(id='field', style={'margin': '10px'})
                        ]),

                        html.Div([
                            html.Img(src='assets/whistle-icon.png', style={'width': '8%',
                                                                    'display': 'inline-block'}), 
                            html.Span(id='referee', style={'margin': '10px'})
                        ])
                    ],
                ),
            ],
        )
    ],
)


dropdown_menus = html.Div([
    html.Div([
        
        dcc.Dropdown(
            id='selected-season',
            options=df_matches_with_clubs_names.sort_values('season')['season'].unique()[::-1],
            value=df_matches_with_clubs_names.sort_values('season')['season'].unique()[-1],
            clearable=False,
            style={'margin-right': '10px', 'padding': '10px', 'width': '200px',
                   'text-align': 'center', 'line-height': 'normal',
                   'option': {'text-align': 'center'}}
        ),
        
        html.Div(id='select-match'),
    ], style={'display': 'flex', 'justify-content': 'flex-end', 'margin': '10px',
              'align-items': 'center'}),
    
], style={'width': '100%', 'height': '100%', 'display': 'flex',
          'justify-content': 'flex-end', 'padding': '10px'})
dcc
from utils.home_figures import *

""" Home Page """
figures = html.Div(id='match-stats-content', className="content", children=[
        # Figures

        # # Goals Count per Minute
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=goals_per_minute_figure),
        # ], style={'width': '100%'}),
        
        # # Goals Count per Minute over Seasons
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=goals_per_minute_season_figure),
        # ], style={'width': '100%'}),

        # # Clubs Scored and Conceded Goals
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=scored_conceded_goals_figure),
        # ], style={'width': '50%'}),


        # html.Div([
        #     # Top 10 Scorers
        #     html.Div(className='default-div', children=[
        #         dcc.Graph(figure=top_10_scorers_figure),
        #     ], style={'width': '125%'}),

        #     # Top 10 assist makers
        #     html.Div(className='default-div', children=[
        #         dcc.Graph(figure=top_10_assist_makers_figure),
        #     ], style={'width': '125%'}),

        # ], style={'width': '40%', 'display': 'inline-block'}),

        # # Top 10 Contributors
        # html.Div(className='default-div', children=[
        #     dcc.Graph(figure=top_10_contributors_figure),
        # ], style={'width': '100%'}),

    ],)

match_page = html.Div([
    dropdown_menus,
    scoreboard,
    figures
])