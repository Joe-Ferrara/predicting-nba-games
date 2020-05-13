# make datatypes sensible in running and totals statistics csvs
# in particular, make totals columns integers

# load

import pandas as pd

teams_running = pd.read_csv('regular_season_teams_running.csv', index_col = 'Unnamed: 0')
teams_totals = pd.read_csv('regular_season_teams_ending.csv')
teams_totals = teams_totals.drop(['Unnamed: 0'], axis=1)
players_running = pd.read_csv('regular_season_players_running.csv', index_col = 'Unnamed: 0')
players_totals = pd.read_csv('regular_season_players_ending.csv')

#######################
# teams_totals dtypes #
#######################

new_types = {}
for col in list(teams_totals.columns):
    if col[-3:len(col)] == 'tot':
        new_types[col] = 'int64'
    elif col[0:4] == 'WINS':
        new_types[col] = 'int64'
    elif col[0:3] == 'LOS':
        new_types[col] = 'int64'
    else:
        continue
new_types['TEAM_ID'] = 'int64'

new_teams_totals = teams_totals.astype(new_types)

new_teams_totals.to_csv('teams_totals.csv')

#########################
# players_totals dtypes #
#########################

players_totals = players_totals.drop(['Unnamed: 0'], axis=1)

new_types = {}
for col in list(players_totals.columns):
    if col[-3:len(col)] == 'TOT':
        new_types[col] = 'int64'

new_types['GAMES'] = 'int64'

new_players_totals = players_totals.astype(new_types)

new_players_totals.to_csv('players_totals.csv')

##########################
# players_running dtypes #
##########################

int_cols = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',  'OREB']
int_cols += ['DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']

new_types = {}
for col in int_cols:
    new_types[col] = 'int64'
for col in list(players_running.columns):
    if col == 'MIN_TOT':
        continue
    if col[-3:len(col)] == 'TOT':
        new_types[col] = 'int64'

new_players_running = players_running.astype(new_types)

new_players_running.to_csv('players_running.csv')

########################
# teams_running dtypes #
########################

int_cols = ['PTS_home', 'AST_home', 'REB_home', 'PTS_away', 'AST_away', 'REB_away']

new_types = {}
for col in int_cols:
    new_types[col] = 'int64'
for col in list(teams_running.columns):
    if col[-3:len(col)] == 'tot':
        new_types[col] = 'int64'

new_teams_running = teams_running.astype(new_types)
new_teams_running.head()

new_teams_running.to_csv('teams_running.csv')
