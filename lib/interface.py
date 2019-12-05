import cv2, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from celluloid import Camera

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
# sphinx_gallery_thumbnail_number = 2
    fig, axes = plt.subplots()
    #camera = Camera(fig)
    #t = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    axes.set_title("10x10 Pixel Compress")
    
    #for i in subface_frame:
        #axes[0].plot(t, np.sin(t + i), color='blue')
        #axes[1].plot(t, np.sin(t - i), color='blue')
        #harvest = np.random.randn(47,79)   
    axes.imshow(subface_frame)
        
        #fig.tight_layout()
        #camera.snap()
            # redraw the canvas
    fig.canvas.draw()

        # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
                sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)


        # display image with opencv or any operation you like
    cv2.imshow("plot",img)

        # display camera feed
        #ret,frame = cap.read()
        #cv2.imshow("cam",frame)

    #k = cv2.waitKey(10) & 0xFF
    #if k == 27:
        #break

    
    #pcm = axes.pcolormesh(harvest)
    #fig.colorbar(pcm, ax=axes)
    #animation = camera.animate()
    
    #plt.show()
    
    
    