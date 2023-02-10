'''
Alarm madoule controls all system's alarm

author: ALI Salhei.D
date: 2022

'''

from playsound import playsound
import pygame



class Alarm():
    '''
    Alarm class manage the alarm and has multi type of alarm like voice alarm,...
    
    '''
    def vioceAlarm(self,path):
        '''
        voiceAlarm method play a voice alarm in the necessary situation
        pygame library used for play voice alarm
        input:
            1# path=> path of the voice alarm file
        
        '''
        playsound(path)
        
        #playing the voice alarm with pygame library

        
    
    
def pyalr(path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(path)
    playing = sound.play()
    while playing.get_busy():
        pygame.time.delay(10)
    
    
    
    

'''    
def main():
    alarm=Alarm()
    alarm.vioceAlarm(".\LookForward.mp3")
    
    
    
if __name__=="__main__":
    main()
'''