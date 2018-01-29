import cv2
import numpy as np
import math
import time
capture = True
eye_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_eye.xml')
#eye_cascade_right = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/right_eye.xml')
nose_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/nose.xml')
mouth_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/mouth.xml')
face_cascade2 = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_alt2.xml')

img = cv2.imread("41.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img1 = cv2.imread("51.png")
distance = []
area= []
W,H=img.shape[:2]
w,h = img1.shape[:2]
"""faces2 = face_cascade2.detectMultiScale(img, 1.1, 7)
#for (x,y,w,h) in faces2:
    print "In face"
    crop_img = img[y:y+h, x:x+w] 
    crop_img= cv2.resize(crop_img,(240,240), interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)"""

eye = eye_cascade.detectMultiScale(gray)
#eye_right = eye_cascade_right.detectMultiScale(gray)
nose = nose_cascade.detectMultiScale(gray)
mouth = mouth_cascade.detectMultiScale(gray)
i=0
for (ex,ey,ew,eh) in eye:
    if i<2:
        print "Detected"
        distance.append(ew+ex)
        area.append(ew*eh)
        cv2.rectangle(crop_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        i=i+1
    else:
        break
i=0

i=0
for (ex,ey,ew,eh) in nose:
    if i<1:
        print "Nose"
        distance.append(ew+ex)
        area.append(ew*eh)
        cv2.rectangle(crop_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        i=i+1
    else:
        break
i=0
for (ex,ey,ew,eh) in mouth:
    if i<1:
        distance.append(ew+ex)
        area.append(ew*eh)
        cv2.rectangle(crop_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        i=i+1
    else:
        break
print "Distance " + str(abs(distance[1]-distance[0]))
print "Left Area " + str(area[0])
print "Right Area " + str(area[1])
cv2.imshow('img',crop_img)

cv2.waitKey(0)
    
cv2.destroyAllWindows()
