# make naive predictions on who will win basketball games
# predictions based on:
# average team pts per game
# average team pts per game home versus away
# average point differential
# average point differential home versus away
# winning percentage
# winning percentage home versus away

import pandas as pd

print('load')

full_stats = pd.read_csv('full_stats_running.csv', index_col = 'Unnamed: 0')

# never use player stats, so remove players stats columns

print('drop players stats')

cols_drop = []
for x in list(full_stats.columns):
    if x[0:3] == 'H_P' or x[0:3] == 'A_P':
        cols_drop.append(x)

full_stats = full_stats.drop(cols_drop, axis = 1)

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

print('')
print('do naive predictions')
print('')

def count_correct_preds(y, y_hat):
    X = pd.concat([y, y_hat], axis = 1)
    X.columns = ['y', 'y_hat']
    def same(x):
        if x['y'] == x['y_hat']:
            return 1
        else:
            return 0
    return X.apply(same, axis=1).sum()

# column to predict
y = full_stats['HOME_TEAM_WINS']

num_games = len(y)

print('total games predicting: ' + str(num_games))
print('')

# predict by average total points
X = full_stats[['HOME_TEAM_PTS_ave', 'AWAY_TEAM_PTS_ave']]

def pts_predict(x):
    if x['HOME_TEAM_PTS_ave'] >= x['AWAY_TEAM_PTS_ave']: # tie goes to home team
        return 1
    else:
        return 0

y_hat = X.apply(pts_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by points per page')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')

# predict be average total points at home versus away
# note that there is a small sample size issue when doing home/away splits
# did not remove first ten home games and first ten away games
# total sample size is half as large for home/away that total games
X = full_stats[['HOME_TEAM_PTS_home_ave', 'AWAY_TEAM_PTS_away_ave']]

def h_a_pts_predict(x):
    if x['HOME_TEAM_PTS_home_ave'] >= x['AWAY_TEAM_PTS_away_ave']:
        return 1
    else:
        return 0

y_hat = X.apply(h_a_pts_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by points per page home/away splits')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')

# predict by point differential
cols = ['HOME_TEAM_PTS_ave', 'HOME_TEAM_PTS_allowed_ave']
cols += ['AWAY_TEAM_PTS_ave', 'AWAY_TEAM_PTS_allowed_ave']

X = full_stats[cols]

def point_diff_predict(x):
    if (x[cols[0]] - x[cols[1]]) >= (x[cols[2]] - x[cols[3]]):
        return 1
    else:
        return 0

y_hat = X.apply(point_diff_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by point differential')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')

# predict by point differential home/away splits
cols = ['HOME_TEAM_PTS_home_ave', 'HOME_TEAM_PTS_home_allowed_ave']
cols += ['AWAY_TEAM_PTS_away_ave', 'AWAY_TEAM_PTS_away_allowed_ave']

X = full_stats[cols]

y_hat = X.apply(point_diff_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by point differential home/away splits')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')

# predict by winning percentage
cols = ['HOME_TEAM_WIN_PCT', 'AWAY_TEAM_WIN_PCT']

X = full_stats[cols]

def win_pct_predict(x):
    if x[cols[0]] >= x[cols[1]]:
        return 1
    else:
        return 0

y_hat = X.apply(win_pct_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by winning percentage')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')

# predict by winning percentage home/away splits
cols = ['HOME_TEAM_WIN_PCT_HOME', 'AWAY_TEAM_WIN_PCT_AWAY']

X = full_stats[cols]

def win_pct_predict(x):
    if x[cols[0]] >= x[cols[1]]:
        return 1
    else:
        return 0

y_hat = X.apply(win_pct_predict, axis=1)

corr_preds = count_correct_preds(y, y_hat)
perc = 100*corr_preds/num_games

print('predicting by winning percentage home/away splits')
print('correctly predicted count: ' + str(corr_preds))
print('correctly predicted perc:  {:.2f}%'.format(perc))
print('')
