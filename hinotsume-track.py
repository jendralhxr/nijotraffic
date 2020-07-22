# python hinotsume-track.py input-video.mp4 reference-image.png 0 82100 labelled-video.mp4
# 00000.MTS starts at 400
# 00001.MTS starts at 0

import numpy as np
import math
import cv2
import sys
import random

THRESHOLD_VAL= 40
THRESHOLD_HEIGHT= 20

startx= 140
stopx= 1644
starty=388
stopy= 468

crop_x_start= 0
crop_x_stop= 900 # shorter window makes life easier
crop_y_start= 0
crop_y_stop= stopy -starty

cap = cv2.VideoCapture(sys.argv[1])
ref= cv2.imread(sys.argv[2])
vsize = (int(1504), int(96))

thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle

gate_right=  crop_x_stop -block_width # position of ID-assignment gate
gate_left= crop_x_start +block_width # position of ID-assignment gate

temp= ref
image_prev= ref
image_display= ref
out = cv2.VideoWriter(sys.argv[5],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)

cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[3]))
framenum = int(sys.argv[3])

while(1):
    ret, frame = cap.read()
    cropped = frame[starty:stopy, startx:stopx]
    
    # crop and subtract [reference] background
    difference= cv2.absdiff(ref, cropped)
    ret,thresh = cv2.threshold(difference,THRESHOLD_VAL,255,cv2.THRESH_BINARY);
    #print(thresh.shape)
    image_cue = cv2.bitwise_and(cropped, thresh)
    
    for i in range(crop_x_start, crop_x_stop-1):
        for j in range(crop_y_stop-1, crop_y_start, -1):
            if (image_cue[j,i][0] or image_cue[j,i][1] or image_cue[j,i][2]) > THRESHOLD_VAL: # if detect object
                image_cue[1,i][0] += 150
                break
                
    # join to obtain contiguous block using green lines    
    block_start= 0    
    for i in range(crop_x_start, crop_x_stop-1):
        if image_cue[1,i][0] > THRESHOLD_VAL:
            block_start= i
        else:
            if (i-block_start) < thickness_min: 
                image_cue[1,i][1] += 100 # green
            else: 
                block_start= 0
    
    block_start= 0
    block_end= 0
    image_display= cropped
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
                        start_point = (block_start, 8) 
                        end_point = (block_end, 72) 
                        label_point= (block_start+10, 40)
                        cv2.rectangle(image_display, start_point, end_point, (255,36,12), 3)
                        cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,36, 12), 3)
                    for n in range(block_start, block_end):
                        image_cue[2,n][2] = vehicle_id    
                    # right to left
                    vehicle_id = 0
                    if (image_prev[3, int((block_start + block_end)/2) ][2] != 0) :
                        vehicle_id= image_prev[3,int((block_start + block_end)/2) ][2]
                        print("{} {} {} {} right".format(vehicle_id, framenum, block_start, block_end))
                        start_point = (block_start, 8) 
                        end_point = (block_end, 72) 
                        label_point= (block_start+10, 40)
                        cv2.rectangle(image_display, start_point, end_point, (12,36,255), 3)
                        cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (12,36, 255), 3)
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
    for j in range(crop_y_start, crop_y_stop):
	#    image_cue[j,gate_left][1] = 255 # red
	#    image_cue[j,gate_right][1] = 255 # red
        image_display[j,gate_left][1] = 255 # red
        image_display[j,gate_right][1] = 255 # red
    cv2.imshow('cue',image_display)
    
    #k = cv2.waitKey(1) & 0xFF
    #if k== ord("c"):
	#	print("snap reference")
	#	cv2.imwrite("ref.png", cropped)
    #if k== 27: # esc
	#	break
	
    out.write(image_display)
    
    #print(framenum)
    framenum += 1
    if framenum> int(sys.argv[4]):
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
