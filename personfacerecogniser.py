import face_recognition
import cv2
import numpy as np
import os
import personeyeration 
import alarm
import wrfile

alr=alarm.Alarm()
person=personeyeration.driveridentity()
namefile=wrfile.read()

face_encodingsDirectory=r'./useridentification/driverdataset/image'
known_face_encodings = []
known_face_names = []
for path in os.listdir(face_encodingsDirectory):
    known_face_encodings.append(np.load(os.path.join(face_encodingsDirectory,path)))
    known_face_names.append(path.split(".")[-2])
    



class driver():
    
    namefile=wrfile.read()
    def recognis(self,image):
    
        face_locations = []
        face_encodings = []
        
        small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        rgb_small_image = small_image[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_image)
        face_encodings = face_recognition.face_encodings(rgb_small_image, face_locations)
        face_names = []
        if known_face_encodings==[]:
            alr.vioceAlarm('./useridentification/voices/service.mp3')
            alr.vioceAlarm('./useridentification/voices/username.mp3')
            uname=input("please enter the username: ")
            while uname in namefile:
                alr.vioceAlarm('./useridentification/voices/repeat.mp3')
                uname=input("please enter the username: ")
            person.newperson(uname)
            for face_encoding in face_encodings:
                face_encoding=np.array(face_encoding)
                np.save(r'./useridentification/driverdataset/image/'+uname,face_encoding)
                break
            return wrfile.read_ear(uname)
            
        else: 
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown" 

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                print(face_distances)#todo
                if face_distances[best_match_index]>0.3:
                    exist,uname,ear=person.doubt()
                    if exist:#todo
                        np.save('./useridentification/driverdataset/image/'+uname,face_encoding)
                        return ear
            
                    else:
                        alr.vioceAlarm('./useridentification/voices/service.mp3')
                        alr.vioceAlarm('./useridentification/voices/username.mp3')
                        uname=input("please enter the username: ")
                        while uname in namefile:
                            alr.vioceAlarm('./useridentification/voices/repeat.mp3')
                            uname=input("please enter the username: ")
                        person.newperson(uname)
                        np.save('./useridentification/driverdataset/image/'+uname,face_encoding)
                        return wrfile.read_ear(uname)

                    
                
                
                elif matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    print(name)#todo
                    return wrfile.read_ear(name)
                break