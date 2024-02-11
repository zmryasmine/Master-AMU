import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn import neighbors as nn
from sklearn.metrics import confusion_matrix

import seaborn as sns
import pandas as pd

def matrice_confusion(actual,predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    m = np.zeros((10, 10))
  
    for a, p in zip(actual, predicted):     
        m[a][p] += 1 
    return m

def affichageMatrice(mc,couleur,titre):
    class_names=[ "0","1",  "2",  "3",  "4" , "5",  "6" , "7",  "8",  "9"]
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns.heatmap(pd.DataFrame(mc,index=class_names,columns=class_names), annot=True, cmap=couleur ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title(titre, y=1.1)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')

digitsData=load_digits() # jeu de données digits
X=digitsData.data # les exemples, un array numpy, chaque élément est aussi un array
y=digitsData.target # les classes

Xtrain, Xtest, ytrain, ytest = train_test_split(X,y,test_size=0.3,random_state=42) 
clf = nn.KNeighborsClassifier(n_neighbors=12, p=2) 
clf.fit(Xtrain, ytrain)
predicted = clf.predict(Xtest)

mc=matrice_confusion(ytest,predicted)

affichageMatrice(mc,"BuGn",'Matrice de confusion')

print(confusion_matrix(ytest, predicted))