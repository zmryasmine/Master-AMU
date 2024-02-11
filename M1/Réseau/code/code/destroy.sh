#!/bin/bash
cd ~/reseaux/projet/VM1 && vagrant destroy -f &
cd ~/reseaux/projet/VM3 && vagrant destroy -f &
cd ~/reseaux/projet/VM1-6 && vagrant destroy -f &
cd ~/reseaux/projet/VM2-6 && vagrant destroy -f &
cd ~/reseaux/projet/VM3-6 && vagrant destroy -f &
wait
