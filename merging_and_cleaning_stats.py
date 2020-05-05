# merger players and game stats
# remove unnecessary stats
# remove percentages that are calculated incorrectly
# replace percentages with correct calculations if possible

import pandas as pd
import numpy as np
import time

time0 = time.time()

# use the csvs output by the Fixing Data Types jupyter notebook
print('loading')

teams_running = pd.read_csv('teams_running.csv', index_col = 'Unnamed: 0')

players_running = pd.read_csv('players_running.csv', index_col = 'Unnamed: 0')

print('Time: ' + str(time.time() - time0))

##############################
# MAKE BLANK MERGE DATAFRAME #
##############################

print("prepocessing")

# dataframe that will hold all data
merge = {}
m = teams_running.shape[0] # number of rows

# columns to keep from teams
# identifiers
teams_cols = ['GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON']
teams_cols += ['HOME_TEAM_ABBREVIATION', 'VISITOR_TEAM_ABBREVIATION']
# results from game, y's
teams_cols += ['PTS_home', 'FG_PCT_home','FT_PCT_home', 'FG3_PCT_home']
teams_cols += ['AST_home', 'REB_home','PTS_away', 'FG_PCT_away', 'FT_PCT_away']
teams_cols += ['FG3_PCT_away', 'AST_away', 'REB_away', 'HOME_TEAM_WINS']
# winning data, home/road splits for each team
teams_cols += ['AWAY_TEAM_LOSSES_AWAY', 'AWAY_TEAM_TOTAL_LOSSES' ]
teams_cols += ['AWAY_TEAM_TOTAL_WINS', 'AWAY_TEAM_WINS_AWAY']
teams_cols += ['AWAY_TEAM_WIN_PCT','AWAY_TEAM_WIN_PCT_AWAY']
teams_cols += ['HOME_TEAM_TOTAL_LOSSES','HOME_TEAM_TOTAL_WINS']
teams_cols += ['HOME_TEAM_WINS_HOME','HOME_TEAM_WIN_PCT']
teams_cols += ['HOME_TEAM_WIN_PCT_HOME']
# points scored and allowed data
teams_cols += ['AWAY_TEAM_PTS_allowed_ave', 'AWAY_TEAM_PTS_allowed_tot']
teams_cols += ['AWAY_TEAM_PTS_ave', 'AWAY_TEAM_PTS_away_allowed_ave']
teams_cols += ['AWAY_TEAM_PTS_away_allowed_tot', 'AWAY_TEAM_PTS_away_ave']
teams_cols += ['AWAY_TEAM_PTS_away_tot', 'AWAY_TEAM_PTS_tot']
teams_cols += ['HOME_TEAM_PTS_allowed_ave', 'HOME_TEAM_PTS_allowed_tot']
teams_cols += ['HOME_TEAM_PTS_ave', 'HOME_TEAM_PTS_home_allowed_ave']
teams_cols += ['HOME_TEAM_PTS_home_allowed_tot', 'HOME_TEAM_PTS_home_ave']
teams_cols += ['HOME_TEAM_PTS_home_tot', 'HOME_TEAM_PTS_tot']

# make the players columns
players_cols = []
pre_players_cols = []
home_away = ['H_P', 'A_P']
for x in home_away:
    for i in range(1, 18): # up to 15 players active for a game
        for col in players_running.columns:
            if col == 'GAME_ID':
                continue
            if col == 'TEAM_ID':
                continue
            if i < 10:
                new_col = x + '0' + str(i) + '_' + col
                players_cols.append(new_col)
            else:
                new_col = x + str(i) + '_' + col
                players_cols.append(new_col)

for col in players_running.columns:
    if col == 'GAME_ID':
        continue
    if col == 'TEAM_ID':
        continue
    pre_players_cols.append(col)


# make merge a blank dataframe with correct data types
for col in teams_cols:
    if type(teams_running[col].iloc[0]) == np.int64:
        merge[col] = [0]*m
    elif type(teams_running[col].iloc[0]) == np.float64:
        merge[col] = [0.0]*m
    else:
        merge[col] = ['blank']*m
for col in players_cols:
    old_col = col[6:]
    if type(players_running[old_col].iloc[0]) == np.int64:
        merge[col] = [0]*m
    elif type(players_running[old_col].iloc[0]) == np.float64:
        merge[col] = [0.0]*m
    else:
        merge[col] = ['blank']*m

merge = pd.DataFrame(merge)

print('Time: ' + str(time.time() - time0))

##########################################
# MERGE THE PLAYERS AND TEAMS DATAFRAMES #
##########################################

print("merging")

def merge_players_stats(merge, i, pre_players_cols, h_players, a_players):

    for j in range(h_players.shape[0]):
        for col in pre_players_cols:
            if j + 1 < 10:
                merge_col = 'H_P0'+ str(j+1) + '_' + col
            else:
                merge_col = 'H_P' + str(j+1) + '_' + col
            merge.at[i, merge_col] = h_players[col].iloc[j]
    for j in range(a_players.shape[0]):
        for col in pre_players_cols:
            if j + 1 < 10:
                merge_col = 'A_P0'+ str(j+1) + '_' + col
            else:
                merge_col = 'A_P' + str(j+1) + '_' + col
            merge.at[i, merge_col] = a_players[col].iloc[j]


# gruop player stats by GAME_ID, TEAM_ID
players_grouped = players_running.groupby(['GAME_ID', 'TEAM_ID'])

# iterate over teams stats by GAME_ID
for i in range(teams_running.shape[0]):

    # merge team stats
    for col in teams_cols:
        merge.at[i, col] = teams_running.at[i, col]

    # get home and away players groups
    game_id = teams_running['GAME_ID'].iloc[i]
    h_team_id = teams_running['HOME_TEAM_ID'].iloc[i]
    h_players = players_grouped.get_group((game_id, h_team_id))
    # sort so easy to discard irrelevent players later
    h_players = h_players.sort_values(by=['PTS', 'AST', 'REB'], ascending=False)
    a_team_id = teams_running['VISITOR_TEAM_ID'].iloc[i]
    a_players = players_grouped.get_group((game_id, a_team_id))
    a_players = a_players.sort_values(by=['PTS', 'AST', 'REB'], ascending=False)

    # merge player stats
    merge_players_stats(merge, i, pre_players_cols, h_players, a_players)

merge.fillna(0.0) # have NaNs in individual game PCT columns when 0 attempts
                  # making those 0.0, shouldn't negatively affect anything
                  # probably will never use these columns

merge.to_csv('full_stats_running.csv')

print('Time: ' + str(time.time() - time0))
