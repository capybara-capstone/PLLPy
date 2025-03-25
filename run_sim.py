"""Sim """
from components.pll import Pll
from utils.settings import Settings
from utils.calculator import Calculator
from utils.sweeper import Sweeper
import numpy as np

settings = Settings(name='pll_example', log_path='./logs')

# pll = Pll(settings=settings)
# pll.start()

# simulate PLL
pll = Pll(settings=settings)
# swp = Sweeper(pll=pll, id=1)

# swp.start(block='lf', parameter='R', values=[None, '8400', '6400'])


pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'], sim_type='PLL')
# pll.save_to_file("./logs/")

# calculate jitter
# calc = Calculator(settings=settings)
# pll_out = np.load("./logs/VCO.npy")
# result = calc.calculate_jitter(pll_out, start_time = 12e-6, stop_time = 24e-6)

# print("Jitter: " + str(result[0]))
