#include <stdio.h> 
#include <unistd.h> 
#include <stdlib.h> 
#include <fcntl.h> 
#include <poll.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <sys/time.h>
#define INTERVAL 1 // msec

FILE *logfile; 
int sensor1, sensor2; 
struct pollfd poll1, poll2; 
struct timeval time_current; 
int ret;
char c1, c2; 
char state; // occlusion at a, b, both, or clear (1, 2, 3, 0) 
char sensor_detect[2]; // whether a vehicle is passing 
char passfirst, pass; 
int count;
ssize_t n; 
/* usage:
	nijo log.txt */ int main(int argc, char **argv){
	// gpio2 and gpio3 init
	system("echo 2 >/sys/class/gpio/export");
    system("echo in >/sys/class/gpio/gpio2/direction");
	system("echo rising >/sys/class/gpio/gpio2/edge");
	system("echo 3 >/sys/class/gpio/export");
    system("echo in >/sys/class/gpio/gpio3/direction");
	system("echo rising >/sys/class/gpio/gpio3/edge");
 
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
    sensor2 = open("/sys/class/gpio/gpio3/value", O_RDONLY);
    if (sensor2 < 0) {
		fprintf(stderr, "error when opening sensor2\n");
        return sensor2;
	}    
	else {
		poll2.fd= sensor2;
		poll2.events= POLLPRI;
		printf("opened gpio3\n");
	}
    
	// sensor routine
	while(1){
		
		logfile= fopen(argv[1], "a");
		// read from sensor1
		sensor_detect[0]= 0;
        lseek(sensor1, 0, SEEK_SET);
		ret = poll(&poll1, 1, INTERVAL);
		read(sensor1, &c1, 1);
		if (c1=='0'){
			sensor_detect[0]= 1;
			if (pass==0) {
				pass=1;
				passfirst=1;
			}
			else if ((pass==255) && (passfirst==2) && (state!=1)){
				pass= 0;
				state=1;
				passfirst= 0;
				gettimeofday(&time_current,NULL);
				printf("%ld 1\n",time_current.tv_sec);
				fprintf(logfile, "%ld 1\n",time_current.tv_sec);
				}
			//printf("pass at sensor1 %d %d\n",pass, passfirst);
			}
		else sensor_detect[0]= 0;
		
		// read from sensor2
		sensor_detect[1]= 0;
        lseek(sensor2, 0, SEEK_SET);
		ret = poll(&poll2, 1, INTERVAL);
		read(sensor2, &c2, 1);
		if (c2=='0'){
			sensor_detect[1]= 1;
			if (pass==0) {
				pass=255;
				passfirst=2;
			}
			else if ((pass==1)&& (passfirst==1) && (state!=2)){
				pass= 0;
				passfirst= 0;
				state=2;
				gettimeofday(&time_current,NULL);
				printf("%ld 2\n",time_current.tv_sec);
				fprintf(logfile, "%ld 2\n",time_current.tv_sec);
				}
			//printf("pass at sensor2 %d %d\n",pass, passfirst);
		}
		else sensor_detect[1]= 0;
		
		// outputs
		// state 1: passing from sensor1 then sensor2
		// state 2: passing from sensor2 then sensor1
		// state 3: occlusion or misalignment
		/*
		if (((state==1) || (state==2)) && (pass==0)){
			gettimeofday(&time_current,NULL);
    		printf("%ld %d\n",time_current.tv_sec, state);
			fprintf(logfile, "%ld %d\n",time_current.tv_sec, state);
			passfirst= 0;
			state= 0;
			}
		else if (sensor_detect[0] && sensor_detect[1] && (state!=3)){
			state= 3;			
			gettimeofday(&time_current,NULL);
    		fprintf(logfile, "%ld c\n",time_current.tv_sec);
    		printf("%ld c\n",time_current.tv_sec);
			}
		*/
		if (!sensor_detect[0] && !sensor_detect[1]){
			//printf("traffic clear\n");
			state= 0;
			count++;
			if (count>5000) {
				passfirst=0; // 10 secs
				count=0;
				}
			pass= 0;
			passfirst= 0;
			}
		
		fclose(logfile);
		}
	}
