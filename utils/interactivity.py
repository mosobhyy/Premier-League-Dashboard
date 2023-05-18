"""import packages"""
from dash import html, dcc
from dash.dependencies import Input, Output
from pages.sideBar import *
from pages.landingPage import *
from pages.homePage import *
from pages.matchesPage import *
from utils.data import *
from utils.matches_figures import *

""" interactivity """
# set the content according to the current pathname

def interactive(app):
    @app.callback(
            Output(component_id="page-content", component_property="children"),
            Input(component_id="url", component_property="pathname")
            )
    def render_page_content(pathname):
        if pathname == "/":
            return landing_page
        if pathname == "/home":
            return sidebar, home_page
        elif pathname == "/matches":
            return sidebar, match_page
        elif pathname == "/messages":
            return sidebar, html.P("Here are all your messages")
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

    @app.callback(
        Output(component_id='champions', component_property='children'),
        Input(component_id="url", component_property="pathname")

    )
    def render_champions(pathname):
        if pathname == "/home":
            champion_season = []
            for season, club_name in df_champions.values:
                champion_season.append(html.Div([
                    html.Img(src='assets/'+club_name.lower()+'.png', width=100),
                    html.P(season, style={'text-align':'center'})
                ], style={'display': 'inline-block', 'margin': '1%'}))
            
            return champion_season
        

    @app.callback(
    Output(component_id='select-match', component_property='children'),
    Input(component_id="selected-season", component_property="value")

    )
    def filter_matches_by_season(selected_season):
            
            filtered_matches_per_season = df_matches_with_clubs_names[df_matches_with_clubs_names['season']==selected_season]
            filtered_matches_per_season = filtered_matches_per_season.sort_values(by='match_date')
            return dcc.Dropdown(
                    [
                        {
                            f"label": html.Div([
                                    html.Img(src=f'../assets/{team1.lower()}.png', width=20, style={'margin-right': '10px'}),
                                    html.Span(f"{team1} VS {team2}", style={'font-size': 15, 'height': '20px', 'display': 'inline-flex', 'align-items': 'center'}),
                                    html.Img(src=f'../assets/{team2.lower()}.png', width=20, style={'margin-left': '10px'}),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'height': '30px', 'place-content': 'center'}),

                            "value": f"{team1} VS {team2}"
                        }
                    for team1, team2 in filtered_matches_per_season[['home_team_name', 'away_team_name']].values],

                    value=filtered_matches_per_season['home_team_name'].values[0] + ' VS ' + filtered_matches_per_season['away_team_name'].values[0],
                    clearable=False,
                    id='selected-match',
            style={'padding': '10px', 'width': '400px', 'text-align': 'center',
                   'line-height': 'normal',
                   'option': {'text-align': 'center'}}
        )
    

    @app.callback(
    Output(component_id='home-team-logo', component_property='src'),
    Output(component_id='away-team-logo', component_property='src'),
    Output(component_id='home-team-score', component_property='children'),
    Output(component_id='away-team-score', component_property='children'),
    Output(component_id='clock', component_property='children'),
    Output(component_id='field', component_property='children'),
    Output(component_id='referee', component_property='children'),
    # Output(component_id='home-team-scorers', component_property='children'),
    # Output(component_id='away-team-scorers', component_property='children'),
    Input(component_id="selected-season", component_property="value"),
    Input(component_id="selected-match", component_property="value")
    )
    def render_scoreboard(selected_season, selected_match):
            team1, team2 = selected_match.split(' VS ')
            home_team_logo = f'../assets/{team1.lower()}.png'
            away_team_logo = f'../assets/{team2.lower()}.png'

            mask = (df_matches_with_clubs_names['season']==selected_season) & (df_matches_with_clubs_names['home_team_name']==team1) & (df_matches_with_clubs_names['away_team_name']==team2)
            filtered_match = df_matches_with_clubs_names[mask]

            home_team_score = filtered_match['home_team_goals']
            away_team_score = filtered_match['away_team_goals']

            clock = filtered_match['match_date']
            field = filtered_match['stadium_name']
            referee = filtered_match['referee']

            # # get goals in target match
            # mask = (df_player_performance['match_id'] == filtered_match['match_id'].values[0]) & (df_player_performance['type_of_stat'].isin(['goal', 'goal (by penalty)', 'own goal']))
            # match_goals_info = df_player_performance[mask]

            # # get scorer(s) info
            # match_goals_info = match_goals_info.merge(df_player_stats, on=['match_id', 'player_id'])

            # # get name(s) of scorer(s)
            # match_goals_info = match_goals_info.merge(df_player, on='player_id')

            # # get scorer(s) by team
            # home_team_scorers = match_goals_info[match_goals_info['is_home_side']==1][['player_name', 'minute']].values
            # away_team_scorers = match_goals_info[match_goals_info['is_home_side']==0][['player_name', 'minute']].values

            # home_team_scorers_to_return = [html.Div([
            #                                     html.Span(' '.join(scorer)+"'",
            #                                             style={'margin': '5px'}),
            #                                     html.Img(src='assets/soccer-ball-icon.png', style={'width': '25%'}), 
            #                                 ], style={'display': 'flex',
            #                                         'align-items': 'baseline',
            #                                         'justify-content': 'start'}) 
            #                               for scorer in home_team_scorers]
            
            # away_team_scorers_to_return = [html.Div([
            #                                     html.Span(' '.join(scorer)+"'",
            #                                             style={'margin': '5px'}),
            #                                     html.Img(src='assets/soccer-ball-icon.png', style={'width': '25%'}), 
            #                                 ], style={'display': 'flex',
            #                                         'align-items': 'baseline',
            #                                         'justify-content': 'start'}) 
            #                               for scorer in away_team_scorers]
            
            return home_team_logo, away_team_logo, home_team_score, away_team_score, clock, field, referee
    

    @app.callback(
         Output(component_id='match-stats-content', component_property='children'),

         Input(component_id="selected-season", component_property="value"),
         Input(component_id="selected-match", component_property="value")
    )
    def update_match_figures(selected_season, selected_match):
        team1, team2 = selected_match.split(' VS ')
        home_team_logo = f'../assets/{team1.lower()}.png'
        away_team_logo = f'../assets/{team2.lower()}.png'
        mask = (df_matches_with_clubs_names['season']==selected_season) & (df_matches_with_clubs_names['home_team_name']==team1) & (df_matches_with_clubs_names['away_team_name']==team2)
        filtered_match = df_matches_with_clubs_names[mask]

        if (df_club_stats['match_id'] == filtered_match['match_id'].values[0]).sum():
             
             figures_dict = get_match_figures(*filtered_match['match_id'])

             figures = [ 
                        html.Div(className='default-div', children=[
                            dcc.Graph(figure=figures_dict['line_ups_figure']),
                         ], style={'width': '100%'}),

                        html.Div(className='default-div', children=[
                            dcc.Graph(figure=figures_dict['timeline_figure']),
                         ], style={'width': '100%'}),

                        html.Div(className='default-div', children=[
                            dcc.Graph(figure=figures_dict['possession_figure']),
                         ], style={'width': '48%'}),
 
                         html.Div(className='default-div', children=[
                             dcc.Graph(figure=figures_dict['shots_figure']),
                         ], style={'width': '48%'}), 

                        html.Div(className='default-div', children=[
                            dcc.Graph(figure=figures_dict['cards_figure']),
                         ], style={'width': '48%'}),

                        html.Div(className='default-div', children=[
                            dcc.Graph(figure=figures_dict['passes_figure']),
                         ], style={'width': '48%'}),

                         ]
             return figures
             
             
        
        return html.Div(className='default-div', children=[
                    html.H4(f'Sorry, No Stats available for Season {selected_season}'),
                ], style={'width': '100%',
                         'padding': '5%',
                         'text-align': 'center'}),
        
