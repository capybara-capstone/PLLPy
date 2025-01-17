import math
import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', 'PLL')))

import divider 

#given in seconds
time_step = 1e-9
stop_time = 1e-5
# power and ground
VDD = 1
VSS = 0
#division value
N = 5

a = []
b = [0, 0, True, True]
o = []

number_of_elements = math.floor(stop_time / time_step)

# discretized input square wave
for i in range(0, number_of_elements):
    if (1+math.sin(i/math.floor(number_of_elements/70)))>1:
        a.append(VDD)
    else:
        a.append(VSS)
    o, b = divider.div(a[i], o, VDD, VSS, N, b)

original_signal = np.array(a)
divided_signal = np.array(o)

fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="pink")
axs[1].plot(divided_signal,color="blue")
plt.show()
