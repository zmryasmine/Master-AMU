var agent{i in 1..6} >= 0;

minimize obj:  sum {i in 1..6} agent[i];

R1: agent[1] + agent[6] >= 9;
R2: agent[2] + agent[1] >= 21;
R3: agent[3] + agent[2] >= 25;
R4: agent[4] + agent[3] >= 16;
R5: agent[5] + agent[4] >= 30;
R6: agent[6] + agent[5] >= 12;