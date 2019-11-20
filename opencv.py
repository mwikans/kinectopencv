import numpy as np
import cv2, time

class KinectRuntime(object):
    def __init__(self, camera = 0):
        self.cap = cv2.VideoCapture(camera)
        self._done = False
        try:
            resp = self.cap.read()
            self.shape = resp[1].shape
            self.valid = True
        except:
            self.shape = None

    def get_frame(self):
        if self.valid:
            ret, frame = self.cap.read()
        else:
            frame = np.ones((480,640,3), dtype=np.uint8)
            col = (0,256,256)
            cv2.putText(frame, "(Error: Camera not accessible)",
                       (65,220), cv2.FONT_HERSHEY_PLAIN, 2, col)
        return frame

    def release(self):
        self.cam.release()

        '''
        while True:
            # Capture frame-by-frame

            green_image = frame.copy()
            green_image[:,:,0] = 0
            green_image[:,:,2] = 0

            # Our operations on the frame come here
            gray = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _image = cv2.applyColorMap(green_image, cv2.COLORMAP_JET)

            # Display the resulting frame
            cv2.imshow('frame',gray)
            cv2.imshow('gframe', green_image)
            cv2.imshow('jframe', _image)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
        '''
