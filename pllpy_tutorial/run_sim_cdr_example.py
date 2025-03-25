"""Sim """
from PLLPY.components.pll import Pll
from PLLPY.utils.settings import Settings
import serdespy as sdp
import numpy as np

settings = Settings(name='CDR_example')
pll = Pll(settings=settings)
settings.update_from_file(setting_file_path='./unit_tests/ut_sett.json')
print(settings.get_settings())
# set up paramaters
nyquist_f = 2e7
samples_per_symbol = 64
voltage_levels = np.array([0, 1])

# pseudo-random data for simulation, an example
data = sdp.prbs13(22)

# set up transmitter waveform
TX = sdp.Transmitter(data, voltage_levels, nyquist_f)
TX.oversample(samples_per_symbol)
data_in = TX.signal_ideal

# start CDR
pll.start_and_monitor()
pll_out = np.array(pll.output)

# sample input datastream again with recovered clock (i.e PLL output log) on rising edge and send it to the decision circuit
trigger_val = 0.5
threshold = 0.5
rising_edge = np.flatnonzero(
    (pll_out[:-1] < trigger_val) & (pll_out[1:] > trigger_val))+1
retimed_data = []

for i in range(len(rising_edge)):
    retimed_data.append(sdp.nrz_decision(data_in[rising_edge[i]], threshold))

print(len(pll.settings.time_array))

pll.show(plot_type='web',
         sim_type='CDR',
         input=data_in[:len(pll.settings.time_array)])

# compare retimed data with input datastream to get BER
err = sdp.prbs_checker(13, data[:len(retimed_data)-1], np.array(retimed_data))
if not isinstance(err, bool):
    print("Bit Error Ratio = ", err[0]/len(retimed_data))
