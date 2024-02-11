set REGION;
set MINOTERIE;

param QTE {REGION} > 0;
param qte {MINOTERIE} > 0;
param distance {MINOTERIE,REGION} >= 0;

var x {i in MINOTERIE, j in REGION} >= 0;

minimize obj:  0.1* sum {i in MINOTERIE, j in REGION} x[i,j] * distance[i,j];

R_MINOTERIE {i in MINOTERIE} : sum{j in REGION} x[i,j] >= qte[i];
R_REGION {j in REGION} : sum{i in MINOTERIE} x[i,j] <= QTE[j];

data;

set REGION := R1 R2 R3;
set MINOTERIE := M1 M2 M3 ;

param:   QTE  :=
  R1   275  
  R2   400  
  R3   300;

param:   qte  :=
   M1     200   
   M2     550   
   M3     225;

param distance (tr):
        M1    M2    M3:=
   R1   210   500   400   
   R2   350   300   220   
   R3   550   200   250;
end;