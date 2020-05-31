import pandas as pd

# load odds

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

####################################
# put team abbreviations into odds #
####################################

print('doing abbreviations')
team_to_abb = {}
with open('team_to_abbreviation.txt', 'r') as f:
    f.readline()
    char = f.read(1)
    while char != '':
        team = char
        char = f.read(1)
        while char != ' ':
            team += char
            char = f.read(1)
        f.read(7) # 8 spaces between team and abbreviation
        abb = f.read(3)
        team_to_abb[team] = abb
        char = f.read(1)
        char = f.read(1)
# random ones that showed up
team_to_abb['Oklahoma City'] = 'OKC'
team_to_abb['LA Clippers'] = 'LAC'

######################################################
# make dictionary with start and end dates of season #
# enables removing of preseason and postseason games #
######################################################

# doing start and end dates
start_date = {}
end_date = {}
with open('season_start_end_dates.txt', 'r') as f:
    season = 0
    while season != 2003:
        season = int(f.read(4))
        f.read(4) # read space
        start = f.read(10)
        f.read(4) # read space
        end = f.read(10)
        start_date[season] = start
        end_date[season] = end
        f.read(1) # read end of line

global ties_ml
ties_ml = 0

def predict_probs_ml(odds, index):
    global ties_ml
    if odds['ML'].iloc[index] == 'NL': # happens once, index 2184 year 2007
        # hardwire the answer
        return [1, 1.0, 0.0, 0.0]
    a_ML = float(odds['ML'].iloc[index]) # visitor moneyline
    h_ML = float(odds['ML'].iloc[index + 1]) # home moneyline
    if a_ML < 0:
        a_prob = -a_ML/(100 - a_ML)
    else:
        a_prob = 100/(a_ML + 100)
    if h_ML < 0:
        h_prob = -h_ML/(100 - h_ML)
    else:
        h_prob = 100/(h_ML + 100)
    margin = abs(h_prob + a_prob - 1)
    if h_prob > a_prob: # tie goes to home team
        h_win = 1.0
    elif h_prob == a_prob:
        ties_ml += 1
        h_win = 0.5
    else:
        h_win = 0.0
    return [h_win, h_prob, a_prob, margin]

global ties_spread
ties_spread = 0
def predict_scores_spread(odds, index):
    global ties_spread
    if odds['ML'].iloc[index] == 'NL': # happens once, index 2184 year 2007
        # hardwire the answer
        return [1.0, 103.75, 80.75]
    if odds['Close'].iloc[index] == 'pk' or odds['Close'].iloc[index] == 'PK':
        ties_spread += 1
        h_win = 0.5
        ov_un = float(odds['Close'].iloc[index + 1])
        h_score = ov_un/2
        a_score = ov_un/2
        return [h_win, h_score, a_score]
    if odds['Close'].iloc[index+1]=='pk' or odds['Close'].iloc[index+1]=='PK':
        ties_spread += 1
        h_win = 0.5
        ov_un = float(odds['Close'].iloc[index])
        h_score = ov_un/2
        a_score = ov_un/2
        return [h_win, h_score, a_score]
    if float(odds['Close'].iloc[index]) > 100: # moneyline with visitor
        # then the spread with home team
        # means home team is favored
        h_win = 1.0
        ov_un = float(odds['Close'].iloc[index])
        sp = float(odds['Close'].iloc[index + 1])
        h_score = (ov_un + sp)/2
        a_score = (ov_un - sp)/2
        return [h_win, h_score, a_score]
    if float(odds['Close'].iloc[index]) < 100:
        h_win = 0.0
        ov_un = float(odds['Close'].iloc[index + 1])
        sp = float(odds['Close'].iloc[index])
        h_score = (ov_un - sp)/2
        a_score = (ov_un + sp)/2
        return [h_win, h_score, a_score]

for pair in odds_csvs:
    old_ml_ties = ties_ml
    old_spread_ties = ties_spread
    different_preds = 0
    year = pair[0]
    print('year is ' + year)
    odds = pair[1]
    for i in range(int(odds.shape[0]/2)):
        index = 2*i
        ml_pred = predict_probs_ml(odds, index)[0]
        spread_pred = predict_scores_spread(odds, index)[0]
        if ml_pred != spread_pred:
            different_preds += 1
    print('number of different predictions: ' + str(different_preds))
    print('number of money line ties: ' + str(ties_ml - old_ml_ties))
    print('number of spread ties: ' + str(ties_spread - old_spread_ties))
    print('')

print('number of money line ties: ' + str(ties_ml))
print('number of spread ties: ' + str(ties_spread))
