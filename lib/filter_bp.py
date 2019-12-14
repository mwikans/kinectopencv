import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter, lfilter_zi
import numpy as np

 
class plotFilter(object): 
    def __init__(self):
        super().__init__()
    
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a


    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        zi = lfilter_zi(b, a)
        y, zo = lfilter(b, a, data, zi=zi*data[0])
        return y

    
    def run(self):
        fs = 1/0.033
        lowcut = 0.10
        highcut = 2.0

        #data = pd.read_csv('example_no negative.csv', sep=",")#, sep=" ", header=None, skiprows=2, skipinitialspace=True)
        data = pd.read_csv('D:\ProgramData\GitHub\kinectopencv\_time_series_frame.csv', header=None, sep=" ")
        data.columns = ["x_value","y_value"]

        t = np.arange(0,101)
        n = data['x_value'].to_numpy()
        x = data['y_value'].to_numpy()

        plt.figure(1)
        plt.title('Raw Signal')
        plt.ylabel('Amplitude')
        plt.xlabel('Time [sec]')
        plt.plot(n, x, label='Raw Signal')
        plt.grid(True)

        y = self.butter_bandpass_filter(x, lowcut, highcut, fs, order=2)
        #y = filter_test_2.bandpass(lowcut, highcut, fs, x)
        print(n.shape)
        print(x.shape)
        print(y.shape)

        plt.figure(2)
        plt.title('Filtered Signal')
        plt.ylabel('c')
        plt.xlabel('Time [sec]')
        plt.plot(n, y, label='Filtered Signal')
        plt.grid(True)
        
        freq_response = np.abs(np.fft.fft(y))
        freq = np.fft.fftfreq(y.shape[-1])
        
        plt.figure(3)
        plt.plot(freq, freq_response, label='BPM FFT')
        plt.title('FFT')
        plt.ylabel('Power Spectrum')
        plt.xlabel('Frequency [Hz]')
        plt.grid(True)

        amp = 2 * np.sqrt(2)
        f, t, Zxx = signal.stft(np.abs(y), fs, window="hann", nperseg=256)
        
        plt.figure(4)
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp)
        plt.grid(True)
        plt.title('STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()
