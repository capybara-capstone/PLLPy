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
N = 4 

def div(a, b, o, VDD, VSS, number_of_elements, N):
    
    counter_up = 0
    counter_down = 0
    toggle_count = N/2
    toggle = True
    ton = False

    for i in range(0, number_of_elements):

        if i == 0:
            o.append(a[0])
        
        elif a[i] == VDD and a[i-1] == VSS:
            if toggle == True: #cleared or starting
                if ton == True: 
                    o.append(VSS)
                    ton = False
                else: 
                    o.append(VDD)
                    ton = True
                toggle = False
                counter_up = 0
                counter_down = 0
            counter_up = counter_up + 1 #transition up
    
        elif a[i] == VSS and a[i-1] == VDD:
            counter_down = counter_down + 1 #transition down
            if ton == True: o.append(VDD)
            else: o.append(VSS) #continue
            if counter_down == toggle_count: toggle = True
            
        else: 
            if ton == True: o.append(VDD)
            else: o.append(VSS) #continue
    return o

# TEST

a = []
b = []
o = []

number_of_elements = math.floor(stop_time / time_step)

# discretized input square wave
for i in range(0, number_of_elements):
    if (1+math.sin(i/math.floor(number_of_elements/70)))>1:
        a.append(VDD)
    else:
        a.append(VSS)
    
o = div(a, b, o, VDD, VSS, number_of_elements, N)

original_signal = np.array(a)
divided_signal = np.array(o)

fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="pink")
axs[1].plot(divided_signal,color="blue")
plt.show()