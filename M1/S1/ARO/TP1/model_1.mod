/* Variable definitions */
var a >= 0;
var b >= 0;
var c >= 0;
var d >= 0;
var e >= 0;
/* Objective function */
maximize R: +0.1*a +0.04*b +0.07*c +0.06*d +0.08*e;

/* Constraints */
R1: +a+b+c+d+e <= 100000;
R2: b+e >= 50000;
R3:+a+e <=50000;
R4: +b+d >= 40000;
R5: +0.04*b +0.06*d >= 0.3*(+0.1*a +0.04*b +0.07*c +0.06*d +0.08*e);

