import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score, adjusted_rand_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("unpopular_songs_full.csv")

columns = ['danceability', 'loudness', 'duration_ms', 'instrumentalness','valence', 'acousticness']
df = data[columns]
print(df)

scaler = StandardScaler()
df = scaler.fit_transform(df)

def davies_bouldin(X, labels):
    clusters = np.unique(labels)
    k = 10
    centres = np.array([X[labels == i].mean(axis=0) for i in clusters])

    cluster_distances = np.zeros((k, k))

    for i in range(k):
        for j in range(k):
            if i != j:
                distance = np.linalg.norm(centres[i] - centres[j])
                cluster_distances[i, j] = distance

    score = np.zeros(k)

    for i in range(k):
        max_diameters = 0
        for j in range(k):
            if i != j:
                diameter = np.max([np.linalg.norm(X[labels == i] - centres[i]), np.linalg.norm(X[labels == j] - centres[j])])
                if diameter > max_diameters:
                    max_diameters = diameter

        score[i] = max_diameters / cluster_distances[i, np.argmax(np.delete(cluster_distances[i, :], i))]

    return np.mean(score)

print("K-MEANS :\n")
X = df
y = data['popularity']

scores_train = []
silhouettes_train = []
rand_train = []
scores_test = []
silhouettes_test = []
rand_test = []

for i in range(10):
    print("Itération :",i+1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None)
    
    kmeans = KMeans(n_clusters=10)  
    kmeans.fit(X_train)
    
    clusters = kmeans.predict(X_test)

    scores_train.append( davies_bouldin_score(X_train, kmeans.labels_))
    silhouettes_train.append(silhouette_score(X_train, kmeans.labels_))
    rand_train.append(adjusted_rand_score(y_train, kmeans.labels_))
    print("Scores sur le jeu d'apprentissage (DB, Silhouette, Rand Index):",davies_bouldin_score(X_train, kmeans.labels_), silhouette_score(X_train, kmeans.labels_), adjusted_rand_score(y_train, kmeans.labels_))

        # Étape 5 : Calculer les scores sur le jeu de test
    scores_test.append(davies_bouldin_score(X_test, clusters))
    silhouettes_test.append(silhouette_score(X_test, clusters))
    rand_test.append(adjusted_rand_score(y_test, clusters))
    print("Scores sur le jeu de test (DB, Silhouette, Rand Index)", davies_bouldin_score(X_test, clusters), silhouette_score(X_test, clusters), adjusted_rand_score(y_test, clusters))



print("KMeans :\n")
print("Moyenne des scores sur le jeu d'apprentissage (DB, Silhouette, Rand Index):",np.mean(scores_train), np.mean(silhouettes_train), np.mean(rand_train))
print("Moyenne des scores sur le jeu de test (DB, Silhouette, Rand Index)",np.mean(scores_test), np.mean(silhouettes_test), np.mean(rand_test))


print("GAUSSIAN :\n")

scores_train = []
silhouettes_train = []
rand_train = []
scores_test = []
silhouettes_test = []
rand_test = []

for i in range(10):
    print("Itération :",i+1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None)
    
    gmm = GaussianMixture(n_components=10)
    gmm.fit(X_train)
    
    clusters = gmm.predict(X_test)

    scores_train.append( davies_bouldin_score(X_train, gmm.predict(X_train)))
    silhouettes_train.append(silhouette_score(X_train, gmm.predict(X_train)))
    rand_train.append(adjusted_rand_score(y_train, gmm.predict(X_train)))
    print("Scores sur le jeu d'apprentissage (DB, Silhouette, Rand Index):",davies_bouldin_score(X_train, gmm.predict(X_train)), silhouette_score(X_train, gmm.predict(X_train)), adjusted_rand_score(y_train, gmm.predict(X_train)))

        # Étape 5 : Calculer les scores sur le jeu de test
    scores_test.append(davies_bouldin_score(X_test, clusters))
    silhouettes_test.append(silhouette_score(X_test, clusters))
    rand_test.append(adjusted_rand_score(y_test, clusters))
    print("Scores sur le jeu de test (DB, Silhouette, Rand Index)",davies_bouldin_score(X_test, clusters), silhouette_score(X_test, clusters), adjusted_rand_score(y_test, clusters))



print("Gaussian Mixture :\n")
print("Moyenne des scores sur le jeu d'apprentissage (DB, Silhouette, Rand Index):",np.mean(scores_train), np.mean(silhouettes_train), np.mean(rand_train))
print("Moyenne des scores sur le jeu de test (DB, Silhouette, Rand Index)",np.mean(scores_test), np.mean(silhouettes_test), np.mean(rand_test))

