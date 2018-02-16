#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#define POINTS 4

FILE *logfile;
int reed[POINTS];
struct timeval timer[POINTS], time_start;
char command[128];
char kara;
ssize_t n;
	
/* usage:
	nenden gpio2 gpio3 gpio17 gpio27 
*/

int main(int argc, char **argv){
	int i;
	// inits
	for (i=0; i<=9; i++){
		sprintf(command,"echo %s >> /sys/class/gpio/export", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"echo in > /sys/class/gpio/%s/direction", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"echo up > /sys/class/gpio/%s/pull", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"/sys/class/gpio/%s/value", argv[i+1]);
		reed[i] = open(argv[i+1], O_RDONLY);
		if (reed[i]==-1) {
			printf("failed to open %s\n", argv[i+1]);
			exit(-1);
			}
		}

	// sensor routine
	while(1){
		for (i=0; i<POINTS; i++){
			read(reed[i], &kara, 1);
			if(kara=='0'){
				if (i==0) // start{
					gettimeofday(&time_start,NULL);
					printf("start!\n");
					}
				else{
					gettimeofday(&(timer[i]),NULL);
					printf("check point %d: %f mikrodetik", i, \
						(timer[i].tv_sec - time_start.tv_sec)*1e6 + timer[i].tv_usec - time_start.tv_usec);
					// physics goes here
					}
				}
				
			}
	}
