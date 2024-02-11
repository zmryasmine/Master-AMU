#!/bin/bash

# Créer l'interface TUN
#tunfd=$(tun_alloc "tun0")

# Configurer l'adresse IP et le masque de sous-réseau
ip addr add 172.16.2.1/28 dev tun0
# Activer l'interface
ip link set dev tun0 up

# Vérifier que l'interface est configurée
ip addr show tun0

