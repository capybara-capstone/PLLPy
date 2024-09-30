#####
# VCO.py:
# Naive-sh implementation of Simulink VCO block.
#
# Block 1 was split into block 1 A and block 1 B, former being the voltage multiplication and latter being angular frq calc, since
# we will never(?) need to re-perform the angular frq calculation, and only need to perform the voltage mult calculation when 
# the input voltage changes.
####

import math
import numpy as np
import matplotlib.pyplot as plt

VDD = 1
VSS = 0
default_frq = 1e6

def block_1_a(input_voltage):
    return (input_voltage * 2 * math.pi)

def block_1_b(default_frequency):
    return  default_frequency * 2 * math.pi

def block_2(input_voltage, angular_frequency):
    return (input_voltage * angular_frequency)

def block_3(new_value, prev_value):
    return (new_value + prev_value)

def block_4(integral):
    return math.cos(integral)

def block_5(sine_out):
    if (sine_out < 0):
        return VSS
    else:
        return VDD


def VCO(a, o, frq):
    total_integral = 0;
    for i in range(0, 100):
        new_voltage = block_1_a(a[i]);
        angular_frq = block_1_b(frq)

        multiply = block_2(new_voltage, angular_frq)
        total_integral = block_3(multiply, total_integral)
        sin_out = block_4(total_integral)
        o.append(block_5(sin_out))

# Test?
a = []
o = []

for i in range(0, 100):
    a.append(math.sin(i/10))

VCO(a, o, default_frq)

original_signal = np.array(a)
output_VCO = np.array(o)
fig, axs = plt.subplots(2)
axs[0].plot(original_signal,color="red")
axs[1].step(np.array(range(0, 100)),output_VCO,color="blue")

plt.show()




