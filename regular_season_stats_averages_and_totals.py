# import pandas and load data

import time

time0 = time.time()

import pandas as pd

games = pd.read_csv('games.csv')

# columns of games
# ['GAME_DATE_EST', 'GAME_ID', 'GAME_STATUS_TEXT', 'HOME_TEAM_ID',
#    'VISITOR_TEAM_ID', 'SEASON', 'HOME_TEAM_ID', 'PTS_home', 'FG_PCT_home',
#    'FT_PCT_home', 'FG3_PCT_home', 'AST_home', 'REB_home', 'TEAM_ID_away',
#    'PTS_away', 'FG_PCT_away', 'FT_PCT_away', 'FG3_PCT_away', 'AST_away',
#       'REB_away', 'HOME_TEAM_WINS']

# data types of columns
# GAME_DATE_EST        object
# GAME_ID               int64
# GAME_STATUS_TEXT     object
# HOME_TEAM_ID          int64
# VISITOR_TEAM_ID       int64
# SEASON                int64
# HOME_TEAM_ID          int64
# PTS_home            float64
# FG_PCT_home         float64
# FT_PCT_home         float64
# FG3_PCT_home        float64
# AST_home            float64
# REB_home            float64
# TEAM_ID_away          int64
# PTS_away            float64
# FG_PCT_away         float64
# FT_PCT_away         float64
# FG3_PCT_away        float64
# AST_away            float64
# REB_away            float64
# HOME_TEAM_WINS        int64

# shape: (23195, 21)

games_players = pd.read_csv('games_details.csv')

# columns of games_players
# ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID',
#       'PLAYER_NAME', 'START_POSITION', 'COMMENT', 'MIN', 'FGM', 'FGA',
#       'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
#       'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']

# data types of columns
# GAME_ID                int64
# TEAM_ID                int64
# TEAM_ABBREVIATION     object
# TEAM_CITY             object
# PLAYER_ID              int64
# PLAYER_NAME           object
# START_POSITION        object
# COMMENT               object
# MIN                   object
# FGM                  float64
# FGA                  float64
# FG_PCT               float64
# FG3M                 float64
# FG3A                 float64
# FG3_PCT              float64
# FTM                  float64
# FTA                  float64
# FT_PCT               float64
# OREB                 float64
# DREB                 float64
# REB                  float64
# AST                  float64
# STL                  float64
# BLK                  float64
# TO                   float64
# PF                   float64
# PTS                  float64
# PLUS_MINUS           float64

# shape: (576782, 28)


teams = pd.read_csv('teams.csv')

# columns of teams
# ['LEAGUE_ID', 'TEAM_ID', 'MIN_YEAR', 'MAX_YEAR', 'ABBREVIATION',
#        'NICKNAME', 'YEARFOUNDED', 'CITY', 'ARENA', 'ARENACAPACITY', 'OWNER',
#        'GENERALMANAGER', 'HEADCOACH', 'DLEAGUEAFFILIATION']

# data types of columns
# LEAGUE_ID               int64
# TEAM_ID                 int64
# MIN_YEAR                int64
# MAX_YEAR                int64
# ABBREVIATION           object
# NICKNAME               object
# YEARFOUNDED             int64
# CITY                   object
# ARENA                  object
# ARENACAPACITY         float64
# OWNER                  object
# GENERALMANAGER         object
# HEADCOACH              object
# DLEAGUEAFFILIATION     object

# shape: (30, 14)

####################################
# put team abbreviation into games #
####################################

print('Time: ' + str(time.time() - time0))
print('doing team abbreviations')

team_abbreviation = {}
for i in range(teams.shape[0]):
    team_abbreviation[teams.at[i, 'TEAM_ID']] = teams.at[i, 'ABBREVIATION']

HOME_TEAM_ABB = [None]*games.shape[0]
VISITOR_TEAM_ABB = [None]*games.shape[0]

for i in range(games.shape[0]):
    home_id = games.at[i, 'HOME_TEAM_ID']
    HOME_TEAM_ABB[i] = team_abbreviation[home_id]
    visitor_id = games.at[i, 'VISITOR_TEAM_ID']
    VISITOR_TEAM_ABB[i] = team_abbreviation[visitor_id]

c1 = 'HOME_TEAM_ABBREVIATION'
c2 = 'VISITOR_TEAM_ABBREVIATION'
df = {c1:HOME_TEAM_ABB, c2:VISITOR_TEAM_ABB}
abbreviations = pd.DataFrame(df)

games = pd.concat([games, abbreviations], axis=1)

#########################################
# PUT GAME DATES INTO PLAYERS DATAFRAME #
#########################################

print('Time: ' + str(time.time() - time0))
print('putting game dates into players dataframe')

# remove unnecessary columns from players dataframe
cols_to_drop = ['TEAM_ABBREVIATION', 'TEAM_CITY', 'START_POSITION', 'COMMENT']
players_aves = games_players.drop(cols_to_drop, axis=1)

# put date and season into players dataframe
# get from games dataframe
dates = {}
for i in range(games.shape[0]):
    game_id = games.at[i, 'GAME_ID']
    date = games.at[i, 'GAME_DATE_EST']
    season = games.at[i, 'SEASON']
    dates[game_id] = [date, season]

SEASON = [None]*players_aves.shape[0]
DATE = [None]*players_aves.shape[0]

for i in range(players_aves.shape[0]):
    game_id = players_aves.at[i, 'GAME_ID']
    DATE[i] = dates[game_id][0]
    SEASON[i] = dates[game_id][1]

dates = pd.DataFrame({'SEASON':SEASON, 'DATE':DATE})

players_aves = pd.concat([players_aves, dates], axis=1)


###################################
# MAKES GAMES REGULAR SEASON ONLY #
###################################

print('Time: ' + str(time.time() - time0))
print("making games regular season only")

# NBA regular season start and end dates
# season  start date    end date
# 2019    2019-10-22    2020-03-11
# 2018    2018-10-16    2019-04-10
# 2017    2017-10-17    2018-04-11
# 2016    2016-10-25    2017-04-12
# 2015    2015-10-27    2016-04-13
# 2014    2014-10-28    2015-04-15
# 2013    2013-10-29    2014-04-16
# 2012    2012-10-30    2013-04-17
# 2011    2011-12-25    2012-04-26
# 2010    2010-10-26    2011-04-13
# 2009    2009-10-27    2010-04-14
# 2008    2008-10-28    2009-04-15
# 2007    2007-10-30    2008-04-16
# 2006    2006-10-31    2007-04-18
# 2005    2005-11-01    2006-04-19
# 2004    2004-11-02    2005-04-20
# 2003    2003-10-28    2004-04-14

# make start and date dictionary using above info in a txt file
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

# go down rows collecting indices of rows of preseason or postseason games
rows_to_remove = []
for i in range(games.shape[0]):
    season = games.at[i, 'SEASON']
    date = games.at[i, 'GAME_DATE_EST']
    if date < start_date[season]: # preseason game
        rows_to_remove.append(i)
    if date > end_date[season]: # postseason game
        rows_to_remove.append(i)

# remove the rows
games = games.drop(rows_to_remove, axis=0)
# reset the index so no numbers are missing
# makes it so rows are numbers 0 to games.shape[0] - 1
games.reset_index(drop=True, inplace=True)

##########################################
# MAKE GAMES_PLAYERS REGULAR SEASON ONLY #
##########################################

print('Time: ' + str(time.time() - time0))
print("making players stats regular season only")

# go down rows collecting indices of rows to be removed
rows_to_remove = []
for i in range(players_aves.shape[0]):
    season = players_aves.at[i, 'SEASON']
    date = players_aves.at[i, 'DATE']
    if date < start_date[season]:
        rows_to_remove.append(i)
    if date > end_date[season]:
        rows_to_remove.append(i)

# remove rows
players_aves = players_aves.drop(rows_to_remove, axis=0)
# reset index
players_aves.reset_index(drop=True, inplace=True)


################################################
### CREATE PLAYER SEASON AVERAGES AND TOTALS ###
################################################

print('Time: ' + str(time.time() - time0))
print("making player season averages and totals")

# replace NaN entries in players_aves dataframe
# fill NaN with 0.0 for float columns and '0:00' for MIN column
values = {}
values['MIN'] = '0:00'
float_cols = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB']
float_cols += ['REB', 'AST', 'STL', 'BLK','TO', 'PF', 'PTS', 'PLUS_MINUS']

for x in float_cols:
    values[x] = 0.0

players_aves.fillna(value = values, inplace = True)

# make a dictionary for the new columns
games_app = [0]*players_aves.shape[0] # games appeared in
mins_to_date = [0.0]*players_aves.shape[0] # total minutes played
mins_ave = [0.0]*players_aves.shape[0] # min ave per game appeared in
new_cols = {'GAMES_APPEARED':games_app, 'MIN_TOT':mins_to_date, 'MIN_AVE':mins_ave}
for x in float_cols: # do totals and averages for float columns
    x_tot = x + '_TOT'
    x_ave = x + '_AVE'
    new_cols[x_tot] = [0.0]*players_aves.shape[0]
    new_cols[x_ave] = [0.0]*players_aves.shape[0]

# make empty dataframe of end of year totals
# dataframe will have one row for each (player_id, season) pair
totals = {}
totals['PLAYER_ID'] = []
totals['PLAYER_NAME'] = []
totals['SEASON'] = []
totals['MIN'] = []
totals['MPG'] = []
totals['GAMES'] = []
for x in float_cols:
    totals[x + '_TOT'] = []
    totals[x + '_AVE'] = []

totals = pd.DataFrame(totals)

# function to update new_cols float columns
def running_floats(group, col, run_tot, ave):
    """Modify run_tot, ave as columns with the running totals and aves of col.

    Return end of season totals for col.
    Group is assumed to be ordered by date.
    run_tot and ave are lists of length # rows of players_ave
    group is the (sorted) group corresponding to a player, season pair.
    col is the column of group to calculate the running total and average of."""
    tot_so_far = 0.0
    ave_so_far = 0.0
    games_appeared = 0.0
    for i in range(group.shape[0]):
        # put the average and total before the game the row represents
        # the average and total going into the game
        index = group.index[i]
        run_tot[index] = tot_so_far
        ave[index] = ave_so_far
        # if min == 0:00 did not appear in game
        # stats not updated in this case
        if group['MIN'].iloc[i] == '0:00':
            continue
        # update total and average
        else:
            games_appeared += 1
            val = group[col].iloc[i]
            tot_so_far += val
            ave_so_far = tot_so_far/games_appeared
    # ending ave and total returned
    return tot_so_far, ave_so_far

#function to get float value of minute
def min_float(s):
    """Given a string s for minutes played, return float for minutes played."""
    if len(s) <= 3:
        return float(s)
    if len(s) == 4:
        return (float(s[0]) + float(s[2:4])/float(60))
    if len(s) == 5:
        return (float(s[0:2]) + float(s[3:5])/float(60))
    return 35.0001 # if s is a nonsensical value can find them later

#function to update new_cols minutes columns
def running_min(group, run_tot, ave):
    """Modify run_tot, ave with the running totals and aves of mins played."""
    tot_so_far = 0.0
    ave_so_far = 0.0
    games_appeared = 0.0
    # put the average and total before the game the row represents
    for i in range(group.shape[0]):
        # put ave and total before the game the row represents
        index = group.index[i]
        run_tot[index] = tot_so_far
        ave[index] = ave_so_far
        # if min == 0:00 did not appear in game
        # stats not updated in this case
        minStr = group['MIN'].iloc[i]
        if minStr == '0:00':
            continue
        else:
            games_appeared += 1
            val = min_float(minStr)
            if val <= 0.0: # nonsensical value
                val = 35.0001 # can find these later
            tot_so_far += val
            ave_so_far = tot_so_far/games_appeared
    # ending ave and total returned
    return tot_so_far, ave_so_far

# function to update GAMES_APPEARED column
def games_app(group, games_appeared):
    g = 0 # games appeared in so far
    for i in range(group.shape[0]):
        index = group.index[i]
        games_appeared[index] = g
        if group['MIN'].iloc[i] != '0:00':
            g += 1
    return g

# do the work using above function

# make the groupby object
players_years_gp = players_aves.groupby(['PLAYER_ID', 'SEASON'])
# loop throught the (player_id, season) pairs
for name, group in players_years_gp:
    group = group.sort_values(by=['DATE'])
    new_row = {} # new row for totals
    new_row['PLAYER_ID'] = [name[0]]
    new_row['SEASON'] = [name[1]]
    new_row['PLAYER_NAME'] = group['PLAYER_NAME'].iloc[0]
    # loop through float columns
    for x in float_cols:
        # get the lists to be updated
        run_tot = new_cols[x + '_TOT']
        ave = new_cols[x + '_AVE']
        # use function
        end_tot, end_ave = running_floats(group, x, run_tot, ave)
        # update totals row
        new_row[x + '_TOT'] = [end_tot]
        new_row[x + '_AVE'] = [end_ave]
    # do minutes
    end_tot, end_ave = running_min(group, new_cols['MIN_TOT'], new_cols['MIN_AVE'])
    new_row['MIN'] = [end_tot]
    new_row['MPG'] = [end_ave]
    # do games appeared
    end_tot = games_app(group, new_cols['GAMES_APPEARED'])
    new_row['GAMES'] = [end_tot]
    # put new row in totals dataframe
    new_row = pd.DataFrame(new_row)
    totals = pd.concat([totals, new_row], axis=0)
# put new columns in players_ave dataframe
new_cols = pd.DataFrame(new_cols)
players_aves = pd.concat([players_aves, new_cols], axis=1)
# save as csv files
players_aves.to_csv('regular_season_players_running_aves_tots_corrected.csv')
totals.to_csv('regular_season_players_ending_aves_tots_corrected.csv')


###################################
### CREATE TEAM SEASON AVERAGES ###
###################################

# not doing totals since seems unnecessary

print('Time: ' + str(time.time() - time0))
print("making team season averages and totals")


# drop unnecessary columns
cols_to_drop = ['GAME_STATUS_TEXT']
games = games.drop(cols_to_drop, axis=1)

# team stats we have, all float columns

# for now not doing game number
# game_num = [0]*games.shape[0] # game number
# new_cols = {'GAME_NUMBER':game_num}

# make a dictionary for the new columns
new_cols = {}
stats_names = ['PTS', 'AST', 'REB']
home_away = ['HOME_TEAM_', 'AWAY_TEAM_']
ave_total = ['_ave', '_tot']
for x in stats_names:
    for p in home_away:
        for q in ave_total:
            new_cols[p + x + q] = [0.0]*games.shape[0]
            new_cols[p + x + '_allowed' + q] = [0.0]*games.shape[0]
    for q in ave_total:
        new_cols['HOME_TEAM_' + x + '_home' + q] = [0.0]*games.shape[0]
        new_cols['AWAY_TEAM_' + x + '_away' + q] = [0.0]*games.shape[0]
        new_cols['HOME_TEAM_' + x + '_home_allowed' + q] = [0.0]*games.shape[0]
        new_cols['AWAY_TEAM_' + x + '_away_allowed' + q] = [0.0]*games.shape[0]

# record win, lose, winning percentage
for p in home_away:
    new_cols[p + 'TOTAL_WINS'] = [0]*games.shape[0]
    new_cols[p + 'TOTAL_LOSSES'] = [0]*games.shape[0]
    new_cols[p + 'WIN_PCT'] = [0.0]*games.shape[0]
new_cols['HOME_TEAM_WINS_HOME'] = [0]*games.shape[0]
new_cols['HOME_TEAM_LOSSES_HOME'] = [0]*games.shape[0]
new_cols['HOME_TEAM_WIN_PCT_HOME'] = [0.0]*games.shape[0]
new_cols['AWAY_TEAM_WINS_AWAY'] = [0]*games.shape[0]
new_cols['AWAY_TEAM_LOSSES_AWAY'] = [0]*games.shape[0]
new_cols['AWAY_TEAM_WIN_PCT_AWAY'] = [0.0]*games.shape[0]


# make empty dataframe of end of year totals
# dataframe will have one row for each (team_id, season) pair
totals = {}
totals['TEAM_ID'] = []
totals['TEAM_ABBREVIATION'] = []
totals['SEASON'] = []
for x in stats_names:
    for q in ave_total:
        totals[x + q] = []
        totals[x + '_home' + q] = []
        totals[x + '_away' + q] = []
        totals[x + '_allowed' + q] = []
        totals[x + '_home_allowed' + q] = []
        totals[x + '_away_allowed' + q] = []
totals['WINS'] = []
totals['LOSSES'] = []
totals['WIN_PCT'] = []
totals['WINS_HOME'] = []
totals['LOSSES_HOME'] = []
totals['WIN_PCT_HOME'] = []
totals['WINS_AWAY'] = []
totals['LOSSES_AWAY'] = []
totals['WIN_PCT_AWAY'] = []

totals = pd.DataFrame(totals)


# for each year, isolate each team

# get team_ids
team_ids = []
for i in range(teams.shape[0]):
    team_ids.append(teams.at[i, 'TEAM_ID'])

# functions

def wins_and_losses(team_id, season_stats, new_cols):
    """Update new_cols with all the wins and losses stats.

    Return the end of year wins and losses."""
    wins = [0,0,0] # wins, wins home, wins away
    losses = [0,0,0] # losses, losses home, losses away
    win_perc = [0.0, 0.0, 0.0] # win perc, win perc home, win perc away
    for i in range(season_stats.shape[0]):
        index = season_stats.index[i]
        if season_stats['HOME_TEAM_ID'].iloc[i] == team_id:
            new_cols['HOME_TEAM_TOTAL_WINS'][index] = wins[0]
            new_cols['HOME_TEAM_WINS_HOME'][index] = wins[1]
            new_cols['HOME_TEAM_TOTAL_LOSSES'][index] = losses[0]
            new_cols['HOME_TEAM_LOSSES_HOME'][index] = losses[1]
            new_cols['HOME_TEAM_WIN_PCT'][index] = win_perc[0]
            new_cols['HOME_TEAM_WIN_PCT_HOME'][index] = win_perc[1]
            if season_stats['HOME_TEAM_WINS'].iloc[i]:
                wins[0] += 1
                wins[1] += 1
            else:
                losses[0] += 1
                losses[1] += 1
            win_perc[0] = wins[0]/(wins[0] + losses[0])
            win_perc[1] = wins[1]/(wins[1] + losses[1])
        else:
            new_cols['AWAY_TEAM_TOTAL_WINS'][index] = wins[0]
            new_cols['AWAY_TEAM_WINS_AWAY'][index] = wins[2]
            new_cols['AWAY_TEAM_TOTAL_LOSSES'][index] = losses[0]
            new_cols['AWAY_TEAM_LOSSES_AWAY'][index] = losses[2]
            new_cols['AWAY_TEAM_WIN_PCT'][index] = win_perc[0]
            new_cols['AWAY_TEAM_WIN_PCT_AWAY'][index] = win_perc[2]
            if season_stats['HOME_TEAM_WINS'].iloc[i]:
                losses[0] += 1
                losses[2] += 1
            else:
                wins[0] += 1
                wins[2] += 1
            win_perc[0] = wins[0]/(wins[0] + losses[0])
            win_perc[2] = wins[2]/(wins[2] + losses[2])
    return wins, losses, win_perc

def running(x, team_id, season_stats, h_aves, a_aves, h_tots, a_tots):
    """Modify aves as column with the running average of x.

    Return ending average."""
    ave_so_far = 0.0
    tot_so_far = 0.0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        if season_stats['HOME_TEAM_ID'].iloc[i] == team_id:
            h_aves[index] = ave_so_far
            h_tots[index] = tot_so_far
            val = season_stats[x + '_home'].iloc[i]
        else:
            a_aves[index] = ave_so_far
            a_tots[index] = tot_so_far
            val = season_stats[x + '_away'].iloc[i]
        tot_so_far += val
        ave_so_far = tot_so_far/(i+1)
    return ave_so_far, tot_so_far

def running_allowed(x, team_id, season_stats, h_aves, a_aves, h_tots, a_tots):
    """Modify aves as column with the running allowed average of x.

    Return ending average.
    To get the allowed, if team is home team, take away team stat.
    If team is away team, take home team stat."""
    ave_so_far = 0.0
    tot_so_far = 0.0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        if season_stats['HOME_TEAM_ID'].iloc[i] == team_id:
            h_aves[index] = ave_so_far
            h_tots[index] = tot_so_far
            val = season_stats[x + '_away'].iloc[i]
        else:
            a_aves[index] = ave_so_far
            a_tots[index] = tot_so_far
            val = season_stats[x + '_home'].iloc[i]
        tot_so_far += val
        ave_so_far = tot_so_far/(i+1)
    return ave_so_far, tot_so_far

def running_home(x, team_id, season_stats, aves, tots):
    """Modify aves as column with the running ave of x as home team.

    Return ending average."""
    ave_so_far = 0.0
    tot_so_far = 0.0
    games_so_far = 0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        aves[index] = ave_so_far
        tots[index] = tot_so_far
        if season_stats['HOME_TEAM_ID'].iloc[i] == team_id:
            val = season_stats[x + '_home'].iloc[i]
            games_so_far += 1
            tot_so_far += val
            ave_so_far = tot_so_far/(games_so_far)
    return ave_so_far, tot_so_far

def running_away(x, team_id, season_stats, aves, tots):

    ave_so_far = 0.0
    tot_so_far = 0.0
    games_so_far = 0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        aves[index] = ave_so_far
        tots[index] = tot_so_far
        if season_stats['VISITOR_TEAM_ID'].iloc[i] == team_id:
            val = season_stats[x + '_away'].iloc[i]
            games_so_far += 1
            tot_so_far += val
            ave_so_far = tot_so_far/(games_so_far)
    return ave_so_far, tot_so_far

def running_home_allowed(x, team_id, season_stats, aves, tots):

    ave_so_far = 0.0
    tot_so_far = 0.0
    games_so_far = 0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        aves[index] = ave_so_far
        tots[index] = tot_so_far
        if season_stats['HOME_TEAM_ID'].iloc[i] == team_id:
            val = season_stats[x + '_away'].iloc[i]
            games_so_far += 1
            tot_so_far += val
            ave_so_far = tot_so_far/(games_so_far)
    return ave_so_far, tot_so_far

def running_away_allowed(x, team_id, season_stats, aves, tots):

    ave_so_far = 0.0
    tot_so_far = 0.0
    games_so_far = 0
    for i in range(season_stats.shape[0]):
        # put average going into the game the row represents
        index = season_stats.index[i]
        aves[index] = ave_so_far
        tots[index] = tot_so_far
        if season_stats['VISITOR_TEAM_ID'].iloc[i] == team_id:
            val = season_stats[x + '_home'].iloc[i]
            games_so_far += 1
            tot_so_far += val
            ave_so_far = tot_so_far/(games_so_far)
    return ave_so_far, tot_so_far

# for each (TEAM_ID, SEASON) pair, isolate those stats

# group by season
games_season_groups = games.groupby(['SEASON'])

# iterate through groups
for name, group in games_season_groups:
    # iterate through team_ids
    for team_id in team_ids:
        # indices for this (TEAM_ID, SEASON) pair
        indices = []
        for i in range(group.shape[0]): # for games in this season
            if group['HOME_TEAM_ID'].iloc[i] == team_id:
                indices.append(group.index[i])
            if group['VISITOR_TEAM_ID'].iloc[i] == team_id:
                indices.append(group.index[i])
        # get the slice of games corresponding to the pair
        season_stats = games.loc[indices]
        # sort games by date
        season_stats = season_stats.sort_values('GAME_DATE_EST')
        # new row for totals
        new_row = {}
        new_row['TEAM_ID'] = [team_id]
        new_row['TEAM_ABBREVIATION'] = [team_abbreviation[team_id]]
        new_row['SEASON'] = [name]
        for x in stats_names:
            # offense averages
            h_aves = new_cols['HOME_TEAM_' + x + '_ave']
            h_tots = new_cols['HOME_TEAM_' + x + '_tot']
            a_aves = new_cols['AWAY_TEAM_' + x + '_ave']
            a_tots = new_cols['AWAY_TEAM_' + x + '_tot']
            end_ave, end_tot = running(x, team_id, season_stats, h_aves, a_aves, h_tots, a_tots)
            new_row[x + '_ave'] = [end_ave]
            new_row[x + '_tot'] = [end_tot]
            # offense home averages
            aves = new_cols['HOME_TEAM_' + x + '_home_ave']
            tots = new_cols['HOME_TEAM_' + x + '_home_tot']
            end_ave, end_tot = running_home(x, team_id, season_stats, aves, tots)
            new_row[x + '_home_ave'] = [end_ave]
            new_row[x + '_home_tot'] = [end_tot]
            # offense away averages
            aves = new_cols['AWAY_TEAM_' + x + '_away_ave']
            tots = new_cols['AWAY_TEAM_' + x + '_away_tot']
            end_ave, end_tot = running_away(x, team_id, season_stats, aves, tots)
            new_row[x + '_away_ave'] = [end_ave]
            new_row[x + '_away_tot'] = [end_tot]
            # defense averages
            h_aves = new_cols['HOME_TEAM_' + x + '_allowed_ave']
            a_aves = new_cols['AWAY_TEAM_' + x + '_allowed_ave']
            h_tots = new_cols['HOME_TEAM_' + x + '_allowed_tot']
            a_tots = new_cols['AWAY_TEAM_' + x + '_allowed_tot']
            end_ave, end_tot = running_allowed(x, team_id, season_stats, h_aves, a_aves, h_tots, a_tots)
            new_row[x + '_allowed_ave'] = [end_ave]
            new_row[x + '_allowed_tot'] = [end_tot]
            # defense home averages
            aves = new_cols['HOME_TEAM_' + x + '_home_allowed_ave']
            tots = new_cols['HOME_TEAM_' + x + '_home_allowed_tot']
            end_ave, end_tot = running_home_allowed(x, team_id, season_stats, aves, tots)
            new_row[x + '_home_allowed_ave'] = [end_ave]
            new_row[x + '_home_allowed_tot'] = [end_tot]
            # defense away averages
            aves = new_cols['AWAY_TEAM_' + x + '_away_allowed_ave']
            tots = new_cols['AWAY_TEAM_' + x + '_away_allowed_tot']
            end_ave, end_tot = running_away_allowed(x, team_id, season_stats, aves, tots)
            new_row[x + '_away_allowed_ave'] = [end_ave]
            new_row[x + '_away_allowed_tot'] = [end_tot]
        # record wins and losses
        wins, losses, win_perc = wins_and_losses(team_id, season_stats, new_cols)
        new_row['WINS'] = [wins[0]]
        new_row['WINS_HOME'] = [wins[1]]
        new_row['WINS_AWAY'] = [wins[2]]
        new_row['LOSSES'] = [losses[0]]
        new_row['LOSSES_HOME'] = [losses[1]]
        new_row['LOSSES_AWAY'] = [losses[2]]
        new_row['WIN_PCT'] = [win_perc[0]]
        new_row['WIN_PCT_HOME'] = [win_perc[1]]
        new_row['WIN_PCT_AWAY'] = [win_perc[2]]
        # put new row in totals dataframe
        new_row = pd.DataFrame(new_row)
        totals = pd.concat([totals, new_row], axis=0)
# put new columns in games dataframe
new_cols_df = pd.DataFrame(new_cols)
games_aves = pd.concat([games, new_cols_df], axis=1)
# save as csv files
totals.to_csv('regular_season_teams_ending_aves_tots_corrected.csv')
games_aves.to_csv('regular_season_teams_running_aves_tots_corrected.csv')

print('Time: ' + str(time.time() - time0))
print('done')
