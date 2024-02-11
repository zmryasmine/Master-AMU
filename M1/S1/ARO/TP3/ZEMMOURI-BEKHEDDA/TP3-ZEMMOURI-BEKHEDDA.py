import glpk

mat = [
    [2, 0, 0, 0],
    [0, 2, 0, 0],
    [0, 0, 3, 0],
    [0, 0, 0, 7]
]
nbDecoupes = 4

obj = 10.0  

while True:
    # Création du problème linéaire réduit
    PL = glpk.LPX()
    PL.name = "pb_lin_reduit"
    PL.obj.maximize = False

    # Ajout des contraintes
    PL.rows.add(4)
    PL.rows[1].name = "R1"
    PL.rows[1].bounds = (97, 97)
    PL.rows[2].name = "R2"
    PL.rows[2].bounds = (610, 610)
    PL.rows[3].name = "R3"
    PL.rows[3].bounds = (395, 395)
    PL.rows[4].name = "R4"
    PL.rows[4].bounds = (211, 211)

    # Ajout des colonnes
    PL.cols.add(nbDecoupes * 4)
    for i in range(1, nbDecoupes + 1):
        PL.cols[i].bounds = (0, 0)
        PL.cols[i].kind = int
        PL.cols[i].obj = 1.0

    pos = 1
    for i in range(1, 5):
        for j in range(nbDecoupes):
            PL.rows[1].matrix[pos] = mat[j][i - 1]
            pos += 1

    # Résolution du problème linéaire
    PL.simplex()

    # Récupération de la solution duale optimale
    dual = [PL.rows[1].dual, PL.rows[2].dual, PL.rows[3].dual, PL.rows[4].dual]
    print("dual.R1 = {0}; dual.R2 = {1}; dual.R3 = {2}; dual.R4 = {3};".format(dual[0], dual[1], dual[2], dual[3]))

    # Création du problème de sac à dos
    pb_sac = glpk.LPX()
    pb_sac.name = "decoupe_opt"
    pb_sac.obj.maximize = True

    # Ajout des contraintes
    pb_sac.rows.add(1)
    pb_sac.rows[1].name = "R1"
    pb_sac.rows[1].bounds = (0, 100)

    # Ajout des colonnes
    pb_sac.cols.add(4)
    for i in range(1, 5):
        pb_sac.cols[i].bounds = (0, 0)
        pb_sac.cols[i].kind = int
        pb_sac.cols[i].obj = dual[i - 1]

    rowD = [0, 1, 1, 1, 1]
    columnD = [0, 1, 2, 3, 4]
    coefD = [0, 45, 36, 31, 14]

    for i in range(1, 5):
        pb_sac.rows[1].matrix[i] = coefD[i]

    # Configuration des options pour la résolution du problème de sac à dos
    param = pb_sac.io
    param.presolve = True

    # Résolution du problème de sac à dos
    pb_sac.intopt(param)
    obj = pb_sac.obj.value

    if obj > 1.0:
        for i in range(1, 5):
            mat.append([pb_sac.cols[i].value])
        nbDecoupes += 1

    # Afficher le résultat
    print("~~~ 45, 36, 31, 14 ~~~")
    for i in range(nbDecoupes):
        print("{", end=" ")
        for j in range(4):
            print(mat[i][j], end=" ")
        print("} : {0} fois".format(PL.cols[i].prim))

    # Libération de la mémoire
    PL.delete()
    pb_sac.delete()
