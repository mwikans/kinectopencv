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
        self.fps = -1
        self.frame_in = np.zeros((10, 10))
        self.frame_out = np.zeros((10, 10))
        self.frame_jetmap = np.zeros((10, 10))
        self.gray = np.zeros((10, 10))
        self.forehead_ = np.zeros((10,10))
        self.green_forehead = np.zeros((10,10))
        cascade_path = resource_path("haarcascade_frontalface_default.xml")
        if not os.path.exists(cascade_path):
            print("Cascade file not present!")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        self.find_faces = True
        self.face_rect = [1, 1, 2, 2]
        self.last_center = np.array([0, 0])

    def find_faces_toggle(self):
        self.find_faces = not self.find_faces
        return self.find_faces

    def shift(self, detected):
        x, y, w, h = detected
        center = np.array([x + 0.5 * w, y + 0.5 * h])
        shift = np.linalg.norm(center - self.last_center)

        self.last_center = center
        return shift    

    def downscale_img(self, frame):
        scale_percent = 10 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
        return frame
    
    def draw_rect(self, rect, col=(0, 255, 0)):
        x, y, w, h = rect
        cv2.rectangle(self.frame_out, (x, y), (x + w, y + h), col, 1)
        cv2.rectangle(self.frame_jetmap, (x, y), (x + w, y + h), col, 1)
        cv2.rectangle(self.gray, (x, y), (x + w, y + h), col, 1)
        
    def RGB2GREEN(self, frame):
        green_image = frame
        green_image[:,:,0] = 0
        green_image[:,:,2] = 0
        return green_image

    def get_subface_coord(self, fh_x, fh_y, fh_w, fh_h):
        x, y, w, h = self.face_rect
        return [int(x + w * fh_x - (w * fh_w / 2.0)),
                int(y + h * fh_y - (h * fh_h / 2.0)),
                int(w * fh_w),
                int(h * fh_h)] 
    
    def get_subface_averaging(self, frame):
        #x, y, w, h = coord
        #subframe = self.frame_in[y:y + h, x:x + w]
        #blue = np.mean(subframe[:, :, 0])
        green = np.mean(frame)
        #red = np.mean(subframe[:, :, 2])
        
        return green
    
    def get_subface(self, coord):
        x, y, w, h = coord
        roi = self.frame_in.copy()[y:y+h, x:x+w] 
            
        return roi    
    
    def face_detection(self):
        frame = self.frame_in.copy()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(cv2.cvtColor(frame,
                                                  cv2.COLOR_BGR2GRAY))
        
        faces = self.face_cascade.detectMultiScale(gray, 1.9, 5)  
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),0)  
            roi_color = frame[y:y+h, x:x+w]
            
            for (x,y,w,h) in faces:
                fh_x = 0.5
                fh_y = 0.13
                fh_w = 0.25
                fh_h = 0.15

                x = int(x + w * fh_x - (w * fh_w / 2.0))
                y = int(y + h * fh_y - (h * fh_h / 2.0))
                w = int(w * fh_w)
                h = int(h * fh_h)

                forehead1 = cv2.rectangle(gray,(x,y),(x+w,y+h),(0,0,255),0)
                roi_green = gray[y:y+h, x:x+w]
            
        return forehead1
    
    def run(self):
        #self.frame_out = self.frame_in.copy()
        #tes = self.face_detection()    
        self.frame_out = self.frame_in.copy()
        self.frame_jetmap = cv2.applyColorMap(self.frame_in.copy(), cv2.COLORMAP_JET)
        self.gray = cv2.equalizeHist(cv2.cvtColor(self.frame_in.copy(),
                                                  cv2.COLOR_BGR2GRAY))
        
        col = (100, 255, 100)
        if self.find_faces:
            cv2.putText(
                self.frame_out, "Press 'S' to lock face and begin",
                       (10, 50), cv2.FONT_HERSHEY_PLAIN, 1.25, col)
            cv2.putText(self.frame_out, "Press 'F' to write to csv",
                       (10, 65), cv2.FONT_HERSHEY_PLAIN, 1.25, col)
            cv2.putText(self.frame_out, "Press 'M' to plot signal",
                       (10, 80), cv2.FONT_HERSHEY_PLAIN, 1.25, col)
            cv2.putText(self.frame_out, "Press 'Esc' to quit",
                       (10, 95), cv2.FONT_HERSHEY_PLAIN, 1.25, col)
        
        #tes2 = self.get_subface_coord(0.5, 0.13, 0.25, 0.15, tes)        
            detected = list(self.face_cascade.detectMultiScale(self.gray, 1.3, 5))
           #                                                     scaleFactor=1.9,
           #                                                     minNeighbors=5,
           #                                                     minSize=(
           #                                                         50, 50),
           #                                                     flags=cv2.CASCADE_SCALE_IMAGE))

            if len(detected) > 0:
                detected.sort(key=lambda a: a[-1] * a[-2])

                if self.shift(detected[-1]) > 10:
                    self.face_rect = detected[-1]
                 
            forehead1 = self.get_subface_coord(0.5, 0.18, 0.25, 0.15)
            self.draw_rect(self.face_rect, col=(255, 0, 0))
            x, y, w, h = self.face_rect
            cv2.putText(self.frame_out, "Face",
                    (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, col)
            self.draw_rect(forehead1)
            x, y, w, h = forehead1
            cv2.putText(self.frame_out, "Forehead",
                    (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, col)
            cv2.putText(self.frame_jetmap, "Forehead",
                    (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, col)
            cv2.putText(self.gray, "Forehead",
                    (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, col)
            self.forehead_ = self.RGB2GREEN(self.get_subface(forehead1))
            self.forehead_ = self.downscale_img(self.forehead_)
            #self.green_forehead = self.forehead_[:, :, 1]
            
            #self.forehead_ = cv2.applyColorMap(self.downscale_img(self.forehead_), cv2.COLORMAP_JET)
            #self.forehead_ = cv2.applyColorMap(self.forehead_, cv2.COLORMAP_JET)
            
            self.averaging = self.get_subface_averaging(self.forehead_)
            self.fps += 1
        
            return