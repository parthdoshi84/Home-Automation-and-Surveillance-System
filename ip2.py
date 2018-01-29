import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_eye.xml')
capture =True
cap =cv2.VideoCapture(0)
ret,pf = cap.read()
ret1,f = cap.read()
ret2,nf = cap.read()
prevFrame = cv2.cvtColor(pf,cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
faces = []
multiple_eyes = []
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
                faces = face_cascade.detectMultiScale(f, 1.3, 5)
                for (x,y,w,h) in faces:
                    print "In face"
                    crop_img = f[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(crop_img)
                    for (ex,ey,ew,eh) in eyes:
                        eye = crop_img[ey:ey+eh,ex:ex+ew]
                        multiple_eyes.append(eye)
                        if(len(eye)==3):
                            eye_anded = diffImg(multiple_eyes[0],multiple_eyes[1],multiple_eyes[2])
                            height, width= anded.shape
                            for i in range(0, height):
                                for j in range(0,width):
                                    v = anded[i,j]
                                    if v>100:
                                        print "Blinked"
                                        detected = 1
                                        break
            
        
    
    print "Not detected"
    cv2.imshow("Frame",anded)
    prevFrame = frame
    frame = nextFrame
    f=nf
    ret2,nf = cap.read()
    
    nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
    key = cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
