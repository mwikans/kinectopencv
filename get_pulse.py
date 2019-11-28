from lib.kinectopencv import KinectRuntime
from lib.interface import plotXY, imshow, waitKey, destroyWindow
from lib.imageprocessing import findFaceGetPulse
import cv2
import numpy as np
import sys

class getPulseApp(object):
    def __init__(self):
        self.cameras = []
        self.selected_cam = 1
        for i in range(3):
            camera = KinectRuntime(camera=i)  # first camera by default
            if camera.valid or not len(self.cameras):
                self.cameras.append(camera)
            else:
                break

        self.w, self.h = 0, 0
        self.pressed = 0

        '''
        Containerized analysis of recieved image frames (an openMDAO assembly)
        is defined next.

        This assembly is designed to handle all image & signal analysis,
        such as face detection, forehead isolation, time series collection,
        heart-beat detection, etc.

        Basically, everything that isn't communication
        to the camera device or part of the GUI
        '''
        self.image_processing = findFaceGetPulse()

        # Maps keystrokes to specified methods
        #(A GUI window must have focus for these to work)
        #self.key_controls = {"s": self.toggle_search,
        #                     "d": self.toggle_display_plot,
        #                     "c": self.toggle_cam,
        #                     "f": self.write_csv}
    #    self.cameras = []
    #    self.selected_cam = 0
    #    for i in range(camera-)
    #def toggle_cam(self):
    #    if len(self.cameras) > 1:
    #        self.processor.find_faces = True
    #        self.bpm_plot = False
    #        destroyWindow(self.plot_title)
    #        self.selected_cam += 1
    #        self.selected_cam = self.selected_cam % len(self.cameras)

    def key_handler(self):
        """
        Handle keystrokes, as set at the bottom of __init__()

        A plotting or camera frame window must have focus for keypresses to be
        detected.
        """

        self.pressed = waitKey(10) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            print("Exiting")
            for cam in self.cameras:
                cam.cam.release()
            #if self.send_serial:
            #    self.serial.close()
            sys.exit()

        #for key in self.key_controls.keys():
        #    if chr(self.pressed) == key:
        #        self.key_controls[key]()

    def main_loop(self):
        frame = self.cameras[self.selected_cam].get_frame()
        #self.h, self.w, _c = output_frame.shape

        #frame_processing = frame.copy()
        # set current image frame to the processor's input
        self.image_processing.frame_in = frame
        # process the image frame to perform all needed analysis
        #self.processor.run(self.selected_cam)
        # collect the output frame for display
        output_frame = self.image_processing.get_faces()
        tes = self.image_processing.run()

        imshow(" ", frame)
        imshow("Input", output_frame)
        imshow("123", tes)

        self.key_handler()

if __name__ == "__main__":
    App = getPulseApp()
    while True:
        App.main_loop()
