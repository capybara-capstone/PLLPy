"""Sim """
from components.pll import Pll
from utils.settings import Settings
import serdespy as sdp
import numpy as np

settings = Settings()
pll = Pll(settings=settings)

#set up paramaters
nyquist_f = 2e7
samples_per_symbol = 20
voltage_levels = np.array([0,1])

#pseudo-random data for simulation
data = sdp.prbs22(11)

#set up transmitter waveform
TX = sdp.Transmitter(data, voltage_levels, nyquist_f)
TX.oversample(samples_per_symbol)
print(type(TX.signal_ideal))
print(TX.signal_ideal)
data_in = TX.signal_ideal

#start CDR
pll.start_cdr(data_in)

#get recovered clock
pll.show(plot_type='web')
pll.save_to_file("./logs/")
pll_out = np.load("logs/VCO.npy")
print(pll_out)

# sample input datastream again with recovered clock (i.e PLL output log)
#todo

# send it to the decision circuit
#sdp.nrz_decision(x,t)

# compare with input datastream to get BER
#err = sdp.prbs_checker(10, data, decision)
#print("Bit Error Ratio = ", err[0]/(decision[10:-10].size*2))
            
