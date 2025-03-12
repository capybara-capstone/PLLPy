#This will be a class for calculators (eventually, for now it's a mess)

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import math

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



pll_out = np.load("../logs/VCO.npy")
pll_time = np.load("../logs/TIME.npy")
offset_freq = 500E6
time_step = 1E-11
divider_n = 60
clk_freq = 1E7

target_freq = divider_n*clk_freq


#plot_data(pll_out, pll_time)

print(len(pll_out))

out_sample = []
time_sample = []

for i in range(30000,40000,1):
    out_sample.append(pll_out[i])
    time_sample.append(pll_time[i])

pll_fft = fft(out_sample)
pll_fftfreq = fftfreq(len(pll_fft), time_step)

pll_fft = pll_fft**2

for x in range(0, len(pll_fft), 1):
    pll_fft[x] = abs(pll_fft[x])

#plot_data(pll_fftfreq, abs(pll_fft))
#plot_data(pll_time, pll_out)
max_index = 0
last_max = 0

for x in range(1, math.floor(len(pll_fft)/2), 1):
    if(pll_fft[x] > last_max):
        last_max = pll_fft[x]
        max_index = x

print(max_index)
print(pll_fftfreq[max_index])

#how many samples is offset frequency?
i = 1

while(pll_fftfreq[i] <= offset_freq):
    i = i + 1

print(i)

centred_spike = []
centred_spike_freq = []

for x in range(max_index - i, max_index + i, 1):
    centred_spike.append(pll_fft[x])
    centred_spike_freq.append(pll_fftfreq[x])

plot_data(centred_spike_freq, centred_spike)

#integrate
integral_result = 0

for x in range(max_index, len(centred_spike), 1):
    integral_result = integral_result + (centred_spike[x] * (centred_spike_freq[x] - centred_spike_freq[x-1]))

integral_result = abs(integral_result)

#calculate jitter

jitter =((1/pll_fftfreq[max_index])/(2*math.pi))*math.sqrt(integral_result)

print(jitter)
