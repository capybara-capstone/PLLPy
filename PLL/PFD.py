#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:36:58 2024

@author: nanik
"""

import numpy as np
from scipy import signal
import math
import matplotlib.pyplot as plt

#power and ground
VDD = 1
VSS = 0


#given in seconds - these will need to be defined globally at some point
time_step = 1e-9
stop_time = 1e-5
time_array = np.arange(0,1e-5,1e-9)

#CAP
C_one = 1.6e-11





def pfd(a, time_array, o):
    #transfer function defined ([numerator], [denominator], time step)
    transferFunction = ([1.0,], [C_one, 0,], time_step)
    initialConditions = 0
    
    for i in range(0, math.floor(stop_time/time_step)):
        time_out, signal_out = signal.dlsim(transferFunction, a[i], time_array[i], initialConditions)
        o.append(signal_out[0])
        initialConditions = signal_out[0]



# TEST

a = []
o = []
number_of_elements = math.floor(stop_time / time_step)

#set up test signal (square wave) - ideally we'll see the square wave be rounded by the filter
for i in range(0, number_of_elements):
    if (1+math.sin(i/math.floor(number_of_elements/20)))>1:
        a.append(VDD)
    else:
        a.append(VSS)

pfd(a, time_array, o)
    

original_signal = np.array(a)
output_pfd = np.array(o)
fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="purple")
axs[1].step(np.array(range(0, number_of_elements)),output_pfd,color="yellow")

plt.show()