#include "extremite.h"
#include "iftun.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h> 
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <netinet/in.h>
#include <sys/select.h>

#define PORT 123



void ext_in(int tunfd, char *server_ip, char *port) {
    int client_socket;
    struct sockaddr_in6 serv_addr;

    // Create socket
    if ((client_socket = socket(AF_INET6, SOCK_STREAM, 0)) < 0) {
        perror("Erreur de la création du socket");
        exit(EXIT_FAILURE);
    }

    serv_addr.sin6_family = AF_INET6;
    serv_addr.sin6_port = htons(atoi(port)); // Use the specified port

    // Specify the server's IPv6 address
    if (inet_pton(AF_INET6, server_ip, &serv_addr.sin6_addr) <= 0) {
        perror("Invalid address/Address not supported");
        exit(EXIT_FAILURE);
    }

    // Connect to the remote server
    if (connect(client_socket, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Erreur de connexion");
        exit(EXIT_FAILURE);
    }

    bidirectional_tunnel( client_socket, tunfd); 
    
    // Transmission des données depuis tun0 à la socket en utilisant la fonction copier
    /*
    
   while (1) {
        copier(tunfd, client_socket);
    }
    */
    close(client_socket);
}





void ext_out(int tunfd,char* port) {
    int server_fd, new_socket;
    struct sockaddr_in6 address;
    int opt = 1;
    socklen_t addrlen = sizeof(address);


    // Create socket
    if ((server_fd = socket(AF_INET6, SOCK_STREAM, 0)) == 0) {
        perror("Erreur de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Set socket options
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("Erreur de configuration de setsockopt");
        exit(EXIT_FAILURE);
    }

    memset(&address, 0, sizeof(address));
    address.sin6_family = AF_INET6;
    address.sin6_addr = in6addr_any; // Accept connections on any available IPv6 address
    address.sin6_port = htons(PORT);

    // Bind socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) == -1) {
        perror("Erreur de liaison du socket à une adresse et un port bind()");
        exit(EXIT_FAILURE);
    }

    // Listen for connections
    if (listen(server_fd, 3) < 0) {
        perror("Erreur d'écoute listen()");
        exit(EXIT_FAILURE);
    }

    printf("Ready for client connect().\n");

    // Wait for incoming connections
    struct sockaddr_in6 client_addr;
    socklen_t client_len = sizeof(client_addr);

    // Accept incoming connection
    if ((new_socket = accept(server_fd, (struct sockaddr *)&client_addr, (socklen_t*)&client_len)) < 0) {
        perror("Erreur d'acceptation de la connexion");
        exit(EXIT_FAILURE);
    }

    char str[INET6_ADDRSTRLEN]; // Buffer to store IPv6 address as a string

    // Convert client's IPv6 address to a string representation
    if (inet_ntop(AF_INET6, &client_addr.sin6_addr, str, sizeof(str))) {
        printf("Client connected ip: %s port: %d\n", str, ntohs(client_addr.sin6_port));
    }

    bidirectional_tunnel(new_socket, tunfd); 
    
    /*
    // Read data from the socket and write to standard output using the copier function
    while (1) {
        copier(new_socket, tunfd);
    }
    */
    close(new_socket);
    close(server_fd);
}
