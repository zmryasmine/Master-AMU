#!/bin/bash

# Define an array of VM directories
vm_directories=("VM1" "VM3" "VM1-6" "VM2-6" "VM3-6" )

# Loop through the array and open a new terminal for each VM
for vm_dir in "${vm_directories[@]}"; do
    mate-terminal -- bash -c "cd ~/reseaux/Projet/$vm_dir && vagrant up && vagrant ssh"
done

# Wait for all terminals to finish
wait
