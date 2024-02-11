from sklearn import decomposition
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

digits = load_digits()

pca = decomposition.PCA(3)  # projection de dim 64 à dim 2
donnees_projetes = pca.fit_transform(digits.data)

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(donnees_projetes[:, 0], donnees_projetes[:, 1], donnees_projetes[:, 2], c=digits.target, edgecolor='none', alpha=0.5,
            cmap=plt.cm.get_cmap('nipy_spectral', 10))
ax.set_xlabel('composante 1')
ax.set_ylabel('composante 2')
ax.set_zlabel('composante 3')
plt.show()