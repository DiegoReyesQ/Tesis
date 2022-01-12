import cv2
import numpy as np
import serial
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

port = serial.Serial("/dev/ttyAMA0", baudrate=9600)
cap = cv2.VideoCapture(0)
img_ref = cv2.imread('John_Symbol.jpg',0)  
#img_ref = [320,320]
img_ref = cv2.resize(img_ref,(320,320))
#print "Size of reference =",img_ref.shape
widht,height = [640,480]
maxW=widht/2
maxH=height/2
rect = np.zeros((4,2),dtype="float32")
dst = np.array([[0,0],[maxW-1,0],[maxW-1,maxH-1],[0,maxH-1]],dtype="float32")
a = ["'","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9"]
b = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s"]

def perspective(image,pts):
    s = pts.sum(axis=1) 
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts,axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    M = cv2.getPerspectiveTransform(rect,dst)
    warped = cv2.warpPerspective(image,M,(maxW,maxH))
    warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(warped)
    threshold = (min_val+max_val)/2
    ret,warped= cv2.threshold(warped,threshold,255,cv2.THRESH_BINARY)
    return warped

        

while(1):
    ret,frame = cap.read()
    GPIO.setup(4,GPIO.OUT)
    GPIO.output(4,GPIO.LOW)

#FILTRADO***********************************************************
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Canny(blur,127,255)

#CONTORNOS**********************************************************
    contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   #contours = sorted(contours,key=cv2.contourArea,reverse=True)
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            moments = cv2.moments(area)
            if area > 5300 and area < 30000:
                #cv2.drawContours(frame,[cnt],0,(0,255,0),2)
                #print area
                warped = perspective(frame,approx.reshape(4,2))
                warped = cv2.resize(warped,(320,320))
                #cv2.imshow("Correccion",warped)
                diffImg = cv2.bitwise_xor(warped,img_ref)
                diff = cv2.countNonZero(diffImg)
                if diff < 32000:    #John < 32000, John Paul < 36000, Robert < 32000
                    GPIO.output(4,GPIO.HIGH)
                    x,y,w,h = cv2.boundingRect(cnt)
                    #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                    mov = int((area-30000)/1300)*-1   #mov 0 -> 18
                    cx = int(moments['m10']/moments['m00'])
                    cx = (x/27)  #mov 0 -> 18
                    print "av-rev =",a[mov]
                    port.write(str(a[mov]))
                    print "izq-der =",b[cx]
                    port.write(str(b[cx]))
                    #cv2.imshow("Mascara",diffImg)
                else:
                    #print "No image to match..."
                    print "av-rev =",a[9]
                    port.write(str(a[9]))
                    print "izq-der =",b[9]
                    port.write(str(b[9]))
                    
    cv2.imshow("Original",frame) 
    #cv2.imshow("Referencia",img_ref)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print "*****PROCESSING STOPPED*****"
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()

