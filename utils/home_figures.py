""" Import Libraries """
import pandas as pd
import plotly.express as px
from utils.data import *

""" Figures """

# Champions
champions_figure = px.bar(x=df_champions['club_name'].value_counts().index, 
                          y=df_champions['club_name'].value_counts().values,
                          labels={'x':'Club Name', 'y': 'Champions Count'},
                          title='Champions')

champions_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                })

# Champions By City
df_champions_info = df_champions.merge(df_club, on='club_name').merge(df_stadium, on='stadium_id')

champions_by_city_figure = px.sunburst(df_champions_info, path=['city', 'club_name'],
                                       title='Champions By City')

champions_by_city_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                        })


# Goals Count per Minute
df_goals_per_minute = df_player_performance[df_player_performance['type_of_stat'] == 'goal']

df_goals_per_minute['minute'] = df_goals_per_minute['minute'].apply(lambda x: int(x.split('+')[0]) + int(x.split('+')[1]) if len(x.split('+'))-1 else int(x))


goals_per_minute_figure = px.line(x=df_goals_per_minute['minute'].value_counts().sort_index().index, 
                                  y=df_goals_per_minute['minute'].value_counts().sort_index().values,
                                  labels={'x': 'Minute', 'y': 'Goals Count'},
                                  title='Goals Count per Minute')
                                  
goals_per_minute_figure.update_layout({
                                    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                    })


# Goals Count per Minute over Seasons
df_goals_per_minute_season = df_goals_per_minute.merge(df_match[['match_id', 'season']], on='match_id')

df_goals_per_minute_season['season'] = pd.to_datetime(df_goals_per_minute_season['season'], format='%Y/%y').dt.year

df_goals_per_minute_season = df_goals_per_minute_season.groupby(by=['season', 'minute']).count()[['match_id']]
df_goals_per_minute_season = df_goals_per_minute_season.rename(columns={'match_id': 'goals_count'}).reset_index()

goals_per_minute_season_figure = px.line(df_goals_per_minute_season, x='minute', y='goals_count',
                                  animation_frame='season',                                  
                                  labels={'minute': 'Minute', 'goals_count': 'Goals Count'},
                                  title='Goals Count per Minute over Seasons')
                                  
goals_per_minute_season_figure.update_layout({
                                    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                    })

# Scored vs. Conceded Goals
home_team_goals = df_match.groupby('home_team_id').agg({'home_team_goals': 'sum',
                                                        'away_team_goals': 'sum'})

away_team_goals = df_match.groupby('away_team_id').agg({'away_team_goals': 'sum',
                                                        'home_team_goals': 'sum'})

home_team_goals.columns = away_team_goals.columns = ['scored', 'conceded']

home_team_goals = home_team_goals.rename_axis('club_id')
away_team_goals = away_team_goals.rename_axis('club_id')

df_goals = (home_team_goals + away_team_goals).reset_index().sort_values(by='scored')
# df_goals['Goal Difference'] = df_goals['scored'] - df_goals['conceded']

df_goals = df_goals.merge(df_club, on='club_id')

scored_conceded_goals_figure = px.bar(df_goals, x=['scored', 'conceded'], y='club_name',
                                      hover_name='club_name', height=910, 
                                      labels={'variable': 'Goals', 'club_name':'Club'},
                                      title="Scored vs. Conceded Goals",
                                      text_auto=True).update_traces(textangle=0).update_layout(xaxis_title=None)

scored_conceded_goals_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                            })

# Top Scorers
df_scorers = df_player_performance[df_player_performance['type_of_stat'] == 'goal']
df_scorers = df_scorers.groupby(by='player_id').count()[['match_id']]
df_scorers.rename(columns={'match_id': 'goals_count'}, inplace=True)
df_scorers = df_scorers.reset_index()

# Get players names
df_scorers = df_scorers.merge(df_player, on='player_id')

# drop unnecessary columns
df_scorers = df_scorers[['player_name', 'goals_count', 'country']]

df_top_10_scorers = df_scorers.sort_values(by='goals_count', ascending=False)[:10]

top_10_scorers_figure = px.bar(df_top_10_scorers, x='player_name', y='goals_count',
                                labels={'player_name': 'Player', 'goals_count': 'Goals Count'},
                                title='Top 10 Scorers')

top_10_scorers_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                     })


# Top assist makers
df_assist_makers = df_player_performance[df_player_performance['type_of_stat'] == 'assist']
df_assist_makers = df_assist_makers.groupby(by='player_id').count()[['match_id']]
df_assist_makers.rename(columns={'match_id': 'assists_count'}, inplace=True)
df_assist_makers = df_assist_makers.reset_index()

# Get players names
df_assist_makers = df_assist_makers.merge(df_player, on='player_id')

# drop unnecessary columns
df_assist_makers = df_assist_makers[['player_name', 'assists_count', 'country']]

df_top_10_assist_makers = df_assist_makers.sort_values(by='assists_count', ascending=False)[:10]

top_10_assist_makers_figure = px.bar(df_top_10_assist_makers, x='player_name', y='assists_count',
                                labels={'player_name': 'Player', 'assists_count': 'Assists Count'},
                                title='Top 10 Assist Makers')

top_10_assist_makers_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                     })



# Top Scorers
df_contributors = df_player_performance[df_player_performance['type_of_stat'].isin(['goal', 'assist'])]
df_contributors = df_contributors.groupby(by='player_id').count()[['match_id']]
df_contributors.rename(columns={'match_id': 'contributors_count'}, inplace=True)
df_contributors = df_contributors.reset_index()

# Get players names
df_contributors = df_contributors.merge(df_player, on='player_id')

# drop unnecessary columns
df_contributors = df_contributors[['player_name', 'contributors_count', 'country']]

df_top_10_contributors = df_contributors.sort_values(by='contributors_count', ascending=False)[:10]

top_10_contributors_figure = px.bar(df_top_10_contributors, x='player_name', y='contributors_count',
                                    labels={'player_name': 'Player', 'contributors_count': 'Contributors Count'},
                                    title='Top 10 Contributors (Goals or Assists)')

top_10_contributors_figure.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                          'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                          })