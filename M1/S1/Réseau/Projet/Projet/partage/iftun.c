#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h> 
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <poll.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>

#include "iftun.h"




int tun_alloc(char *dev, short flags)
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
  ifr.ifr_flags = flags ; 
  if( *dev )
    strncpy(ifr.ifr_name, dev, IFNAMSIZ);

  if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ){
    close(fd);
    return err;
  }
  strcpy(dev, ifr.ifr_name);
  return fd;
}      

int copy_tun(int src, int dst){
    if (src == -1) {
        perror("Source file is not open :/ ");
        return -1;
    }   
    
    if (dst == -1) {
        perror("Destination file is not open :/ ");
        return -1;
    }  
    
    char buff[1500];
    
    ssize_t n = 0;
    
    n = read(src, &buff, 1499);
    if (n < 0) {
        perror("Error reading :/");
        return n;
    }
    
    buff[n] = '\0';
    write(dst, &buff, n);
    
    return n;
}   

void bidirectional_tunnel(int fd_sock, int fd_tun) {
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
/*
int main (int argc, char** argv){

  int tunfd;
  printf("Création de %s\n",argv[1]);
  tunfd = tun_alloc(argv[1], IFF_TUN | IFF_NO_PI);
  printf("tunfd :%d\n",tunfd);
  
  
  if (tunfd < 0) {
    perror("tun_alloc error");
    return 1;
  }
  
  printf("Faire la configuration de %s...\n",argv[1]);
  printf("tunfd :%d\n",tunfd);
  printf("Appuyez sur une touche pour continuer\n");
  getchar();
  printf("Interface %s Configurée:\n",argv[1]);
  system("ip addr show tun0");
  
  int dst = 1;
  
  while (1) {
    copy_tun(tunfd, dst);
  }
  
  
  
  
  
  printf("Appuyez sur une touche pour terminer\n");
  getchar();

  return 0;
}
*/

