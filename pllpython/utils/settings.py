"""Settings class"""
import os
import json
import numpy as np
from math import floor

# pylint: disable=C0301


class Settings:
    """Setting class"""

    def __init__(self,
                 name: str,
                 log_path: str = './',
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-11,
                 sim_time: int = 24e-6):
        self.name = name
        self.sample_count = int(floor(sim_time/time_step))
        self.global_plot_mode = 'local'  # local web None
        self.vdd = vdd
        self.vss = vss
        self.time_step = time_step
        self.sim_time = sim_time
        self.time_array = np.arange(0, self.sim_time, self.time_step)
        self.log = {'log_path': log_path}
        self.clk = {'k_vco': 20e6,
                    'fo': 0,
                    'white_phase_noise_spectral_density': 3e-10,
                    'low_frequency_phase_noise': 0,
                    'plot_mode': self.global_plot_mode
                    }
        self.vco = {'k_vco': 1e9,
                    'fo': 1000e6,
                    'white_phase_noise_spectral_density': 0,
                    'low_frequency_phase_noise': 0,
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
                   'R': 8400,
                   'id': 0,
                   'max_sat': None,
                   'min_sat': None,
                   'plot_mode': self.global_plot_mode
                   }
        self.pll = {
            'id': 0,
            'plot_mode': self.global_plot_mode}

    def update_from_file(self, setting_file_path: str):
        """
        Dynamically updates settings from a JSON file

        Args:
            setting_file_path (str): Path to the JSON file containing settings

        Returns:
            str: Status message of the update process
        """
        try:
            if not os.path.isfile(setting_file_path):
                raise FileNotFoundError
            with open(setting_file_path, 'r') as file:
                update_settings = json.load(file)

            def deep_update(original, update):
                """
                Recursively update nested dictionaries or lists

                Args:
                    original: Original value to be updated
                    update: New value to update with

                Returns:
                    Updated value
                """
                if update == "None":
                    return None

                if isinstance(original, dict) and isinstance(update, dict):
                    for key, value in update.items():
                        original[key] = deep_update(
                            original.get(key, {}), value)
                    return original

                if isinstance(original, list) and isinstance(update, list):
                    return original + update

                return update

            for key, value in update_settings.items():
                if key in ['time_step', 'sim_time']:
                    setattr(self, key, value)
                    if hasattr(self, 'time_step') and hasattr(self, 'sim_time'):
                        self.sample_count = int(
                            floor(self.sim_time / self.time_step))
                        self.time_array = np.arange(
                            0, self.sim_time, self.time_step)
                else:
                    current_value = getattr(self, key, {})
                    updated_value = deep_update(current_value, value)
                    setattr(self, key, updated_value)

            return "Settings updated successfully"

        except FileNotFoundError:
            return f"Error: File not found at {setting_file_path}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON file at {setting_file_path}"
        except Exception as e:
            return f"Unexpected error updating settings: {str(e)}"

    def get_settings(self):
        """
        Dynamically retrieve all current settings

        Returns:
            dict: Current settings of the instance
        """
        # Get all attributes except built-in and private ones
        settings = {
            key: getattr(self, key)
            for key in dir(self)
            if not key.startswith('__') and
            not callable(getattr(self, key))
        }
        return settings

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
