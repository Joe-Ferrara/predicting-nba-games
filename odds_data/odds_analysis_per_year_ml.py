import pandas as pd

###############################################
# load and put all seasons into one dataframe #
###############################################

# utility functions
def pred_win_error(i, odds, col):
    pred = odds['PRED_HOME_TEAM_WINS'].iloc[i]
    if pred == 0.5:
        col[i] = 0
    else:
        pred = int(pred)
        actual = odds['HOME_TEAM_WINS'].iloc[i]
        col[i] = (1+pred+actual)%2

for i in range(7, 20):
    if i < 10:
        year = '200' + str(i)
    else:
        year = '20' + str(i)
    file = 'odds_' + year + '_ml.csv'
    odds = pd.read_csv(file, index_col = 'Unnamed: 0')
    new_col = {'PRED_WIN_CORRECT':[0]*odds.shape[0]}
    for i in range(odds.shape[0]):
        pred_win_error(i, odds, new_col['PRED_WIN_CORRECT'])
    # make dataframe
    col = new_col['PRED_WIN_CORRECT']
    perc = sum(col)/len(col)
    print(year + ' Percent Correct: ' + str(perc))
