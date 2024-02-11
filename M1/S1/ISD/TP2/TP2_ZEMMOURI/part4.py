import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn import neighbors as nn

digitsData=load_digits() # jeu de données digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

#Premier appel
print("Premier appel :")
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.25, random_state=42) 
print(Xtrain[:3,:], ytrain[:3])
print(Xtest[:3,:], ytest[:3])

#Deuxième appel
print("Deuxième appel :")
Xtrain2, Xtest2, ytrain2, ytest2 = train_test_split(X,y,test_size=0.25, random_state=42) 
print(Xtrain2[:3,:], ytrain2[:3])
print(Xtest2[:3,:], ytest2[:3])

#Troisème appel
print("Troisième appel :")
Xtrain3, Xtest3, ytrain3, ytest3 = train_test_split(X,y,test_size=0.25, random_state=15) 
print(Xtrain3[:3,:], ytrain3[:3])
print(Xtest3[:3,:], ytest3[:3])

#Sans split
nb_voisins = 36
liste = []
for nb in range(1,nb_voisins):
    clf = nn.KNeighborsClassifier(nb) 
    clf.fit(X, y) 
    liste.append((1-clf.score(X,y)))

#Avec split
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.5, random_state=42) 
clf = nn.KNeighborsClassifier(3) 
clf.fit(Xtrain, ytrain)
print('erreur avec split :',(1-clf.score(Xtest,ytest)), 'vs sans: ',liste[2])
print('score avec split :',clf.score(Xtest,ytest), 'vs sans :', clf.score(X,y) )

#Variation de k avec split
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3, random_state=42) 
nb_voisins = 36
liste2 = []
for nb in range(1,nb_voisins):
    clf = nn.KNeighborsClassifier(nb) 
    clf.fit(Xtrain, ytrain) 
    #predicted_X = clf.predict(Xtest)
    liste2.append((1-clf.score(Xtest,ytest)))
    print('Taux d\'erreur pour k=', nb, (1-clf.score(Xtest,ytest)))

plt.figure(figsize=(10, 8))
plt.plot(range(1,nb_voisins), liste,label='Sans split', marker='o')
plt.plot(range(1,nb_voisins), liste2,label='Avec split', marker='o')
plt.xlabel('Valeur de k')
plt.ylabel('Erreur d\'apprentissage')
plt.title('Evolution du taux d\'erreur selon le nombre de voisins k.')
plt.xticks(np.arange(0,36,1))
plt.legend()
plt.grid()
plt.show()

#Hold_out répété
liste = []
for i in range(10):
    Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3) 
    clf = nn.KNeighborsClassifier(3) 
    clf.fit(Xtrain, ytrain)
    #predicted_X = clf.predict(Xtest)
    print('Erreur n°', i+1,':',(1-clf.score(Xtest,ytest)))
    liste.append((1-clf.score(Xtest,ytest)))

print('Estimation du hold_out répété 10 fois:',np.mean(liste))

#Validation croisée
clf = nn.KNeighborsClassifier(3) 
scores = cross_val_score(clf, X, y, cv=10)
error = 1 - np.mean(scores)
print("Taux d'erreur (k=3) par validation croisée : ", error, "scores :", np.mean(scores))

#F1_Mesure 
mon_score = cross_val_score(clf, X, y, cv=5, scoring = 'f1_macro')
print("F1_mesure obtenue :",mon_score)
print("Moyenne :",mon_score.mean())