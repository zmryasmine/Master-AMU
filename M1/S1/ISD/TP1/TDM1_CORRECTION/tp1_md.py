#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 09:26:56 2023

@author: cecile
"""

import numpy as np
from sklearn.datasets import load_digits
import random
import math
digits = load_digits()
miss_digits = load_digits()
nbmissingvalues = random.randint(1000,2000)
for imissingvalue in range(nbmissingvalues):
    lig = random.randint(0,1763)
    col = random.randint(0,63)
    miss_digits.data[lig,col] = math.nan
mdd1 = miss_digits.data.copy() # pour tester methode 1
mdd2 = miss_digits.data.copy() # pour tester methode 2 
mdd3 = miss_digits.data.copy() # pour tester methode 3

# nb de valeurs manquantes sur 
# toutes les colonnes du dataset D
def nb_val_manquantes(D):
    nbmv = 0
    for x in np.nditer(D):
       if np.isnan(x):
        nbmv += 1
    return nbmv

nbmv = nb_val_manquantes(mdd1)

# nb val manquantes par colonne (retour: tableau numpy)
def nbvmanquantes_col(X):
    nbcol = X.shape[1]
    nbmvcol = np.zeros(nbcol, dtype=int) #nb de val manquantes par colonne (variable)
    for col in range(nbcol):
        for x in np.nditer(X[:,col]):
            if np.isnan(x):
                nbmvcol[col] += 1
    return nbmvcol

nbmvcol = nbvmanquantes_col(mdd1)
print("Nombre de valeurs manquantes colonne par colonne = ", nbmvcol)
print("Nombre de valeurs manquantes au total = ", nbmvcol.sum(), " (must be equal to : ", nbmv, ')')

# PREMIERE METHODE : stationnaire (pas de nouvelle valeur)
data = mdd1
print("VAL MANQUANTES AVANT ", nb_val_manquantes(mdd1))
nbcol = data.shape[1]
nbmvcol = np.zeros(nbcol, dtype=int)
for col in range(nbcol):
    freq = np.unique(data[:,col], return_counts=True)
    index = np.argmax(freq[1])
    mostfrequent_value = freq[0][index]
    for i in range(data.shape[0]):
        if np.isnan(data[i,col]):
            data[i,col] = mostfrequent_value

mdd1 = data

print("VAL MANQUANTES APRES ", nb_val_manquantes(mdd1))

# DEUXIEME METHODE (moyenne conditionnee par les classes)
nbcol = data.shape[1]
print("VAL MANQUANTES AVANT ", nb_val_manquantes(mdd2))
data = mdd2

nbmvcol = np.zeros(nbcol, dtype=int)
targets = miss_digits.target
iex = []
for classe in range(10): # index des exemples de chaque classe
    iex.append(np.argwhere(targets==classe))
for col in range(nbcol):
#    moyenne_classes = np.zeros(10)
    for classe in range(10):
        # recuperation de la moyenne de cette colonne pour ex de classe classe
        # ajustement pour garantir que la moyenne n'est pas NaN
        moyenne = np.nanmean(data[iex[classe],col]) # non prise en compte des NaN dans moyenne
        if np.isnan(moyenne):
            moyenne = np.nanmean(data[:,col])
        for i in iex[classe]:
            # remplacement des valeurs manquantes
            if np.isnan(data[i,col]):
                data[i,col] = moyenne
    
mdd2 = data
print("VAL MANQUANTES APRES ", nb_val_manquantes(mdd2))

# TROISIEME METHODE (completion selon kppv de sklearn)
from sklearn.impute import KNNImputer
import math

print("VAL MANQUANTES AVANT ", nb_val_manquantes(mdd3))
data = mdd3
k = int(math.log(data.shape[0])) # heuristique pour nombre de voisins
imputer = KNNImputer(n_neighbors=k)
mdd3 = imputer.fit_transform(data)

print("VAL MANQUANTES APRES ", nb_val_manquantes(mdd3))

# MEILLEURE METHODE ?
def score_imputation(Xinit, Ximputed):
    nb_row = Xinit.shape[0]
    nb_col = Xinit.shape[1]
    error = 0.
    for i in range(nb_row):
        for j in range(nb_col):
            error = error + (Xinit[i,j] -  Ximputed[i,j]) ** 2
    return error

# Calcul de l'erreur de chaque methode
data = load_digits().data
erreur_stationnaire = score_imputation(data, mdd1)
erreur_moy_cond = score_imputation(data, mdd2)
erreur_kppv = score_imputation(data, mdd3)
erreurs = [erreur_stationnaire, erreur_moy_condi, erreur_kppv]
print('Erreur stationnaire = ', erreur_stationnaire)
print('Erreur Moy/classe = ', erreur_moy_cond)
print('Erreur kppv = ', erreur_kppv)