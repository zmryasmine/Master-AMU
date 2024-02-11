set PERIODE;
param Agent_Periode {i in PERIODE} > 0;

var agent{i in PERIODE} >= 0;

minimize obj:  sum {i in PERIODE} agent[i];

R1: agent[1] + agent[6] >= Agent_Periode[1];
R2: agent[2] + agent[1] >= Agent_Periode[2];
R3: agent[3] + agent[2] >= Agent_Periode[3];
R4: agent[4] + agent[3] >= Agent_Periode[4];
R5: agent[5] + agent[4] >= Agent_Periode[5];
R6: agent[6] + agent[5] >= Agent_Periode[6];

data;
set PERIODE:= 1 2 3 4 5 6;

param Agent_Periode :=
1 9
2 21
3 25
4 16
5 30
6 12;
end;