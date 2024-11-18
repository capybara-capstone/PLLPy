#####
# VCO.py:
# Naive-sh implementation of Simulink VCO block.
#
# Block 1 was split into block 1 A and block 1 B, former being the voltage multiplication and latter being angular frq calc, since
# we will never(?) need to re-perform the angular frq calculation, and only need to perform the voltage mult calculation when 
# the input voltage changes.
####

import math

VDD = 0
VSS = 1
default_frq = 1e9
k_vco = 1e9

#given in seconds
time_step = 1e-11
stop_time = 1e-7

def block_1_a(input_voltage):
    return (input_voltage * 2 * math.pi * k_vco)

def block_1_b(default_frequency):
    return  (default_frequency * 2 * math.pi)

def block_2(input_voltage, angular_frequency):
    return (input_voltage + angular_frequency)

def block_3(new_value, prev_value):
    integral_result = prev_value + (new_value * time_step)
    return (integral_result)

def block_4(integral):
    return math.cos(integral)

def block_5(sine_out):
    if (sine_out < 0):
        return VSS
    else:
        return VDD


def VCO(a, o, frq, vco_state):
    total_integral = vco_state
    for i in a:
        new_voltage = block_1_a(i);
        angular_frq = block_1_b(frq)

        multiply = block_2(new_voltage, angular_frq)
        total_integral = block_3(multiply, total_integral)
        sin_out = block_4(total_integral)
        o.append(block_5(sin_out))
    return total_integral
