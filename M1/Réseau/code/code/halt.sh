#!/bin/bash
cd ~/reseaux/projet/VM1 && vagrant halt &
cd ~/reseaux/projet/VM3 && vagrant halt &
cd ~/reseaux/projet/VM1-6 && vagrant halt &
cd ~/reseaux/projet/VM2-6 && vagrant halt &
cd ~/reseaux/projet/VM3-6 && vagrant halt &
wait
