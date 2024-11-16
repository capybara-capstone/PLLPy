import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class Signal():
    def __init__(self, wave, fs):
        self.wave = wave
        self.fs = fs
        self.rising_edges = self.find_rising_edges()
        self.falling_edges = self.find_falling_edges()

    def find_rising_edges(self):
        if self.wave[0] == 1:
            return np.insert(np.append(np.where(np.diff(self.wave) > 0)[0],self.fs), 0, 0)
        return np.append(np.where(np.diff(self.wave) > 0)[0],self.fs)

    def find_falling_edges(self):
        return np.where(np.diff(self.wave) < 0)[0]

class LPD():
    def __init__(self, input_singal_1, input_signal_2, fs:int):
        self.in1:Signal = Signal(input_singal_1, fs)
        self.in2:Signal = Signal(input_signal_2, fs)
        self.up = Signal(np.linspace(0, 0, fs, endpoint=False),fs)
        self.down = Signal(np.linspace(0, 0, fs, endpoint=False),fs)
        self.phase_diff = None

    def get_wave_diff(self):
        
        for re_index in range(1,len(self.in1.rising_edges)):
            if self.in1.rising_edges[re_index-1] < self.in2.rising_edges[re_index-1]:
                for index, data_point in enumerate(self.in1.wave[self.in1.rising_edges[re_index-1]:self.in1.rising_edges[re_index]]):
                    if data_point == 1 and self.in2.wave[index+self.in1.rising_edges[re_index-1]] == 0:
                        self.up.wave[index+self.in1.rising_edges[re_index-1]] = 1
                    else:
                        self.up.wave[index+self.in1.rising_edges[re_index-1]] = 0
            elif self.in2.rising_edges[re_index-1] < self.in1.rising_edges[re_index-1]:
                for index, data_point in enumerate(self.in2.wave[self.in2.rising_edges[re_index-1]:self.in2.rising_edges[re_index]]):
                    if data_point == 1 and self.in1.wave[index+self.in2.rising_edges[re_index-1]] == 0:
                        self.down.wave[index+self.in2.rising_edges[re_index-1]] = 1
                    else:
                        self.down.wave[index+self.in2.rising_edges[re_index-1]] = 0
            else:
                for index, data_point in enumerate(self.in1.rising_edges[self.in1.rising_edges[re_index-1]:self.in1.rising_edges[re_index]]):
                    self.up.wave[index+self.in1.rising_edges[re_index-1]] = 0
                    self.down.wave[index+self.in1.rising_edges[re_index-1]] = 0

        self.up.rising_edges = self.up.find_rising_edges()
        self.up.falling_edges = self.up.find_falling_edges()
        self.down.rising_edges = self.down.find_rising_edges()
        self.down.falling_edges = self.down.find_falling_edges()

    def get_phase_diff(self):
        delta = None
        period = None
        for up_rising_edge_index in range(1,len(self.up.rising_edges)):
            period = self.up.rising_edges[up_rising_edge_index] - self.up.rising_edges[up_rising_edge_index-1]
            delta = self.up.falling_edges[up_rising_edge_index-1]-self.up.rising_edges[up_rising_edge_index-1]
        if delta != None and period != None:
            self.phase_diff = np.rint(np.degrees((delta*2*np.pi)/period))
        else:
            self.phase_diff = None

    def show_waves(self,fs):
        print('IN 1')
        print(f'Rising: {self.in1.rising_edges}')
        print(f'Falling: {self.in1.falling_edges}')
        
        print('IN 2')
        print(f'Rising: {self.in2.rising_edges}')
        print(f'Falling: {self.in2.falling_edges}')

        t = np.linspace(0, 1, fs, endpoint=False)

        plt.figure(figsize=(14, 6))

        plt.subplot(4, 1, 1)
        plt.plot(t, self.in1.wave, label="Signal 1", color='blue')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Signal 1")
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.plot(t, self.in2.wave, label="Signal 2", color='orange')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Signal 2")
        plt.legend()
        
        plt.subplot(4, 1, 3)
        plt.plot(t, self.up.wave, label="Signal 1", color='blue')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Signal 1")
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(t, self.down.wave, label="Signal 2", color='orange')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Signal 2")
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':


    freq = 5
    fs = 1000  # Sampling frequency
    t = np.linspace(0, 1, fs, endpoint=False)

    # Generate the square wave
    square_wave = (signal.square(2 * np.pi * freq * t) + 1) / 2
    square_wave2 = (signal.square(2 * np.pi * freq * t - np.pi/2) + 1) / 2
    

    lpd = LPD(square_wave,square_wave2,fs)
    lpd.get_wave_diff()
    lpd.get_phase_diff()
    lpd.show_waves(fs)
