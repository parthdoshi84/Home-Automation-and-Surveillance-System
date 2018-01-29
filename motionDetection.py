import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('C://Users/Admin/Downloads/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml')
capture =True
cap =cv2.VideoCapture(0)
ret,pf = cap.read()
ret1,f = cap.read()
ret2,nf = cap.read()
prevFrame = cv2.cvtColor(pf,cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
nextFrame = cv2.cvtColor(nf,cv2.COLOR_BGR2GRAY)
faces = []
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
        if detected == 1:
            break
    if detected==1:
        faces = face_cascade.detectMultiScale(f, 1.3, 5)
        print "detected"
        for (x,y,w,h) in faces:
            print "In face"
            cv2.imshow('img',f)
            crop_img = f[y:y+h, x:x+w] 
            cv2.imshow("cropped", crop_img)
                       
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
        cv2.imwrite('4.png',crop_img)
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

'''cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''
