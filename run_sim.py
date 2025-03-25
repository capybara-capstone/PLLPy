"""Sim """
from components.pll import Pll
from utils.settings import Settings
from utils.calculator import Calculator
import numpy as np

settings = Settings(name='pll_example')

# pll = Pll(settings=settings)
# pll.start()

pll = Pll(settings=settings)
pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'], sim_type='PLL')
pll.save_to_file("./logs/")

calc = Calculator(settings=settings)

pll_out = np.load("./logs/VCO.npy")
result = calc.calculate_jitter(pll_out, start_time = 12e-6, stop_time = 24e-6) #[jitter, standard deviation]

print("Jitter: " + str(result[0]))
