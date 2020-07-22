# python difframe.py input.mp4 reference-image.png 0 82100 output.mp4
# 00000.MTS starts at 400


import numpy as np
import math
import cv2
import sys

THRESHOLD_VAL= 40
THRESHOLD_HEIGHT= 20

startx= 140
stopx= 1644
starty=388
stopy= 468

cap = cv2.VideoCapture(sys.argv[1])
ref= cv2.imread(sys.argv[2])
vsize = (int(1504), int(96))

temp= ref
out = cv2.VideoWriter(sys.argv[5],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)

cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[3]))
framenum = int(sys.argv[3])

while(1):
    ret, frame = cap.read()
    cropped = frame[starty:stopy, startx:stopx]
    
    difference= cv2.absdiff(ref, cropped)
    ret,thresh = cv2.threshold(difference,THRESHOLD_VAL,255,cv2.THRESH_BINARY);
    #print(thresh.shape)
    temp = cv2.bitwise_and(cropped, thresh)
    
    out.write(temp)
    print(framenum)
    cv2.imshow('diff',temp)
    k = cv2.waitKey(1) & 0xFF
    if k== ord("c"):
		print("print reference")
		cv2.imwrite("ref.png", cropped)
    if k== 27: # esc
		break
		
    print(framenum)
    framenum += 1
    if framenum> int(sys.argv[4]):
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
