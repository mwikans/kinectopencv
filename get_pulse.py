from opencv import KinectRuntime
import cv2
import numpy as np
import sys

class getPulseApp(object):
    def __init__(self):
        self.cameras = KinectRuntime()
    #    self.cameras = []
    #    self.selected_cam = 0
    #    for i in range(camera-)

    def main_loop(self):
        output_frame = self.cameras.get_frame()

        cv2.imshow("Processed", output_frame)

if __name__ == "__main__":

    App = getPulseApp()

    while True:
        App.main_loop()
