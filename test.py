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

cols = []
for x in pre_players:
    for y in stat_cols:
        cols.append(x + y + '_AVE')
player_stats = full_stats[cols]

player_and_team_stats = pd.concat([player_stats, team_stats], axis=1)
player_and_team_win_stats = pd.concat([player_stats, team_win_stats], axis=1)


# get data ready for machine learning algorithms

# column to predict
y = full_stats['HOME_TEAM_WINS']
y.reset_index(drop=True, inplace=True)

# X's
data = [player_stats, team_stats, player_and_team_stats]

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

# do logistic regression

from sklearn.linear_model import LogisticRegression

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
test_percents = []

for i in range(len(train_data)):
    X_t, y_t = train_data[i][0], train_data[i][1]
    log_reg = LogisticRegression()
    log_reg.fit(X_t, y_t)
    y_t_hat = log_reg.predict(X_t)
    train_percents.append(perc_corr(y_t, y_t_hat))
    X_v, y_v = validation_data[i][0], validation_data[i][1]
    y_v_hat = log_reg.predict(X_v)
    val_percents.append(perc_corr(y_v, y_v_hat))
    X_test, y_test = test_data[i][0], test_data[i][1]
    y_test_hat = log_reg.predict(X_test)
    test_percents.append(perc_corr(y_test, y_test_hat))
print('')
print('logistic regression')
print('train percentages')
perc_strs = ['{:.2f}'.format(x) for x in train_percents]
print(perc_strs)
print('validation percentages')
perc_strs = ['{:.2f}'.format(x) for x in val_percents]
print(perc_strs)
print('')
print('test percentages')
perc_strs = ['{:.2f}'.format(x) for x in test_percents]
print(perc_strs)
print('')


# do a neural network

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
    test_scaled.append([scaler.transform(X_test), test_data[i][1]])

# try a few different alphas for overfitting

print('MLPClassifier')

alphas = [1000, 900]
layers = [(100, 75, 50), (100, 100, 100)]

for a in alphas:
    for l in layers:
        print('alpha = ' + str(a))
        print('layers = ' + str(l))

        train_percents = []
        val_percents = []
        test_percents = []

        for i in range(len(train_scaled)):
            clf = MLPClassifier(solver='lbfgs', activation='tanh', alpha=a, hidden_layer_sizes=l)
            X_t = train_scaled[i][0]
            y_t = train_scaled[i][1]
            clf.fit(X_t, y_t)
            y_t_hat = clf.predict(X_t)
            train_percents.append(perc_corr(y_t, y_t_hat))
            X_v, y_v = validation_data[i][0], validation_data[i][1]
            y_v_hat = clf.predict(X_v)
            val_percents.append(perc_corr(y_v, y_v_hat))
            X_test = test_scaled[i][0]
            y_test = test_scaled[i][1]
            y_test_hat = clf.predict(X_test)
            test_percents.append(perc_corr(y_test, y_test_hat))

        print('train percentages')
        perc_strs = ['{:.2f}'.format(x) for x in train_percents]
        print(perc_strs)
        print('validation percentages')
        perc_strs = ['{:.2f}'.format(x) for x in val_percents]
        print(perc_strs)
        print('test percentages')
        perc_strs = ['{:.2f}'.format(x) for x in test_percents]
        print(perc_strs)
