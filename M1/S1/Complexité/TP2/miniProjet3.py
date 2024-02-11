import math
import random
import time
import subprocess

def generate_sudoku(n):
    # Créer une grille vide
    grid = [[0] * n for _ in range(n)]

    # Remplir aléatoirement certaines cases
    for _ in range(random.randint(n, n*2)):
        row, col, num = random.randint(0, n-1), random.randint(0, n-1), random.randint(1, n)
        while grid[row][col] != 0:
            row, col = random.randint(0, n-1), random.randint(0, n-1)
        grid[row][col] = num

    return grid


def variable(i, j, k):
    return (i - 1) * n**2 + (j - 1) * n + k

def manipulationNumeroExistant(k, i, j, n, clauses):
    # Il faut le prendre (ajouter une clause de taille 1, avec le littéral correspondant à "mettre le nombre k sur [i,j]")
    c = [variable(i, j, k)]
    clauses.append(c)

    # Il ne doit plus y avoir le numéro k sur la ligne i
    for m in range(1, n+1):
        if i == m:
            continue
        c = [-variable(m, j, k)]
        clauses.append(c)

    # Il ne doit plus y avoir le numéro k sur la colonne j
    for l in range(1, n+1):
        if j == l:
            continue
        c = [-variable(i, l, k)]
        clauses.append(c)

    # Il ne doit plus y avoir de numéro autre que k sur le carré [i,j]
    for p in range(1, n+1):
        if k == p:
            continue
        c = [-variable(i, j, p)]
        clauses.append(c)
   
def sudoku_to_sat(board):
    # n = int(math.sqrt(len(board)))
    n = len(board)
    clauses = []

    def variable(i, j, k):
        return (i - 1) * n**2 + (j - 1) * n + k


    # Chaque cellule contient au moins un chiffre
    for i in range(1, n+1):
        for j in range(1, n+1):
            clauses.append([variable(i, j, k) for k in range(1, n+1)])

    # Chaque cellule contient au plus un chiffre
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n+1):
                for l in range(k+1, n+1):
                    clauses.append([-variable(i, j, k), -variable(i, j, l)])

    # Chaque chiffre apparaît au moins une fois dans chaque ligne
    for i in range(1, n+1):
        for k in range(1, n+1):
            clauses.append([variable(i, j, k) for j in range(1, n+1)])

    # Chaque chiffre apparaît au moins une fois dans chaque colonne
    for j in range(1, n+1):
        for k in range(1, n+1):
            clauses.append([variable(i, j, k) for i in range(1, n+1)])

    # Chaque chiffre apparaît au plus une fois dans chaque ligne
    for i in range(1, n+1):
        for k in range(1, n+1):
            for j in range(1, n+1):
                for l in range(j+1, n+1):
                    clauses.append([-variable(i, j, k), -variable(i, l, k)])

    # Chaque chiffre apparaît au plus une fois dans chaque colonne
    for j in range(1, n+1):
        for k in range(1, n+1):
            for i in range(1, n+1):
                for l in range(i+1, n+1):
                    clauses.append([-variable(i, j, k), -variable(l, j, k)])

    # Chaque chiffre apparaît au plus une fois dans chaque région
    for r in range(1, n+1):
        for k in range(1, n+1):
            for i in range(1, n+1):
                for j in range(1, n+1):
                    for l in range(j+1, n+1):
                        for m in range(1, n+1):
                            clauses.append([-variable(n*(i-1)+j, n*(j-1)+l, k), -variable(n*(i-1)+j, n*(j-1)+m, k)])
    #"""
    for i in range(1, n+1):
        for j in range(1, n+1):
            if board[i-1][j-1] != 0:
                manipulationNumeroExistant(board[i-1][j-1], i, j, n, clauses)
    #"""
    return clauses

def write_DIMACS_CNF(file_path, nb_variables, nb_clauses, clauses):
    with open(file_path, "w") as f:
        # Écrire la ligne de description du problème
        f.write(f"p cnf {nb_variables} {nb_clauses}\n")

        # Écrire les clauses dans le fichier
        for clause in clauses:
            clause.append(0)  # Ajouter 0 à la fin de chaque ligne
            f.write(" ".join(map(str, clause)) + "\n")


n = 9
sudoku_grid = generate_sudoku(n)
print(len(sudoku_grid))

"""
# Exemple d'utilisation avec une grille de taille 4x4 (n=2)
sudoku_grid = [
    [0, 0, 0, 0],
    [1, 3, 4, 0],
    [0, 4, 3, 1],
    [0, 0, 0, 0]
]
"""
# Afficher la grille générée
for row in sudoku_grid:
    print(" ".join(map(str, row)))
#print("Clauses ",sudoku_to_sat(sudoku_grid))
debut = time.time() 
clauses = sudoku_to_sat(sudoku_grid)
fin = time.time()  
temps_execution = fin - debut  
print("Temps de réduction :", temps_execution * 1000, "milisecondes")

nb_variables = n**3
nb_clauses = len(clauses)


file_path = "sudoku.cnf"
write_DIMACS_CNF(file_path, nb_variables, nb_clauses, clauses)


debut = time.time() 
cmd = ["minisat", "sudoku.cnf","affectation_minisat_sudoku.txt"]
resultat = subprocess.run(cmd, capture_output = True, text = True)
fin = time.time()  
temps_execution = fin - debut  
print("Temps d'exécution minisat :", temps_execution * 1000, "milisecondes")
print("Résultat :",resultat.stdout)