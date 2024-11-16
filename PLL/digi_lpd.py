import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def get_phase_diff_signal(signal1, signal2, signal3, signal4, t):
    # if rising edge s1 before re s2 
            # if s1 = 1 and s2 =0 then 1
    # if re s2 before re s1 
            #if s2 = 1 and s1 = 0 then 1
    
    #first data point 
    # if signal1[0] == 1 and signal2[0] == 0:
    #     #s1 re before s2
    print("----")
    print("singal 1")
    re1, fe1 = find_edges_01(signal1,t)
    # re1 = np.delete(re1,0)
    re1 = np.append(re1,1000) 
    print(type(signal1))
    print(f'rising_edges: {re1} falling_edges: {fe1}')
    print("singal 2")
    re2, fe2 = find_edges_01(signal2,t)
    re2 = np.delete(re2,1)
    # re2 = np.append(re2,1000) 
    print(f'rising_edges: {re2} falling_edges: {fe2}')
    print("----")

    for re_index in range(1,len(re1)):
        if re1[re_index-1] < re2[re_index-1]:
            for index, data_point in enumerate(signal1[re1[re_index-1]:re1[re_index]]):
                if data_point == 1 and signal2[index+re1[re_index-1]] == 0:
                    signal3[index+re1[re_index-1]] = 1
                else:
                    signal3[index+re1[re_index-1]] = 0
        elif re2[re_index-1] < re1[re_index-1]:
            for index, data_point in enumerate(signal2[re2[re_index-1]:re2[re_index]]):
                if data_point == 1 and signal1[index+re2[re_index-1]] == 0:
                    signal4[index+re2[re_index-1]] = 1
                else:
                    signal4[index+re2[re_index-1]] = 0
        else:
            for index, data_point in enumerate(signal1[re1[re_index-1]:re1[re_index]]):
                signal3[index+re1[re_index-1]] = 0
                signal4[index+re1[re_index-1]] = 0
            
        
        
    return signal3, signal4

def find_edges_01(wave, time_array):
    differences = np.diff(wave)
    # rising_edges = time_array[:-1][differences > 0]
    # falling_edges = time_array[:-1][differences < 0]
    rising_indices = np.where(differences > 0)[0]
    falling_indices = np.where(differences < 0)[0]
    
    # return rising_edges, falling_edges
    return rising_indices, falling_indices

# def get_rising_edge(signal, count=2):
    
#     rising_edge_indices = []
    
#     for index,data_point in enumerate(signal):
#         if data_point == 1:
#             if signal[index - 1] == 0:
#                 rising_edge_indices.append(index)
#                 if len(rising_edge_indices) == count:
#                     break
    
#     return rising_edge_indices

# def get_falling_edge(signal,count=2):

#     falling_edge_indices = []
    
#     for index,data_point in enumerate(signal):
#         if data_point == 1:
#             if signal[index + 1] == 0:
#                 falling_edge_indices.append(index)
#                 if len(falling_edge_indices) == count:
#                     break
    
#     return falling_edge_indices


# def get_phase_diff(rising_edges,falling_edges):
#     period = rising_edges[1] - rising_edges[0] + 2
#     delta = falling_edges[0] - rising_edges[0] + 2
#     return np.ceil(np.degrees((delta*2*np.pi)/period))
        

if __name__ == '__main__':
    
    freq = 5
    fs = 1000
    
    t = np.linspace(0, 1, fs, endpoint=False)
    signal1 = (np.sign(np.sin(2 * np.pi * freq * t)) + 1) / 2
    signal2 = (np.sign(np.sin(2 * np.pi * freq * t - np.pi / 4)) + 1) / 2
    signal_up = np.linspace(0, 0, fs, endpoint=False)
    signal_down = np.linspace(0, 0, fs, endpoint=False)
    
    signal_up, signal_down = get_phase_diff_signal(signal1,signal2,signal_up,signal_down,t)
    # signal_down = get_phase_diff_signal(signal2,signal1,signal_down,t)
    
    # print(get_rising_edge(signal_up))
    
    # print(get_falling_edge(signal_up))
    # print(get_phase_diff(get_rising_edge(signal_up),get_falling_edge(signal_up)))
    time = np.arange(len(signal1)) / fs
    
    plt.figure(figsize=(14, 6))

    plt.subplot(4, 1, 1)
    plt.plot(time, signal1, label="Signal 1", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 1")
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(time, signal2, label="Signal 2", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 2")
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(time, signal_up, label="Up", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Up")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(time, signal_down, label="Down", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Down")
    plt.legend()
    
    plt.tight_layout()
    plt.show()