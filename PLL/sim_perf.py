"""Sim """
import cProfile
import pstats
from pstats import SortKey
from components.pll import Pll
from components.vco import Vco
from components.lpd import Lpd
from components.lf import LoopFilter
from components.divider import Divider
from utils.settings import Settings


ob = cProfile.Profile()
ob.enable()

settings = Settings()

pll = Pll(settings=settings)
pll.start()

# pll = Pll(settings=settings)
# pll.start_and_monitor()
# pll.show(plot_type=settings.pll['plot_mode'])

# vco = Vco(settings=settings)
# vco.unit_test()

# lpd = Lpd(settings=settings)
# lpd.unit_test()

# lf = LoopFilter(settings=settings)
# lf.unit_test()

# div = Divider(settings=settings)
# div.unit_test()

ob.disable()
with open('single_test.txt', 'w', encoding='utf-8') as f:
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(ob, stream=f).sort_stats(sortby)
    ps.print_stats()
