import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import datetime

# Read in the team hashes
team_hashes = {}
with open('team_hashtags.txt', 'r') as f:
    for line in f:
        words = line.split()
        team = words[0].replace('-', ' ')
        hashes = words[1:]
        team_hashes[team] = hashes


# Get all hashtags from one tweet using regex
def get_hashtags(tweet):
    pattern = r'#{1}\w*'
    return re.findall(pattern, tweet)

#Returns true if a tweet only contains hashtags
#for one team, denoted "which_team"
#Does this by popping off the key of the given team
def one_team_only(one_tweet, which_team):
    all_teams = team_hashes.copy()
    good = all_teams.pop(which_team)
    temp = [team_hashes[key] for key in all_teams]
    bad_teams = [item for sublist in temp for item in sublist]
    bad_teams = set(bad_teams)
    curr_hashes = set(get_hashtags(one_tweet))
    
    if len(list(curr_hashes & bad_teams)) != 0:
            return False
    return True

# Read in the data, any of 4 seasons.
# Concatenated if needed
#Make sure to change datetime to UTC timezone
s1 = pd.read_csv('2020_all_data.csv', index_col=0)
s2 = pd.read_csv('2019_all_data.csv', index_col=0)
s3 = pd.read_csv('2018_all_data.csv', index_col=0)
s4 = pd.read_csv('2017_all_data.csv', index_col=0)
full = pd.concat([s4,s3,s2,s1],axis=0)
full['Datetime'] = pd.DatetimeIndex(full['Datetime'], tz='US/Eastern')
full['Datetime'] = full['Datetime'].dt.tz_convert('UTC')
full['Home'] = np.where(full['Home'] == 'Washington Redskins', 'Washington Football Team', full['Home'])
full['Away'] = np.where(full['Away'] == 'Washington Redskins', 'Washington Football Team', full['Away'])
full['Home'] = np.where(full['Home'] == 'San Diego Chargers', 'Los Angeles Chargers', full['Home'])
full['Away'] = np.where(full['Away'] == 'San Diego Chargers', 'Los Angeles Chargers', full['Away'])
full['Home'] = np.where(full['Home'] == 'St Louis Rams', 'Los Angeles Rams', full['Home'])
full['Away'] = np.where(full['Away'] == 'St Louis Rams', 'Los Angeles Rams', full['Away'])
full['Home'] = np.where(full['Home'] == 'Oakland Raiders', 'Las Vegas Raiders', full['Home'])
full['Away'] = np.where(full['Away'] == 'Oakland Raiders', 'Las Vegas Raiders', full['Away'])

# Initialize containers
home_tweets = []
away_tweets = []

#Given a game time datetime in UTC, and name of team
#scrapes twitter for tweets for that team.
#Can change look back period, e.g. 1-3 days
#Can change like requirement; cap at 10k
def one_game_one_team(game_time, team_name):
    start = game_time - datetime.timedelta(days=1,hours=1)
    end = game_time - datetime.timedelta(hours=1)
    date_range = " since:" + start.strftime('%Y-%m-%d') + " until:" + end.strftime('%Y-%m-%d')
    
    team_tags = " OR ".join(team_hashes[team_name])
    query = team_tags + date_range
    
    # Scrape the tweets for the date_range. Also have to filter based on the 
    # time stamp so as not to capture tweets during and after games.
    to_return = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > 10000:
            break
        if not (start <= tweet.date and tweet.date <= end):
            continue
        if tweet.likeCount < 10:
            continue
        if not one_team_only(tweet.content.lower(), team_name):
            continue
        tw = tweet.content.lower()
        to_return.append(tw)
    return to_return


#Given a dataframe of season information, 
#get tweets for each team, for each game.
#Can later be used to vectorize each game
#Can later be used to make corpus.
def get_season_tweets(df):
    for game in range(len(df)):
        print("Processing game number {}".format(game))
        gametime = df.iloc[game]['Datetime']
        hometeam = df.iloc[game]['Home']
        awayteam = df.iloc[game]['Away']
        
        h_tweets = one_game_one_team(gametime, hometeam)
        a_tweets = one_game_one_team(gametime, awayteam)
        
        home_tweets.append(h_tweets)
        away_tweets.append(a_tweets)
        
    return  

import pickle
with open('data/pickled_tweets/home.pkl', 'wb') as f:
    pickle.dump(home_tweets, f)
with open('data/pickled_tweets/away.pkl', 'wb') as f:
    pickle.dump(away_tweets, f)



