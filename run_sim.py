"""Sim """
from utils.sim import Sim



sim = Sim()
sim.add_pll()
sim.start()

# pll = Pll(settings=sett)
# pll.start()

# **UNIT TESTS**

# PFD unit test
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
