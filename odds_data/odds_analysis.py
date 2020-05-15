import pandas as pd

###############################################
# load and put all seasons into one dataframe #
###############################################

odds_csvs = []

for i in range(7, 20):
    if i < 10:
        year = '200' + str(i)
    else:
        year = '20' + str(i)
    file = 'odds_' + year + '.csv'
    odds_csvs.append(pd.read_csv(file, index_col = 'Unnamed: 0'))

odds = pd.concat(odds_csvs, axis=0)
odds.reset_index(drop=True, inplace=True)

####################################
# make a dataframe to record error #
####################################

# columns for new datafram
new_cols = {}
new_cols_names = ['PRED_WIN_CORRECT', 'HOME_SCORE_ERROR', 'AWAY_SCORE_ERROR', 'SPREAD_ERROR', 'OVER_UNDER_ERROR']
for name in new_cols_names:
    new_cols[name] = [0.0]*odds.shape[0]
new_cols['PRED_WIN_CORRECT'] = [0]*odds.shape[0]

# utility functions
def pred_win_error(i, odds, col):
    pred = odds['PRED_HOME_TEAM_WINS'].iloc[i]
    if pred == 0.5:
        col[i] = 0
    else:
        pred = int(pred)
        actual = odds['HOME_TEAM_WINS'].iloc[i]
        col[i] = (1+pred+actual)%2

def h_score_error(i, odds, col):
    error = abs(odds['HOME_PTS'].iloc[i] - odds['PRED_HOME_PTS'].iloc[i])
    col[i] = error

def a_score_error(i, odds, col):
    error = abs(odds['AWAY_PTS'].iloc[i] - odds['PRED_AWAY_PTS'].iloc[i])
    col[i] = error

def spread_error(i, odds, col):
    pred_spread = odds['PRED_HOME_PTS'].iloc[i] - odds['PRED_AWAY_PTS'].iloc[i]
    pred_spread = abs(pred_spread)
    actual_spread = abs(odds['HOME_PTS'].iloc[i] - odds['AWAY_PTS'].iloc[i])
    error = abs(pred_spread - actual_spread)
    col[i] = error

def over_under_error(i, odds, col):
    pred_ov_un = odds['PRED_HOME_PTS'].iloc[i] + odds['PRED_AWAY_PTS'].iloc[i]
    actual_ov_un = odds['HOME_PTS'].iloc[i] + odds['AWAY_PTS'].iloc[i]
    error = abs(pred_ov_un - actual_ov_un)
    col[i] = error

# record the errors
for i in range(odds.shape[0]):
    pred_win_error(i, odds, new_cols['PRED_WIN_CORRECT'])
    h_score_error(i, odds, new_cols['HOME_SCORE_ERROR'])
    a_score_error(i, odds, new_cols['AWAY_SCORE_ERROR'])
    spread_error(i, odds, new_cols['SPREAD_ERROR'])
    over_under_error(i, odds, new_cols['OVER_UNDER_ERROR'])
# make dataframe
analysis = pd.DataFrame(new_cols)

######################################
# do analysis of the recorded errors #
######################################

def within(col, x):
    """Returns percentage of col that is less than or equal to x."""
    col = col.sort_values()
    number = 0
    while col.iloc[number] <= x and number < len(col):
        number += 1
    return number+1

all_correct = 0
for i in range(analysis.shape[0]):
    if analysis['HOME_SCORE_ERROR'].iloc[i] == 0.0:
        if analysis['AWAY_SCORE_ERROR'].iloc[i] == 0.0:
            all_correct += 1

print('Vegas Predictions')
print('')

correct_pred = analysis.PRED_WIN_CORRECT.sum()
percent_correct = 100*correct_pred/analysis.shape[0]
#perc_f = "{:.2f}".format(percent_correct)
print('correctly predicted winner: {:.2f}%'.format(percent_correct))
print('')
error = (analysis.HOME_SCORE_ERROR.mean() + analysis.AWAY_SCORE_ERROR.mean())/2
print('average score prediction error: {:.2f}'.format(error))
h_score_err = analysis['HOME_SCORE_ERROR']
a_score_err = analysis['AWAY_SCORE_ERROR']
all_scores_err = pd.concat([h_score_err, a_score_err], axis=0)
perc90 = all_scores_err.quantile(0.9)
print('90% of predicted scores are within {:.2f}'.format(perc90))
perc = 100*within(all_scores_err, 10)/(2*analysis.shape[0])
print('percent of predicted scores within 10: {:.2f}%'.format(perc))
print('')
corr_guess = within(all_scores_err, 0)
print('{:d} scores predicted correct'.format(corr_guess))
print('(score is of a home team or away team)')
print('{:d} total score predicted correct'.format(all_correct))
print('(correctly predict home and away team)')
print('total number of games: ' + str(analysis.shape[0]))
print('')


error = analysis.SPREAD_ERROR.mean()
print('average spread error: {:.2f}'.format(error))
perc90 = analysis.SPREAD_ERROR.quantile(0.9)
print('90% of spreads are within {:.2f}'.format(perc90))
perc = 100*within(analysis['SPREAD_ERROR'], 3)/analysis.shape[0]
print('percent spread within 3: {:.2f}%'.format(perc))
print('')

error = analysis.OVER_UNDER_ERROR.mean()
print('average over/under error: {:.2f}'.format(error))
perc90 = analysis.OVER_UNDER_ERROR.quantile(0.9)
print('90% of over/unders are within {:.2f}'.format(perc90))
perc = 100*within(analysis['OVER_UNDER_ERROR'], 10)/analysis.shape[0]
print('percent over/under within 10: {:.2f}%'.format(perc))
