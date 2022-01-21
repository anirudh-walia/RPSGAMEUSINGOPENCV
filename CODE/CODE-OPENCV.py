import cv2
import numpy as np
import math
import random
cap = cv2.VideoCapture(0)
import time  

def game():  
    cv2.putText(frame,'READY',(220,200), font, 2, (0,0,255), 3, cv2.LINE_AA)
    go_list = ['GO!', 'GO!!', 'GO!!!','GO!!!!',]
    go_item = random.choice(go_list)
    cv2.putText(frame,go_item,(223,250),font,2,(0,0,255),3,cv2.LINE_AA)
    ges_list = ['STONE', 'SCISSORS', 'PAPER']
    ges_item = random.choice(ges_list)
    cv2.putText(frame,ges_item,(480,50),font,1,(0,0,255),3,cv2.LINE_AA)
    
while(1):
        
    try:  
          
        ret,frame=cap.read()
        frame=cv2.flip(frame,1)
        kernel=np.ones((3,3),np.uint8)
        roi=frame[100:300, 100:300]
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)
        
        hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        lower_skin=np.array([0,10,60], dtype=np.uint8)
        upper_skin=np.array([20,150,255], dtype=np.uint8)
        mask = cv2.inRange(hsv,lower_skin,upper_skin)      
        mask=cv2.dilate(mask,kernel,iterations=5)
        mask=cv2.GaussianBlur(mask,(5,5),100) 
        
        hand_contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=max(hand_contours,key=lambda x: cv2.contourArea(x))
        epsilon=0.0005*cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,epsilon,True)
       
        hull = cv2.convexHull(cnt)
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
        arearatio=((areahull-areacnt)/areacnt)*100
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
        x=0
        
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start=tuple(approx[s][0])
            end=tuple(approx[e][0])
            far=tuple(approx[f][0])
            pt=(100,180)
            
            
            a = math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)
            b = math.sqrt((far[0]-start[0])**2 + (far[1]-start[1])**2)
            c = math.sqrt((end[0]-far[0])**2 + (end[1]-far[1])**2)
            s = (a+b+c)/2
            area_tri = math.sqrt(s*(s-a)*(s-b)*(s-c))
            d=(2*area_tri)/a
            angle=math.acos((b**2+c**2-a**2)/(2*b*c))*57
            
            if angle <= 90 and d>30:
                x += 1
                cv2.circle(roi, far, 3, [255,0,0], -1)
            cv2.line(roi,start, end, [0,255,0], 2)
    
        x+=1
        font = cv2.FONT_HERSHEY_SIMPLEX
        if x==1:
            if areacnt<2000:
                cv2.putText(frame,'REPOSITION PLEASE!!!',(100,50), font, 1, (0,215,255), 3, cv2.LINE_AA)
            else:
                if arearatio<12:
                    cv2.putText(frame,'STONE',(10,50), font, 1, (0,0,255), 3, cv2.LINE_AA)


        elif x==2:
            cv2.putText(frame,'SCISSORS',(10,50), font, 1, (0,255,0), 3, cv2.LINE_AA)
            
        elif x==3:
         
              if arearatio<27:
                    cv2.putText(frame,'SCISSORS',(10,50), font, 1, (0,255,0), 3, cv2.LINE_AA)
              else:
                    cv2.putText(frame,'SCISSORS',(10,50), font, 1, (0,255,0), 3, cv2.LINE_AA)
                    
        elif x==4:
            cv2.putText(frame,'PAPER',(10,50), font, 1, (255,0,0), 3, cv2.LINE_AA)
            
        elif x==5:
            cv2.putText(frame,'PAPER',(10,50), font, 1, (255,0,0), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'Reposition',(10,50), font, 1, (0,0,0), 3, cv2.LINE_AA)
      
        game()
        
        cv2.imshow('MASK',mask)
        cv2.imshow('GAME',frame)
        
    except:
        pass
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    
cv2.destroyAllWindows()
cap.release()    