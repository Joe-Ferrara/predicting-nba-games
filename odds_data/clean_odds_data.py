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

#################################
# functions to make new columns #
#################################

def predict_scores(odds, index):
    if odds['ML'].iloc[index] == 'NL': # happens once, index 2184 year 2007
        # hardwire the answer
        return [1.0, 103.75, 80.75]
    if odds['Close'].iloc[index] == 'pk' or odds['Close'].iloc[index] == 'PK':
        h_win = 0.5
        ov_un = float(odds['Close'].iloc[index + 1])
        h_score = ov_un/2
        a_score = ov_un/2
        return [h_win, h_score, a_score]
    if odds['Close'].iloc[index+1]=='pk' or odds['Close'].iloc[index+1]=='PK':
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

def predict_probs(odds, index):
    if odds['ML'].iloc[index] == 'NL': # happens once, index 2184 year 2007
        # hardwire the answer
        return [1.0, 0.0, 0.0]
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
    return [h_prob, a_prob, margin]

def make_date(year, old_date):
    if len(old_date) == 3:
        month = '0' + old_date[0]
        day = old_date[1:3]
    else:
        month = old_date[0:2]
        day = old_date[2:4]
    if int(month) < 10:
        year = str(int(year) + 1)
    return year + '-' + month + '-' + day

def make_teams(odds, index, team_to_abb):
    if odds['VH'].iloc[index] == 'V':
        h_team = team_to_abb[odds['Team'].iloc[index + 1]]
        a_team = team_to_abb[odds['Team'].iloc[index]]
    else:
        h_team = team_to_abb[odds['Team'].iloc[index]]
        a_team = team_to_abb[odds['Team'].iloc[index + 1]]
    return h_team, a_team

def make_score(odds, index):
    if odds['VH'].iloc[index] == 'V':
        h_score = odds['Final'].iloc[index + 1]
        a_score = odds['Final'].iloc[index]
    else:
        h_score = odds['Final'].iloc[index]
        a_score = odds['Final'].iloc[index + 1]

    return h_score, a_score

#######################
# make new dataframes #
#######################

# columns of new dataframe
cols = ['DATE', 'HOME_TEAM', 'AWAY_TEAM', 'HOME_PTS', 'AWAY_PTS', 'HOME_TEAM_WINS', 'PRED_HOME_TEAM_WINS', 'PRED_HOME_PTS', 'PRED_AWAY_PTS', 'PRED_HOME_WIN_PROB', 'PRED_AWAY_WIN_PROB', 'MARGIN', 'OLD_INDEX']
# prediction columns
pred_cols = ['PRED_HOME_TEAM_WINS', 'PRED_HOME_PTS', 'PRED_AWAY_PTS']
pred_cols += ['PRED_HOME_WIN_PROB', 'PRED_AWAY_WIN_PROB', 'MARGIN']

print('doing main work')

for pair in odds_csvs:
    year = pair[0]
    print('year is ' + year)
    odds = pair[1]
    new_odds = {}
    for col in cols:
        new_odds[col] = []
    for i in range(int(odds.shape[0]/2)):
        index = 2*i
        # do the date
        date = odds['Date'].iloc[index]
        new_date = make_date(year, str(date))
        if new_date>=start_date[int(year)] and new_date<=end_date[int(year)]:
            new_odds['DATE'].append(new_date)
            new_odds['OLD_INDEX'].append(odds.index[index])
        else:
            # do not record pre and post season games
            continue
        # teams
        h_team, a_team = make_teams(odds, index, team_to_abb)
        new_odds['HOME_TEAM'].append(h_team)
        new_odds['AWAY_TEAM'].append(a_team)
        # score
        h_score, a_score = make_score(odds, index)
        new_odds['HOME_PTS'].append(h_score)
        new_odds['AWAY_PTS'].append(a_score)
        if h_score > a_score:
            new_odds['HOME_TEAM_WINS'].append(1)
        else:
            new_odds['HOME_TEAM_WINS'].append(0)
        # predictions
        scores = predict_scores(odds, index)
        probs = predict_probs(odds, index)
        predictions = scores + probs
        for i in range(len(predictions)):
            new_odds[pred_cols[i]].append(predictions[i])
    new_odds = pd.DataFrame(new_odds)
    # save
    new_odds.to_csv('odds_' + year + '.csv')
