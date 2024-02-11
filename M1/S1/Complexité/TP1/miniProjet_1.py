import numpy as np
import time
import matplotlib.pyplot as plt

# Version récursive
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Version itérative
def fibonacci_iterative(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        fib = [0, 1]
        for i in range(2, n + 1):
            fib.append(fib[i - 1] + fib[i - 2])
        return fib[n]
    
# Version basée sur l'exponentiation de matrice
#Declarer une methode qui calcule le produit des deux matrices
def matrixProduct(a, b):
    # Get the dimensions of matrices a and b
    kSize = len(b)
    iSize = len(a)
    jSize = len(b[0])

    # Initialize the result matrix with zeros
    result = [[0 for j in range(jSize)] for i in range(iSize)]

    # Perform matrix multiplication
    for i in range(iSize):
        for j in range(jSize):
            for k in range(kSize):
                result[i][j] += a[i][k] * b[k][j]

    return result

def expoMatrix(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    result = [[0], [1]]
    base = [[0, 1], [1, 1]]

    def expoMatrixRec(n, matrix):
        if n == 1:
            return matrix
        if n % 2 == 0:
            half_power = expoMatrixRec(n // 2, matrix)
            return matrixProduct(half_power, half_power)
        else:
            previous_power = expoMatrixRec(n - 1, matrix)
            return matrixProduct(matrix, previous_power)

    base = expoMatrixRec(n, base)
    result = matrixProduct(base, result)
    return result[0][0]

#Autre méthode
def fibonacci_matrix(n):
    F = np.array([[1, 1], [1, 0]], dtype=object)
    if n == 0:
        return 0
    power = np.linalg.matrix_power(F, n - 1)
    return power[0, 0]

# Comparaison de l'efficacité relative
def compare_efficiency(max_n):
    for n in range(max_n + 1):
        recursive_result = fibonacci_recursive(n)
        iterative_result = fibonacci_iterative(n)
        matrix_result = fibonacci_matrix(n)
        expo_Matrix = expoMatrix(n)
        print(f"n = {n}: Recursive = {recursive_result}, Iterative = {iterative_result}, Matrix_1 = {matrix_result}, Matric_2 = {expo_Matrix}")

# Testons jusqu'à quelle valeur de n nous pouvons aller en un temps raisonnable
max_n = 45 
compare_efficiency(max_n)

