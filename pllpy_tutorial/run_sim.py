from PLLPY.utils.settings import Settings
from PLLPY.components.pll import Pll
from PLLPY.utils.sweeper import Sweeper
from PLLPY.utils.calculator import Calculator
import numpy as np

settings = Settings(name='pll_example')
settings.set_global_plot_mode(mode='local')
calc = Calculator(settings=settings)

# PLL
pll = Pll(settings=settings)
pll.start_and_monitor()
pll.show()

# Jitter Calculator
result = calc.calculate_jitter(
    np.array(pll.output), start_time=12e-6, stop_time=24e-6)
pll.log.info('Jitter %s', result)
print(f'Jitter: {result}')

# Sweeper
settings.set_lf_parameter(parameter='C2', value=None)
sweep = Sweeper(pll=pll, id=1)
sweep.start(block='lf', parameter='R', values=[None, '8400', '6400'])
