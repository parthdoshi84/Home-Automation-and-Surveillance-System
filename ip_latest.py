
import cv2

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
        faces1 = face_cascade1.detectMultiScale(f, 1.1, 7)
        faces2 = face_cascade2.detectMultiScale(f, 1.1, 7)
        print "detected"
        
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
            
        r=61
        for face in human_faces1:
            
            cv2.imwrite(str(r) + '.png',face)
            r=r+1
        r=71
        for face in human_faces2:
            cv2.imwrite(str(r) + '.png',face)
            r=r+1
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


