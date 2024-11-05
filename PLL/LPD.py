import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from utilities import *

class LPD():
    def __init__(self, sig1, sig2):
        self.sig1 = sig1
        self.sig2 = sig2
        self.delta_phase = None

    def phase_diff(self):
        #Assuming same freq Constant Freq
        peaks,_ = find_peaks(self.sig1)
        peaks2,_ = find_peaks(self.sig2)
        self.delta_phase = ((peaks[0] - peaks2[0])/(peaks[0] - peaks[1]))*360 # (time diff)/period*360 where time diff is index of same value in each signal
    
    def phase_diff_const_diff_freq(self):
        #Assuming aplitude 1 diff freq constant freq
        phase_diff = []
        for index,point in enumerate(self.sig1):
            phase_diff.append((np.arccos(point) - np.arccos(self.sig2[index])) * (180/np.pi))
        
        return np.array(phase_diff)

if __name__ == '__main__':
    data = generate_sine_wave(frequency=440, amplitude=1, duration=1, sampling_rate=44100)
    clk = generate_sine_wave(frequency=440, amplitude=1, duration=1, sampling_rate=44100, shift=np.pi)
    
    lpd = LPD(data,clk)
    diff = lpd.phase_diff_const_diff_freq()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Adjust the figsize as needed

    ax1.plot(data[:1000], label = 'Signal 1')
    ax1.plot(clk[:1000], label = 'Signal 2')
    ax1.set_title('Input Signals')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()

    ax2.plot(diff[:1000])
    ax2.set_title('Phase Diff')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Phase Diff (°)')
    ax2.legend()
    ax2.grid()
    
    plt.tight_layout()

    plt.show()
    

    
    