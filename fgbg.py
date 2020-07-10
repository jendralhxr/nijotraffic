import numpy as np
import math
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
fgbg = cv2.createBackgroundSubtractorMOG2(400, 40, bool(0))

vsize = (int(1800-140), int(470-380))
out = cv2.VideoWriter(sys.argv[4],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)
    
framenum = int(sys.argv[2])

while(1):
    framenum += 1
    print(framenum)
    ret, frame = cap.read()
    #cv2.imshow('frame',frame)
    cropped = frame[380:470, 140:1800]
    
    fmask_gray = fgbg.apply(cropped)
    fmask_rgb = cv2.cvtColor(fmask_gray, cv2.COLOR_GRAY2RGB);
    result = cv2.bitwise_and(cropped, fmask_rgb)
    
    #cv2.imshow('frame',frame)
    #cv2.imshow('frame',result)
    out.write(result)
    #k = cv2.waitKey(16) & 0xff
    if framenum>int(sys.argv[3]):
	    break

cap.release()
out.release()
cv2.destroyAllWindows()
