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
stop_time = 10e-6
#number_of_elements = math.floor(stop_time / time_step)
number_of_elements = 6000
#input array
a = []

#output arrays
ref_clock_out = []
lpd_out = []
loop_filter_out = []
vco_out = []
divider_out = []

#for debug
gain = []

#globals needed for VCO
k_vco = 6.2832e9
k_vco_ref = 1.2566e8

#setup initial conditions
ref_clock_state_holder = 0
divider_state_holder = [0, 0, False, True]
loop_filter_state_holder = 0
filter_previous_sample1 = 0
filter_previous_sample2 = 0
feedback = 0
vco_state_holder = 0

#setup lpd
lpd = LPD.LPD([0],[0])

#MAIN loop
#use textbook value for parameters (there is a calculation you can use for ideal) - if the parameters are weird your values will be weird.
for i in range(0, number_of_elements):

    #reference clock

    ref_clock_state_holder = VCO.VCO([0], ref_clock_out, 1e7, ref_clock_state_holder, k_vco_ref)


    #LPD
    lpd.get_wave_diff(ref_clock_out[i], feedback) 

    #Loop Filter
    loop_filter_out, loop_filter_state_holder, gain = PFD_loopFilter.pfd([filter_previous_sample1, lpd.out[i]], [filter_previous_sample2, lpd.out2[i]], loop_filter_out, VDD, VSS, time_step, stop_time, loop_filter_state_holder)
    filter_previous_sample1 = lpd.out[i]
    filter_previous_sample2 = lpd.out2[i]

    #VCO
    vco_state_holder = VCO.VCO([loop_filter_out[i]], vco_out, 1e6, vco_state_holder, k_vco)

    #divider
    divider_out, divider_state_holder = divider.div(vco_out[i], divider_out, VDD, VSS, 3, divider_state_holder)
    
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

fig, axs = plt.subplots(4)



axs[0].title.set_text("Divider")
axs[0].plot(divider_out, color="green")

axs[1].title.set_text("Loop Filter")
axs[1].plot(loop_filter_out, color="green")

axs[2].title.set_text("Voltage Controlled Oscillator")
axs[2].plot(vco_out, color="green")

axs[3].title.set_text("REFCLK")
axs[3].plot(ref_clock_out, color="green")


plt.show()
