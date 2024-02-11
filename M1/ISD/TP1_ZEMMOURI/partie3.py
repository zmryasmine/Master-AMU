import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   

df = pd.read_csv('fruit.csv')

# X est un dataframe
def normaMinMax(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") # pour ne pas tenir compte de cette information
    nbl, nbc = Xn.shape
    for i in range(nbl):
        for j in range(nbc):
            # comprendre ces lignes
            Xn.iloc[i,j] = ( X.iloc[i,j] - X.iloc[:,j].min() ) / (X.iloc[:,j].max() - X.iloc[:,j].min())
    Xn["Fruit"] = X["Fruit"]
    return Xn

def normaMean(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit") 
    for column in Xn.columns:
        Xn[column] = (X[column] - X[column].mean()) / (X[column].max() - X[column].min())
    Xn["Fruit"] = X["Fruit"]
    return Xn

def normaStandard(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit")
    for column in Xn.columns:
        mean = X[column].mean()
        std = X[column].std()
        Xn[column] = (X[column] - mean) / std
    Xn["Fruit"] = X["Fruit"]
    return Xn


def normaProjBall(X):
    Xn = X.copy()
    Xn.drop(columns="Fruit")
    mean = Xn.mean()
    data = Xn - mean
    norm = np.linalg.norm(data, axis=1)
    Xn = data.div(norm, axis=0)
    Xn["Fruit"] = X["Fruit"]
    return Xn

normalized_data_MinMax = normaMinMax(df)
normalized_data_Mean = normaMean(df)
normalized_data_Standard = normaStandard(df)
normalized_data_ProjBall = normaProjBall(df)

plt.figure(figsize=(6, 6))
plt.scatter(normalized_data_MinMax['Weight'], normalized_data_MinMax['Length'], c=normalized_data_MinMax['Fruit'], cmap='coolwarm')
plt.title('Normalisation Min-Max')
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(normalized_data_Mean['Weight'], normalized_data_Mean['Length'], c=normalized_data_Mean['Fruit'], cmap='viridis')
plt.title('Normalisation Mean')
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(normalized_data_Standard['Weight'], normalized_data_Standard['Length'], c=normalized_data_Standard['Fruit'], cmap='rainbow')
plt.title('Normalisation Standard')
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(normalized_data_ProjBall['Weight'], normalized_data_ProjBall['Length'], c=normalized_data_ProjBall['Fruit'], cmap='twilight')
plt.title('Normalisation Projection sur la Sphère Unitaire')
plt.show()

plt.figure(figsize=(12, 12))

# Nuage de points pour la normalisation Min-Max
plt.scatter(normalized_data_MinMax['Weight'], normalized_data_MinMax['Length'], c=normalized_data_MinMax['Fruit'], cmap='coolwarm', label='Min-Max')

# Nuage de points pour la normalisation Mean
plt.scatter(normalized_data_Mean['Weight'], normalized_data_Mean['Length'], c=normalized_data_Mean['Fruit'], cmap='viridis', label='Mean')

# Nuage de points pour la normalisation Standard
plt.scatter(normalized_data_Standard['Weight'], normalized_data_Standard['Length'], c=normalized_data_Standard['Fruit'], cmap='rainbow', label='Standard')

# Nuage de points pour la normalisation Projection sur la Sphère Unitaire
plt.scatter(normalized_data_ProjBall['Weight'], normalized_data_ProjBall['Length'], c=normalized_data_ProjBall['Fruit'], cmap='twilight', label='Projection')

plt.legend()

plt.title('Comparaison des Normalisations')
plt.xlabel('Poids')
plt.ylabel('Longueur')

plt.show()