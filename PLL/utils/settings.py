"""Settings class"""
from math import floor

# pylint: disable=C0301


class Settings:
    """Setting class"""

    def __init__(self,
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-11,
                 sim_time: int = 4e-6):
        self.sample_count = int(floor(sim_time/time_step))
        self.global_plot_mode = None  # local web None
        self.vdd = vdd
        self.vss = vss
        self.time_step = time_step
        self.sim_time = sim_time
        self.clk = {'k_vco': 1.2566e8,
                    'fo': 1e7,
                    'plot_mode': self.global_plot_mode
                    }
        self.vco = {'k_vco': 6.2832e9,
                    'fo': 1000e6,
                    'plot_mode': self.global_plot_mode}
        self.divider = {'n': 60,
                        'plot_mode': self.global_plot_mode}
        self.lpd = {
            'plot_mode': self.global_plot_mode}
        self.lf = {'pull_up': 25e-6,
                   'pull_down': 25e-6,
                   'R': None,
                   'C': 16e-12,
                   'plot_mode': self.global_plot_mode
                   }
        self.pll = {
            'plot_mode': self.global_plot_mode}
