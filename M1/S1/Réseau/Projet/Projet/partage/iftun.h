#ifndef IFTUN_H
#define IFTUN_H

int tun_alloc(char *dev, short flags);
int copy_tun(int src, int dst);
void bidirectional_tunnel(int fd1, int fd2);


#endif
