#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:34:58 2023

@author: cecile
"""
from partie1_TP2 import erreur_app
import numpy as np
from sklearn import neighbors as nn # importation du package d'algorithmes travaillant sur les points voisins
import matplotlib.pyplot as plt  # le package de visualisation
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

# LES DONNEES
digitsData=load_digits() # jeu de donnees digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

# PRODUCTION DE SOUS ECHANTILLONS

# une valeur de random_state
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.25, random_state=42) 
print(Xtrain[:3,:], ytrain[:3])
print(Xtest[:3,:], ytest[:3])

# autre valeur de random_state
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.25, random_state=18) 
print(Xtrain[:3,:], ytrain[:3])
print(Xtest[:3,:], ytest[:3])

# on verifie que les splits obtenus sont bien differents avec les deux valeurs de random_state

# EVALUATION DU SCORE SUR UN SPLIT avec k=3
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.5, random_state=42) 
k = 3
clf = nn.KNeighborsClassifier(k) 
clf.fit(Xtrain, ytrain) # apprentissage du model sur une partie de l'echantillon
erreur = 1 - clf.score(Xtest, ytest) # observation de l'erreur du modele sur de nouvelles donnees
print(erreur)

Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3, random_state=42) 
rangek = np.arange(1,26,dtype=int)
erreur_test = np.zeros(25)
for k in rangek:
    clf = nn.KNeighborsClassifier(k) 
    clf.fit(Xtrain,ytrain)
    erreur_test[k-1] = 1-clf.score(Xtest,ytest)

plt.plot(rangek, erreur_test)
plt.plot(rangek, erreur_app, color="red")

# REPETITIONS DE 10 HOLD-OUT DIFFERENTS ET MOYENNAGE k=3
erreur_test = np.zeros(10)
k = 3
for iho in range(10):
    Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3, random_state=iho) # graine change
    clf = nn.KNeighborsClassifier(k) 
    clf.fit(Xtrain,ytrain)
    erreur_test[iho] = 1-clf.score(Xtest,ytest)
print(erreur_test)
print (erreur_test.mean())