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
crop_x_stop= 1400
crop_y_start= 0
crop_y_stop= 90

gate_right= 1200
gate_left= 200


thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle

ret, frame= cap.read()
image_cue= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
image_prev= image_cue	

latch_cue = numpy.empty(255, dtype=int)


framenum= 0
while(1):
	ret, frame = cap.read()
	framenum+=1
	image_cue= frame[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
	
	for i in range(crop_x_start, crop_x_stop-1):
		for j in range(crop_y_stop-1, crop_y_start, -1):
			if (image_cue[j,i][0] or image_cue[j,i][1] or image_cue[j,i][2]) > threshold_min: # if detect object
				for j in range(crop_y_start, crop_y_stop):
					image_cue[j,i][0] += 150
				break
				
	# join to obtain contiguous block using green lines	
	block_start= 0	
	for i in range(crop_x_start, crop_x_stop-1):
		if image_cue[1,i][0] > threshold_min:
			block_start= i
		else:
			if (i-block_start) < thickness_min: 
				for j in range(crop_y_start, crop_y_stop):
					image_cue[j,i][1] += 100 # green
			else: 
				block_start= 0
	
	#remove spurious lines
	block_start= 0
	block_end= 0
	for i in range(crop_x_start, crop_x_stop-1):
		if (image_cue[1,i][0] > 0 or image_cue[1,i][1] > 0) and block_start==0:
			block_start= i
		elif (image_cue[1,i][0] == 0 and image_cue[1,i][1] == 0) and block_end==0:
			block_end= i
			if ((block_end-block_start) <= block_width) and block_start!=0 and block_end != 0:
				for n in range(block_start, block_end):
					for j in range(crop_y_start, crop_y_stop):
						image_cue[j,n][0] = 0 # blue
						image_cue[j,n][1] = 0 # green
						image_cue[j,n][2] = 0 # red
			#print("{} start{} stop{}".format(framenum, block_start, block_end))
			
			# apply identifier
			elif (block_start!= 0) and (block_end != 0):
				
				# from right: red: 1 to 99
				# from left: 101 to 200
				# retain the value while in the middle
				if (block_start > gate_left) and (block_end < gate_right):
					if (image_prev[1, int((block_start + block_end)/2) ][2] != 0) :
						vehicle_id= image_prev[1, int((block_start + block_end)/2) ][2]
						if latch_cue[vehicle_id] == 1:
							# check if closer to 
							print("just exited: {} {} {}".format(vehicle_id, framenum, block_end-block_start))
							latch_cue[vehicle_id]= 0
					else:
						vehicle_id= 254
					for n in range(block_start, block_end):
						for j in range(crop_y_start, crop_y_stop):
							image_cue[j,n][2] = vehicle_id	
							
				if (block_start < gate_left) and (gate_left < block_end):
					if (image_prev[1, int((block_start + block_end)/2) ][2] != 0) :
						vehicle_id=  image_prev[1, int((block_start + block_end)/2) ][2]
					else:
						vehicle_id= random.randint(1, 99)
						print("left gate: {} {} {}".format(vehicle_id, framenum, block_end-block_start))
						latch_cue[vehicle_id]= 1
					for n in range(block_start, block_end):
						for j in range(crop_y_start, crop_y_stop):
							image_cue[j,n][2] = vehicle_id
				
				if (block_start < gate_right) and (gate_right < block_end):
					if (image_prev[1, int((block_start + block_end)/2) ][2] != 0) :
						vehicle_id= image_prev[1, int((block_start + block_end)/2) ][2]
					else:
						vehicle_id= random.randint(101, 199)
						print("right gate: {} {} {}".format(vehicle_id, framenum, block_end-block_start))
						latch_cue[vehicle_id]= 1
					for n in range(block_start, block_end):
						for j in range(crop_y_start, crop_y_stop):
							image_cue[j,n][2] = vehicle_id
							
						
			block_start= 0
			block_end= 0
			
	
	image_prev= image_cue;

	# draw the gate
	for j in range(crop_y_start, crop_y_stop):
		image_cue[j,gate_left][1] = 255 # red
		image_cue[j,gate_right][1] = 255 # red
	
	cv2.imshow('cue',image_cue)
	
	k = cv2.waitKey(1)	
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
