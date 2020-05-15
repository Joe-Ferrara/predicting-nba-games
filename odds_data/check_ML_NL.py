import pandas as pd

odds_csvs = []
for i in range(7, 20):
    if i < 9:
        year = '200' + str(i) + '-0' + str(i + 1)
    elif i == 9:
        year = '200' + str(i) + '-' + str(i + 1)
    else:
        year = '20' + str(i) + '-' + str(i + 1)
    file_name = 'nba_odds_' + year + '.csv'
    year = year[0:4]
    odds_csvs.append([year, pd.read_csv(file_name)])

bad_indices = []

for pair in odds_csvs:
    year = pair[0]
    odds = pair[1]
    for i in range(odds.shape[0]//2):
        index = 2*i
        if odds['ML'].iloc[index] == 'NL':
            bad_indices.append([year, index])
            print(odds.iloc[[index]])
            print(odds.iloc[[index+1]])
print(len(bad_indices))
print(bad_indices)

# there is only one
