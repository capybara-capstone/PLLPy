# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:17:24 2024

@author: Sharmieka
"""

# power and ground
VDD = 1
VSS = 0

def div(input, o, VDD, VSS, N, stored_state):
    
    #counter_up = 0
    #counter_down = 0
    #toggle_count = N/2
    #toggle = True
    #ton = False


    #counter_up = stored_state[3]
    #counter_down = stored_state[4]
    #toggle_count = N/2
    #toggle = stored_state[2]
    #ton = stored_state[1]  
    
    a = [stored_state[0], input] #prev input, current input

    transition_count = stored_state[1]
    ton = stored_state[2]
    startFlag = stored_state[3]
    
    transition_count_max = 2*N
    transition_count_half = N


    if ((a[1] == VDD and a[0] == VSS) or (a[1] == VSS and a[0] == VDD)): #transition up or down
        if (transition_count == transition_count_max-1):
            transition_count = 0
            if (ton):
                o.append(VSS)
                ton = False
            else:
                o.append(VDD)
                ton = True     
        elif (transition_count == transition_count_half-1):
            transition_count +=1 
            if (ton):
                o.append(VSS)
                ton = False
            else:
                o.append(VDD)
                ton = True
        else: #unimportant transition
            transition_count +=1
            if ton == True: 
                o.append(VDD)
            else: 
                o.append(VSS) 

    else: # continue, not a transition
        if ton == True: 
            o.append(VDD)
        else: 
            o.append(VSS) 
                
    return o, [a[1], transition_count, ton, startFlag] 

