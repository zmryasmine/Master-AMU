#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 19:50:08 2023

@author: cecile
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Lecture des donnees
def q121():
    data = np.loadtxt('eucalyptus.txt')
    h = data[:,0]
    c = data[:,1]
    return h,c

# Nuage de points
h,c = q121()
plt.scatter(c,h)

# Apprentissage et visualtion + score du regresseur
from sklearn.model_selection import cross_val_score

h,c = q121()
C = c.reshape(-1,1) #obtention d'un X multivarie avec une seule variable
#
# Entrainement
#
lr = LinearRegression()
lr.fit(C,h)
print("Paramètres = "+str(lr.coef_)+" "+str(lr.intercept_))
#
# Affichage graphique
#
plt.scatter(c,h)
plt.plot(c,lr.predict(C),'r')
#
# coefficient de determination (score) par validation croisee 10 folds
#
lr = LinearRegression()
scores = cross_val_score(lr, C, h, cv=10)    
print("Score = "+str(scores.mean())) # coefficient de determination

# le score pour l'eucalyptus de circonference x=22.8
lr.fit(C,h)
print(lr.predict(np.array([22.8]).reshape(1, -1)))

#
# AJOUT DE NON LINEARITE
#
from mpl_toolkits.mplot3d import Axes3D

h,c = q121()
s = np.sqrt(c)
C = c.reshape(-1,1)
S = np.sqrt(C)
CS = np.concatenate((C,S),axis=1)
#
# Entrainement
#
lr = LinearRegression()
lr.fit(CS,h)
print("Paramètres = "+str(lr.coef_)+" "+str(lr.intercept_))
#
# Affichage graphique
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(c,s,h)
ax.plot(c,s,lr.predict(CS),'r')
#
# coefficient de determination (score) par validation croisee 10 folds
#
lr = LinearRegression()
scores = cross_val_score(lr, CS, h, cv=10)
print("Score = "+str(scores.mean())) # coefficient de determination

# Ajout autre linearite
h,c = q121()
C = c.reshape(-1,1)
S = np.sqrt(C)
CAR = C**2
CS = np.concatenate((C,S),axis=1)
TOT = np.concatenate((CS,CAR),axis=1)
#
# Entrainement
#
lr = LinearRegression()
lr.fit(TOT,h)
print("Paramètres = "+str(lr.coef_)+" "+str(lr.intercept_))
#
# coefficient de determination (score) par validation croisee 10 folds
#
lr = LinearRegression()
scores = cross_val_score(lr, TOT, h, cv=10)
print("Score = "+str(scores.mean())) # coefficient de determination
