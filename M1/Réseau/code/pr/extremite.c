#include "extremite.h"
#include "iftun.h"

#include <sys/socket.h> 
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <strings.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/sendfile.h>
#include <poll.h>
#include <sys/stat.h>
#include <sys/ioctl.h>

#include <linux/if_tun.h>
void read_data(int fd_sock, int fd_tun){

  struct pollfd pfds[2];
  int r;

  pfds[0] = (struct pollfd) {.fd = fd_sock, .events = POLLIN};
  pfds[1] = (struct pollfd) {.fd = fd_tun, .events = POLLIN};


  while (1) {
    r = poll(pfds, 2, -1);
    if (r < 0){
      perror("poll()");
      return;
    }

    if(pfds[0].revents & POLLIN) {
      copy_tun(fd_sock, fd_tun);
    }

    if(pfds[1].revents & POLLIN) {
      copy_tun(fd_tun, fd_sock);
    }
  }
}
void ext_out(int fd){
    int r;
    int s;
    int c;

    struct addrinfo * resol;
    struct addrinfo socket_type = {AI_PASSIVE, PF_INET6, SOCK_STREAM, 0, 0, NULL, NULL, NULL};
    struct sockaddr_in client;

    int addrlen;
    char * port = "123";

    r = getaddrinfo(NULL, port, &socket_type, &resol);
    if (r < 0){
      perror("getaddrinfo()");
      return;
    }

    s = socket( resol->ai_family, resol->ai_socktype, resol->ai_protocol);
    if (s < 0){
      perror("Socket()");
      return;
    }

    r = bind(s, resol -> ai_addr, sizeof(struct  sockaddr_in6));
    if (r < 0){
      perror("bind()");
      return;
    }

    r = listen(s, 1);
    if (r < 0){
      perror("listen()");
      return;
    }
    

    while (1) {
      addrlen = sizeof(client);
      c = accept(s, (struct sockaddr *)&client, (socklen_t*)&addrlen);

    if (c < 0){
      perror("accept()");
      continue;
    }

    read_data(c, fd);

    close(c);
    }
}


void ext_in( int fd, char* ip, char* port) {
  int r;
  int clientSock;
  struct addrinfo *res;

  r = getaddrinfo(ip, port, NULL, &res);
      if (r < 0){
      perror("getaddrinfo()");
      return;
    }

    clientSock = socket( res->ai_family, res->ai_socktype, res->ai_protocol);
    if (clientSock < 0){
      perror("Socket()");
      return;
    }

    r = connect(clientSock, res->ai_addr, res->ai_addrlen);
    if (r < 0){
      perror("connect()");
      return;
    }


    printf("Connextion établie.\n");
    freeaddrinfo(res);

    read_data(clientSock, fd);

    close(clientSock);
}
