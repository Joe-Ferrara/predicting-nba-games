
import pandas as pd

# 2016 NYK at PHX has points wrong

odds = pd.read_csv('odds_2016.csv', index_col = 'Unnamed: 0')

for i in range(odds.shape[0]):
    if odds['AWAY_PTS'].iloc[i] == 10.0:
        odds.at[i, 'AWAY_PTS'] = 111.0
        odds.at[i, 'HOME_PTS'] = 113.0

odds.to_csv('odds_2016.csv')
