import numpy as np 
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn import neighbors as nn

digitsData=load_digits() # jeu de données digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

nb_voisins = 36
liste = []
for nb in range(1,nb_voisins):
    clf = nn.KNeighborsClassifier(nb) 
    clf.fit(X, y) 
    liste.append((1-clf.score(X,y)))
    print('Taux d\'erreur pour k=', nb, (1-clf.score(X,y)))

plt.figure(figsize=(15, 10))
plt.plot(range(1,nb_voisins), liste, marker='o')
plt.xlabel('Valeur de k')
plt.ylabel('Erreur d\'apprentissage')
plt.title('Evolution du taux d\'erreur selon le nombre de voisins k.')
plt.xticks(np.arange(0,36,1))
plt.grid()
plt.show()

print('Best k=',np.argsort(liste)[1]+1)
