import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
ret,frame = cap.read()
img = cv2.imread("simbolo.jpg",0)
cv2.imshow('Original',img)
img = cv2.resize(img,(100,100))
w,h = img.shape[::-1]
x,y = 0,0



#cv2.rectangle(frame,[220,180],[280,420], (0, 255, 0),1)

while(True):
        ret, frame = cap.read()
        #frame = [640,480]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray,img,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        x = (top_left[0] + bottom_right[0])/2
        y = (top_left[1] + bottom_right[1])/2
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0),1)
        #cv2.putText(frame,"x ="+ str(x), (bottom_right[0]+10,bottom_right[1]+10), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2)
        cv2.putText(frame, "["+ str(x)+","+str(y)+"]", (bottom_right[0]+10,bottom_right[1]+10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), 1)
        print 'x=',x
        
        cv2.imshow('MATCH',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                print "***PROCESSING STOPPED***"
                break

cap.Release()
cv2.destroyAllWindows()
