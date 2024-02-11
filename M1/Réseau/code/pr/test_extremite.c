#include "extremite.h"
#include "iftun.h"

#include <stdio.h>
#include <string.h>
#include <linux/if_tun.h>

int main(int argc, char** argv){

    char ifname[10];
    strcpy(ifname, "tun0");
    
    int tunfd;
    tunfd = tun_alloc(ifname, IFF_TUN | IFF_NO_PI);

    if (tunfd < 0){
        perror("error tun_alloc()");
        return 1;
    }

    if (argc == 1){
        ext_out(tunfd);
        return 0
    }

    if(argc =! 3){
        fprintf(stderr, "usage: ./text_extremite ip port");
        return 1; 
    }

    char* ip = argv[1];
    char* port = argv[2];
    ext_in(tunfd, ip, port);

    return 0;

}