# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:17:24 2024

@author: Sharmieka
"""

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
