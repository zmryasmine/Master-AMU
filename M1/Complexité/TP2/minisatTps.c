#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

int main(void) {
  struct timeval start, end;
  double time_spent;

  // Démarrer le chronomètre
  gettimeofday(&start, NULL);

  // Exécuter la commande
  system("minisat formule.cnf affectation.txt");

  // Arrêter le chronomètre
  gettimeofday(&end, NULL);

  // Calculer le temps écoulé
  time_spent = (end.tv_sec - start.tv_sec) +
              (end.tv_usec - start.tv_usec) / 1000000.0;

  // Afficher le temps d'exécution
  printf("Temps d'exécution : %f secondes\n", time_spent);

  return 0;
}
