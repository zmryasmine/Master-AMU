import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn import neighbors as nn

digitsData=load_digits() # jeu de données digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

p_values = [1, 2, 5]
scores = []

# Faire varier p
for p in p_values:
    k_values = list(range(1, 21))
    p_scores = []
    
    # Faire varier k
    for k in k_values:
        clf = nn.KNeighborsClassifier(n_neighbors=k, p=p) 
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = clf.score(X_test,y_test)
        p_scores.append(accuracy)
    
    scores.append(p_scores)
    
for i, p in enumerate(p_values):
    plt.plot(k_values, scores[i], label=f'p={p}')

plt.xlabel('Nombre de voisins (k)')
plt.ylabel('Précision')
plt.title('Impact de la distance (p) et de k sur les performances de KNN')
plt.legend()
plt.show()

