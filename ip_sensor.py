#!usr/bin/python

import Adafruit_DHT as ada
import numpy as np
import warnings
import mcp3208
import dweepy
import thread
import math
import time
import sys
import cv2
import os

warnings.filterwarnings("ignore")
print "Initialising..."

############# IP Var #############
face_cascade1 = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
img=cv2.imread("Sagar Collection.png")
capture =True
cap =cv2.VideoCapture(0)
ret,pf = cap.read()
ret1,f = cap.read()
ret2,nf = cap.read()
prevFrame = cv2.cvtColor(pf,cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
human_faces1 = []
human_faces2 = []
r=1
s=11

############# Sensor Var #############
#spi=mcp3208.MCP3208(0)
dweepy.dweet_for('near',{'MQ2':0,'MQ3':0,'MQ135':0,'Temp':0,'Humid':0,'Count':0})
time.sleep(1)


############# Sensor Reading #############
def sensor_read():
  try:
    count = 0
    while True:
      count = count + 1
      '''mq2 = spi.read(0)
      mq3 = spi.read(1)
      mq135 = spi.read(2)
      humid,temp = ada.read_retry(11,4,retries=5,delay_seconds=0.05)'''
      mq2 = mq3 = mq135 = 300
      humid = temp = 50
      if temp is not None and humid is not None:
        thread.start_new_thread(dweepy.dweet_for,('near',{'MQ2':mq2,'MQ3':mq3,'MQ135':mq135,'Temp':temp,'Humid':humid,'Count':count},))
      else:
        thread.start_new_thread(dweepy.dweet_for('near',{'MQ2':mq2,'MQ3':mq3,'MQ135':mq135,'Count':count},))
      time.sleep(3)
  except(KeyboardInterrupt,SystemExit):
    print 'Cleaning processes'
    sys.exit()
  finally:
    sys.exit()

thread.start_new_thread(sensor_read,())

print 'Running...'
print 'See output at freeboard.io/board/bJzXov'
print 'NOTE: To stop program use CTRL+C'

############# Template Matching #############
def template_match(r,face):
    global img
    cv2.imwrite('1.png',face)
    print "Matching with Template"
    #img1 = cv2.imread(str(r) + ".png")
    W,H=img.shape[:2]
    w,h = face.shape[:2]
    res = cv2.matchTemplate(img,face,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    a1 = W*H
    a2= (bottom_right[1]-top_left[1])*(bottom_right[0]-top_left[0])
    if(max_val>0.65 and ((max_loc[0]>=0 and max_loc[0]<=10 and max_loc[1]>=0 and max_loc[1]<=10) or (max_loc[0]>=230 and max_loc[0]<=250 and max_loc[1]>=0 and max_loc[1]<=10) or (max_loc[0]>=0 and max_loc[0]<=10 and max_loc[1]>=230 and max_loc[1]<=250) or (max_loc[0]>=230 and max_loc[0]<=250 and max_loc[1]>=230 and max_loc[1]<=250))):
        print 'Welcome, Door is now Open'
    else:
        print "No Match Found"

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

detected = 0
############# Motion Detection #############
while capture:
    anded = diffImg(prevFrame,frame,nextFrame)
    
    height, width= anded.shape
    for i in range(0, height):
        for j in range(0,width):
            v = anded[i,j]
            if v>100:
                print "Motion Detected"
                detected = 1
                break
        if detected==1:
            break
    ############# Face Detection #############
    if detected==1:
        faces1 = face_cascade1.detectMultiScale(f, 1.1, 7)
        faces2 = face_cascade2.detectMultiScale(f, 1.1, 7)
        
        crop_img=0
        for (x,y,w,h) in faces1:
            print "In face1"
            crop_img = f[y:y+h, x:x+w]
            crop_img= cv2.resize(crop_img,(240,240), interpolation = cv2.INTER_CUBIC)
            human_faces1.append(crop_img)
        for (x,y,w,h) in faces2:
            print "In face2"
            crop_img = f[y:y+h, x:x+w] 
            crop_img= cv2.resize(crop_img,(240,240), interpolation = cv2.INTER_CUBIC)
            human_faces2.append(crop_img)               
            
        
        for face in human_faces1:
            #cv2.imwrite(str(r) + '.png',face)
            thread.start_new_thread(template_match,(r,face,))
            r=r+1
        
        for face in human_faces2:
            #cv2.imwrite(str(s) + '.png',face)
            s=s+1

        del human_faces1[:]
        del human_faces2[:]

        time.sleep(2)
    else:
        print "Not detected"
    
    if detected==1:
        ret,pf = cap.read()
        ret1,f = cap.read()
        ret2,nf = cap.read()
        prevFrame = cv2.cvtColor(pf,cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
        nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
    else:
        prevFrame = frame
        frame = nextFrame
        f=nf
        ret2,nf = cap.read()
        nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
    detected = 0
cap.release()
cv2.destroyAllWindows()
