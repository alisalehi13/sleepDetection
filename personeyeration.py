import cv2 as cv 
import numpy as np 
import csv
import alarm
import eyeSleepD
import time
import wrfile

alr=alarm.Alarm()
eye=eyeSleepD.mediaPipeEyeDe()


class driveridentity():
    
    
    def newperson(self,username):
        ear=[]
        iTime=[]
        identifiTime=3
        beeb=0
        idmod=True  

        alr.vioceAlarm('./useridentification/voices/service.mp3')
        alr.vioceAlarm('./useridentification/voices/closeeye.mp3')
        capture=cv.VideoCapture(0)
        while idmod:
            if beeb==0:
                alr.vioceAlarm('./useridentification/voices/BEEP.mp3')
                beeb+=1

            isOk,frame=capture.read()
            if isOk:

                    
                frame=eye.eyeMesh(frame)
                iTime.append(time.time())
                if eye.EAR!="undifined":
                    ear.append(eye.EAR)
                
                
                
                cv.imshow('frame',frame)
                if cv.waitKey(1) & 0xFF==ord('q'):
                    break
                
                  
                if iTime[-1]-iTime[0]>identifiTime:
                    alr.vioceAlarm('./useridentification/voices/BEEP.mp3')
                    idmod=False
                    Ear=np.array(ear)
                    self.userEar=np.mean(Ear)+(np.max(Ear)-np.min(Ear))/4
                    capture.release()
                    cv.destroyAllWindows()
                    
                    
        if username!="guest0":            
            wrfile.write([username,self.userEar])
        return self.userEar  #todo  
                

    def doubt(self):
        alr.vioceAlarm('./useridentification/voices/hello_dubt.mp3')
        username=input("please your usernaem or enter N if you aren't ouruser : ")
        if username!="n" or username=="N":
            with open('./useridentification/driverdataset/csv/driver.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for line in csv_reader:
                    if len(line)==2:
                        if line[0]==username:
                            return True ,line[0] , float(line[1])
                        
        elif username=="n" or username=="N":
            return False ,0 ,0
                        











def main():
    nperson=driveridentity()
    nperson.newperson(username="hasan")



if __name__=="__main__":
    main()
                    
                    
    
                    
                    
            


