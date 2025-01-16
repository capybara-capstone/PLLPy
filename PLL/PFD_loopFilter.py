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

'''
#given in seconds - these will need to be defined globally at some point
time_step = 1e-9
stop_time = 1e-5
'''

def pfd(a, b, o, VDD, VSS, time_step, stop_time, state_vector):

    #cap
    C_one = 0.47e-9

    #transfer function definition
    numerator = [1.0,]
    denominator = [C_one, 0,]
    transferFunction = signal.TransferFunction(numerator, denominator)

    #make time array
    time_array = np.arange(0, stop_time, time_step)

    #gain
    gain_a = 2.5e-5
    gain_b = -2.5e-5
    c = []
    
    for i in range(0, len(a)):
        c.append(gain_a*float(a[i]) + gain_b*float(b[i]))

    for i in range(1, len(c)):
        inputArray= [c[i-1],c[i]]
        inputTime= [time_array[i-1], time_array[i]]
        time_out, signal_out, xout = signal.lsim(transferFunction, U=inputArray, T=inputTime, X0=state_vector)
        o.append(signal_out[1])
        state_vector=xout[1]
    return o, state_vector


