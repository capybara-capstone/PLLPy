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
stop_time = 4e-6
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
k_vco = 1e9

#setup initial conditions
ref_clock_state_holder = 0
divider_state_holder = [0, False, True, 0, 0]

#setup lpd
lpd = LPD.LPD(0,0)

#MAIN loop
for i in range(0, number_of_elements):

    #reference clock
    ref_clock_state_holder = VCO.VCO([0], ref_clock_out, 1e9, ref_clock_state_holder)

    #LPD
    

    #Loop Filter

    #VCO

    #divider
    divider_out, divider_state_holder = divider.div(ref_clock_out[i],divider_out,VDD,VSS,2,100,divider_state_holder)


#plotting

ref_clock_out = np.array(ref_clock_out)
divider_out = np.array(divider_out)

fig, axs = plt.subplots(2)
axs[0].plot(ref_clock_out, color="red")
axs[1].plot(divider_out, color="green")


plt.show()
