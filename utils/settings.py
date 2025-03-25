"""Settings class"""
import os
from math import floor

# pylint: disable=C0301


class Settings:
    """Setting class"""

    def __init__(self,
                 name: str,
                 log_path:str,
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-11,
                 sim_time: int = 6e-6):
        self.name = name
        self.sample_count = int(floor(sim_time/time_step))
        self.global_plot_mode = 'None'  # local web None
        self.vdd = vdd
        self.vss = vss
        self.time_step = time_step
        self.sim_time = sim_time
        self.log = {'log_path': log_path}
        self.clk = {'k_vco': 1.2566e8,
                    'fo': 1e7,
                    'plot_mode': self.global_plot_mode
                    }
        self.vco = {'k_vco': 6.2832e9,
                    'fo': 1000e6,
                    'plot_mode': self.global_plot_mode
                    }
        self.divider = {'n': 60,
                        'plot_mode': self.global_plot_mode}
        self.lpd = {
            'plot_mode': self.global_plot_mode}
        self.lf = {'pull_up': 25e-6,
                   'pull_down': 25e-6,
                   'C': 16e-12,
                   'C2': None,
                   'R': None,
                   'plot_mode': self.global_plot_mode
                   }
        self.pll = {
            'id': 0,
            'plot_mode': self.global_plot_mode}

    def set_global_plot_mode(self, mode: str):
        """Sets plot mode"""
        self.global_plot_mode = mode

    def set_name(self, name: str):
        """Sets settings name"""
        self.name = name

    def set_vdd(self, vdd):
        """Sets vdd value"""
        self.vdd = vdd

    def set_vss(self, vss):
        """Sets vss value"""
        self.vss = vss

    def set_log_path(self, path: str):
        """Sets logs path"""
        self.log['log_path'] = path

    def set_time(self, sim_time: int, time_step: int):
        """Updates time parameters"""
        self.sim_time = sim_time
        self.time_step = time_step
        self.sample_count = int(floor(sim_time/time_step))

    def set_vco_parameter(self, parameter: str, value):
        """Updates vco parameters

        If parameter is "all" then value is a dict replacing all the values.
        Else it checks if the specified parameter is part of the settings and upadates it.
        """
        if parameter == 'all':
            self.vco = value
            return f'Updated LF settings to {self.vco}'
        if parameter in self.vco.keys():
            self.vco[f'{parameter}'] = value
            return f'Updated VCO {parameter} to {value}'
        return f'Parameter does not exist in VCO settings\nAvailable settings are {self.vco.keys()}'

    def set_clk_parameter(self, parameter: str, value):
        """Updates vco parameters

        If parameter is "all" then value is a dict replacing all the values.
        Else it checks if the specified parameter is part of the settings and upadates it.
        """
        if parameter == 'all':
            self.clk = value
            return f'Updated CLK settings to {self.clk}'

        if parameter in self.clk.keys():
            self.clk[f'{parameter}'] = value
            return f'Updated CLK {parameter} to {value}'
        return f'Parameter does not exist in CLK settings\nAvailable settings are {self.vco.keys()}'

    def set_lf_parameter(self, parameter: str, value):
        """Updates vco parameters

        If parameter is "all" then value is a dict replacing all the values.
        Else it checks if the specified parameter is part of the settings and upadates it.
        """
        if parameter == 'all':
            self.lf = value
            return f'Updated LF settings to {self.lf}'
        if parameter in self.lf.keys():
            self.lf[f'{parameter}'] = value
            return f'Updated LF {parameter} to {value}'
        return f'Parameter does not exist in LF settings\nAvailable settings are {self.lf.keys()}'

    def set_divider_parameter(self, parameter: str, value):
        """Updates vco parameters

        If parameter is "all" then value is a dict replacing all the values.
        Else it checks if the specified parameter is part of the settings and upadates it.
        """
        if parameter == 'all':
            self.divider = value
            return f'Updated Divider settings to {self.lf}'
        if parameter in self.lf.keys():
            self.divider[f'{parameter}'] = value
            return f'Updated Divider {parameter} to {value}'
        return f'Parameter does not exist in LF settings\nAvailable settings are {self.divider.keys()}'
