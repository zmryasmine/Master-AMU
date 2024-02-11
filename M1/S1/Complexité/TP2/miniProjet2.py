import random
from itertools import product
import time
import subprocess

nb_noeuds = random.randint(3, 10)
print("Nombre de sommets du graphe :",nb_noeuds)

k = random.randint(2, nb_noeuds)
print("Nombre de sommets dans une clique :",k)

nb_noeuds = 3
k = 3

def var(i, j):
    return (i - 1) * k + j  # Variables commencent à 1 dans  CNF

def random_graph(size):
    graph = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(i, size):
            if i == j:
                graph[i][j] = 0
            else:
                r = random.random()
                if r > 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
                else:
                    graph[i][j] = 0
                    graph[j][i] = 0

    return graph

def clique_SAT(graphe, k):
    nb_sommets = len(graphe)
    nb_variables = nb_sommets * k
    nb_clauses = 0
    clauses = []


    # Contrainte 1 : Chaque sommet ne peut être à la fois le jème et le j'ème de la zone dense
    for i in range(1, nb_sommets + 1):
        for j in range(1, k + 1):
            for m in range(j + 1, k + 1):
                clauses.append([-var(i, j), -var(i, m)])
                nb_clauses += 1

    # Contrainte 2 : Les sommets i et i' ne peuvent pas être les jèmes de la zone dense
    for i in range(1, nb_sommets + 1):
        for m in range(i + 1, nb_sommets + 1):
            for j in range(1, k + 1):
                clauses.append([-var(i, j), -var(m, j)])
                nb_clauses += 1

    # Contrainte 3 : Si pas d'arête entre i et i', alors i et i' ne sont pas tous deux dans la zone dense
    for i in range(1, nb_sommets + 1):
        for m in range(i + 1, nb_sommets + 1):
            if graphe[i-1][m-1] == 0 and graphe[m-1][i-1] == 0:
                for j in range(1, k + 1):
                    clauses.append([-var(i, j), -var(m, j)])
                    nb_clauses += 1

    # Contrainte 4 : Pour tout j, il existe i tel que i est le jème sommet de la zone dense
    for j in range(1, k + 1):
        clause = [var(i, j) for i in range(1, nb_sommets + 1)]
        clauses.append(clause)
        nb_clauses += 1

    return nb_variables, nb_clauses, clauses

def write_DIMACS_CNF(file_path, nb_variables, nb_clauses, clauses):
    with open(file_path, "w") as f:
        # Écrire la ligne de description du problème
        f.write(f"p cnf {nb_variables} {nb_clauses}\n")

        # Écrire les clauses dans le fichier
        for clause in clauses:
            clause.append(0)  # Ajouter 0 à la fin de chaque ligne
            f.write(" ".join(map(str, clause)) + "\n")

def verifier_SAT(affectation, formule):
    for clause in formule:
        clause_satisfaite = False  # Réinitialiser à False pour chaque nouvelle clause
        #print(clause)
        for literal in clause:
            #print(literal)
            if literal in affectation:
                clause_satisfaite = True
                break  # Sortir de la boucle dès qu'un littéral est satisfait
        
        #print(clause_satisfaite)
        if not clause_satisfaite:
            return False  # Si la clause n'est pas satisfaite, la formule entière ne peut pas être satisfaite

    return True  

def brute_reduit(formule, nombre_variables):
    valeurs_variables = [[i, -i] for i in range(1, nb_variables + 1)]
    for combinaison in product(*valeurs_variables):

        #print(combinaison)
        if verifier_SAT(combinaison, formule):
            print(combinaison)
            data = str(combinaison).replace('(', '').replace(')', '').replace(',', '')
            with open('affectation_brute.txt', 'w') as file:
                file.write(str(data))
            
            return True
    return False



graphe = random_graph(nb_noeuds)
nb_variables, nb_clauses, clauses = clique_SAT(graphe, k)

# Afficher les résultats
print("Nombre de variables :",nb_variables)
print("Nombre de clauses :",nb_clauses)
print("Clauses :")
for clause in clauses:
    print(clause)


file_path = "formula_.cnf"

# Utiliser les valeurs précédemment obtenues (num_variables, num_clauses, clauses)
write_DIMACS_CNF(file_path, nb_variables, nb_clauses, clauses)


debut = time.time() 
resultat_force_brute = brute_reduit(clauses, nb_variables)

fin = time.time()  
temps_execution = fin - debut  
print("Temps d'exécution brute :", temps_execution * 1000, "milisecondes")

print("Algorithme brute avec Réduction : ", resultat_force_brute)


debut = time.time() 
cmd = ["minisat", "formule.cnf","affectation_minisat.txt"]
resultat = subprocess.run(cmd, capture_output = True, text = True)
fin = time.time()  
temps_execution = fin - debut  
print("Temps d'exécution minisat :", temps_execution * 1000, "milisecondes")
print("Résultat :",resultat.stdout) 
