import cv2
import mediapipe as mp
import time
import keyboard 
import autopy
import numpy as np
import mouse

def fingerupordownthumb(firstpoint,secondpoint):
    if(firstpoint[1]>secondpoint[1]):
        return True
    else:
        return False


def fingerupordown(firstpoint,secondpoint):
    if(firstpoint[2]>secondpoint[2]):
        return True
    else:
        return False

mphands=mp.solutions.hands
hands=mphands.Hands(min_detection_confidence=0.6,
    min_tracking_confidence=0.6,)
mpdraw=mp.solutions.drawing_utils

screenshot=False

cap=cv2.VideoCapture(0)
writer=cv2.VideoWriter("file.avi",cv2.VideoWriter_fourcc(*'MJPG'),
                         25, (640,480))
ctime=ptime=0
ix=0
iy=0
cposx=cposy=pposx=pposy=0
scrnw,scrnh=autopy.screen.size()
clickedorno=False

while(True):
    listoflandmarks=[]
    ret,frame=cap.read()
    imgrgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.rectangle(frame,(100,100),(540,380),(255,255,255),2,1)
    results=hands.process(imgrgb)
    h,w,_=frame.shape
    #check for multiple hands
    if(results.multi_hand_landmarks):
        for handcount,indivdual_hand in enumerate(results.multi_hand_landmarks):
           
            for ids,lm in enumerate(indivdual_hand.landmark):
            
                cx,cy=int(lm.x*w),int(lm.y*h)
                listoflandmarks.append([ids,cx,cy])
               # if(ids==8 or ids==12):
                   
                   # cv2.circle(frame,(cx,cy),20,(255,0,0),-1)
            mpdraw.draw_landmarks(frame,indivdual_hand,mphands.HAND_CONNECTIONS)
    
    #fps Calculation
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    

    if(len(listoflandmarks)!=0):    
        
        if( len(results.multi_hand_landmarks)==1 and
           fingerupordown(listoflandmarks[8],listoflandmarks[6]) and
           clickedorno==False and fingerupordown(listoflandmarks[12],listoflandmarks[10])):
            autopy.mouse.click()
            clickedorno=True            
        if(not fingerupordown(listoflandmarks[8],listoflandmarks[6]) and not fingerupordown(listoflandmarks[12],listoflandmarks[10]) ):
            clickedorno=False
   

        ix=listoflandmarks[8][1]
        iy=listoflandmarks[8][2]
        x1=np.interp(ix,(100,540),(0,scrnw))
        y1=np.interp(iy,(100,380),(0,scrnh))
        cposx=pposx+(x1-pposx)/5
        cposy=pposy+(y1-pposy)/5
        if(fingerupordown(listoflandmarks[12],listoflandmarks[10]) and len(results.multi_hand_landmarks)==1):
            try:
                    cv2.circle(frame,(ix,iy),20,(0,255,0),-1)
                    cv2.putText(frame,"Mouse Move Mode",(10,80),1,1,(255,0,0),2)
                    autopy.mouse.move(scrnw-cposx,cposy)
            except:
                    pass
        
        
        
        if(not fingerupordown(listoflandmarks[12],listoflandmarks[10])
           and not fingerupordown(listoflandmarks[16],listoflandmarks[14])
           and fingerupordownthumb(listoflandmarks[4],listoflandmarks[2])
           and    fingerupordown(listoflandmarks[20],listoflandmarks[18])):
            cv2.putText(frame,"Scroll Mode",(10,80),1,1,(255,0,0),2)
            mouse.wheel(-1)
        elif(not fingerupordown(listoflandmarks[12],listoflandmarks[10])
             and not fingerupordown(listoflandmarks[16],listoflandmarks[14])
             and not fingerupordownthumb(listoflandmarks[4],listoflandmarks[2]) 
             and   fingerupordown(listoflandmarks[20],listoflandmarks[18]) ):
            cv2.putText(frame,"Scroll Mode",(10,80),1,1,(255,0,0),2)
            mouse.wheel(1)
            
       
            
        if(screenshot==False and 
           fingerupordown(listoflandmarks[8],listoflandmarks[5]) and
           fingerupordown(listoflandmarks[12],listoflandmarks[9])and 
           fingerupordown(listoflandmarks[16],listoflandmarks[13]) and
           fingerupordown(listoflandmarks[20],listoflandmarks[17])):
                screenshot=True
                keyboard.send("windows+PrtScn")
                print("Screenshot Taken",screenshot)
                
        if(not fingerupordown(listoflandmarks[8],listoflandmarks[5]) and not fingerupordown(listoflandmarks[12],listoflandmarks[9])and  not fingerupordownthumb(listoflandmarks[16],listoflandmarks[13]) and  not fingerupordownthumb(listoflandmarks[20],listoflandmarks[17])):            
                screenshot=False
                
     
            
        
        pposx=cposx
        pposy=cposy
    writer.write(frame)
    cv2.putText(frame,str(int(fps)),(10,50),1,2,(255,0,0))
    cv2.imshow("Frame",cv2.resize(frame,(360,280)))
    k=cv2.waitKey(1)
    if(k==ord('q')):
        break
cap.release()
writer.release()
cv2.destroyAllWindows()