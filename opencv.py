import numpy as np
import cv2

#class KinectRuntime(object):
    #def __init__(self):
    #    self._done = False

    #def show_camera(self):
cap = cv2.VideoCapture(0)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

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
cap.release()
cv2.destroyAllWindows()

#__main__ = "Kinect Camera"
#run_ = KinectRuntime();
#run_.show_camera();
