import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import datetime
import pickle
import nltk

#Suppose you have a corpus called "corpus"

#Define a list of stopwords to remove.
stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

#Delete from corpus any words which
#are 2 letters or less, are a stop word,
#or are a hashtag
revised_corpus = corpus.copy()
for key in list(revised_corpus.keys()):
    if len(key) <= 2:
        del revised_corpus[key]
    elif key in stopwords:
        del revised_corpus[key]
    elif key[0] == '#':
        del revised_corpus[key]


#Create a list of the top grams (whether they're bigrams or unigrams)
top_grams = [x[0] for x in sorted(revised_corpus.items(), key=lambda x: x[1], reverse=True)[:1000]]


#Turns a list of tweets (for one team, for one game)
#into a vector using the top_grams
from collections import Counter
def vectorize_list(list_of_tweets, corpus):
    num_tweets = len(list_of_tweets)
    lol = [x.split() for x in list_of_tweets]
    with_repeats = [item for sublist in lol for item in sublist]
    counts = dict(Counter(with_repeats))
    to_return = []
    for key in corpus:
        num = counts[key]/num_tweets if key in counts else 0
        to_return.append(num)
    return to_return


#Create lists of vectors for home, away games
num_h_tweets = [vectorize_list(game, top_grams) for game in home_tweets]
num_a_tweets = [vectorize_list(game, top_grams) for game in away_tweets]

#Turn into arrays
home_vecs = np.array(num_h_tweets)
away_vecs = np.array(num_a_tweets)

#Concatenate home, away to form input matrix.
X = np.concatenate([home_vecs, away_vecs], axis=1)