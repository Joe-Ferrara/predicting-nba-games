import pandas as pd

global betting
betting = pd.read_csv('betting_full.csv', index_col = 'Unnamed: 0')

cs = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

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

# bet $100 on every game where probability differs by c
for c in cs:
    print('c = ' + str(c))
    print('')
    log_money = 100000
    log_bets = 0
    log_won_bets = 0
    mlp_money = 100000
    mlp_bets = 0
    mlp_won_bets = 0
    for i in range(betting.shape[0]):
        log_prob = betting['LOG_REG_PROB'].iloc[i]
        mlp_prob = betting['MLP_PROB'].iloc[i]
        odds_prob = betting['ODDS_PROB_HOME'].iloc[i]
        decide = decide_to_bet(log_prob, odds_prob, c)
        if decide[0]:
            log_bets += 1
            log_money -= 100
            money = bet(100, decide[1], i)
            log_money += money
            if money > 0:
                log_won_bets += 1
        decide = decide_to_bet(mlp_prob, odds_prob, c)
        if decide[0]:
            mlp_bets += 1
            mlp_money -= 100
            money = bet(100, decide[1], i)
            mlp_money += money
            if money > 0:
                mlp_won_bets += 1
    print('logistic regression betting money: $' + str(log_money))
    print('logistic regression money lost: $' + str(100000 - log_money))
    print('number bets: ' + str(log_bets))
    print('won bets: ' + str(log_won_bets))
    print('percentage of won bets: ' + str(log_won_bets/log_bets))
    print('')
    print('mlp betting money: $' + str(mlp_money))
    print('mlp betting money lost: $' + str(100000 - mlp_money))
    print('number bets: ' + str(mlp_bets))
    print('won bets: ' + str(mlp_won_bets))
    print('percentage of won bets: ' + str(mlp_won_bets/mlp_bets))
    print('')
