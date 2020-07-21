#!/usr/bin/env python3
import numpy
import cv2
import sys
import math
import random
# todo: single pixel horizontal shadow instead of block highlight

print(sys.argv[1])
cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
frame = cap.read()

threshold_min= 20

crop_x_start= 0
crop_x_stop= 900
crop_y_start= 0
crop_y_stop= 90

thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle

gate_right=  crop_x_stop -block_width # position of ID-assignment gate
gate_left= crop_x_start +block_width # position of ID-assignment gate

ret, frame= cap.read()
image_cue= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
image_prev= image_cue    


framenum= float(sys.argv[2])
while(1):
    ret, frame = cap.read()
    framenum+=1
    image_cue= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
    
    for i in range(crop_x_start, crop_x_stop-1):
        for j in range(crop_y_stop-1, crop_y_start, -1):
            if (image_cue[j,i][0] or image_cue[j,i][1] or image_cue[j,i][2]) > threshold_min: # if detect object
                image_cue[1,i][0] += 150
                
    # join to obtain contiguous block using green lines    
    block_start= 0    
    for i in range(crop_x_start, crop_x_stop-1):
        if image_cue[1,i][0] > threshold_min:
            block_start= i
        else:
            if (i-block_start) < thickness_min: 
                image_cue[1,i][1] += 100 # green
            else: 
                block_start= 0
    
    block_start= 0
    block_end= 0
    for i in range(crop_x_start, crop_x_stop-1):
        if (image_cue[1,i][0] > 0 or image_cue[1,i][1] > 0) and block_start==0:
            block_start= i
        elif (image_cue[1,i][0] == 0 and image_cue[1,i][1] == 0) and block_end==0:
            block_end= i
            #remove spurious lines less than minimum block width
            if ((block_end-block_start) <= block_width) and block_start!=0 and block_end != 0:
                for n in range(block_start, block_end):
                    image_cue[1,n][0] = 0 # blue
                    image_cue[1,n][1] = 0 # green
                    image_cue[1,n][2] = 0 # red
            #print("{} start{} stop{}".format(framenum, block_start, block_end))
            
            # apply identifier
            elif (block_start!= 0) and (block_end != 0):
                
                # from right: red: 1 to 99
                # from left: 101 to 200
                # retain the value while in the middle
                # in the middle
                if (block_start >= gate_left) and (block_end <= gate_right):
                    # left to right
                    vehicle_id = 0
                    if (image_prev[2,int((block_start + block_end)/2) ][2] != 0) :
                        vehicle_id= image_prev[2,int((block_start + block_end)/2) ][2]
                        print("{} {} {} {} left".format(vehicle_id, framenum, block_start, block_end))
                    for n in range(block_start, block_end):
                        image_cue[2,n][2] = vehicle_id    
                    # right to left
                    vehicle_id = 0
                    if (image_prev[3, int((block_start + block_end)/2) ][2] != 0) :
                        vehicle_id= image_prev[3,int((block_start + block_end)/2) ][2]
                        print("{} {} {} {} right".format(vehicle_id, framenum, block_start, block_end))
                    for n in range(block_start, block_end):
                        image_cue[3,n][2] = vehicle_id    
                        
                #left to right
                if (block_start < gate_left) and (gate_left < block_end):
                    if (image_prev[2, int((block_start + block_end)/2) ][2] != 0) :
                        vehicle_id=  image_prev[2, int((block_start + block_end)/2) ][2]
                        #if (image_prev[3, int((block_start + block_end)/2) ][2] == 0):
                        #    print("{} {} {} {} left".format(vehicle_id, framenum, block_start, block_end))
                    else:
                        vehicle_id= random.randint(1, 80)
                        #if (image_prev[3, int((block_start + block_end)/2) ][2] == 0):
                        #    print("{} {} {} {} leftnew".format(vehicle_id, framenum, block_start, block_end))
                    for n in range(block_start, block_end):
                        image_cue[2,n][2] = vehicle_id
                
                # right to left
                if (block_start < gate_right) and (gate_right < block_end):
                    if (image_prev[3, int((block_start + block_end)/2) ][2] != 0) :
                        vehicle_id= image_prev[3, int((block_start + block_end)/2) ][2]
                        #if (image_prev[2, int((block_start + block_end)/2) ][2] == 0):
                        #print("{} {} {} {} rightedge".format(vehicle_id, framenum, block_start, block_end))
                    else:
                        vehicle_id= random.randint(81, 160)
                        #if (image_prev[2, int((block_start + block_end)/2) ][2] == 0):
                        #print("{} {} {} {} rightnew".format(vehicle_id, framenum, block_start, block_end))
                    for n in range(block_start, block_end):
                        image_cue[3,n][2] = vehicle_id
                            
            block_start= 0
            block_end= 0
    
    image_prev= image_cue;

    #draw the gate
    #or j in range(crop_y_start, crop_y_stop):
    #    image_cue[j,gate_left][1] = 255 # red
    #    image_cue[j,gate_right][1] = 255 # red
    #    cv2.imshow('cue',image_cue)
    #print(framenum)
    #k = cv2.waitKey(1)    
    #if k == 27:
    #    break

cap.release()
cv2.destroyAllWindows()
