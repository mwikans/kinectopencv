import numpy as np
import cv2, time
from threading import Thread

class KinectRuntime(object):
    def __init__(self, camera = 0):
        self.cap = cv2.VideoCapture(camera)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.valid = False
        self.stopped = False
        try:
            #resp = self.cap.read()
            (self.grabbed, self.frame) = self.cap.read()        
            self.shape = self.frame[1].shape
            self.valid = True
        except:
            self.shape = None

    def start(self):
        Thread(target=self.get_frame, args=()).start()
        return self

    def resize_image(self, frame):
        height , width , layers =  frame.shape
        new_h=round(height/3)
        new_w=round(width/3)
        resize = cv2.resize(frame, (new_w, new_h)) 
        
        return resize
    
    def get_frame(self):
        if self.valid:
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                else:
                    (self.grabbed, self.frame) = self.cap.read()
        else:
            self.frame = np.ones((480,640,3), dtype=np.uint8)
            col = (0,256,256)
            cv2.putText(self.frame, "(Error: Camera not accessible)",
                        (65,220), cv2.FONT_HERSHEY_PLAIN, 2, col)
        
    def release(self):
        self.cap.release()
        self.stop()
        
    def stop(self):
        self.stopped = True