import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#Question 6 :

X = np.array([5.5, 6.0, 6.5, 6.0, 5.0, 6.5, 4.5, 5])
X = X.reshape(-1, 1)
y = np.array([420, 380, 350, 400, 440, 380, 450, 420])

regFalse = LinearRegression(fit_intercept = False).fit(X, y)
y_pred=regFalse.predict(X)

print("Score :",regFalse.score(X, y))
print("Paramètres : Coef =",regFalse.coef_,", Intercept =", regFalse.intercept_)
print("MSE :",mean_squared_error(y, y_pred))

plt.scatter(X, y)
plt.plot(X, y_pred, color='red')
plt.plot(X,(regFalse.coef_*X)+regFalse.intercept_, color='green')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Régression linéaire sans prendre en compte l\'intercept. ')
plt.show()