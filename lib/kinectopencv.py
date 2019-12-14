import numpy as np
import cv2, time

class KinectRuntime(object):
    def __init__(self, camera = 0):
        self.cap = cv2.VideoCapture(camera)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.valid = False
        try:
            resp = self.cap.read()
            self.shape = resp[1].shape
            self.valid = True
        except:
            self.shape = None

    def resize_image(self, frame):
        height , width , layers =  frame.shape
        new_h=round(height/3)
        new_w=round(width/3)
        resize = cv2.resize(frame, (new_w, new_h)) 
        
        return resize
                
    def get_frame(self):
        if self.valid:
            _,frame = self.cap.read()
            #frame = self.resize_image(frame) 
        else:
            frame = np.ones((480,640,3), dtype=np.uint8)
            col = (0,256,256)
            cv2.putText(frame, "(Error: Camera not accessible)",
                       (65,220), cv2.FONT_HERSHEY_PLAIN, 2, col)
        return frame

    def release(self):
        self.cam.release()
