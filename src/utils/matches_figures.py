""" Import Libraries """
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data import *
# from utils.interactivity import *


def get_match_figures(match_id):
    
    figures_dict = {}

    df_filtered_match = df_matches_with_clubs_names[df_matches_with_clubs_names['match_id'] == match_id].copy()

    df_filtered_match_stats = df_club_stats[df_club_stats['match_id'] == match_id].copy()
    df_filtered_match_stats = df_filtered_match_stats.merge(df_club, on='club_id')

    # Get teams' names
    home_team_name = df_filtered_match['home_team_name'].values[0]
    away_team_name = df_filtered_match['away_team_name'].values[0]

    # Line-ups

    # Get player stats in target match
    df_filtered_match_squad = df_player_stats[df_player_stats['match_id'] == df_filtered_match['match_id'].values[0]]

    # Get player names
    df_filtered_match_squad = df_filtered_match_squad.merge(df_player, on='player_id')

    # Get team of each player 
    df_filtered_match_squad['club_name'] = df_filtered_match_squad['is_home_side'].apply(lambda x: home_team_name if x else away_team_name)

    # sort player by players in line-up
    df_filtered_match_players = df_filtered_match_squad.sort_values(by='is_in_starting_11', ascending=False)

# Get teams squad
    home_team_squad = df_filtered_match_players[df_filtered_match_players['is_home_side'] == 1]['player_name']
    away_team_squad = df_filtered_match_players[df_filtered_match_players['is_home_side'] == 0]['player_name']
    
    # create the original table
    line_ups_figure = go.Figure(data=[go.Table(
            header=dict(values=[home_team_name, away_team_name],
                        fill_color='paleturquoise',
                        ),
            cells=dict(values=[home_team_squad, away_team_squad],
                    fill_color='lavender',
                    )),
        ])

    # highlight the first 11 rows with a different background color

    cell_colors = [['lightblue'] * 11 + ['white'] * (len(home_team_squad)-11)]
    cell_colors

    line_ups_figure.update_traces(cells=dict(fill_color=cell_colors))

    line_ups_figure.update_layout(title='Line-ups')

    line_ups_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                   })
                                   
    figures_dict['line_ups_figure'] = line_ups_figure

    # Timeline
    
    # Get timeline in target match
    filtered_match_timeline_mask = (df_player_performance['match_id'] == df_filtered_match['match_id'].values[0]) & (df_player_performance['type_of_stat'].str.lower() != 'assist')
    df_filtered_match_timeline_info = df_player_performance[filtered_match_timeline_mask]

    # Get scorer(s) info
    df_filtered_match_timeline_info = df_filtered_match_timeline_info.merge(df_player_stats, on=['match_id', 'player_id'])

    # Get name(s) of scorer(s)
    df_filtered_match_timeline_info = df_filtered_match_timeline_info.merge(df_player, on='player_id')

    df_filtered_match_timeline_info['club_name'] = df_filtered_match_timeline_info['is_home_side'].apply(lambda x: home_team_name if x == 1 else away_team_name)

    # get interesting columns only
    df_filtered_match_timeline_info = df_filtered_match_timeline_info[['player_name', 'type_of_stat', 'minute', 'club_name']]

    # Casting `minute` dtype from `object` to `int`
    df_filtered_match_timeline_info['minute'] = df_filtered_match_timeline_info['minute'].apply(lambda x: int(x.split('+')[0]) + int(x.split('+')[1]) if len(x.split('+'))-1 else int(x))
    
    #  Sort by `minute`
    df_filtered_match_timeline_info = df_filtered_match_timeline_info.sort_values(by='minute').reset_index(drop=True)

    # Convert the minute column to start and end times
    df_filtered_match_timeline_info['start_time'] = pd.to_datetime(df_filtered_match['match_date'].values[0]) + pd.to_timedelta(df_filtered_match_timeline_info['minute'], unit='m')
    df_filtered_match_timeline_info['end_time'] = df_filtered_match_timeline_info['start_time'] + pd.to_timedelta('1 minute')

    # Uppercase for events for better visualiztion
    df_filtered_match_timeline_info['type_of_stat'] = df_filtered_match_timeline_info['type_of_stat'].str.upper()
    
    # color map of each event in match
    color_map = {'GOAL': 'darkgreen', 
                'GOAL (BY PENALTY)': 'green',
                'SECOND YELLOW CARD (AND/OR RED': 'lightgray',
                'OWN GOAL': 'gray',
                'RED CARD': 'red'}


    # Create the Gantt chart
    timeline_figure = px.timeline(df_filtered_match_timeline_info, 
                                  x_start='start_time', 
                                  x_end='end_time', 
                                  y='club_name', 
                                  color='type_of_stat',
                                  color_discrete_map=color_map,
                                  labels={'type_of_stat': 'Event', 'club_name': 'Club'},
                                  hover_name='player_name',
                                  hover_data={'minute': ':.0f', 'start_time': False, 'end_time': False, })

    # Add annotations for each timeline
    for index, row in df_filtered_match_timeline_info.iterrows():
        home_team_name = df_filtered_match['home_team_name'].values[0]
        away_team_name = df_filtered_match['away_team_name'].values[0]

        home_team_goals_sum_mask = (df_filtered_match_timeline_info['club_name'] == home_team_name) & (df_filtered_match_timeline_info['type_of_stat'].str.lower().isin(['goal', 'goal (by penalty)']))
        home_team_own_goals_sum_mask = (df_filtered_match_timeline_info['club_name'] == home_team_name) & (df_filtered_match_timeline_info['type_of_stat'].str.lower() == 'own goal')

        away_team_goals_sum_mask = (df_filtered_match_timeline_info['club_name'] == away_team_name) & (df_filtered_match_timeline_info['type_of_stat'].str.lower().isin(['goal', 'goal (by penalty)'])) 
        away_team_own_goals_sum_mask = (df_filtered_match_timeline_info['club_name'] == away_team_name) & (df_filtered_match_timeline_info['type_of_stat'].str.lower() == 'own goal')

        home_team_goals_sum = len(df_filtered_match_timeline_info[:index+1][home_team_goals_sum_mask | away_team_own_goals_sum_mask])
        away_team_goals_sum = len(df_filtered_match_timeline_info[:index+1][away_team_goals_sum_mask | home_team_own_goals_sum_mask])

        timeline_figure.add_annotation(x=row['start_time'], y=row['club_name'], 
                            text=str(home_team_goals_sum) + ': ' + str(away_team_goals_sum) ,
                            textangle=-45, font=dict(color='white'), bgcolor='darkgreen', 
                            showarrow=False, xanchor='center',yshift=74)

    # Set the chart title and axis labels
    timeline_figure.update_layout(title='Timeline',
                    xaxis_title='Time',
                    yaxis_title='Team')

    timeline_figure.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up


    timeline_figure.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                   })


    figures_dict['timeline_figure'] = timeline_figure

    # Possession
    df_filtered_match_possession = df_filtered_match_stats[['club_name', 'possession']].copy()

    color_map = {home_team_name: '#636EFA', # blue 
                away_team_name: '#EF553B'} # red

    possession_figure = px.pie(df_filtered_match_possession, values='possession', hole=0.5,
                               names='club_name',
                               color='club_name',
                               color_discrete_map=color_map,
                               hover_name='club_name',
                               title='Posession')

    possession_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                     })
    
    figures_dict['possession_figure'] = possession_figure

    # Shots
    df_filtered_match_stats['shots_off_target'] = df_filtered_match_stats['shots'] - df_filtered_match_stats['shots_on_target']
    df_filtered_match_shots = df_filtered_match_stats[['club_name', 'shots', 'shots_on_target', 'shots_off_target']].copy()
    df_filtered_match_shots.rename(columns={'shots_on_target': 'On Target',
                                        'shots_off_target': 'Off Target',}, inplace=True)
    df_filtered_match_shots = df_filtered_match_shots.melt(id_vars=['club_name', 'shots'], var_name='shots_type', value_name='count')
    
    shots_figure = px.sunburst(df_filtered_match_shots, path=['club_name', 'shots_type', 'count'],
                               values='count',
                               labels={'id': 'Club'},
                               title='Shots')

    shots_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                })

    figures_dict['shots_figure'] = shots_figure

    # Cards
    df_filtered_match_cards = df_filtered_match_stats[['club_name', 'yellow_cards', 'red_cards']]
    df_filtered_match_cards = df_filtered_match_cards.rename(columns={'yellow_cards': 'Yellow',
                                                                      'red_cards': 'Red'})
    
    cards_figure = px.bar(df_filtered_match_cards, x='club_name', y=['Yellow', 'Red'],
                          labels={'variable': 'Card', 'club_name':'Club', 'value': 'Cards Count'})

    cards_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                               'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                               })
    figures_dict['cards_figure'] = cards_figure

    # Passes
    df_filtered_match_passes = df_filtered_match_stats[['club_name', 'passes']]
    df_filtered_match_passes

    # set teams representation colors
    color_map = {home_team_name: '#636EFA', # blue 
                 away_team_name: '#EF553B'} # red

    passes_figure = px.bar(df_filtered_match_passes, x='club_name', y='passes',
                                        labels={'variable': 'Passes', 'club_name':'Club'},
                                        color='club_name',
                                        color_discrete_map=color_map)

    passes_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                })

    figures_dict['passes_figure'] = passes_figure


    return figures_dict