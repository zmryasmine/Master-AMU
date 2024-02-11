#!/bin/bash
cd ~/reseaux/projet/VM1 && rm -r .vagrant &
cd ~/reseaux/projet/VM3 && rm -r .vagrant &
cd ~/reseaux/projet/VM1-6 && rm -r .vagrant &
cd ~/reseaux/projet/VM2-6 && rm -r .vagrant &
cd ~/reseaux/projet/VM3-6 && rm -r .vagrant &
wait
