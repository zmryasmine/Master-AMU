package knapsack;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

class Sacs {
    int poids;
    int valeur;

    public Sacs(int poids, int valeur) {
        this.poids = poids;
        this.valeur = valeur;
    }
}

class Noeud {
    int niveau;
    int valeur;
    int poids;
    double borneSup;
    ArrayList<Boolean> listInclus; // savoir quel objet est inclus dans le noeud

    public Noeud(int niveau, int valeur, int poids, ArrayList<Boolean> listInclus) {
        this.niveau = niveau;
        this.valeur = valeur;
        this.poids = poids;
        this.listInclus = listInclus;
    }
}

public class Main {
  public static int sac_a_dos( int capacite, Sacs[] mesSacs) {
	  
	  int nombreSacs = mesSacs.length;
	  //Trier les objets par ordre décroissant selon le ratio (valeur/poids)
	  Arrays.sort(mesSacs, (sac1, sac2) -> Double.compare((double) sac2.valeur / sac2.poids, (double) sac1.valeur / sac1.poids));
	  
	  //Initailiser une queue pour stocker les noeuds de l'arbre pour faire un parcours en profondeur selon la priorité
	  PriorityQueue<Noeud> queue = new PriorityQueue<>((sac1, sac2) -> Double.compare(sac2.borneSup, sac1.borneSup));
	  
	  
	  Noeud racine = new Noeud(-1, 0, 0, new ArrayList<>());
	  
	  //On débute avec la racine dont le niveau est -1
	  racine.borneSup = borneSup(racine, capacite, mesSacs, nombreSacs);
	  
	  queue.offer(racine);
	  
	  int optimum = 0;
	  
	  while(!queue.isEmpty()) {
		  Noeud noeud = queue.poll();
		  
		  //Si la borne est supérieur à l'optimum
		  if(noeud.borneSup > optimum) {
			  int niveau = noeud.niveau + 1;
			  
			  
			  //Prioriser la gauche : inclure le noeud
			  Noeud gauche = new Noeud(niveau, noeud.valeur + mesSacs[niveau].valeur, noeud.poids + mesSacs[niveau].poids, new ArrayList<>(noeud.listInclus));
			  gauche.listInclus.add(true);
			  gauche.borneSup = borneSup(gauche, capacite, mesSacs, nombreSacs);
			  
			  if(gauche.poids <= capacite && gauche.valeur > optimum) {
				  optimum = gauche.valeur;
			  }
			  if (gauche.borneSup > optimum) {
				  queue.offer(gauche);
			  }
			  
			  //Droit : ne pas inclure le noeud 
			  Noeud droit = new Noeud(niveau, noeud.valeur, noeud.poids, new ArrayList<>(noeud.listInclus));
			  droit.listInclus.add(false);
			  droit.borneSup = borneSup(droit, capacite, mesSacs, nombreSacs);
			  
			  if (droit.borneSup > optimum) {
				  queue.offer(droit);
			  }
		  }
	  }
	  return optimum;
  }
  
  //Calcul de la borne supérieure en fonction de la capacité restante et de la valeur totale des objets qui peuvent encore être ajoutés.
  private static double borneSup(Noeud noeud, int capacite, Sacs[] mesSacs, int nombreSacs) {
	  
	  if (noeud.poids >= capacite) return 0;
	  
	  double borneSup = noeud.valeur;
	  int poids = noeud.poids;
	  int niveau = noeud.niveau + 1;
	  
	  while ( niveau < nombreSacs && poids + mesSacs[niveau].poids <= capacite) {
		  	poids += mesSacs[niveau].poids;
		  	borneSup += mesSacs[niveau].valeur;
		  	niveau++;
	  }
	  
	  if (niveau < nombreSacs) {
		  borneSup += (double) (capacite - poids) / mesSacs[niveau].poids * mesSacs[niveau].valeur ;
			  
		  }
	  
	  return borneSup; 
  }
  public static void main(String[] args) throws FileNotFoundException, IOException {
	 
	  for (int i=0; i<5; i++) {
	     String filePath =  ".\\Instances\\sac" + i +".txt";// Spécifiez le chemin complet de votre fichier

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            // Lisez la capacité du sac-à-dos à partir de la première ligne
            int capacite = Integer.parseInt(br.readLine());

            List<Sacs> sacs = new ArrayList<>();

            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                int poids = Integer.parseInt(parts[0]);
                int valeur = Integer.parseInt(parts[1]);
                sacs.add(new Sacs(poids, valeur));
            }

            // Convertissez la liste en tableau si nécessaire
            Sacs[] mesSacs = sacs.toArray(new Sacs[0]);
	   
      long startTime = System.currentTimeMillis();
	  int optimum = sac_a_dos(capacite, mesSacs);
	  long endTime = System.currentTimeMillis();
	  System.out.println("Optimum du sac" + i + " est : "+ optimum +".");
        System.out.println("Temps d'execution du sac" + i + " : "+ (endTime - startTime) + "ms.\n");
        
        }
	  
  }

  }
}
