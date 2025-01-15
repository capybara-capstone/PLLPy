# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:17:24 2024

@author: Sharmieka
"""

import numpy as np
import matplotlib.pyplot as plt
import math

time_step = 1e-9
stop_time = 1e-5

# power and ground
VDD = 1
VSS = 0

# Divider ratio
N = 6


def div(a, o, VDD, VSS, number_of_elements, N):
    
    transition_up_count = 0
    transition_up_count_half = N-(1*(N//2)-1)
    transition_up_count_max = N+1 # same for even and odd
    transition_down_count = 0 # down does not matter for even
    transition_down_count_half = 0 
    ton = True
    isOdd = False
    
    if (N%2 != 0):
        isOdd = True
        transition_down_count_half = N-(1*(N//2))
        
    for i in range(0, number_of_elements):

        if i == 0:
            o.append(a[0]) # starting 
        
        elif a[i] == VDD and a[i-1] == VSS:
            transition_up_count = transition_up_count + 1
            if (isOdd):
                if transition_up_count == transition_up_count_max:
                    ton = True 
                    transition_up_count = 1 # first of new cycle for odd N
                    transition_down_count = 0   
            elif (not isOdd):
                if transition_up_count == transition_up_count_half:
                    ton = False
                elif transition_up_count == transition_up_count_max:
                    ton = True
                    transition_up_count = 1 # first of new cycle for even N
                    transition_down_count = 0
            if ton == True: 
                o.append(VDD)
            else: 
                o.append(VSS) 
    
        elif a[i] == VSS and a[i-1] == VDD:
            transition_down_count = transition_down_count + 1
            if (isOdd):
                if transition_down_count == transition_down_count_half:
                    ton = False
            if ton == True: # also not isOdd
                o.append(VDD)
            else: 
                o.append(VSS) 
            
        else: # continue
            if ton == True: 
                o.append(VDD)
            else: 
                o.append(VSS) 
    return o

# TEST

a = []
b = []
o = []

number_of_elements = math.floor(stop_time / time_step)

# discretized input square wave
for i in range(0, number_of_elements):

    if (1+math.sin(i/math.floor(number_of_elements/50)))>1:

        a.append(VDD)
    else:
        a.append(VSS)
    
o = div(a, o, VDD, VSS, number_of_elements, N)

original_signal = np.array(a)
divided_signal = np.array(o)
print(len(o))
print(len(a))
fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="pink")
axs[1].plot(divided_signal,color="blue")
plt.show()