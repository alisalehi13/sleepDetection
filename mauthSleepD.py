'''
This madoule detect the mauth and calculate mauth aspect ratio

in this madoule mediapipe and dlib libraries used for face detection and mauth landmark detection

author:ALI Salehi.D

date:2022
'''


import cv2 as cv
import mediapipe as mp
import time
import math
from math import  hypot as hp
from matplotlib import pyplot as plt
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib





MAUTHM=[78,191,95,80,88,81,178,82,87,13,14,312,317,311,402,310,318,415,324,308]#mauth landmark for mediapipe library
  
class mediaPipeMAUTHDe():
    '''
    ========================================================================
   |       mediapipe base mauthdetector class .This class detect              |
   |       the person face and with mauth landmarks and calculate             |
   |                    mauth aspect ration value                             |
   |                                                                          |
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
        # self.faceMeshh=self.mpFaceMesh.FaceMesh(self.staticMode,self.maxFaces,self.minDetectionCon,self.minTrackCon)
        self.faceMeshh=self.mpFaceMesh.FaceMesh()
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1,circle_radius=2)
        self.MAR="undifined"



    def MAUTHMesh(self,img,draw=True):
        '''
        MAUTHMesh method gives an image as input and 
        detect mauth if exist and calculate the Mar
        
        '''
        self.imgRGB=cv.cvtColor(img,cv.COLOR_RGB2BGR)#bgr image to rgb for mediapipe input
        self.result=self.faceMeshh.process(self.imgRGB)
        
        
        if self.result.multi_face_landmarks:#check that if any faces detec
            for faceLms in self.result.multi_face_landmarks:
                mauth=list(enumerate(faceLms.landmark))
                
                if len(mauth) !=0:#if draw input is true this pease of code draw the eye landmarks 
                    if draw:
                    
                        for id in MAUTHM:
                            ih,iw,ic=img.shape
                            x,y=int(iw*mauth[id][1].x),int(ih*mauth[id][1].y)
                            cv.circle(img,(x,y),1,(0,255,0),-1)
                    
                    ih,iw=img.shape[:2]
                    self.MAR=(hp(int(iw*mauth[81][1].x)- int(iw*mauth[178][1].x), int(ih*mauth[81][1].y) - int(ih*mauth[178][1].y))+hp(int(iw*mauth[311][1].x) - int(iw*mauth[402][1].x), int(ih*mauth[311][1].y) - int(ih*mauth[402][1].y)))/(hp(int(iw*mauth[78][1].x) - int(iw*mauth[308][1].x), int(ih*mauth[78][1].y) - int(ih*mauth[308][1].y))*2)
                
        else:
            self.MAR="undifined"
        return img










# main function for the local running

def main():
    capture=cv.VideoCapture(0)

    mauth=mediaPipeMAUTHDe()
    # mauth=dlibMAUTHDe()
    # mauth=dlibMAUTHDe()
    while True:

        isOk,frame=capture.read()
        if isOk:
            frame=mauth.MAUTHMesh(frame)
            Mar=mauth.MAR
            # if mauth.EAR <0.25 :
            #    cv.rectangle(frame,(0,0),(frame.shape[1],frame.shape[0]),(0,0,255),3)


            frame=cv.flip(frame,1)
            cv.putText(frame,str(Mar),(0,20),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
            cv.imshow("frame",frame)

            


            # Ear.append(mauth.EAR)
            


            key=cv.waitKey(1)
            if key==ord('q'):
                break
            
            

    capture.release()
    cv.destroyAllWindows()


    # plt.plot(Ear)
    # plt.show()


if __name__=="__main__":
    main()