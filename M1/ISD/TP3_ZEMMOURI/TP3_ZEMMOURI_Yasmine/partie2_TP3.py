from http.cookiejar import LoadError
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from mpl_toolkits.mplot3d import Axes3D

def loadData(path):
    data = np.loadtxt(path)
    return data[:,0], data[:,1].reshape(-1,1)

myScores = []

#Question 1,2 et 3 :
h,c = loadData('eucalyptus.txt')
reg = LinearRegression().fit(c, h)
print("Paramètres : Coef =",reg.coef_,", Intercept =", reg.intercept_)
print("MSE :",mean_squared_error(h, reg.predict(c)))
scores = cross_val_score(reg, c, h, cv=10)    
print("Cross_val =",scores.mean())
myScores.append(scores.mean())

print("Prediction de 22,8 =",reg.predict(np.array(22.8).reshape(-1,1)))

plt.scatter(c, h, marker='.')
plt.plot(c, reg.predict(c), color='red')
plt.plot(c,(reg.coef_*c)+reg.intercept_, color='green')
plt.xlabel('c')
plt.ylabel('h')
plt.title('Régression Linéaire sur les données Eucalyptus')
plt.show()

#Question 4 :

h , c1 = loadData('eucalyptus.txt')
c2 = np.sqrt(c1)
c = np.concatenate((c1,c2),axis=1)
print(c.shape)

linear = LinearRegression().fit(c, h)
print("Paramètres avec sqrt(c) : Coef =",linear.coef_,", Intercept =", linear.intercept_)
print("MSE  avec sqrt(c):",mean_squared_error(h, linear.predict(c)))
scores = cross_val_score(linear, c, h, cv=10)    
print("Cross_val avec sqrt(c):",scores.mean())
myScores.append(scores.mean())

#Affichage 3D
from mpl_toolkits.mplot3d import Axes3D
h_ = linear.coef_[0]*c1+linear.coef_[1]*c2+linear.intercept_
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(c1,c2,h, marker='.')
#ax.plot(c1,c2,h_,'r', marker='.')

plt.plot(c, h, color="blue", linewidth=0, marker=".")
plt.plot(c, linear.predict(c), ".", color="red", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.title('Régression Linéaire sur les données Eucalyptus avec sqrt(c)')
plt.show()

#Question 5 :

h , c1 = loadData('eucalyptus.txt')
c2 = np.sqrt(c1)
c3 = c1**2
C = np.concatenate((c1,c2,c3),axis=1)
print(C.shape)

lin_reg = LinearRegression().fit(C, h)
print("Paramètres avec c^2: Coef =",lin_reg.coef_,", Intercept =", lin_reg.intercept_)
print("MSE avec c^2:",mean_squared_error(h, lin_reg.predict(C)))
scores = cross_val_score(lin_reg, C, h, cv=10)    
print("Cross_val avec c^2:",scores.mean())
myScores.append(scores.mean())

#Question 6 :
# Régression 1 avec seulement c, Régression 2 avec sqrt(c), Régression 3 avec sqrt(c) et c^2.
print("Meilleur score by cross_val =",np.max(myScores),"de la régression num :",np.argmax(myScores)+1)