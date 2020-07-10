#!/usr/bin/env python3
import numpy as np
import cv2
import sys
import math

# todo: single pixel horizontal shadow instead of block highlight

print(sys.argv[1])
cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
frame = cap.read()

threshold_min= 20

crop_x_start= 0
crop_x_stop= 1400
crop_y_start= 0
crop_y_stop= 90

gate_right= 200
gate_left= 1200


thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle

framenum= 0
while(1):
	ret, frame = cap.read()
	framenum+=1
	image= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
	
	for i in range(crop_x_start, crop_x_stop-1):
		for j in range(crop_y_stop-1, crop_y_start, -1):
			if (image[j,i][0] or image[j,i][1] or image[j,i][2]) > threshold_min: # if detect object
				for j in range(crop_y_start, crop_y_stop):
					image[j,i][0] += 150
				break
				
	# join to obtain contiguous block using green lines	
	block_start= 0	
	for i in range(crop_x_start, crop_x_stop-1):
		if image[1,i][0] > threshold_min:
			block_start= i
		else:
			if (i-block_start) < thickness_min: 
				for j in range(crop_y_start, crop_y_stop):
					image[j,i][1] += 100 # green
			else: 
				block_start= 0
	
	#remove spurious lines
	block_start= 0
	block_stop= 0
	for i in range(crop_x_start, crop_x_stop-1):
		if (image[1,i][0] > 0 or image[1,i][1] > 0) and block_start==0:
			block_start= i
		elif (image[1,i][0] == 0 and image[1,i][1] == 0) and block_stop==0:
			block_stop= i
			if ((block_stop-block_start) <= block_width) and block_start!=0 and block_stop != 0:
				for n in range(block_start, block_stop):
					for j in range(crop_y_start, crop_y_stop):
						image[j,n][0] = 0 # blue
						image[j,n][1] = 0 # green
						image[j,n][2] = 0 # red
			#print("{} start{} stop{}".format(framenum, block_start, block_stop))
			block_start= 0
			block_stop= 0
					
	# apply identifier
	# detect passing from right or left
	# from right: red: 1 to 99
	# from left: 101 to 200
	# infer the passes
	
	# draw the gate
	for j in range(crop_y_start, crop_y_stop):
		image[j,gate_left][2] = 255 # red
		image[j,gate_right][2] = 255 # red

	
	cv2.imshow('frame',image)
	k = cv2.waitKey(1)	
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
