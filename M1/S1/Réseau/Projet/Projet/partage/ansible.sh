#!/bin/bash
cd /vagrant
echo m1reseaux |  sudo -S ansible-playbook -c local -v config.yml
