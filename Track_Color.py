import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while(1):
    ret,img = cap.read()
    #img = [640,480]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    greenlow = np.array([49,50,50],dtype=np.uint8)
    greenhigh = np.array([80,255,255],dtype=np.uint8)
    mask = cv2.inRange(hsv,greenlow,greenhigh)
    #mask = cv2.erode(mask,None,iterations=2)
    #mask = cv2.dilate(mask,None,iterations=2)
    
    moments = cv2.moments(mask)
    area = moments['m00']
    i = 4
    #print area

    if(area > 2000):
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
        cv2.rectangle(img, (x-5,y-5),(x+5,y+5),(255,0,0),2)
        cv2.putText(img,"pos:"+str(x)+","+str(y),(x+10,y+10), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        x = (x-320)/15
        print ("x=",x)

    cv2.imshow("Mask",mask)
    cv2.imshow("Track",img) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print ("***PROCESSING STOPPED***")
        cv2.destroyAllWindows()
        break
cap.release()
        
