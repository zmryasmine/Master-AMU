#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:34:58 2023

@author: cecile
"""
import numpy as np
from sklearn import neighbors as nn # importation du package d'algorithmes travaillant sur les points voisins
import matplotlib.pyplot as plt  # le package de visualisation
from sklearn.datasets import load_digits

# LES DONNEES
digitsData=load_digits() # jeu de données digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

# VARIATION DU NOMBRE DE VOISINS
rangek = np.arange(1,26,dtype=int)
erreur_app = np.zeros(25)
for k in rangek:
    clf = nn.KNeighborsClassifier(k) 
    clf.fit(X,y)
    erreur_app[k-1] = 1-clf.score(X,y)

plt.plot(rangek, erreur_app)