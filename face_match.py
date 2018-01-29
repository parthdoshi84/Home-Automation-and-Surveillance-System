import cv2
import numpy as np
import math
import time
capture = True
eye_cascade_left = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_eye.xml')

img = cv2.imread("41.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img1 = cv2.imread("51.png")
distance = []
area= []
W,H=img.shape[:2]
w,h = img1.shape[:2]
eyes = eye_cascade_left.detectMultiScale(gray)
#eye_right = eye_cascade_right.detectMultiScale(gray)
i=0
for (ex,ey,ew,eh) in eyes:
    if i<2:
        distance.append(ew+ex)
        area.append(ew*eh)
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        i=i+1
    else:
        break
print "Distance " + str(abs(distance[1]-distance[0]))
print "Left Area " + str(area[0])
print "Right Area " + str(area[1])
cv2.imshow('img',img)

cv2.waitKey(0)
    
cv2.destroyAllWindows()
