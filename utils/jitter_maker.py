import numpy as np
import matplotlib.pyplot as plt

def plot_data(x: np.ndarray, y: np.ndarray):

    """
    Plots the given x and y data using matplotlib with a purple line.
    Parameters:
    x (np.ndarray): Array of x values.
    y (np.ndarray): Array of y values.
    """


    plt.figure(figsize=(8, 5))  # Set figure size
    plt.plot(x, y, color='purple', linestyle='-', marker='o', markersize=5)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Data Plot")
    plt.grid(True)
    plt.show()

    # Example usage:
    # x_data = np.array([1, 2, 3, 4, 5])
    # y_data = np.array([2, 3, 5, 7, 11])
    # plot_data(x_data, y_data)


jitter = 0.1
length_of_array = 10000
frequency = 500E6
period = 1 / 500E6
UI = period / 2
time_step = 1E-11

n_symbols = round(length_of_array*time_step / UI)

#generate random Gaussian distributed TX jitter values
epsilon = np.random.normal(0, jitter*UI, n_symbols)
epsilon.clip(UI)
epsilon[0]=0

print(len(epsilon))

#calculate time duration of each sample
sample_time = time_step

#setup and ideal signal
ideal = []

samples_per_symbol = round(UI / time_step)
symbol = 1

for i in range(0, length_of_array, 1):
    if(i % samples_per_symbol == 0):
        symbol = symbol * -1
    ideal.append(symbol)

plot_data(np.arange(0, length_of_array, 1), ideal)


#initializes non_ideal (jitter) array
non_ideal = np.zeros_like(ideal)

#populates non_ideal array to create TX jitter waveform
for symbol_index,symbol_epsilon in enumerate(epsilon):
    epsilon_duration = int(round(symbol_epsilon/sample_time))
    start = int(symbol_index*samples_per_symbol)
    end = int(start+epsilon_duration)
    flip=1
    if symbol_index==0:
        continue
    if symbol_epsilon<0:
        start,end=end,start
        flip=-1
        non_ideal[start:end]=flip*(ideal[symbol_index*samples_per_symbol-samples_per_symbol]-ideal[symbol_index*samples_per_symbol])
        
#calculate TX output waveform
jitter_signal = np.copy(non_ideal+ideal)

for x in range(0, len(jitter_signal), 1):
    if(jitter_signal[x]>1):
        jitter_signal[x]=1
    elif(jitter_signal[x]<-1):
        jitter_signal[x]=-1


plot_data(np.arange(0,length_of_array,1), jitter_signal)

jitter_diff = []

for x in range(0, length_of_array, 1):
    if(jitter_signal[x] != ideal[x]):
        jitter_diff.append(1)
    else:
        jitter_diff.append(0)

plot_data(np.arange(0,length_of_array,1), jitter_diff)

np.save("../logs/ideal.npy", ideal)
np.save("../logs/jitter.npy", jitter_signal)
