#ifndef _EXTREMITE_H_
#define _EXTREMITE_H_

void ext_out(int fd);
void ext_in(int fd, char* ip, char* port);
void read_data(int fd_sock, int fd_tun);

#endif

