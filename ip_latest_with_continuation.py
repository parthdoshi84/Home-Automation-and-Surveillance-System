
import cv2
import time
import numpy as np
import math

face_cascade1 = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_alt2.xml')
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

def template_match(r):
    img = cv2.imread("Parth Collection.png")
    img1 = cv2.imread(str(r) + ".png")
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
        print max_val
    else:
        print "mismatch"
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    cv2.imshow('Image',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print max_val


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

detected = 0
while capture:
    anded = diffImg(prevFrame,frame,nextFrame)
    
    height, width= anded.shape
    for i in range(0, height):
        for j in range(0,width):
            v = anded[i,j]
            if v>100:
                print "Motion Detected"
                detected= 1
                break
            if detected==1:
                break
    if detected==1:
        faces1 = face_cascade1.detectMultiScale(f, 1.1, 7)
        faces2 = face_cascade2.detectMultiScale(f, 1.1, 7)
        
        crop_img=0
        for (x,y,w,h) in faces1:
            print "In face"
            crop_img = f[y:y+h, x:x+w]
            crop_img= cv2.resize(crop_img,(240,240), interpolation = cv2.INTER_CUBIC)
            human_faces1.append(crop_img)
        for (x,y,w,h) in faces2:
            print "In face"
            crop_img = f[y:y+h, x:x+w] 
            crop_img= cv2.resize(crop_img,(240,240), interpolation = cv2.INTER_CUBIC)
            human_faces2.append(crop_img)               
            
        
        for face in human_faces1:
            cv2.imwrite(str(r) + '.png',face)
            template_match(r)
            r=r+1
        
        for face in human_faces2:
            cv2.imwrite(str(s) + '.png',face)
            s=s+1

        del human_faces1[:]
        del human_faces2[:]

        time.sleep(10)

        
                    
    else:
        print "Not detected"
    cv2.imshow("Frame",anded)
    prevFrame = frame
    frame = nextFrame
    f=nf
    ret2,nf = cap.read()
    nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
    if detected==1:
        ret,pf = cap.read()
        ret1,f = cap.read()
        ret2,nf = cap.read()
        prevFrame = cv2.cvtColor(pf,cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
        nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
    detected =0
    key = cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


