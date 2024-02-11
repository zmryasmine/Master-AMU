import time

#Fonction pour extraire les clauses :
def extraire_formule(path):
    nb_variables = 0
    nb_clauses = 0
    formule = []
    conforme = True

    with open(path,'r') as file:
        lignes=file.readlines()
    
    if not lignes:
        print("Le fichier DIMACS CNF est vide.")
        conforme = False

    if not lignes[0].startswith('p cnf'):
        print("La première ligne ne commence pas par 'p cnf'.")
        conforme = False

    for ligne in lignes:
        if ligne.startswith('p cnf'):
            # Extraire le nombre de variables et de clauses à partir de la ligne 'p cnf'
            _, _, nb_variables, nb_clauses = ligne.split()
            nb_variables, nb_clauses = int(nb_variables), int(nb_clauses)
            if len(lignes)-1 != nb_clauses:
                print("Le nombre de clauses n'est pas respecté.")
                conforme = False
        elif ligne.startswith(('-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                # Convertir la ligne en une liste d'entiers
                clause = list(map(int, ligne.split()[:-1]))  # Ignorer le dernier élément (0)
                formule.append(clause)
    for num_ligne, ligne in enumerate(lignes[1:], start=2):  # Commencer à partir de la deuxième ligne
        if not ligne.endswith('0\n'):
            print("La ligne",num_ligne,"ne se termine pas par 0.")
            conforme = False
    
    return nb_variables, nb_clauses, formule, conforme


#Fonction pour extraire les littéraux :

def extraire_affectation(path):
    with open(path, 'r') as file:
        ligne = file.readline().strip()
    # Convertir la ligne en une liste d'entiers
    affectation = list(map(int, ligne.split()))

    return affectation


#Fonctions pour vérifier l'affectation des littéraux :
def valider_affectation(affectation, nb_variables):
    if len(affectation) != nb_variables:
        print("Le nombre d'affectations ne correspond pas au nombre de variables dans le fichier DIMACS CNF.",len(affectation),"!=",nb_variables)
        return False

    return True


#Vérificateur SAT :


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

path = 'C:\\Users\\user\\Desktop\\M1\\Complexité\\Data\\clauses\\hanoi5.cnf'

debut = time.time()
nb_variables, nb_clauses, formule, conforme = extraire_formule(path)

if conforme : # Afficher les résultats
    print("Nombre de variables:", nb_variables)
    print("Nombre de clauses:", nb_clauses)
    #print("Formule CNF:", formule)

    filename = 'C:\\Users\\user\\Desktop\\M1\\Complexité\\Data\\affectation\\hanoi5.txt'
    affectation = extraire_affectation(filename)
 
    if valider_affectation(affectation,nb_variables):
        #print("Affectation aux variables:", affectation)
        extraction = time.time()       
        if verifier_SAT(affectation, formule):
            print("La formule est satisfaite.")
        else:
            print("La formule n\'est pas satisfaite.")

        fin = time.time()
        print("Durée extraction =", (extraction - debut) * 1000, "ms.")
        print("Durée de vérification =",(fin-extraction) * 1000, "ms.")
        print("Temps d'exécution =", (fin - debut) * 1000, "ms.")




"""
def satisfait_formule(affectation, formule):
    for clause in formule:
        clause_satisfaite = False
        for literal in clause :
            if (literal > 0 and affectation[abs(literal) -1] == 1):
                clause_satisfaite = True
                break
            if (literal < 0 and affectation[abs(literal) -1] == 0):
                clause_satisfaite = True
                break
        
        if not clause_satisfaite:
            return False
        
    return True
"""