# python difframe.py crop0.mp4 ref0.png 0 82100 flag0.mp4
# python difframe.py crop1.mp4 ref1.png 0 82430 flag1.mp4

import numpy as np
import math
import cv2
import sys

THRESHOLD_VAL= 50

cap = cv2.VideoCapture(sys.argv[1])
ref= cv2.imread(sys.argv[2])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[3]))

temp= ref
vsize = (int(1504), int(96))
out = cv2.VideoWriter(sys.argv[5],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)
    
framenum = int(sys.argv[3])

while(1):
    framenum += 1
    print(framenum)
    ret, frame = cap.read()
    
    difference= cv2.absdiff(ref, frame)
    ret,thresh = cv2.threshold(difference,THRESHOLD_VAL,255,cv2.THRESH_BINARY);
    temp = cv2.bitwise_and(difference, thresh)
    
    out.write(temp)
    print(framenum)
    #cv2.imshow('diff',temp)
    #k = cv2.waitKey(1)
    if framenum> int(sys.argv[4]):
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
