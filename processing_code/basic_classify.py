import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import datetime
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

#Suppose you have a data matrix X and response Y
cutoff = np.floor(len(X)*.8)

X_train = X[:cutoff]
Y_train = Y[:cutoff]
X_test = X[cutoff:]
Y_test = Y[cutoff:]

lr = LogisticRegression()
lr.fit(X_train, Y_train)
lr.score(X_test, Y_test)

ada = AdaBoostClassifier(n_estimators=1000)
ada.fit(X_train, Y_train)
ada.score(X_test, Y_test)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, Y_train)
rf.score(X_test, Y_test)

mlp = MLPClassifier(max_iter=1000)
mlp.fit(X_train, Y_train)
mlp.score(X_test, Y_test)

gnb = GaussianNB().fit(X_train, Y_train)
gnb.score(X_test, Y_test)


