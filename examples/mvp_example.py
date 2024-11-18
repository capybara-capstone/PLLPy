import matplotlib.pyplot as plt
import numpy as np
import math
import os, sys


sys.path.insert(0, os.path.abspath(os.path.join('..','PLL')))


import VCO
import LPD
import PFD_loopFilter
import divider


#setting up some globals
VDD = 1
VSS = 0
time_step = 1e-11
stop_time = 1e-6
number_of_elements = math.floor(stop_time / time_step)

#input array
a = []

#output arrays
ref_clock_out = []
lpd_out = []
loop_filter_out = []
vco_out = []
divider_out = []

#globals needed for VCO
k_vco = 6.2832e9

#setup initial conditions
ref_clock_state_holder = 0
divider_state_holder = [0, False, True, 0, 0]
loop_filter_state_holder = 0
filter_previous_sample1 = 0
filter_previous_sample2 = 0
feedback = 0
vco_state_holder = 0

#setup lpd
lpd = LPD.LPD([0],[0])

#MAIN loop
for i in range(0, number_of_elements):

    #reference clock
    ref_clock_state_holder = VCO.VCO([0], ref_clock_out, 1.2566e8, ref_clock_state_holder)

    #LPD
    lpd.get_wave_diff(ref_clock_out[i], feedback) 

    #Loop Filter
    loop_filter_out, loop_filter_state_holder = PFD_loopFilter.pfd([filter_previous_sample1, lpd.out[i]], [filter_previous_sample2, lpd.out2[i]], loop_filter_out, VDD, VSS, time_step, stop_time, loop_filter_state_holder)
    filter_previous_sample1 = lpd.out[i]
    filter_previous_sample2 = lpd.out2[i]

    #VCO
    vco_state_holder = VCO.VCO([loop_filter_out[i]], vco_out, 1000e6, vco_state_holder)

    #divider
    divider_out, divider_state_holder = divider.div(vco_out[i],divider_out,VDD,VSS,2,20,divider_state_holder)
    
    #feedback
    feedback = divider_out[i]


#plotting

ref_clock_out = np.array(ref_clock_out)
divider_out = np.array(divider_out)
loop_filter_out = np.array(loop_filter_out)
vco_out = np.array(vco_out)

print(len(ref_clock_out))
print(len(divider_out))
print(len(lpd.out))
print(len(lpd.out2))
print(len(loop_filter_out))
print(len(vco_out))

fig, axs = plt.subplots(6)
axs[0].plot(ref_clock_out, color="red")
axs[1].plot(divider_out, color="green")
axs[2].plot(lpd.out, color="blue")
axs[3].plot(lpd.out2, color="blue")
axs[4].plot(loop_filter_out, color="purple")
axs[5].plot(vco_out, color="pink")


plt.show()
