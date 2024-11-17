import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import os

class LPD():
    def __init__(self, input_signal_1, input_signal_2):
        self.in1 = input_signal_1
        self.in2 = input_signal_2
        self.out = []
        self.out2 = []
        self.sample = 0
        self.last_in1 = input_signal_1[0]
        self.last_in2 = input_signal_2[0]
        self.phase_diff = None
        self.result1 = 0
        self.result2 = 0

    def get_wave_diff(self,input_signal_1,input_signal_2):
        if len(input_signal_1) != len(input_signal_2):
            raise Exception

        for sample in range(len(input_signal_1)):
           
           #up logic

           risingEdgeDetected = 0 
            
           if input_signal_1[sample] == 0:
                self.result1 = 0
                self.last_in1 = 0

           elif input_signal_1[sample] == 1:
               if self.last_in1 == 0: #rising edge detected
                    self.result1 = 1
                    risingEdgeDetected = 1
                
               self.last_in1 = 1

           if input_signal_2[sample] == 1 and risingEdgeDetected == 0:
               self.result1 = 0

           self.out.append(self.result1)

           #down logic

           risingEdgeDetected = 0
            
           if input_signal_2[sample] == 0:
               self.result2 = 0
               self.last_in2 = 0

           elif input_signal_2[sample] == 1:
              if self.last_in2 == 0: #rising edge detected
                self.result2 = 1
                risingEdgeDetected = 1
            
              self.last_in2 = 1

           if input_signal_1[sample] == 1 and risingEdgeDetected ==0:
               self.result2 = 0

           self.out2.append(self.result2)


           

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

'''

if __name__ == '__main__':


    data = pd.read_csv(os.path.basename(big_test))
    time = data['time'].to_numpy()
    in_a = data['IN_A'].to_numpy()
    in_b = data['IN_B'].to_numpy()
    out_1 = data['OUT_1']
    out_2 = data['OUT_2']
    # plt.figure(figsize=(10, 8))
    # # Plot each variable
    # plt.subplot(4, 1, 1)
    # plt.plot(time, in_a, label='IN_A')
    # plt.subplot(4, 1, 2)
    # plt.plot(time, in_b, label='IN_B')
    # plt.subplot(4, 1, 3)
    # plt.plot(time, out_1, label='OUT_1')
    # plt.subplot(4, 1, 4)
    # plt.plot(time, out_2, label='OUT_2')

    # # Add labels, legend, and grid
    # plt.title('CSV Data Plot')
    # plt.xlabel('Time')
    # plt.ylabel('Values')
    # plt.legend()
    # plt.grid(True)

    # # Show the plot
    # plt.tight_layout()
    # plt.show()
    
    
    # freq = 5
    # fs = 1000  # Sampling frequency
    # fs_low = 500
    # t_low = np.linspace(0, 1, fs_low, endpoint=False)
    # t = np.linspace(0, 1, fs, endpoint=False)

    # # # Generate the square wave
    # square_wave = (signal.square(2 * np.pi * 5 * t_low) + 1) / 2
    # square_wave2 = (signal.square(2 * np.pi * 5 * t - np.pi/2) + 1) / 2
    # square_wave2 = square_wave2[:fs_low]
    # # square_wave = (signal.square(2 * np.pi * 5 * t - np.pi/2) + 1) / 2
    # # square_wave2 = (signal.square(2 * np.pi * 5 * t_low) + 1) / 2
    # # square_wave = square_wave[:fs_low]

    square_wave_pairs = in_a.reshape(-1, 2)
    square_wave2_pairs = in_b.reshape(-1,2)

    '''

    #USAGE EXAMPLE


    '''

    lpd = LPD(square_wave_pairs[0],square_wave2_pairs[0])
    square_wave_pairs = square_wave_pairs[1:]
    square_wave2_pairs = square_wave2_pairs[1:]

    for index, sample in enumerate(square_wave_pairs):
        lpd.get_wave_diff(sample,square_wave2_pairs[index])
    
    '''

    #END USAGE EXAMPLE


    '''

    plt.figure(figsize=(14, 6))

    plt.subplot(4, 1, 1)
    plt.plot(time,in_a, label="Signal 1", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 1")
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(time,in_b, label="Signal 2", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 2")
    plt.legend()
    
    plt.subplot(4, 1, 3)
    plt.plot(list(range(len(time)-2)), lpd.out, label="Out 1 ", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("out 1")
    
    plt.subplot(4, 1, 4)
    plt.plot(list(range(len(time)-2)), lpd.out2, label="Out 2", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("out 2")

    plt.legend()
    plt.tight_layout()
    plt.show()

'''
