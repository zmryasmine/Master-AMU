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

kmeans = KMeans(n_clusters=10)
kmeans_clusters = kmeans.fit_predict(X)

gmm = GaussianMixture(n_components=10)
gmm_clusters = gmm.fit_predict(X)

rand_index = adjusted_rand_score(kmeans_clusters, gmm_clusters)

print("Rand Index entre K-Means et GMM :",rand_index)

df['popularity']= data['popularity']

df['KMeans_Cluster'] = kmeans_clusters

# Compter le nombre d'occurrences de chaque niveau de popularité dans chaque cluster
cluster_popularity_counts = df.groupby(['KMeans_Cluster', 'popularity']).size().unstack(fill_value=0)

print(cluster_popularity_counts)

vrai_labels = df['popularity']

rand_index = adjusted_rand_score(vrai_labels, kmeans_clusters)

print("Rand Index Kmeans avec vérité terrain:",rand_index)

# Calculer les distances entre chaque chanson et les centres des clusters
distances = cdist(df_features, centers, metric='euclidean')

# Identifier les indices des chansons les plus proches de chaque centre de cluster
indices_plus_proches = np.argmin(distances, axis=0)

# Afficher les résultats
for i, indice_chanson in enumerate(indices_plus_proches):
    print(f"Centre du Cluster {i + 1} - Chanson la plus proche : {data['track_name'].iloc[indice_chanson]}")


centroides = kmeans.cluster_centers_

# Créer un DataFrame pour les centroides pour une analyse plus facile
df_centroides = pd.DataFrame(centroides, columns=df_features.columns)

print(df_centroides)

