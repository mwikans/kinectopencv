from opencv import KinectRuntime
from interface import plotXY, imshow, waitKey, destroyWindow
import cv2
import numpy as np
import sys

class getPulseApp(object):
    def __init__(self):
        self.cameras = []
        self.selected_cam = 0
        for i in range(3):
            camera = KinectRuntime(camera=i)  # first camera by default
            if camera.valid or not len(self.cameras):
                self.cameras.append(camera)
            else:
                break

        self.w, self.h = 0, 0
        self.pressed = 0

        # Maps keystrokes to specified methods
        #(A GUI window must have focus for these to work)
        #self.key_controls = {"s": self.toggle_search,
        #                     "d": self.toggle_display_plot,
        #                     "c": self.toggle_cam,
        #                     "f": self.write_csv}
    #    self.cameras = []
    #    self.selected_cam = 0
    #    for i in range(camera-)
    def toggle_cam(self):
        if len(self.cameras) > 1:
            self.processor.find_faces = True
            self.bpm_plot = False
            destroyWindow(self.plot_title)
            self.selected_cam += 1
            self.selected_cam = self.selected_cam % len(self.cameras)

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
        output_frame = self.cameras[self.selected_cam].get_frame()
        #self.h, self.w, _c = output_frame.shape

        imshow("Processed", output_frame)

        self.key_handler()

if __name__ == "__main__":

    App = getPulseApp()

    while True:
        App.main_loop()
