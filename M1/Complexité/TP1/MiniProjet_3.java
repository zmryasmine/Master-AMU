//package myPackage;

import java.util.ArrayList;
public class MiniProjet_3  {


    public static void main(String[] args) {
        // remplir l'ensemble des transition de la MT dans la matrice
        // les transition suivante c'est pour reconnaitre le mot "ab"
        //on remplie chaque ligne de la façon suivante {qi,  à verfier, Qsuivant, à écrire, Direction},
        Character matrice[][] = new Character[][]{
            {'0', 'a', '1', 'a', 'R'},
            {'0', 'b', 'N', 'b', 'S'},
            {'1', 'a', 'N', 'a', 'S'},
            {'1', 'b', '2', 'b', 'R'},
            {'2', 'a', 'N', 'a', 'S'},
            {'2', 'b', 'N', 'b', 'S'},
            {'2', '#', 'Y', '#', 'S'}


        };


// fonction qui prend en entrée les transition de la Mt, le mot a verifier, ainsi que la position du depart sur le ruban
Solution(matrice, "ab", 0); //

    }

    public static void Solution(Character matrice[][], String mot, int position) {
        int Pos = position;
        int q=0;
        int  j =0;
        int T=0;

        ArrayList<Character> ruban = new ArrayList<Character>();
        char[] caracteres = mot.toCharArray();
        // Ajout des caractères à l'ArrayList
        for (char c : caracteres) {
            ruban.add(c);
        }

          while(T==0 ) {

              if (matrice.length == j){
                  break;
              }
                  if (Character.getNumericValue(matrice[j][0]) == q) {

                      if (ruban.get(Pos) == matrice[j][1]) {

                          if (matrice[j][2] != 'N') { // on verifie qu'on est pas sur un etat final de refus

                              if (matrice[j][2] == 'Y') { //si on est sur un etat final d'acceptation on accepte le mot sinoon on passe a else


                                  System.out.println("mot reconnu");
                                  System.out.println("le contenue du ruban est : ");
                                  for (int i=0; i<ruban.size(); i++) {
                                      System.out.print(ruban.get(i));
                                  }

                                  T = 1;

                              } else { //on met à jour l'état, le symbole sur le ruban, et la position du ruban en fonction de la transition.
                                  ruban.set(Pos, matrice[j][3]);

                                  if (matrice[j][4] == 'R') {
                                      Pos += 1;

                                      if (Pos >= ruban.size()) { // si la position depasse la taille du ruban, on etand le ruban par un # qui represente un blanc

                                          ruban.add('#');
                                      }
                                      q = Character.getNumericValue(matrice[j][2]);
                                  } else if (matrice[j][4] == 'L') {
                                      Pos -= 1;
                                      if (Pos < 0) {

                                          ruban.add(0, '#');
                                      }
                                      q = Character.getNumericValue(matrice[j][2]);
                                  }
                              }
                          } else {
                              System.out.println("mot refusé");
                              System.out.println("le contenue du ruban est : ");
                              for (int i=0; i<ruban.size(); i++) {
                                  System.out.print(ruban.get(i));
                              }
                              T = 1;


                          }
                      }

                  }

              j++;
            }
    }
}