// -*- coding: utf-8 -*-
import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class TriRapide {
    static final int taille = 100_000_000;               // Longueur du tableau à trier
    static final int[] tableau = new int[taille];        // Le tableau d'entiers à trier
    static final int borne = 10 * taille;                // Valeur maximale dans le tableau
    static int poolsize = 4; // Nombre de Threads dans le ThreadPool
    static ExecutorService executor = Executors.newFixedThreadPool(poolsize); // ThreadPool qui utilise un nombre fixe de threads pour executer des taches en parrallèle
    static CompletionService<Void> completionService = new ExecutorCompletionService<>(executor); // Pour l'exécution des taches de manière asynchrone et ordonnée
    static AtomicInteger taskCounter = new AtomicInteger(0); // Compteur du nombre de taches executées

    // Fonction pour échanger deux éléments dans un tableau
    private static void echangerElements(int[] t, int m, int n) {
        int temp = t[m];
        t[m] = t[n];
        t[n] = temp;
    }

    // Fonction de partitionnement du tableau
    private static int partitionner(int[] t, int début, int fin) {
        int v = t[fin];                     // Choix (arbitraire) du pivot : t[fin]
        int place = début;                  // Place du pivot, à droite des éléments déplacés
        for (int i = début; i < fin; i++) {  // Parcours du *reste* du tableau
            if (t[i] < v) {                  // Cette valeur t[i] doit être à droite du pivot
                echangerElements(t, i, place); // On le place à sa place
                place++;                       // On met à jour la place du pivot
            }
        }
        echangerElements(t, place, fin);      // Placement définitif du pivot
        return place;
    }

    // Fonction de tri rapide récursive
    private static void trierRapidement(int[] t, int début, int fin) {
        if (début < fin) {                // S'il y a un seul élément, il n'y a rien à faire!
            int p = partitionner(t, début, fin);
            trierRapidement(t, début, p - 1);
            trierRapidement(t, p + 1, fin);
        }
    }

    // Fonction pour afficher une partie du tableau
    private static void afficher(int[] t, int début, int fin) {
        for (int i = début; i <= début + 3; i++) {
            System.out.print(" " + t[i]);
        }
        System.out.print("...");
        for (int i = fin - 3; i <= fin; i++) {
            System.out.print(" " + t[i]);
        }
        System.out.println();
    }

    // Fonction pour comparer deux tableaux
    public static boolean comparerTableau(int[] t, int[] tab) {
        for (int i = 0; i < t.length; i++) {
            if (t[i] != tab[i]) return false;
        }
        return true;
    }

    // Fonction exécutée par chaque tâche asynchrone
    public static void tacheTrier(int[] t, int début, int fin) {
        double centième = 0.01 * taille;  // Contrainte de la taille du tableau : pour choix du tri séquentiel ou parralèle
        if (début < fin) {
            int place = partitionner(t, début, fin);
            if (place - début > centième) {   // Si la partie gauche est supérieure à un centième du tableau global :
                submitTask(() ->  tacheTrier(t, début, place - 1));
            } else {
                trierRapidement(t, début, place - 1);
            }
            if (fin - place > centième) {  // Si la partie droite est supérieure à un centième du tableau global :
                submitTask(() ->  tacheTrier(t, place + 1, fin));
            } else {
                trierRapidement(t, place + 1, fin);
            }
        }
    }
    private static void submitTask(Runnable task) {
        taskCounter.incrementAndGet(); // Incrémenter le compteur de taches
        completionService.submit(task, null); // Soumettre la tache de tri au service en temps que callable, et ne rien avoir en retour
    }
    // Fonction pour exécuter le tri parallèle
    private static void triParralèle(int[] t) {
        tacheTrier(t, 0, taille - 1); // Lancer la tache
        try {
            while (taskCounter.getAndAdd(-1) > 0) { // Tant qu'il ya des taches
                completionService.take(); // Consulter le résultat, dans notre cas le tableau
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }

    public static void main(String[] args) {
        Random aléa = new Random();
        for (int i = 0; i < taille; i++) {  // Remplissage aléatoire du tableau
            tableau[i] = aléa.nextInt(2 * borne) - borne;
        }
        System.out.print("Tableau initial : ");
        afficher(tableau, 0, taille - 1);  // Affiche le tableau à trier

        // Version séquentielle :
        int[] tableauSéquentiel = Arrays.copyOf(tableau, tableau.length);
        long débutDuTri = System.nanoTime();

        trierRapidement(tableauSéquentiel, 0, taille - 1);  // Tri du tableau

        long finDuTri = System.nanoTime();
        long duréeDuTriSéquentiel = (finDuTri - débutDuTri) / 1_000_000;

        System.out.println("Version séquentielle : " + duréeDuTriSéquentiel + " ms.");

        System.out.print("Tableau trié : ");
        afficher(tableauSéquentiel, 0, taille - 1);  // Affiche le tableau obtenu

        // Version parallèle :
        int[] tableauParallèle = Arrays.copyOf(tableau, tableau.length);
        débutDuTri = System.nanoTime();

        triParralèle(tableauParallèle);  // Tri du tableau

        finDuTri = System.nanoTime();
        long duréeDuTriParallèle = (finDuTri - débutDuTri) / 1_000_000;

        System.out.println("Version parallèle : " + duréeDuTriParallèle + " ms.");

        System.out.print("Tableau trié : ");
        afficher(tableauParallèle, 0, taille - 1);  // Affiche le tableau obtenu

        // Affichage du gain de temps entre les deux versions.
        System.out.println("Gain observé : " + ((float) duréeDuTriSéquentiel) / (float) duréeDuTriParallèle);

        // Comparaison entre deux tableaux
        if (comparerTableau(tableauSéquentiel, tableauParallèle)) {
            System.out.println("Les tris sont cohérents.");
        } else System.out.println("Les tris ne sont pas cohérents.");
    }
}


/*

Tableau initial :  228899394 885675863 638806569 -30204790... 755576311 19221073 -8268259 -356722161
Version séquentielle : 9442 ms.
Tableau trié :  -999999997 -999999992 -999999990 -999999978... 999999952 999999964 999999968 999999996
Version parallèle : 2886 ms.
Tableau trié :  -999999997 -999999992 -999999990 -999999978... 999999952 999999964 999999968 999999996
Gain observé : 3.2716563
Les tris sont cohérents.

 */