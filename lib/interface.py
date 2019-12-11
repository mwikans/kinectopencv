import cv2, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

"""
Wraps up some interfaces to opencv user interface methods (displaying
image frames, event handling, etc).

If desired, an alternative UI could be built and imported into get_pulse.py 
instead. Opencv is used to perform much of the data analysis, but there is no
reason it has to be used to handle the UI as well. It just happens to be very
effective for our purposes.
"""
def resize(*args, **kwargs):
    return cv2.resize(*args, **kwargs)

def moveWindow(*args,**kwargs):
    return

def imshow(*args,**kwargs):
    return cv2.imshow(*args,**kwargs)
    
def destroyWindow(*args,**kwargs):
    return cv2.destroyWindow(*args,**kwargs)

def waitKey(*args,**kwargs):
    return cv2.waitKey(*args,**kwargs)


"""
The rest of this file defines some GUI plotting functionality. There are plenty
of other ways to do simple x-y data plots in python, but this application uses 
cv2.imshow to do real-time data plotting and handle user interaction.

This is entirely independent of the data calculation functions, so it can be 
replaced in the get_pulse.py application easily.
"""
def plot_histogram(subface_frame):
    fig, axes = plt.subplots()
    
    axes.set_title("Pixel Downscaling")
    
    for i in range(subface_frame.shape[0]):
        for j in range(subface_frame.shape[1]):
            axes.text(j, i, subface_frame[i, j], ha="center", va="center", color="w")
    
    axes.imshow(subface_frame)
    
    fig.canvas.draw()
    
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
                sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    cv2.imshow("plot",img)
    