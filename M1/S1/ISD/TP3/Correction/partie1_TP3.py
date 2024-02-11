#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 19:50:08 2023

@author: cecile
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

x = np.array([5.5,6.0,6.5,6.0,5.0,6.5,4.5,5])
X = x.reshape(-1,1)
y = np.array([420,380,350,400,440,380,450,420])
lr = LinearRegression()
# Apprentissage du régresseur
lr.fit(X,y)
# Affichage du score MSE calcule sur exemples d'apprentissage (empirique)
print("MSE = "+str(mean_squared_error(y,lr.predict(X))))
# Coefficient de determination
print("Score = "+str(lr.score(X,y))) 
# Affichage des parametres appris: les valeurs des coefficients de l'equation de droite alpha et beta
print("Paramètres = "+str(lr.coef_)+" "+str(lr.intercept_))

# Affichage du nuage de points et des droites
# deux points sur la droite apprise, pour affichage en vert
import matplotlib.pyplot as plt
x0, x1 = 4.0,7.0 
y0 = lr.coef_*x0+lr.intercept_
y1 = lr.coef_*x1+lr.intercept_
plt.plot([x0,x1], [y0,y1], 'g')
# le nuage de points
plt.scatter(x,y,c="blue")
# la droite predicte calculee sur toutes les donnees
plt.plot(X,lr.predict(X),'r')
plt.show()

#
# Apprentissage du regresseur sans calcul du biais
#
lr = LinearRegression(fit_intercept=False)
lr.fit(X,y)
print("MSE = "+str(mean_squared_error(y,lr.predict(X))))
print("Score = "+str(lr.score(X,y))) # coefficient de determination
print("Paramètres = "+str(lr.coef_)+" "+str(lr.intercept_))    
x0, x1 = 4.0,7.0
y0 = lr.coef_*x0+lr.intercept_
y1 = lr.coef_*x1+lr.intercept_
plt.plot([x0,x1], [y0,y1], 'g')
plt.scatter(x,y,c="blue")
plt.plot(X,lr.predict(X),'r')
plt.show()