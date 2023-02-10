'''
The main part of project .this script use module to 
detect drowsiness and alarming to driver.


author:Ali Salehi.D
date:2022
'''
import cv2 as cv
import numpy as np
import mauthSleepD
import eyeSleepD
import headpose
import time
import alarm
import personfacerecogniser
import personeyeration
import HE
import sys





def sleepfinder(EarTreshold):
    eye=eyeSleepD.mediaPipeEyeDe()#object of eyeSleepD module 
    mauth=mauthSleepD.mediaPipeMAUTHDe()#object of mauthSleepD module 
    head=headpose.HeadPose()#object of headpose module
    alr=alarm.Alarm()
    pos=True
    poseTime=[]
    Stime=[]
    Ltime=[]
    eyeTreshold=0.31
    timeTreshold=0.7
    Martreshold=0.25
    yawNumber=0
    lookTreshold=2
    eyeClose=0
    eyeClosebool=True
    eyeCloseTreash=3
    yaw=[0,0]
    situationTresh=1
    eyeTresholds=None
    Ptime=[]
    capture=cv.VideoCapture(0)
    while True:
        isOk,frame=capture.read()
        if isOk:

            
            #calling methods
            frame=HE.histogram_equalization(frame)
            img1=eye.eyeMesh(frame.copy())
            img2=mauth.MAUTHMesh(frame.copy())
            posDirection=head.hpos(frame.copy())
            
            if eyeClose>=eyeCloseTreash:
                alr.vioceAlarm("./alarmvoiceandmusics/Sleepy.mp3")
                eyeClose=0
            #todo
            
            if posDirection=="Forward":
                Ear=eye.EAR
                Mar=mauth.MAR
                #checking for Yawing
                if Mar!="undifined":
                    yaw[1]=Mar
                    if  yaw[1]>Martreshold and yaw[0]<Martreshold:
                        yawNumber+=1
                    yaw[0]=Mar
                    
                if Ear!="undifined":
                    #checking the eye aspect ratio and time of closness of eyes
                    if  Ear<eyeTreshold:
                        Stime.append(time.time())
                        if Stime[-1]-Stime[0]>timeTreshold:
                            alr.vioceAlarm("./alarmvoiceandmusics/alarm.mp3")
                            
                            
                            #this pease cont the number of eyeclose period
                            if eyeClosebool:
                                eyeClose+=1
                            cv.rectangle(frame,(0,0),(frame.shape[1]-1,frame.shape[0]-1),(0,0,255),1)
                            eyeClosebool=False
                    
                    if Ear>eyeTreshold:
                        eyeClosebool=True
                        Stime=[]                    
                        

                Ptime=[]
                    
            elif posDirection=="Looking Right" or posDirection=="Looking Left" or posDirection=="Looking Up" or posDirection=="Looking Down":
                Ptime.append(time.time())
                if Ptime[-1]-Ptime[0]>lookTreshold:
                    alr.vioceAlarm("./alarmvoiceandmusics/LookForward.mp3")

            if Ear=="undifined" or posDirection=="undifined":
                poseTime.append(time.time())
                if poseTime[-1]-poseTime[0]>situationTresh:
                    alr.vioceAlarm("./alarmvoiceandmusics/situation.mp3")
                    poseTime=[]
                    
                

            
        #     cv.imshow('frame',frame)
        # if cv.waitKey(1) & 0xFF==ord('q'):
        #     break

    cv.destroyAllWindows()
    capture.release()








