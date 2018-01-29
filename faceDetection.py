import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml') 
img = cv2.imread('messi.jpg')
W,H,D= img.shape
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    crop_img = img[y:y+h, x:x+w] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    cv2.imshow("cropped", crop_img)
    print crop_img.shape

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
