'''
This madoule detect the eye and calculate eye aspect ratio

in this madoule mediapipe and dlib libraries used for face detection and eye landmark detection

author:ALI Salehi.D

date:2022
'''

#imprtation necessary packages

import cv2 as cv
import mediapipe as mp
from math import  hypot as hp
from matplotlib import pyplot as plt
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import time
import HE


# ===========================mediapipe eyedetector class  ========================================


LEFT_EYE =[ 362,385,387,263,373,380]#left eye landmarks number in mediapipe library
RIGHT_EYE=[ 33,160,158,133,153,144 ]#ritht eye landmarks number in mediapipe librayr


class mediaPipeEyeDe():
    '''
    ========================================================================
   |       mediapipe base eyedetector class .This class detect              |
   |       the person face and with eye landmarks and calculate             |
   |                    eye aspect ration value                             |
   |                                                                        |
    ========================================================================
    '''

    def __init__(self,staticMode=False,maxFaces=1,minDetectionCon=0.5,minTrackCon=0.5):
        
        self.staticMode=staticMode
        self.maxFaces=maxFaces
        self.minDetectionCon=minDetectionCon
        self.minTrackCon=minTrackCon

        #creating object of mediapipe library
        
        self.mpDraw=mp.solutions.drawing_utils
        self.mpFaceMesh=mp.solutions.face_mesh
        #self.faceMeshh=self.mpFaceMesh.FaceMesh(self.staticMode,self.maxFaces,self.minDetectionCon,self.minTrackCon)
        self.faceMeshh=self.mpFaceMesh.FaceMesh()
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1,circle_radius=2)
        self.EAR='undifined'



    def eyeMesh(self,img,draw=True):
        '''
        eyeMesh method give an image as input and 
        detect eyes if exist and calculate the Ear
        
        '''
        
        
        self.imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)#bgr image to rgb for mediapipe input
        self.result=self.faceMeshh.process(self.imgRGB)
        faces=[]



        if self.result.multi_face_landmarks:#check that if any faces detec
            for faceLms in self.result.multi_face_landmarks:
                
                
                
                if draw:#if draw input is true this pease of code draw the eye landmarks 
                    eyes=list(enumerate(faceLms.landmark))
                    for id in LEFT_EYE+RIGHT_EYE:
                        ih,iw,ic=img.shape
                        x,y=int(iw*eyes[id][1].x),int(ih*eyes[id][1].y)
                        cv.circle(img,(x,y),1,(0,255,0),-1)
                        
                        
                        
                
                ih,iw=img.shape[:2]
                self.EAR=(hp(int(iw*eyes[160][1].x)- int(iw*eyes[144][1].x), int(ih*eyes[160][1].y) - int(ih*eyes[144][1].y))+hp(int(iw*eyes[158][1].x) - int(iw*eyes[153][1].x), int(ih*eyes[158][1].y) - int(ih*eyes[153][1].y)))/(hp(int(iw*eyes[133][1].x) - int(iw*eyes[33][1].x), int(ih*eyes[33][1].y) - int(ih*eyes[133][1].y))*4)
                self.EAR+=(hp(int(iw*eyes[385][1].x)- int(iw*eyes[373][1].x), int(ih*eyes[385][1].y) - int(ih*eyes[373][1].y))+hp(int(iw*eyes[387][1].x) - int(iw*eyes[380][1].x), int(ih*eyes[380][1].y) - int(ih*eyes[387][1].y)))/(hp(int(iw*eyes[362][1].x) - int(iw*eyes[263][1].x), int(ih*eyes[362][1].y) - int(ih*eyes[263][1].y))*4)
        else:
            self.EAR='undifined'
        return img























# main function for the local running

def main():
    capture=cv.VideoCapture(0)

    eye=mediaPipeEyeDe()
    Ear=[]
    # eye=dlibEyeDe()
    while True:

        isOk,frame=capture.read()
        if isOk:
            frame=HE.histogram_equalization(frame)
            # frame=HE.hist_equ(frame)            
            frame=eye.eyeMesh(frame)
            EAR1=eye.EAR
            if EAR1!="undifined":
               #51 21 17
                if  EAR1<0.326 :
                    cv.rectangle(frame,(0,0),(frame.shape[1],frame.shape[0]),(0,0,255),3)
                Ear.append(eye.EAR)
            frame=cv.flip(frame,1)
            cv.imshow("frame",frame)
            key=cv.waitKey(1)
            if key==ord('q'):
                break
    capture.release()
    cv.destroyAllWindows()
    plt.plot(Ear)
    plt.show()


if __name__=="__main__":
    main()