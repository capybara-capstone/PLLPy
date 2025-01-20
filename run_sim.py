import simpy
from components.pll import Pll
from components.settings import Settings
from components.divider import Divider
from components.lpd import Lpd
from components.vco import Vco
from components.pfd import Pfd

env = simpy.Environment()
sett = Settings()
pll = Pll(settings=sett)
pll.start()

# **UNIT TESTS**

# # PFD unit test
# pfd = Pfd(env)
# pfd.unit_test()
# env.run(until=1e-5)
# pfd.show(plot=True)

# # LPD unit test
# lpd = Lpd(env)
# lpd.unit_test()
# env.run(until=1e-5)
# lpd.show(plot=True)

# # VCO unit test
# vco = Vco(env)
# vco.unit_test()
# env.run(until=1e-5)
# vco.show(plot=True)

# # Divider unit test
# div = Divider(env)
# div.unit_test()
# env.run(until=1e-5)
# div.show(plot=True)
