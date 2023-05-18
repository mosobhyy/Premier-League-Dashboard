""" Import Libraries """
import numpy as np
import pandas as pd
import os

DATA_PATH = ('' if 'dataset' in os.listdir() else '../') + 'dataset/clean'

""" reading data """
df_champions = pd.read_csv(os.path.join(DATA_PATH, 'champions.csv'))
df_club = pd.read_csv(os.path.join(DATA_PATH, 'club.csv'))
df_club_stats = pd.read_csv(os.path.join(DATA_PATH, 'club_stats.csv'))
df_manager = pd.read_csv(os.path.join(DATA_PATH, 'manager.csv'))
df_manager_club = pd.read_csv(os.path.join(DATA_PATH, 'manager_club.csv'))
df_match = pd.read_csv(os.path.join(DATA_PATH, 'match.csv'))
df_player = pd.read_csv(os.path.join(DATA_PATH, 'player.csv'))
df_player_club = pd.read_csv(os.path.join(DATA_PATH, 'player_club.csv'))
df_player_performance = pd.read_csv(os.path.join(DATA_PATH, 'player_performance.csv'))
df_player_stats = pd.read_csv(os.path.join(DATA_PATH, 'player_stats.csv'))
df_stadium = pd.read_csv(os.path.join(DATA_PATH, 'stadium.csv'))

df_matches_with_clubs_names = df_match.merge(df_club[['club_id', 'club_name']], left_on='home_team_id',
                                             right_on='club_id').rename(columns={'club_name': 'home_team_name'})

df_matches_with_clubs_names = df_matches_with_clubs_names.merge(df_club[['club_id', 'club_name']], left_on='away_team_id',
                                                                right_on='club_id').rename(columns={'club_name': 'away_team_name'})

df_matches_with_clubs_names = df_matches_with_clubs_names.merge(df_stadium, on='stadium_id')

# df_matches_with_clubs_names.drop(columns=df_matches_with_clubs_names.filter(like='id').columns,
#                                  inplace=True)