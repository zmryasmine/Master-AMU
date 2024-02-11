#!/bin/bash
cd ~/reseaux/projet/VM1 && vagrant up &
cd ~/reseaux/projet/VM3 && vagrant up &
cd ~/reseaux/projet/VM1-6 && vagrant up &
cd ~/reseaux/projet/VM2-6 && vagrant up &
cd ~/reseaux/projet/VM3-6 && vagrant up &
wait
