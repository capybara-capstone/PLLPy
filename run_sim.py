"""Sim """
from components.pll import Pll
from utils.settings import Settings
#import serdespy as sdp

settings = Settings()

pll = Pll(settings=settings)
data_in = sdp.prbs22(9) #an example
pll.start_cdr(data_in)

#pll = Pll(settings=settings)
#pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'])
pll.save_to_file("./logs/", 'CDR')

# get the PLL output log 
# sample input datastream again with recovered clock (i.e PLL output log)
# send it to the decision circuit
#sdp.nrz_decision(x,t)
# compare with input to get BER
            
