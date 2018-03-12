#include <stdio.h> 
#include <unistd.h> 
#include <stdlib.h> 
#include <fcntl.h> 
#include <poll.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <sys/time.h>
#define INTERVAL 10 // msec

FILE *logfile; 
int sensor1, sensor2; 
struct pollfd poll1, poll2; 
struct timeval time_current, time_speed, time_length; 
int ret;
char c1, c2; 
char state; // occlusion at a, b, both, or clear (1, 2, 3, 0) 
char sensor_detect[2]; // whether a vehicle is passing 
char passfirst, pass; 
int count;
ssize_t n; 

/* usage:
	nijo log.txt */ 
	
int main(int argc, char **argv){
	// gpio2 and gpio3 init
	system("echo 2 >/sys/class/gpio/export");
    system("echo in >/sys/class/gpio/gpio2/direction");
	system("echo rising >/sys/class/gpio/gpio2/edge");
	
	// opening sensor descriptors
    sensor1 = open("/sys/class/gpio/gpio2/value", O_RDONLY);
    if (sensor1 < 0) {
		fprintf(stderr, "error when opening sensor1\n");
        return sensor1;
	}
	else {
		poll1.fd= sensor1;
		poll1.events= POLLPRI;
		printf("opened gpio2\n");
	}
    b
	// sensor routine
	while(1){
		logfile= fopen(argv[1], "a");
		// read from sensor1
		sensor_detect[0]= 0;
        lseek(sensor1, 0, SEEK_SET);
		ret = poll(&poll1, 1, INTERVAL);
		read(sensor1, &c1, 1);
		if ((c1=='0') && !state){ // adjust whether NPN or PNP photodiode
			gettimeofday(&time_current,NULL);
			printf("%ld\n",time_current.tv_sec);
			fprintf(logfile, "%ld\n",time_current.tv_sec);
			state=~0;
			}
		if (cl=='1'){
			state= 0;
		}
			
		fclose(logfile);
		}
	}
