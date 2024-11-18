# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:17:24 2024

@author: Sharmieka
"""

# power and ground
VDD = 1
VSS = 0

def div(a, o, VDD, VSS, number_of_elements, N, stored_state):
    
    #counter_up = 0
    #counter_down = 0
    #toggle_count = N/2
    #toggle = True
    #ton = False


    counter_up = stored_state[3]
    counter_down = stored_state[4]
    toggle_count = N/2
    toggle = stored_state[2]
    ton = stored_state[1]
    
    a = [stored_state[0], a]


    input_ton = 1 #default is no extension
    if toggle_count.is_integer() == False:
        toggle_count = toggle_count - 0.5
        input_ton = 0 #get number of samples to extend
        
    for i in range(1, number_of_elements):

        if i == 0:
            o.append(a[0])
        
        elif a[i] == VDD and a[i-1] == VSS:
            if toggle == True: #cleared or starting
                if ton == True: 
                  
                    #append half ton times more
                    o.extend([VDD] * input_ton)
                    o.append(VSS)
                    ton = False
                else: 
                    #o.append(VDD)
                    o.extend([VSS] * input_ton)

                    o.append(VDD)
                    ton = True
                toggle = False
                counter_up = 0
                counter_down = 0
            else:
                if ton:
                    o.append(VDD)
                else:
                    o.append(VSS)
            counter_up = counter_up + 1 #transition up
    
        elif a[i] == VSS and a[i-1] == VDD:
            counter_down = counter_down + 1 #transition down

            if input_ton == 0: input_ton = i

            if ton == True: o.append(VDD)
            else: o.append(VSS) #continue
            if counter_down == toggle_count: toggle = True
            
        else: 
            if ton == True: o.append(VDD)
            else: o.append(VSS) #continue
    return o, [a[1], ton, toggle, counter_up, counter_down] 

