import pandas as pd

global betting
betting = pd.read_csv('betting_full.csv', index_col = 'Unnamed: 0')

pred_cols = ['LOG_REG_PROB', 'MLP_PROB', 'ODDS_PROB_HOME']
print('correlation coefficient')
print(betting[pred_cols].corr(method='pearson'))
print('')


def bet(d, team, index):
    """Place bet of d on team for game index of global betting.

    team is either HOME or AWAY."""
    ml = betting[team + '_ML'].iloc[index]
    h_win = betting['HOME_TEAM_WINS'].iloc[index]
    if team == 'HOME' and h_win == 1:
        win_bet = True
    else:
        win_bet = False
    if win_bet:
        if ml > 0:
            net = d + d*ml/100
        else:
            net = d + d*100/(-ml)
    else:
        net = 0
    return net

def decide_to_bet(pred_prob, odds_prob, c):
    diff = abs(pred_prob - odds_prob)
    if diff < c:
        return [0,'']
    if pred_prob > 0.5:
        return [1, 'HOME']
    else:
        return [1, 'AWAY']


betting.sort_values(by='DATE', inplace=True)
betting.reset_index(drop=True, inplace=True)

cs = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
probs = ['LOG_REG', 'MLP']

for p in probs:
    print('Prediction Method: ' + p)
    print('')
    for c in cs:
        print('c = ' + str(c))
        rounds = []
        money_hist = []
        dates = []
        money = 3000
        bets = 0
        won_bets = 0
        i = 0
        round = 0
        while i < betting.shape[0]:
            date = betting['DATE'].iloc[i]
            dates.append(date)
            rounds.append(round)
            round += 1
            money_hist.append(money)
            games = []
            while i < betting.shape[0] and date == betting['DATE'].iloc[i]:
                games.append(i)
                i += 1
            games_to_bet = []
            for j in games:
                prob = betting[p + '_PROB'].iloc[j]
                odds_prob = betting['ODDS_PROB_HOME'].iloc[j]
                decide = decide_to_bet(prob, odds_prob, c)
                if decide[0]:
                    bets += 1
                    games_to_bet.append([j, decide[1]])
            if len(games_to_bet) > 0:
                bets += len(games_to_bet)
                d = 100/len(games_to_bet)
                for game in games_to_bet:
                    money -= d
                    winnings = bet(d, game[1], game[0])
                    money += winnings
                    if winnings > 0:
                        won_bets += 1
        print('end money: $' + str(money))
        print('money lost: $' + str(3000 - money))
        print('number bets: ' + str(bets))
        print('number won bets: ' + str(won_bets))
        print('percentage bets won: ' + str(won_bets/bets))
        print('')

## always bet the favorite

print('always bet the favorite')
favorite_meaning = [[0.55, 0.45], [0.6, 0.4], [0.65,0.35], [0.70, 0.30], [0.75, 0.25]]
for i in range(len(favorite_meaning)):
    print('favorite amount = ' + str(favorite_meaning[i][0]))
    home = favorite_meaning[i][0]
    away = favorite_meaning[i][1]
    bets = 0
    money = 100000
    won_bets = 0
    for i in range(betting.shape[0]):
        odds_prob = betting['ODDS_PROB_HOME'].iloc[i]
        if odds_prob >= home:
            bets += 1
            money -= 100
            winnings = bet(100, 'HOME', i)
            money += winnings
            if winnings > 0:
                won_bets += 1
        elif odds_prob <= away:
            bets += 1
            money -= 100
            winnings = bet(100, 'AWAY', i)
            money += winnings
            if winnings > 0:
                won_bets += 1
        else:
            continue
    print('end money: $' + str(money))
    print('money lost: $' + str(100000 - money))
    print('number bets: ' + str(bets))
    print('number won bets: ' + str(won_bets))
    print('percentage bets won: ' + str(won_bets/bets))
    print('')
