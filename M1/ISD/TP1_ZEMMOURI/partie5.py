from sklearn.datasets import load_digits
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn import decomposition  

digits = load_digits()

print("Digits shape:",digits.data.shape)

pca = decomposition.PCA(3)  # projection dans espace à deux axes (deux dimensions)
donnees_projetes = pca.fit_transform(digits.data)

print("Après PCA:",donnees_projetes.shape)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(donnees_projetes[:, 0], donnees_projetes[:, 1], donnees_projetes[:, 2], c=digits.target, edgecolor = 'none', cmap=plt.cm.get_cmap('nipy_spectral', 10))

ax.set_xlabel('Composante 1')
ax.set_ylabel('Composante 2')
ax.set_zlabel('Composante 3')

legend = ax.legend(*scatter.legend_elements(), title="Classes")
ax.add_artist(legend)

plt.show()