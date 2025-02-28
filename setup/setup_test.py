"""Setup Run"""
import sys
from components.pll import Pll
from components.vco import Vco
from components.lpd import Lpd
from components.lf import LoopFilter
from components.divider import Divider
from utils.settings import Settings

settings = Settings()

vco = Vco(settings=settings)
if vco.unit_test() != 0:
    sys.exit(-1)

lpd = Lpd(settings=settings)
if lpd.unit_test() != 0:
    sys.exit(-1)


lf = LoopFilter(settings=settings)
if lf.unit_test() != 0:
    sys.exit(-1)

div = Divider(settings=settings)
if div.unit_test() != 0:
    sys.exit(-1)

pll = Pll(settings=settings)
pll.start()
