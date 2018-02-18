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
struct pollfd pfd; 
double elapsed[POINTS];
char command[128];
char kara[4];
ssize_t n;
	
/* usage	nenden gpio2 gpio3 gpio17 gpio27 

polling from https://raspberrypi.stackexchange.com/questions/44416/polling-gpio-pin-from-c-always-getting-immediate-response
*/

int main(int argc, char **argv){
	int i;
	// inits
	/*for (i=0; i<POINTS; i++){
		sprintf(command,"echo %s >> /sys/class/gpio/export", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"echo in > /sys/class/gpio/%s/direction", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"echo up > /sys/class/gpio/%s/pull", argv[i+1]);
		if (system(command)==-1) exit(1);
		sprintf(command,"/sys/class/gpio/%s/value", argv[i+1]);
		printf("opening: %s\n",command);
		reed[i] = open(command, O_RDONLY);
		if (reed[i]==-1) {
			printf("failed to open %s\n", argv[i+1]);
			exit(-1);
			}
		}
*/
		reed[0] = open("/sys/class/gpio/gpio2/value", O_RDONLY);
		reed[1] = open("/sys/class/gpio/gpio3/value", O_RDONLY);
		reed[2] = open("/sys/class/gpio/gpio17/value", O_RDONLY);
		reed[3] = open("/sys/class/gpio/gpio27/value", O_RDONLY);
	
	// sensor routine
	while(1){
		for (i=0; i<POINTS; i){
			poll(&pfd, 1, -1); //
			lseek(reed[i], 0, SEEK_SET);
			n= read(reed[i], kara, 2);
			printf("read: %d %d\n",kara[0], kara[1]);
			if(kara[0]=='0'){
				if (i==0){ // start
					gettimeofday(&time_start,NULL);
					printf("start!\n");
					i++;
					}
				else{
					gettimeofday(&(timer[i]),NULL);
					elapsed[i]= (timer[i].tv_sec - time_start.tv_sec) + (timer[i].tv_usec - time_start.tv_usec); 
					printf("check point %d: %f detik\n", i, elapsed[i]/1e6);
					// physics goes here
					i++;
					}
				if (i==POINTS-1) { // end of track, wait for new start
					i=0; 
					break;
					}				
				}
			}
		}
}
