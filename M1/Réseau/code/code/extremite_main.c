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


int tun_alloc(char *dev)
{
  struct ifreq ifr;
  int fd, err;

  if( (fd = open("/dev/net/tun", O_RDWR)) < 0 ){
    perror("alloc tun");
    exit(-1);
  }

  memset(&ifr, 0, sizeof(ifr));

  /* Flags: IFF_TUN   - TUN device (no Ethernet headers) 
   *        IFF_TAP   - TAP device  
   *
   *        IFF_NO_PI - Do not provide packet information  
   */ 
  ifr.ifr_flags = IFF_TUN; 
  if( *dev )
    strncpy(ifr.ifr_name, dev, IFNAMSIZ);

  if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ){
    close(fd);
    return err;
  }
  strcpy(dev, ifr.ifr_name);
  return fd;
}      

int copier(int src, int dst){
  if (src==-1) {
    perror("src vide");
    return -1;
  }
  
   if (dst==-1) {
    perror("dst vide");
    return -1;
  }
  
  
  char buff[1500];
  
  ssize_t n = 0;
  
  n = read(src, &buff, 1500);
//  printf("n :%f\n",n);
printf("Received data: ");
    for (int i = 0; i < n; i++) {
        printf("%02X ", buff[i]);
    }
    printf("\n");

  if (n<0) {
     perror("read retour negatif");
     return n;
  }
 
  buff[n] = '\0';
  write(dst, &buff, n);

    // Ajout de la logique pour afficher les données envoyées
    printf("Sent data: ");
    for (int i = 0; i < n; i++) {
        printf("%02X ", buff[i]);
    }
    printf("\n");

    return n;
}

void ext_in(int tunfd, const char *server_ip, const char *port) {
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
    
      /*  while (1) {
        char buffer[1024];
        ssize_t bytes_received = read(tunfd, buffer, sizeof(buffer));
        printf("dd%d",1);
        if (bytes_received <= 0) {
            break;
        }

        buffer[bytes_received] = '\0';
        printf("send to server: %s\n", buffer);
        fflush(stdout); // Flush stdout to ensure immediate output

printf("Packet: ");
for (int i = 0; i < bytes_received; i++) {
    printf("%02X ", buffer[i]);
}
printf("\n");

        // Write received data to standard output
        send(client_socket, buffer, bytes_received, 0);
    }
*/
    fd_set read_fds;
    int max_fd;

    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(tunfd, &read_fds);
        FD_SET(client_socket, &read_fds);

        max_fd = tunfd > client_socket ? tunfd : client_socket;

        // Utiliser select pour attendre l'activité sur les descripteurs de fichier
        if (select(max_fd + 1, &read_fds, NULL, NULL, NULL) == -1) {
            perror("Erreur de select");
            exit(EXIT_FAILURE);
        }

        // Lire depuis le tunnel et écrire vers la socket
        if (FD_ISSET(tunfd, &read_fds)) {
            copier(tunfd, client_socket);
        }

        // Lire depuis la socket et écrire vers le tunnel
        if (FD_ISSET(client_socket, &read_fds)) {
            copier(client_socket, tunfd);
        }
    }
     
/*

    // Transmission des données depuis tun0 à la socket en utilisant la fonction copier
   while (1) {
        copier(tunfd, client_socket);
    }
*/
    
  /*      while (1) {
        // Envoyer des données au serveur
        printf("Message au serveur : ");
        char buffer[1024];
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Recevoir la réponse du serveur
        ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            break;
        }
        buffer[bytes_received] = '\0';
        printf("Reçu du serveur : %s\n", buffer);
    }*/
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
    fd_set read_fds;
    int max_fd;

    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(tunfd, &read_fds);
        FD_SET(new_socket, &read_fds);

        max_fd = tunfd > new_socket ? tunfd : new_socket;

        // Utiliser select pour attendre l'activité sur les descripteurs de fichier
        if (select(max_fd + 1, &read_fds, NULL, NULL, NULL) == -1) {
            perror("Erreur de select");
            exit(EXIT_FAILURE);
        }

        // Lire depuis le tunnel et écrire vers la socket
        if (FD_ISSET(tunfd, &read_fds)) {
            copier(tunfd, new_socket);
        }

        // Lire depuis la socket et écrire vers le tunnel
        if (FD_ISSET(new_socket, &read_fds)) {
            copier(new_socket, tunfd);
        }
    }

/*
        
    // Read data from the socket and write to standard output using the copier function
 while (1) {

        copier(new_socket, tunfd);
    }
*/
  /*  while (1) {
        // Recevoir des données du client
        char buffer[1024];
        ssize_t bytes_received = recv(new_socket, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            break;
        }

        buffer[bytes_received] = '\0';
        printf("Reçu du client : %s\n", buffer);

        // Envoyer une réponse au client
        printf("Réponse au client : ");
        fgets(buffer, sizeof(buffer), stdin);
        send(new_socket, buffer, strlen(buffer), 0);
    }
*/



// Redirect received data to standard output
   /* while (1) {
        char buffer[1024];
        ssize_t bytes_received = recv(new_socket, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            break;
        }

        buffer[bytes_received] = '\0';
        printf("Received from client: %s\n", buffer);
        fflush(stdout); // Flush stdout to ensure immediate output

        // Write received data to standard output
        write(STDOUT_FILENO, buffer, bytes_received);
    }*/
    close(new_socket);
    close(server_fd);
}


int main(int argc, char** argv) {
    int tunfd = tun_alloc(argv[1]);
    char * port=argv[3];
    printf("Création de %s\n", argv[1]);
    printf("Faire la configuration de %s...\n", argv[1]);
    printf("Appuyez sur une touche pour continuer\n");
    getchar();
    printf("Interface %s Configurée:\n", argv[1]);
    system("chmod +x configure-tun.sh");
    system("./configure-tun.sh");
    system("ip a");

    if (argc < 3) {
        printf("Veuillez fournir suffisamment d'arguments.\n");
        return 1;
    }

    if (strcmp(argv[2], "ext_in") == 0) {
        printf("Testing ext_in...\n");
        ext_in(tunfd, "fc00:1234:1::16", port);
    } else if (strcmp(argv[2], "ext_out") == 0) {
        printf("Testing ext_out...\n");
        ext_out(tunfd,port);
    } else {
        printf("Commande non reconnue : %s\n", argv[2]);
        return 1;
    }

    return 0;
}

