import math
import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', 'PLL')))

import PFD_loopFilter 
import VCO
# TEST

#power and ground
VDD = 1
VSS = 0

#given in seconds - these will need to be defined globally at some point
time_step = 1e-9
stop_time = 1e-5

a = []
b = []
o = []
c = []
number_of_elements = math.floor(stop_time / time_step)

#set up test signal (square wave) - ideally we'll see the square wave be rounded by the filter
for i in range(0, number_of_elements):
    if (1+math.sin(i/math.floor(number_of_elements/31)))>1:
        a.append(VDD)
    else:
        a.append(VSS)
for i in a:
    if i == VDD:
        b.append(VSS)
    elif i == VSS:
        b.append(VDD)

state_vector = 0

o, state_vector, c = PFD_loopFilter.pfd(a, b, o, VDD, VSS, time_step, stop_time, state_vector)

o.append(o[len(o)-1])


original_signal = np.array(a)
down_signal = np.array(b)
output_pfd = np.array(o)
gain = np.array(c)
fig, axs = plt.subplots(4)

axs[0].title.set_text("UP")
axs[0].plot(original_signal,color="purple")


axs[1].title.set_text("DOWN")
axs[1].plot(down_signal,color="purple")

axs[2].title.set_text("Output")
axs[2].step(np.array(range(0, number_of_elements)),output_pfd,color="purple")

axs[3].title.set_text("Gain")
axs[3].step(np.array(range(0, number_of_elements)),gain,color="red")
plt.show()
