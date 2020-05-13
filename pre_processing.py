import pandas as pd

print('load')

full_stats = pd.read_csv('full_stats_running.csv', index_col = 'Unnamed: 0')

###################################################
# remove season before 2007 to match betting data #
###################################################

print('drop pre 2007')

rows_drop = []
for i in range(full_stats.shape[0]):
    if full_stats['SEASON'].iloc[i] < 2007:
        rows_drop.append(i)

full_stats.drop(rows_drop, axis=0, inplace=True)
full_stats.reset_index(drop=True, inplace=True)

# remove first 10 games of each season
# these are 'small' sample size games

print('drop first 10 games')

rows_drop = []
for i in range(full_stats.shape[0]):
    wins = full_stats['HOME_TEAM_TOTAL_WINS'].iloc[i]
    losses = full_stats['HOME_TEAM_TOTAL_LOSSES'].iloc[i]
    if wins + losses <= 10:
        rows_drop.append(i)
        continue
    wins = full_stats['AWAY_TEAM_TOTAL_WINS'].iloc[i]
    losses = full_stats['AWAY_TEAM_TOTAL_LOSSES'].iloc[i]
    if wins + losses <= 10:
        rows_drop.append(i)

full_stats.drop(rows_drop, axis=0, inplace=True)
full_stats.reset_index(drop=True, inplace=True)

###################
# make team stats #
###################

print('make team stats')

# drop players columns
cols_drop = []
for x in list(full_stats.columns):
    if x[0:3] == 'H_P' or x[0:3] == 'A_P':
        cols_drop.append(x)
team_stats_full = full_stats.drop(cols_drop, axis = 1)
# drop totals stats
cols_drop = []
for x in list(team_stats_full.columns):
    if x[len(x) - 3:len(x)] == 'tot':
        cols_drop.append(x)
team_stats_full.drop(cols_drop, axis=1, inplace=True)

# drop game results stats
cols_drop = ['AST_home', 'AST_away', 'FG3_PCT_away', 'FG3_PCT_home']
cols_drop += ['FG_PCT_away', 'FG_PCT_home', 'FT_PCT_away', 'FT_PCT_home']
cols_drop += ['GAME_ID', 'HOME_TEAM_ABBREVIATION', 'HOME_TEAM_ID', 'PTS_away']
cols_drop += ['PTS_home', 'REB_away', 'REB_home', 'SEASON']
cols_drop += ['VISITOR_TEAM_ABBREVIATION', 'VISITOR_TEAM_ID', 'HOME_TEAM_WINS']
team_stats_full.drop(cols_drop, axis=1, inplace=True)

# team_stats_full columns

# AWAY_TEAM_LOSSES_AWAY
# AWAY_TEAM_PTS_allowed_ave
# AWAY_TEAM_PTS_ave
# AWAY_TEAM_PTS_away_allowed_ave
# AWAY_TEAM_PTS_away_ave
# AWAY_TEAM_TOTAL_LOSSES
# AWAY_TEAM_TOTAL_WINS
# AWAY_TEAM_WINS_AWAY
# AWAY_TEAM_WIN_PCT
# AWAY_TEAM_WIN_PCT_AWAY
# HOME_TEAM_PTS_allowed_ave
# HOME_TEAM_PTS_ave
# HOME_TEAM_PTS_home_allowed_ave
# HOME_TEAM_PTS_home_ave
# HOME_TEAM_TOTAL_LOSSES
# HOME_TEAM_TOTAL_WINS
# HOME_TEAM_WINS_HOME
# HOME_TEAM_WIN_PCT
# HOME_TEAM_WIN_PCT_HOME

# just team winning stats

win_cols = ['AWAY_TEAM_LOSSES_AWAY', 'AWAY_TEAM_TOTAL_LOSSES']
win_cols += ['AWAY_TEAM_TOTAL_WINS', 'AWAY_TEAM_WINS_AWAY', 'AWAY_TEAM_WIN_PCT']
win_cols += ['AWAY_TEAM_WIN_PCT_AWAY', 'HOME_TEAM_TOTAL_LOSSES']
win_cols += ['HOME_TEAM_TOTAL_WINS', 'HOME_TEAM_WINS_HOME', 'HOME_TEAM_WIN_PCT']
win_cols += ['HOME_TEAM_WIN_PCT_HOME']

team_stats_win = team_stats_full[win_cols]

# just points stats

pts_stats = []
for x in list(team_stats_full.columns):
    if x not in win_cols:
        pts_stats.append(x)

team_stats_pts = team_stats_full[pts_stats]

team_stats = [team_stats_full, team_stats_win, team_stats_pts]

# TEAM STATS: team_stats_full, team_stats_win, team_stats_pts
#             team_stats list with these in this order

######################
# make players stats #
######################

print('make player stats')

# make top 9 players of each team's average stats
# needed prefixes
pre_players = []
for i in range(1, 10):
    pre_players += ['H_P0' + str(i) + '_', 'A_P0' + str(i) + '_']
# all player stats
stat_cols = ['MIN']
stat_cols += ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB']
stat_cols += ['REB', 'AST', 'STL', 'BLK','TO', 'PF', 'PTS', 'PLUS_MINUS']
# stats not calculated from other stats
# i.e. pts = 2*fgm + 3*fg3m + 1*ftm
stat_cols_no_red = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB']
stat_cols_no_red += ['DREB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PLUS_MINUS']
# just have the larger result stats, i.e. pts
stat_cols_res = ['MIN', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS']
stat_cols_res += ['PLUS_MINUS']
# put these in a lisst
player_stat_types = [stat_cols, stat_cols_no_red, stat_cols_res]
# make list of player stats of the three types
player_stats = []
for stats in player_stat_types:
    cols = []
    for x in pre_players:
        for y in stats:
            cols.append(x + y + '_AVE')
    player_stats.append(full_stats[cols])

# PLAYER STATS: player_stats is list with
#               player_stats[0] all player stats
#               player_stats[1] indep cols of player stats
#               player_stats[2] dep cols of player stats

#########################
# player and team stats #
#########################

print('make player and team stats')

player_and_team = []
for X in player_stats:
    for Y in team_stats:
        player_and_team.append(pd.concat([X, Y], axis=1))

#########################
# machine learning prep #
#########################

print('machine learning prep')

# get data ready for machine learning algorithms
# convention: only use full player, full team, and full player and full team

# column to predict
y = full_stats['HOME_TEAM_WINS']
y.reset_index(drop=True, inplace=True)

# X's
data = [player_stats[0], team_stats[0], player_and_team[0]]

# split data into train, validation, test sets
from sklearn.model_selection import train_test_split

test_data = [] # games from 2018 and 2019
test_indices = []
for i in range(full_stats.shape[0]):
    if full_stats['SEASON'].iloc[i]==2018 or full_stats['SEASON'].iloc[i]==2019:
        test_indices.append(i)
for X in data:
    test_data.append([X.iloc[test_indices], y.iloc[test_indices]])

y_non_test = y.drop(test_indices)
non_test_data = [X.drop(test_indices, axis=0) for X in data]
train_data = []
val_data = []

for X in non_test_data:
    X_t, X_v, y_t, y_v = train_test_split(X, y_non_test, train_size=0.8, test_size=0.2, random_state=0)
    train_data.append([X_t, y_t])
    val_data.append([X_v, y_v])

print('')

print('games in train data: ' + str(train_data[0][0].shape[0]))
print('games in validation data: ' + str(val_data[0][0].shape[0]))
print('games in test data: ' + str(test_data[0][0].shape[0]))

print('')
