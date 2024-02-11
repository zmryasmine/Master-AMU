#include "extremite.h"
#include "iftun.h"

#include <stdio.h>
#include <string.h>
#include <linux/if_tun.h>

int main(int argc, char** argv){

    char ifname[10];
    strcpy(ifname, "tun0");
    
    int tunfd;
    char* ip = argv[2];
    char* port = argv[1];
    tunfd = tun_alloc(ifname, IFF_TUN | IFF_NO_PI);

    if (tunfd < 0){
        perror("error tun_alloc()");
        return 1;
    }

    printf("Création de tun0.\n");
    printf("Faire la configuration de tun0.....\n");
    printf("Appuyez sur une touche pour continuer\n");
    getchar();
    printf("Interface tun0 configurée..\n");
   system("chmod +x configure-tun.sh");
   system("./configure-tun.sh");
    //ip route add @reseau VM1 ou VM3 via 172.16.2.10 dev tun0 
    //VM1 : 	172.16.2.144 pour VM3-6
    //VM3 :     172.16.2.176 pour VM1-6
    system("ip a show tun0");
    printf("Appuyez sur une touche pour continuer\n");
    getchar();

    if (argc == 1){
        
        system("ip route add 172.16.2.176 via 172.16.2.10 dev tun0");
        //ip route add @reseau VM1 ou VM3 via 172.16.2.10 dev tun0 
        //VM3 :     172.16.2.176 pour VM1-6
        ext_out(tunfd,port);
        return 0;
    }

    if(argc =! 3){
        system("ip route add 172.16.2.144 via 172.16.2.10 dev tun0");
          //ip route add @reseau VM1 ou VM3 via 172.16.2.10 dev tun0 
    //VM1 : 	172.16.2.144 pour VM3-6
        fprintf(stderr, "usage: ./text_extremite port ip");
        return 1; 
    }

    ext_in(tunfd, ip, port);

    return 0;

}

