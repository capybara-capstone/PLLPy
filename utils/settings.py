"""Settings class"""
import os
from math import floor

# pylint: disable=C0301


class Settings:
    """Setting class"""

    def __init__(self,
                 name: str,
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-11,
                 sim_time: int = 6e-6):
        self.name = name
        self.sample_count = int(floor(sim_time/time_step))
        self.global_plot_mode = 'local'  # local web None
        self.vdd = vdd
        self.vss = vss
        self.time_step = time_step
        self.sim_time = sim_time
        self.log = {'log_path': os.path.join(os.getcwd(), 'logs')}
        self.clk = {'k_vco': 1.2566e8,
                    'fo': 1e7,
                    'plot_mode': self.global_plot_mode
                    }
        self.vco = {'k_vco': 6.2832e9,
                    'fo': 1000e6,
                    'plot_mode': self.global_plot_mode,
                    'id': 0
                    }
        self.divider = {'n': 60,
                        'plot_mode': self.global_plot_mode}
        self.lpd = {
            'plot_mode': self.global_plot_mode}
        self.lf = {'pull_up': 25e-6,
                   'pull_down': 25e-6,
                   'C': 16e-12,
                   'C2': 1.6e-12,
                   'R': 6400,
                   'id': 0,
                   'plot_mode': self.global_plot_mode
                   }
        self.pll = {
            'id': 0,
            'plot_mode': self.global_plot_mode}
