import cv2
import sys
import os
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class findFaceGetPulse(object):
    def __init__(self):
        self.frame_in = np.zeros((10, 10))
        self.frame_out = np.zeros((10, 10))
        cascade_path = resource_path("haarcascade_frontalface_default.xml")
        if not os.path.exists(cascade_path):
            print("Cascade file not present!")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def get_faces(self):
        green_image = self.frame_in.copy()
        green_image[:,:,0] = 0
        green_image[:,:,2] = 0
        return green_image

    def face_detection(self):
        frame = self.frame_in.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)  
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x+30,y+30),(x+w-30,y+h-30),(255,0,0),0)  
            roi_color = frame[y+30:y+h-30, x+30:x+w-30]
        return roi_color
    
    def run(self):
        #self.frame_out = self.frame_in.copy()
        tes = self.face_detection()    
        
        return tes
