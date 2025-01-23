from simpy import Environment
import numpy as np


class Settings():
    def __init__(self,
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-9,
                 sim_time: int = 10e-6):
        self.env = Environment()
        self.vdd = vdd
        self.vss = vss
        self.time_step = time_step
        self.sim_time = sim_time
        self.clk = {'k_vco': 1.2566e8,
                    'fo': 1e7}
        self.vco = {'k_vco': 6.2832e9,
                    'fo': 1e6}
        self.dividor = {'n': 5}
        self.pfd = {'gains': np.array([2.5e-5, -2.5e-5]),
                    'resistors': [],
                    'capacitors': [1.6e-11]
                    }
        self.lpd = {}
        self.components = {'clk': self.clk,
                           'vco': self.vco,
                           'dividor': self.dividor,
                           'pfd': self.pfd,
                           'lpd': self.lpd}
