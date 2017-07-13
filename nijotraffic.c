#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>

#define BAUD 19200
#define BUFFER_SIZE 64

FILE *logfile;
int sensor1, sensor2;
struct timeval time_current;
char command[128];
char kara, buffer;
char sensor_detect[2]; // whether a vehicle is passing
unsigned int len;
ssize_t n;

/* usage:
	nijo /dev/ttyS1 /dev/ttyS2 log.txt
*/

int main(int argc, char **argv){
	sprintf(command,"stty -F %s %d",argv[1], BAUD);
	sprintf(command,"stty -F %s %d",argv[2], BAUD);
	// opening sensor descriptors
    sensor1 = open(argv[1], O_RDWR | O_NOCTTY | O_SYNC);
    if (sensor1 < 0) {
		fprintf(stderr, "error when opening sensor1\n");
        return sensor1;
	}
    sensor2 = open(argv[2], O_RDWR | O_NOCTTY | O_SYNC);
    if (sensor2 < 0) {
		fprintf(stderr, "error when opening sensor2\n");
        return sensor2;
	}    
	
	// sensor routine
	while(1){
		// send distance commands
		sprintf(command,"D");
		n = write(sensor1, command, 1);
        n = write(sensor2, command, 1);
        sensor_detect[0]= 0;
        sensor_detect[1]= 0;
        
		// read from sensor1
		buffer=1;
		while (buffer){
			len=read(sensor1, &kara, 1);
			if (len==1){
				if(kara=='E') sensor_detect[0]= 1; // detecting occlusion
				if(kara!=0xa) buffer= 2;
				if((kara==0xa) && (buffer==2)) buffer=0; // end of line
					}
				}
		
		// read from sensor2
		buffer=1;
		while (buffer){
			len=read(sensor2, &kara, 1);
			if (len==1){
				if(kara=='E') sensor_detect[1]= 1; // detecting occlusion
				if(kara!=0xa) buffer= 2;
				if((kara==0xa) && (buffer==2)) buffer=0; // end of line
					}
				}
		
		// compare, if either is null, write things to logfile
		logfile= fopen(argv[3], "a");
		if (sensor_detect[0] && sensor_detect[1]){
			gettimeofday(&time_current,NULL);
    		fprintf(logfile, "%ld c\n",time_current.tv_sec);
    		printf("%ld c\n",time_current.tv_sec);
			sensor_detect[0]= 0;
			sensor_detect[1]= 0;
			}
		else if (sensor_detect[0]){
			gettimeofday(&time_current,NULL);
    		fprintf(logfile, "%ld a\n",time_current.tv_sec);
			printf("%ld a\n",time_current.tv_sec);
			sensor_detect[0]= 0;
			}
		else if (sensor_detect[1]){
			gettimeofday(&time_current,NULL);
    		fprintf(logfile, "%ld b\n",time_current.tv_sec);
			printf("%ld b\n",time_current.tv_sec);
			sensor_detect[1]= 0;
			}
		else printf("traffic clear\n");	
		sensor_detect[0]= 0;
		sensor_detect[1]= 0;
		fclose(logfile);
		}
	}
