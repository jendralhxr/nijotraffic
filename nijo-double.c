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
		if (c1=='0'){ // adjust whether NPN or PNP photodiode
			sensor_detect[0]= 1;
			if (passfirst==0) {
				pass=1;
				passfirst=1;
				gettimeofday(&time_current,NULL);
			}
			else if ((pass==255) && (passfirst==2) && (state!=1)){
				pass= 0;
				state=1;
				passfirst= 0;
				gettimeofday(&time_speed,NULL);
				printf("%ld a %ld",time_current.tv_sec, (time_speed.tv_sec-time_current.tv_sec)*1000000+time_speed.tv_usec-time_current.tv_usec);
				fprintf(logfile, "%ld a %d",time_current.tv_sec, (time_speed.tv_sec-time_current.tv_sec)*1000000+time_speed.tv_usec-time_current.tv_usec);
				}
			//printf("pass at sensor1 %d %d\n",pass, passfirst);
			}
		else sensor_detect[0]= 0;
		
		// read from sensor2
		sensor_detect[1]= 0;
        lseek(sensor2, 0, SEEK_SET);
		ret = poll(&poll2, 1, INTERVAL);
		read(sensor2, &c2, 1);
		if (c2=='0'){ // adjust whether NPN or PNP photodiode
			sensor_detect[1]= 1;
			if (passfirst==0) {
				pass=255;
				passfirst=2;
				gettimeofday(&time_current,NULL);
			}
			else if ((pass==1)&& (passfirst==1) && (state!=2)){
				pass= 0;
				passfirst= 0;
				state=2;
				gettimeofday(&time_speed,NULL);
				printf("%ld b %ld",time_current.tv_sec, (time_speed.tv_sec-time_current.tv_sec)*1000000+time_speed.tv_usec-time_current.tv_usec);
				fprintf(logfile, "%ld b %d",time_current.tv_sec, (time_speed.tv_sec-time_current.tv_sec)*1000000+time_speed.tv_usec-time_current.tv_usec);
				}
			//printf("pass at sensor2 %d %d\n",pass, passfirst);
		}
		else sensor_detect[1]= 0;
		
		if (!sensor_detect[0] && !sensor_detect[1]){
			//printf("traffic clear\n");
			if (state){
				gettimeofday(&time_length,NULL);
				printf(" %ld\n",(time_length.tv_sec-time_current.tv_sec)*1000000+time_length.tv_usec-time_current.tv_usec);
				fprintf(logfile, " %ld\n",(time_length.tv_sec-time_current.tv_sec)*1000000+time_length.tv_usec-time_current.tv_usec);
				state= 0;
				passfirst= 0;
				count= 0;
				pass= 0;
				}
			count++;
			if (count>2000) { // 2 sec 
				passfirst=0; 
				count=0;
				}
			pass= 0;
			}
		fclose(logfile);
		}
	}
