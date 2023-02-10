'''
this madoule calculate position of person head and face direction

author:ALI Salehi.D

date:2022
'''
import cv2
import mediapipe as mp
import numpy as np
import time






class HeadPose():
    '''
    ========================================================================
   |       mediapipe base head position recognition class .                 |
   |       This class detect the person face and calculate head             |
   |        direction and position                                          |
   |                                                                        |
    ========================================================================
    '''

    def __init__(self,staticMode=False,maxFaces=1,minDetectionCon=0.5,minTrackCon=0.5):
        self.staticMode=staticMode
        self.maxFaces=maxFaces
        self.minDetectionCon=minDetectionCon
        self.minTrackCon=minTrackCon

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    def hpos(self,image):
        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        text="undifined"
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False
        
        # Get the result
        results = self.face_mesh.process(image)
        
        # To improve performance
        image.flags.writeable = True
        
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []    
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])       
                
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)
                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360
                # print(x,"   ",y,"   ",z)

                # See where the user's head tilting
                if y < -16:
                    text = "Looking Left"
                elif y > 16:
                    text = "Looking Right"
                elif x < -10:
                    text = "Looking Down"
                elif x > 19:
                    text = "Looking Up"
                else:
                    text = "Forward"

                # Display the nose direction
                # nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10) , int(nose_2d[1] - x * 10))
                
                cv2.line(image, p1, p2, (255, 0, 0), 3)

        return text





def main():


    cap = cv2.VideoCapture(0)
    head=HeadPose()
    while cap.isOpened():
        success, image = cap.read()
        text=head.hpos(image)
        cv2.imshow('Head Pose Estimation', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()