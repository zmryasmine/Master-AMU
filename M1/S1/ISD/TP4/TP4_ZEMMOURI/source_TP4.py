#Import des librairies nécessaires 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import time
import seaborn as sns

data = pd.read_csv("unpopular_songs_full.csv") #Lecture du fichier USS
#Statistiques sur nos données
print("Informations sur le DataFrame :")
print(data.info())
print("Description du DataFrame :")
print(data.describe())

print("Valeurs manquantes par colonne:")
print(data.isnull().sum())
data.hist(figsize=(10, 10))
plt.show()

#Matrice de corrélation :
matrice = data.corr()
print("Matrice de corrélation:")
print(matrice)

plt.figure(figsize=(12, 10))
sns.heatmap(matrice, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title("Matrice de Corrélation")
plt.show()


#Distribution des valeurs de popularity :
plt.figure(figsize=(10, 6))
plt.hist(data['popularity'], bins=20, color='blue', alpha=0.7)
plt.title('Distribution de la Popularité')
plt.xlabel('Popularity')
plt.ylabel('Fréquence')
plt.grid(True)
plt.show()

#Nombre d\'occurrences de chaque classe :
print("Nombre d\'occurrences de chaque classe :")
counts = data['popularity'].value_counts()
counts = counts.sort_index()
for popularity, count in counts.items():
    print("Classe",popularity,":",count,"occurrences.")

print("Corrélation de popularity :")
print(matrice['popularity'])

#Suppression des colonnes :
col = ['track_name', 'track_artist',
       'track_id', 'Unnamed: 17','key','explicit','liveness','mode','acousticness','loudness']
data = data.drop(columns = col)
print("DataFrame après suppression des colonnes jugées inutiles :")
print(data.info())
#Standarisation des attributs réels :
df = data.drop('popularity', axis=1)
print("Avant standarisation :")
print(data.head())
col = df.select_dtypes(include=['float64']).columns
scaler = StandardScaler()
df[col] = scaler.fit_transform(df[col])
df['popularity'] = data['popularity']
print("Après standarisation :")
print(df.head())

X = df.drop('popularity', axis=1)
y = df['popularity']

#Arbre de décision :
clf = DecisionTreeClassifier(max_depth=5)

debut = time.time()
scores = cross_val_score(clf, X, y, cv=10)  
duree = time.time() - debut

print("Performances du classifieur arbre de décision:")
error = 1 - np.mean(scores)
print("Taux d'erreur  : ", error, "scores :", np.mean(scores), "Temps :", duree,"s.")

#KPP :
k = int(np.log(len(X)))

knn = KNeighborsClassifier(n_neighbors=k)
debut = time.time()
scores = cross_val_score(knn, X, y, cv=10)
duree = time.time() - debut

print("Performances du classifieur KPP:")
error = 1 - np.mean(scores)
print("Taux d'erreur  : ", error, "scores :", np.mean(scores), "Temps :", duree,"s.")

#Visualisation de l'arbre :
clf.fit(X, y)

plt.figure(figsize=(30, 10))
plot_tree(clf, filled=True, feature_names=list(X.columns), class_names=[str(i) for i in range(12)], rounded=True, precision=2, fontsize=10)
plt.show()

#Colonnes discriminantes :
feature_importances = clf.feature_importances_

importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
top_features = importance_df.head(6)
print("Les 6 colonnes les plus discriminantes :")
print(top_features)

col =[ 'energy','valence','duration_ms','speechiness','danceability','instrumentalness']
x = X[col]
best_k = 0
best_accuracy = 0

for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, x, y, cv=10)
    accuracy = np.mean(scores)
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_k = k

print("Meilleur k:", best_k)
print("Précision correspondante:", best_accuracy)

