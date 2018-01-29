import cv2
import numpy as np
import math
import time
capture = True
img = cv2.imread("Sagar Collection.png")
img1 = cv2.imread("Parth2.png")
W,H=img.shape[:2]
w,h = img1.shape[:2]
res = cv2.matchTemplate(img,img1,cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
print max_loc
print max_val
bottom_right = (top_left[0] + w, top_left[1] + h)
a1 = W*H
a2= (bottom_right[1]-top_left[1])*(bottom_right[0]-top_left[0])
print a1
print a2
if(max_val>0.65 and ((max_loc[0]>=0 and max_loc[0]<=10 and max_loc[1]>=0 and max_loc[1]<=10) or (max_loc[0]>=230 and max_loc[0]<=250 and max_loc[1]>=0 and max_loc[1]<=10) or (max_loc[0]>=0 and max_loc[0]<=10 and max_loc[1]>=230 and max_loc[1]<=250) or (max_loc[0]>=230 and max_loc[0]<=250 and max_loc[1]>=230 and max_loc[1]<=250))):
    print 'match'
else:
    print "mismatch"
cv2.rectangle(img,top_left, bottom_right, 255, 2)
cv2.imshow('Image',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

print max_val
