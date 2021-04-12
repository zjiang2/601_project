import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import datetime
import nltk

unigram_corpus = {}
bigram_corpus = {}

# count unigrams
def count_unigrams(tweet):
    global unigram_corpus
    words = tweet.split(" ")
    for word in words:
        if word in unigram_corpus:
            unigram_corpus[word] += 1
        else:
            unigram_corpus[word] = 1

# get bigrams from the list of tweets
def count_bigrams(tweet):
    global bigram_corpus
    bigrams = nltk.bigrams(tweet.split(" "))
    for bg in bigrams:
        if bg in bigram_corpus:
            bigram_corpus[bg] += 1
        else:
            bigram_corpus[bg] = 1


# Load pickled tweet data.
with open('data/pickled_tweets/home.pkl', 'rb') as f:
    home_tweets = pickle.load(f)
with open('data/pickled_tweets/away.pkl', 'rb') as f:
    away_tweets = pickle.load(f)

#Now, home tweets is a list of list of tweets
#Has n_games number of lists, each list a list of tweets
#Ditto for away tweets

#Create the corpus
for tweet in home_tweets:
	count_unigrams(tweet)
	count_bigrams(tweet)
for tweet in away_tweets:
	count_unigrams(tweet)
	count_bigrams(tweet)
