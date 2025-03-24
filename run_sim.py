"""Sim """
from components.pll import Pll
from utils.settings import Settings

settings = Settings(name='pll_example')

# pll = Pll(settings=settings)
# pll.start()

pll = Pll(settings=settings)
pll.start_and_monitor()
pll.show(plot_type=settings.pll['plot_mode'])
pll.save_to_file("./logs/")
