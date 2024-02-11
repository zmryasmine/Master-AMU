import numpy as np
from sklearn.datasets import load_digits
import random
import math
from sklearn.impute import KNNImputer, SimpleImputer

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

def globalement(data):
    return np.isnan(data).sum()

def par_colonnes(data):
    return np.isnan(data).sum(axis=0)

def replaceByMode(mdd1):
    mode_replacer = SimpleImputer(strategy='most_frequent')
    return  mode_replacer.fit_transform(mdd1)

def combinaison_lin(data, targets):
    data_norm = data.copy()
    unique = np.unique(targets)

    for t in unique:
        exemples = data[targets == t]

        for i in range(exemples.shape[1]):
            moy = np.nanmean(exemples[:, i])  
            manquantes = np.isnan(exemples[:, i])  
            exemples[manquantes, i] = moy 

        data_norm[targets == t] = exemples

    return data_norm

def knn(mdd3,k):
    knn_replacer = KNNImputer(n_neighbors=k)
    return knn_replacer.fit_transform(mdd3)

def ecart(data,real):
    return np.mean((data - real) ** 2)

manquantes_glob = globalement(miss_digits.data)
manquantes_col = par_colonnes(miss_digits.data)

print("Nombre de valeurs manquantes globalement initialement:", manquantes_glob)
print("Nombre de valeurs manquantes par colonne initialement:", manquantes_col)

data_normalised_mode = replaceByMode(mdd1)
print("Nombre de valeurs manquantes globalement après méthode 1:", globalement(data_normalised_mode.data))
print("Nombre de valeurs manquantes par colonne après méthode 1:", par_colonnes(data_normalised_mode.data))


data_normalised_lin = combinaison_lin(mdd2, miss_digits.target)
print("Nombre de valeurs manquantes globalement après méthode 2:", globalement(data_normalised_lin.data))
print("Nombre de valeurs manquantes par colonne après méthode 2:", par_colonnes(data_normalised_lin.data))

data_normalised_knn = knn(mdd3,5)
print("Nombre de valeurs manquantes globalement après méthode 3:", globalement(data_normalised_knn.data))
print("Nombre de valeurs manquantes par colonne après méthode 3:", par_colonnes(data_normalised_knn.data))

methods = [("Mode", ecart(data_normalised_mode, digits.data)), ("Combinaison Linéaire", ecart(data_normalised_lin, digits.data)), ("KNN Imputer", ecart(data_normalised_knn, digits.data))]
methods = sorted(methods, key=lambda x: x[1])

print("Tri meilleure méthode :",methods)