#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:34:58 2023

@author: cecile
"""
from sklearn import neighbors as nn # importation du package d'algorithmes travaillant sur les points voisins
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# LES DONNEES
digitsData=load_digits() # jeu de donnees digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

from sklearn.metrics import confusion_matrix
k = 6
pminkowski = 5

Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3, random_state=42) 
clf = nn.KNeighborsClassifier(n_neighbors=k, p=pminkowski) 
clf.fit(Xtrain,ytrain)
yPredit = clf.predict(Xtest)
confusion = confusion_matrix(ytest, yPredit)
score = clf.score(Xtest, ytest)
erreur = 1. - score

print(confusion)
print(erreur)
print(score)