set MOIS;

param Cout {MOIS} > 0;
param Demande {MOIS} > 0;
param Capacite {MOIS} > 0;

var p{i in MOIS} >= 0;
var r{i in MOIS} >= 0; 
minimize obj:  (sum {i in MOIS} p[i] * Cout[i]) + (0.015* sum {i in MOIS} r[i] * Cout[i]);

R1: r[1]= 2750 + p[1] - Demande[1];
R2 {i in 2..6}: r[i] = r[i-1] + p[i] - Demande[i];
R3 {i in MOIS}: r[i] >= 1500;
R4 {i in MOIS}: r[i] <= 6000;
R5: 2750 + p[1] >= Demande[1];
R6 {i in 2..6}: r[i-1] + p[i] >= Demande[i];
R7 {i in MOIS}: p[i] <= Capacite[i];
R8 {i in MOIS}: p[i] >= Capacite[i]/2;

data;

set MOIS := 1 2 3 4 5 6;

param:   Cout  :=
1 240
2 250
3 265
4 285
5 280
6 285;

param:   Demande  :=
1 1000
2 4500
3 6000
4 5500
5 3500
6 4000;

param:   Capacite  :=
1 4000
2 3500
3 4000
4 4500
5 4000
6 3500;
end;