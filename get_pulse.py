from lib.kinectopencv import KinectRuntime
from lib.interface import plot_histogram, imshow, waitKey, destroyWindow
from lib.imageprocessing import findFaceGetPulse
from lib.filter_bp import plotFilter
import cv2
import numpy as np
import sys
import time

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
        
        self.fileOutput = []
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

        # Init parameters for the cardiac data plot
        self.bpm_plot = False
        self.heatmap_plot = False
        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"
        
        self.bandpass_filter = plotFilter()
        
        self.save_data = False
        # Maps keystrokes to specified methods
        #(A GUI window must have focus for these to work)
        self.key_controls = {"s": self.toggle_search,
                             "d": self.toggle_histogram_plot,
        #                     "c": self.toggle_cam,
                             "f": self.toggle_write_csv,
                             "m": self.toggle_matplot}
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
    
    def write_csv(self):
        """
        Writes current data to a csv file
        """
        sec = self.image_processing.fps / 30
        
        L = ["%.3f" % (sec), " ", "%.3f" % self.image_processing.averaging, "\n"]
        self.fileOutput.writelines(L)
        
        #fn = "Webcam-pulse" + str(datetime.datetime.now())
        #fn = fn.replace(":", "_").replace(".", "_")
        
        #info = {
        #    "x_value": "%.3f" % (sec),
        #    "y_value": "%.3f" % self.image_processing.averaging,
        #}
        
        #data = np.vstack((self.processor.times, self.processor.samples)).T
        #np.savetxt(fn + ".csv", data, delimiter=',')
        #print("Writing csv")
        print("%.3f" % (sec), "%.3f" % self.image_processing.averaging)

    def toggle_search(self):
        """
        Toggles a motion lock on the processor's face detection component.

        Locking the forehead location in place significantly improves
        data quality, once a forehead has been sucessfully isolated.
        """
        #state = self.processor.find_faces.toggle()
        state = self.processor.find_faces_toggle()
        print("face detection lock =", not state)
    
    def toggle_write_csv(self):
        """
        Toggle to save the data to csv file.
        """
        if self.save_data:
            print("Saving frame data buffer finish")
            self.save_data = False
            self.fileOutput.close()
        else:
            print("Saving frame data buffer start")
            self.fileOutput = open("_time_series_frame.csv","w")
            self.save_data = True
    
    def toggle_histogram_plot(self):#, subface_frame):
        if self.heatmap_plot:
            self.heatmap_plot = False
            destroyWindow("plot")
        else:
            self.heatmap_plot = True
            
    def toggle_matplot(self):
        """
        Toggle to show the time series signal.
        """
        if self.bpm_plot:
            self.bpm_plot = False
        else:
            self.bpm_plot = True
    
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

        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()

    def main_loop(self):
        frame = self.cameras[self.selected_cam].get_frame()
        #self.h, self.w, _c = output_frame.shape

        #frame_processing = frame.copy()
        # set current image frame to the processor's input
        self.image_processing.frame_in = frame
        # process the image frame to perform all needed analysis
        #self.processor.run(self.selected_cam)
        # collect the output frame for display
        output_frame = self.image_processing.frame_out
        output_jetmap = self.image_processing.frame_jetmap
        output_gray = self.image_processing.gray
        
        forehead = self.image_processing.forehead_
        
        tes = self.image_processing.run()
               
        
        #self.toggle_histogram_plot(forehead)
        #tes = self.image_processing.face_detection()
        #imshow("Input", frame)
        imshow("Interface", output_frame)
        imshow("Jetmap", output_jetmap)
        imshow("Gray", output_gray)
        imshow("Forehead", forehead)
        #print(forehead)
        #print(self.image_processing.averaging)
        #print(self.image_processing.green_forehead)
        
        if self.save_data:
            self.write_csv()
         
        if self.heatmap_plot:
            plot_histogram(self.image_processing.forehead_)
 
        if self.bpm_plot:
            if self.save_data:
                self.save_data = False
            self.bandpass_filter.run()
            self.bpm_plot = False
                
        self.key_handler()

if __name__ == "__main__":
    App = getPulseApp()
    while True:
        App.main_loop()
