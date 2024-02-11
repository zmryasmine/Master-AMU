En premier lieu, un Thread 'SaverImage' appelé "saver" chargé de sauvegarder périodiquement les images.
Le Thread saver exécute sa fonction "run" via l'appel de start().
Afin de ne pas lancer la coloration avant le début de l'exécution du threat saver, nous utilisé un thread.wait() sur le main(comme le main est un thread).
Le thread saver a ainsi le temps de lancer son run et débuter la sauvegarde avec la premier image pic000.png, tant qu'il n'ya pas une demande de stoper la sauvegarde (stopRequete=false).
Dès que le thread sauvegarde la première image (Image 0), il lance un thread.notify() afin de "reveiller" le main en attente. Ce dernier continue son exécution et débute la coloration.

Le thread saver fait la sauvegarde de cette manière :
Tant qu'une demande de stoper la sauvegarde n'est pas faite, on sauvegarde l'image, puis on attend un certain laps de temps pour atteindre les 100ms (la méthode image.save() prends entre 20ms et 30ms dans notre cas, ce qui n'atteind pas les 100ms demandées.
Nous avons ainsi choisis d'utiliser un thread.sleep() de 70ms afin de satisfaire la contraire de 10 images par secondes.
Ensuite, le nombre d'images est incrémenté. Si le nombre d'images dépasse les 500, nous lançons une demande de stopper la sauvegarde qui met fin à la boucle while.

Pour revenir au main, dès que la coloration est finie, nous avons choisis d'utiliser un Thread.sleep(100) afin de laisser sufisamment de temps au thread saver de finir sa sauvegarde, potentiellement en cours.
Puis, une demande de stopper la sauvegarde est lancée.


En exécutant ce code, nous obtenons les résultats suivant :

Enregistrement terminé : 114 fichier(s) PNG créé(s).
Durée = 13967.0 ms.


Le temps de sleep du thread saver peut différer d'une machine à une autre.

Le gift a été fait avec ezgift.com