import pandas as pd

print('load')

full_stats = pd.read_csv('full_stats_running.csv', index_col = 'Unnamed: 0')

# remove season before 2007 to match betting data

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


# make team stats

# drop players columns
cols_drop = []
for x in list(full_stats.columns):
    if x[0:3] == 'H_P' or x[0:3] == 'A_P':
        cols_drop.append(x)
team_stats = full_stats.drop(cols_drop, axis = 1)
# drop totals stats
cols_drop = []
for x in list(team_stats.columns):
    if x[len(x) - 3:len(x)] == 'tot':
        cols_drop.append(x)
team_stats.drop(cols_drop, axis=1, inplace=True)
# drop game results stats
cols_drop = ['AST_home', 'AST_away', 'FG3_PCT_away', 'FG3_PCT_home']
cols_drop += ['FG_PCT_away', 'FG_PCT_home', 'FT_PCT_away', 'FT_PCT_home']
cols_drop += ['GAME_ID', 'HOME_TEAM_ABBREVIATION', 'HOME_TEAM_ID', 'PTS_away']
cols_drop += ['PTS_home', 'REB_away', 'REB_home', 'SEASON']
cols_drop += ['VISITOR_TEAM_ABBREVIATION', 'VISITOR_TEAM_ID', 'HOME_TEAM_WINS']
team_stats.drop(cols_drop, axis=1, inplace=True)

# team stats columns

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

team_win_stats = team_stats[win_cols]

# just points, rebounds, assists stats

pts_stats = []
for x in list(team_stats.columns):
    if x not in win_cols:
        pts_stats.append(x)

team_pts_stats = team_stats[pts_stats]

# make top 8 players of each team's average stats
# needed prefixes
pre_players = []
for i in range(1, 9):
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

# combine various player_stats with team win stats
player_and_team = []
for X in player_stats:
    player_and_team.append(pd.concat([X, team_win_stats], axis=1))

# get data ready for machine learning algorithms

# column to predict
y = full_stats['HOME_TEAM_WINS']
y.reset_index(drop=True, inplace=True)

# X's
data = player_stats + [team_stats, team_win_stats, team_pts_stats]
data += player_and_team

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
validation_data = []

for X in non_test_data:
    X_t, X_v, y_t, y_v = train_test_split(X, y_non_test, train_size=0.8, test_size=0.2, random_state=0)
    train_data.append([X_t, y_t])
    validation_data.append([X_v, y_v])

# MLP model

def perc_corr(y, y_hat):
    """Return the percent of entries where y and y_hat agree.

    y, y_hat are series of 0's and 1's with the same length."""
    total = len(y)
    correct = 0
    for i in range(len(y)):
        if y.iloc[i] == y_hat[i]:
            correct += 1
    return 100*correct/total

train_percents = []
val_percents = []

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# scale for neural network
# scale columns so mean is 0 and variance is 1
# different than what's done in paper

train_scaled = []
val_scaled = []
test_scaled = []

for i in range(len(train_data)):
    scaler = StandardScaler()
    X_t = train_data[i][0]
    X_v = validation_data[i][0]
    X_test = test_data[i][0]
    scaler.fit(X_t)
    train_scaled.append([scaler.transform(X_t), train_data[i][1]])
    val_scaled.append([scaler.transform(X_v), validation_data[i][1]])
    # test_scaled.append(scaler.transform(X_test))

# try a few different alphas for overfitting

print('MLPClassifier')

# put a bunch of inputs to test here
# these are not necessarily the best choices
# just an example of ones I tried to narrow down search
alphas = [1000, 500, 250, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001]
sizes = [(100, 50, 50), (100, 75, 50), (10, 10, 10, 10), (16, 8, 4, 2, 1)]
act = ['tanh', 'relu', 'logistic']



for x in act:
    for y in sizes:
        for z in alphas:
            print("activation: " + x)
            print("layers: " + str(y))
            print("alpha: " + str(z))

            train_percents = []
            val_percents = []

            for i in range(len(train_scaled)):
                clf = MLPClassifier(solver='lbfgs', activation=x, alpha=z,     hidden_layer_sizes=y)
                X_t = train_scaled[i][0]
                y_t = train_scaled[i][1]
                clf.fit(X_t, y_t)
                y_t_hat = clf.predict(X_t)
                train_percents.append(perc_corr(y_t, y_t_hat))
                X_v, y_v = validation_data[i][0], validation_data[i][1]
                y_v_hat = clf.predict(X_v)
                val_percents.append(perc_corr(y_v, y_v_hat))

            print('train percentages')
            perc_strs = ['{:.2f}'.format(x) for x in train_percents]
            print(perc_strs)
            print('validation percentages')
            perc_strs = ['{:.2f}'.format(x) for x in val_percents]
            print(perc_strs)
