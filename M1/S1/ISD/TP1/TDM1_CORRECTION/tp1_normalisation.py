import pandas as pd
poba = pd.read_csv('fruits.csv')
poba.describe()

# X est un dataframe
def normaMinMax(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") # pour ne pas tenir compte de cette information
    nbl, nbc = Xn.shape
    for i in range(nbl):
        for j in range(nbc):
            Xn.iloc[i,j] = ( X.iloc[i,j] - X.iloc[:,j].min() ) / (X.iloc[:,j].max() - X.iloc[:,j].min())
    Xn["Fruit"] = X["Fruit"]
    return Xn

def normaMean(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") # pour ne pas tenir compte de cette information
    nbl, nbc = Xn.shape
    for i in range(nbl):
        for j in range(nbc):
            mean_j = X.iloc[:,j].mean()
            Xn.iloc[i,j] = ( X.iloc[i,j] - mean_j ) / (X.iloc[:,j].max() - X.iloc[:,j].min())
    Xn["Fruit"] = X["Fruit"]
    return Xn

def normaStandard(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") # pour ne pas tenir compte de cette information
    nbl, nbc = Xn.shape
    for i in range(nbl):
        for j in range(nbc):
            mean_j = X.iloc[:,j].mean()
            std_j = X.iloc[:,j].std()
            Xn.iloc[i,j] = ( X.iloc[i,j] - mean_j ) / std_j
    Xn["Fruit"] = X["Fruit"]
    return Xn

from numpy import linalg as LA

def normaProjBall(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") # pour ne pas tenir compte de cette information
    nbl, nbc = Xn.shape
    for i in range(nbl):
        for j in range(nbc):
            mean_j = X.iloc[:,j].mean()
            norm_j = LA.norm(np.array(X.iloc[:,j]))
            Xn.iloc[i,j] = ( X.iloc[i,j] - mean_j ) / norm_j
    Xn["Fruit"] = X["Fruit"]
    return Xn

import pylab as pl

def affichage_nuages()
    colors = ["red", "blue"]
    fruits = ["pomme", "banane"]
    titre = ["MinMax", "Moyenne", "Standardisation", "Sphere"]
    
    pl.figure(figsize = (7,5))
    
    TXd = np.array(poba.iloc[:,0:2]) # deux premieres colonnes
    TXt = np.array(poba.iloc[:,2])    
    for c in range(2):
        pl.scatter(TXd[TXt==c][:, 0], TXd[TXt==c][:, 1], color = colors[c],\
                   label = fruits[c])
        
    pl.legend()
    pl.xlabel("Weight")
    pl.ylabel("Length")
    pl.title("Donnees initiales")
    pl.show()
    
    N = [normaMinMax(poba), normaMean(poba), normaStandard(poba), normaProjBall(poba)]
    fig, axs = pl.subplots(2, 2, figsize=(16,10))
    
    k = 0 # indice du nuage de points
    for x in range(2): #  position du nuage de points a afficher sur abscisse de grille de nuages
        for y in range(2): # position du nuage de points a afficher sur ordonnee de grille de nuages
            i = k // 2
            j = k % 2
            TNkd = np.array(N[k].iloc[:,0:2]) # deux premieres colonnes
            TNkt = np.array(N[k].iloc[:,2])   # derniere colonne: la classe pour la couleur
            k = k + 1
            for c in range(2): #pour chaque couleur (classe)
                # affichage du nuage de points
                axs[i,j].scatter(TNkd[TNkt==c][:,0], TNkd[TNkt==c][:,1], color = colors[c], label = fruits[c])
            axs[i,j].set_xlabel("Weight")
            axs[i,j].set_ylabel("Length")
            axs[i,j].set_title(titre[k-1])
    pl.show()