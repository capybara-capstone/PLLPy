"""Sim """
from components.pll import Pll
from utils.settings import Settings

settings = Settings()

# pll = Pll(settings=settings)
# pll.start()

pll = Pll(settings=settings)
pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'])

settings.lf['R'] = 8400
pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'])
