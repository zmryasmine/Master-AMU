#!/bin/bash
cd /tmp
curl -o debianTP.box https://pageperso.lis-lab.fr/emmanuel.godard/boxes/debianTP.box
curl -o debianTP.box.md5 https://pageperso.lis-lab.fr/emmanuel.godard/boxes/debianTP.box.md5
md5sum -c debianTP.box.md5
vagrant box remove -f "m1reseaux"
vagrant box add /tmp/debianTP.box --name "m1reseaux"
