import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFormLayout, QLabel, QVBoxLayout,QGroupBox,QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2 as cv
import wrfile
from functools import partial
import codriver
import alarm
# 
import numpy as np
import mauthSleepD
import eyeSleepD
import headpose
import time
import alarm
import personfacerecogniser
import personeyeration
import HE
import time
# 



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
height=800
width=1200
namelist=wrfile.read()
ystime=[]
yawTH=15

class hello(QDialog):
    def __init__(self):
        super(hello,self).__init__()
        loadUi("hellow.ui",self)
        self.have_ac.clicked.connect(self.account)
        self.guest.clicked.connect(self.gst)
        self.new_ac.clicked.connect(self.newAc)
        
        
        
    def account(self):
        acc=choosAcc()
        widget.addWidget(acc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gst(self):
        sh=show(mode=0,uname="guest")
        widget.addWidget(sh)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def newAc(self):
        new=createAcc()
        widget.addWidget(new)
        widget.setCurrentIndex(widget.currentIndex()+1)    
        

#========================================================================================================





class View(QDialog):
    def __init__(self,EarT):
        super().__init__()
        loadUi("dview.ui",self)
        self.Back.clicked.connect(self.backF)
        self.EarT=EarT
        self.Worker=mainWorker(self.EarT)
        self.Worker.start()
        self.Worker.dataupdate.connect(self.update)
        self.eN=[]
        
        
        
    
    def backF(self):#todo hello
        self.Worker.stop()
        hi=hello()
        widget.addWidget(hi)
        widget.setCurrentIndex(widget.currentIndex()+1)  
        
    def update(self,S,S_1,yaw,ey):
        if S:
            if S_1:
                pixmap = QPixmap('./picture/26a0.png')
                self.label.setPixmap(pixmap)
            else:
                self.label.clear()
        else:
            pixmap = QPixmap('./picture/Coffee_icon.webp')
            self.label_2.setPixmap(pixmap)
            self.eN.append([yaw,ey,time.time()])
            if len(self.eN)>=2:
                if self.eN[-1][-1]-self.eN[-2][-1]>1800:
                    self.label_2.clear()
            
        
        
        



class mainWorker(QThread):#guest driver
    dataupdate=pyqtSignal(bool,bool,float,int)
    def __init__(self,ET):
        self.ET=ET
        super().__init__()
        
    def run(self):
        eye=eyeSleepD.mediaPipeEyeDe()#object of eyeSleepD module 
        mauth=mauthSleepD.mediaPipeMAUTHDe()#object of mauthSleepD module 
        head=headpose.HeadPose()#object of headpose module
        alr=alarm.Alarm()
        pos=True
        self.ThreadActive=True
        poseTime=[]
        Stime=[]
        Ltime=[]
        eyeTreshold=self.ET
        timeTreshold=0.7
        Martreshold=0.25
        yawNumber=0
        lookTreshold=2
        eyeClose=0
        eyeClosebool=True
        eyeCloseTreash=2
        yaw=[0,0]
        situationTresh=1
        eyeTresholds=None
        Ptime=[]
        
        
        
        capture=cv.VideoCapture(0)
        while self.ThreadActive:
            isOk,frame=capture.read()
            if isOk:

            
            #calling methods
                frame=HE.histogram_equalization(frame)
                img1=eye.eyeMesh(frame.copy())
                img2=mauth.MAUTHMesh(frame.copy())
                posDirection=head.hpos(frame.copy())
            
                if eyeClose>=eyeCloseTreash:
                    self.dataupdate.emit(False,False,yawNumber,eyeClose)#todo
                    alarm.pyalr(r'C:\Users\alisa\OneDrive\Desktop\ml\project\alarmvoiceandmusics\Sleepy.mp3')#todo emit
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
                        if yawNumber>yawTH:
                            # ystime.append(time.time())
                            self.dataupdate.emit(False,True,yawNumber,eyeClose)
                            # if ystime[-1]-ystime[-2]>1800:
                            #     ystime=[]
                            
                    
                    if Ear!="undifined":
                    #checking the eye aspect ratio and time of closness of eyes
                        if  Ear<eyeTreshold:
                            Stime.append(time.time())
                            if Stime[-1]-Stime[0]>timeTreshold:
                                self.dataupdate.emit(True,True,yawNumber,eyeClose)
                                
                                alarm.pyalr(r"C:\Users\alisa\OneDrive\Desktop\ml\project\alarmvoiceandmusics\alarm.mp3")
                            
                            
                                #this pease cont the number of eyeclose period
                                if eyeClosebool:
                                    eyeClose+=1
                                cv.rectangle(frame,(0,0),(frame.shape[1]-1,frame.shape[0]-1),(0,0,255),1)
                                eyeClosebool=False
                    
                        if Ear>eyeTreshold:
                            self.dataupdate.emit(True,False,yawNumber,eyeClose)
                            eyeClosebool=True
                            Stime=[]                    
                        

                    Ptime=[]
                    
                elif posDirection=="Looking Right" or posDirection=="Looking Left" or posDirection=="Looking Up" or posDirection=="Looking Down":
                    Ptime.append(time.time())
                    if Ptime[-1]-Ptime[0]>lookTreshold:
                        alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\alarmvoiceandmusics\LookForward.mp3")

                if Ear=="undifined" or posDirection=="undifined":
                    poseTime.append(time.time())
                    if poseTime[-1]-poseTime[0]>situationTresh:
                        alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\alarmvoiceandmusics\situation.mp3")
                        poseTime=[]
        
            
    def stop(self):
        self.ThreadActive=False
        self.quit()





  #================================================================================================      
        
        
class choosAcc(QDialog):
    def __init__(self):
        super(choosAcc,self).__init__()
        loadUi("choose_acc.ui",self)
        formlayot=QFormLayout()
        bot_list=[]
        namelist=wrfile.read()
        groupbox=QGroupBox()
        
        for i in range(len(namelist)):
            bot_list.append(0)
            bot_list[i]=Bott()
            bb=bot_list[i].bot()
            bb.setText(namelist[i])
            formlayot.addRow(bb)
        groupbox.setLayout(formlayot)
        self.list_d.setWidget(groupbox)
        for i in range(len(namelist)):
            bot_list[i].bot().clicked.connect(partial(self.name,namelist[i]))
        
        self.back_1.clicked.connect(self.back)
    
        
        
    
        
        
    def back(self):
        hi=hello()
        widget.addWidget(hi)
        widget.setCurrentIndex(widget.currentIndex()+1)    
        
            
    def name(self,name):
        vie=View(float(wrfile.read_ear(name=name)))
        widget.addWidget(vie)
        widget.setCurrentIndex(widget.currentIndex()+1)  
                
#=======================================================================================


class createAcc(QDialog):
    def __init__(self):
        super(createAcc,self).__init__()
        loadUi("create_account.ui",self)
        self.back.clicked.connect(self.backh)
        self.enter.clicked.connect(self.Enter)
        
        
        
        
        
    def Enter(self):
        uname=self.name.text()
        uname=uname.strip()
        if len(uname)==0:
            self.error_1.setText("Please Enter a valid username")
        elif uname in namelist:
            self.error_1.setText("Username exist")
        else:   
            sh=show(mode=1,uname=uname)
            widget.addWidget(sh)
            widget.setCurrentIndex(widget.currentIndex()+1)    
                
            
            
    def backh(self):
        hi=hello()
        widget.addWidget(hi)
        widget.setCurrentIndex(widget.currentIndex()+1)    
             
        
        
     
        
        
class Bott(QDialog):
    def __init__(self):
        super(Bott,self).__init__()
        loadUi("bottom.ui",self)
        
    def bot(self):
        return self.bott

        
  
class show(QDialog):
    def __init__(self,mode,uname):
        self.mode=mode
        self.uname=uname
        super().__init__()
        loadUi("show.ui",self)  
        
        
        self.VBL=QVBoxLayout()
        self.FeedLabel=self.label
        self.VBL.addWidget(self.FeedLabel)
        
        
        if mode==0:
            self.Worker1=Worker1(uname="guest")
            self.Worker1.start()
            self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot_1) 
            self.stop.clicked.connect(partial(self.close,self.Worker1))
            
        
        if mode==1:
            self.Worker2=Worker2(uname=self.uname)
            self.Worker2.start()
            self.Worker2.ImageUpdate_1.connect(self.ImageUpdateSlot_2)
            self.stop.clicked.connect(partial(self.close,self.Worker2))
           
            
    def close(self,Worker):
        if Worker.uname=="guest":
            Worker.stop()#todo ckeck that ear is true
            view=View()
            widget.addWidget(view)
            widget.setCurrentIndex(widget.currentIndex()+1)  
        else:
            Worker.stop()
            hi=hello()
            widget.addWidget(hi)
            widget.setCurrentIndex(widget.currentIndex()+1) 
            
        
        
    def ImageUpdateSlot_1(self,Image,E):
        if E:
            self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        else:
            eyT=self.Worker1.userEar
            self.Worker1.stop()
            vie=View(eyT)
            widget.addWidget(vie)
            widget.setCurrentIndex(widget.currentIndex()+1)  
            
            
            
    def ImageUpdateSlot_2(self,Image,E):
        if E:
            self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
        else:
            self.Worker2.stop()
            hi=hello()
            widget.addWidget(hi)
            widget.setCurrentIndex(widget.currentIndex()+1) 
            
     
        
        
        
      
class Worker1(QThread):#guest driver
    ImageUpdate=pyqtSignal(QImage,bool)
    def __init__(self,uname):
        super().__init__()
        self.uname=uname
    def run(self):
        ear=[]
        iTime=[]
        identifiTime=3
        beeb=0
        idmod=True
        eye=eyeSleepD.mediaPipeEyeDe()
        alr=alarm.Alarm()
        self.ThreadActive=True
        alr.vioceAlarm(r'C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\guest.mp3')#todo guest driver voice
        alr.vioceAlarm(r'C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\closeeye.mp3')
        capture=cv.VideoCapture(0)
            
        while self.ThreadActive and idmod:
            if beeb==0:
                alr.vioceAlarm(r'C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\alarm-police-fire-ambulance-etc-sound-effect-26-11504.mp3')
                beeb+=1
            ret, frame=capture.read()
            if ret:
                frame1=HE.histogram_equalization(frame.copy())
                frame1=eye.eyeMesh(frame1)#todo HE
                iTime.append(time.time())
                if eye.EAR!="undifined":
                    ear.append(eye.EAR)
                    
                if iTime[-1]-iTime[0]>identifiTime:
                    alr.vioceAlarm(r'C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\alarm-police-fire-ambulance-etc-sound-effect-26-11504.mp3')
                    idmod=False
                    Ear=np.array(ear)
                    self.userEar=np.mean(Ear)+(np.max(Ear)-np.min(Ear))/4
                    # self.userEar+=0.02
                    #todo check that number is float
                    #todo linking to the gif page
                Image=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
                FlippedImage=cv.flip(Image,1)
                ConvertToQtFormat=QImage(FlippedImage.data,FlippedImage.shape[1],FlippedImage.shape[0],QImage.Format_RGB888)
                Pic=ConvertToQtFormat.scaled(640,480,Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic,True)
                #todo    pass to the a page that illuminate the sleepy stage and showes the gif
        self.ImageUpdate.emit(Pic,False)    
    def stop(self):
        self.ThreadActive=False
        self.quit()  
        
        
        
        
        
        
                
class Worker2(QThread):#create new account
    def __init__(self,uname):
        super(Worker2,self).__init__()
        self.uname=uname
        
    ImageUpdate_1=pyqtSignal(QImage,bool)

    def run(self):
        ear=[]
        iTime=[]
        identifiTime=3
        beeb=0
        idmod=True
        eye=eyeSleepD.mediaPipeEyeDe()
        alr=alarm.Alarm()
        self.ThreadActive=True
        alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\newacc.mp3")
        alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\closeeye.mp3")
        capture=cv.VideoCapture(0)
            
        while self.ThreadActive and idmod:
            if beeb==0:
                alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\alarm-police-fire-ambulance-etc-sound-effect-26-11504.mp3")
                beeb+=1
            ret, frame=capture.read()
            if ret:
                frame1=HE.histogram_equalization(frame.copy())
                frame1=eye.eyeMesh(frame)#todo HE
                iTime.append(time.time())
                if eye.EAR!="undifined":
                    ear.append(eye.EAR)
                    #todo take user naem
                if iTime[-1]-iTime[0]>identifiTime:
                    alr.vioceAlarm(r"C:\Users\alisa\OneDrive\Desktop\ml\project\useridentification\voices\alarm-police-fire-ambulance-etc-sound-effect-26-11504.mp3")
                    idmod=False
                    Ear=np.array(ear)
                    userEar=np.mean(Ear)+(np.max(Ear)-np.min(Ear))/4+0.02
                    # if userEar==None:
                        #todo doig the process from zero but with new sound
                    wrfile.write([self.uname,userEar])#todo user name
                Image=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
                FlippedImage=cv.flip(Image,1)
                ConvertToQtFormat=QImage(FlippedImage.data,FlippedImage.shape[1],FlippedImage.shape[0],QImage.Format_RGB888)
                Pic=ConvertToQtFormat.scaled(640,480,Qt.KeepAspectRatio)
                self.ImageUpdate_1.emit(Pic,True)
        # capture.release()
        self.ImageUpdate_1.emit(Pic,False)
       
        #todo voice back button
        
            
                           
    def stop(self):
        self.ThreadActive=False
        self.quit()
        hi=hello()
        widget.addWidget(hi)
        widget.setCurrentIndex(widget.currentIndex()+1)   
 
              


      
                    
                
                
                
                 
              
              
              
              
              
              
                
            
      
                

app=QApplication(sys.argv)
welcome=hello()
widget=QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(height)
widget.setFixedWidth(width)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exiting")
        
        









