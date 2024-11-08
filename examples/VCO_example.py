import math
import numpy as np
import matplotlib.pyplot as plt
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', 'PLL')))

import VCO

VDD = 0
VSS = 1
default_frq = 1e6
k_vco = 1e6

#given in seconds
time_step = 1e-9
stop_time = 1e-5

# Test?
a = []
o = []
number_of_elements = math.floor(stop_time / time_step)

for i in range(0, number_of_elements):
    a.append(1+math.sin(i/math.floor(number_of_elements/10)))
    #a.append(1)

VCO.VCO(a, o, default_frq)

original_signal = np.array(a)
output_VCO = np.array(o)
fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="red")
axs[1].step(np.array(range(0, number_of_elements)),output_VCO,color="blue")

plt.show()