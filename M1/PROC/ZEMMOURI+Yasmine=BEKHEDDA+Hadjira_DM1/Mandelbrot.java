import java.awt.Color;

public class Mandelbrot {
    final static int taille = 500 ;   // nombre de pixels par ligne et par colonne
    final static Picture image = new Picture(taille, taille) ;  // Il y a donc taille*taille pixels blancs ou gris à déterminer
    final static int max = 20_000 ;  // C'est le nombre maximum d'itérations pour déterminer la couleur d'un pixel
    final static int maxImages = 500 ; // Nombre maximum de fichiers produits
    static int imagesCount = 0; // Compteur d'images produites
    
    
   
    public static void main(String[] args) throws InterruptedException  {
        final long début = System.nanoTime() ;
        
         SaverImage saver = new SaverImage(); //Thread qui se charge de la sauvegarde des images périodiquement
         saver.start();
         
         try {
             synchronized (Mandelbrot.class) {
                 Mandelbrot.class.wait(); //Utiliser le wait pour laisser le temps au thread 'saver' de sauvegarder la première image
             }
         } catch (InterruptedException e) {
             e.printStackTrace();
         }
         
        for (int i = 0; i < taille; i++) {
            for (int j = 0; j < taille; j++) {
                colorierPixel(i,j) ;
            }
            // image.show();         // Pour visualiser l'évolution de l'image
        }
        
        Thread.sleep(100); //Attendre que le thread 'saver' finisse la sauvegarde de la dernière image
        
        saver.stopSauvegarde(); //Stopper la sauvegarde.
        
        
        try {
        	saver.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        final long fin = System.nanoTime() ;
        final long durée = (fin - début) / 1_000_000 ;
        System.out.println("Enregistrement terminé : " + imagesCount + " fichier(s) PNG créé(s).");
        System.out.println("Durée = " + (double) durée  + " ms.") ;
        
        //image.show() ;
    }    
    
 static class SaverImage extends Thread {
	   
	    private volatile boolean stopRequete = false; //Afin de pouvoir stopper la sauvegarde après la fin de la coloration
    	
    	public void run() {
    		
    		while (!stopRequete) {
    			
    			if(imagesCount == 1)  synchronized (Mandelbrot.class) {
                    Mandelbrot.class.notify(); //Quand l'image 0 est sauvegardée, le thread 'reveille' le main avec notify 
                }
    			 String fileName = String.format("pic%03d.png", imagesCount);
                 image.save(fileName);
                 try {
                     this.sleep(60); // image.save prend un certain temps (entre 20 et 30ms dans nos machines), 100ms - 30 = 70
                 } catch (InterruptedException e) {
                     Thread.currentThread().interrupt();
                 }
                 
                 imagesCount++;
                 
                 
                 if (imagesCount >= maxImages) {
                     this.stopSauvegarde();
    		}
           

    	}
    	
    		
    	
    }
    	public void stopSauvegarde() {
            this.stopRequete = true;
        }
 }
    // La fonction colorierPixel(i,j) colorie le pixel (i,j) de l'image en gris ou blanc
    public static void colorierPixel(int i, int j) {
        final Color couleur = new Color(235, 64, 52) ;
        final Color blanc = new Color(255, 255, 255) ;
        final double xc = -.5 ;
        final double yc = 0 ; // Le point (xc,yc) est le centre de l'image
        final double region = 2 ;
        /*
          La région du plan considérée est un carré de côté égal à 2.
          Elle s'étend donc du point (xc - 1, yc - 1) au point (xc + 1, yc + 1)
          c'est-à-dire du point (-1.5, -1) en bas à gauche au point (0.5, 1) en haut
          à droite
        */
        double a = xc - region/2 + region*i/taille ;
        double b = yc - region/2 + region*j/taille ;
        // Le pixel (i,j) correspond au point (a,b)
        if (mandelbrot(a, b, max)) image.set(i, j, couleur) ;
        else image.set(i, j, blanc) ; 
    }

    // La fonction mandelbrot(a, b, max) détermine si le point (a,b) est gris
    public static boolean mandelbrot(double a, double b, int max) {
        double x = 0 ;
        double y = 0 ;
        for (int t = 0; t < max; t++) {
            if (x*x + y*y > 4.0) return false ; // Le point (a,b) est blanc
            double nx = x*x - y*y + a ;
            double ny = 2*x*y + b ;
            x = nx ;
            y = ny ;
        }
        return true ; // Le point (a,b) est gris
    }
}

