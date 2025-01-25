"""Settings class"""
import logging
import os
from simpy import Environment
import numpy as np


class Settings():
    """Setting class"""

    def __init__(self,
                 vdd: int = 1,
                 vss: int = 0,
                 time_step: int = 1e-9,
                 sim_time: int = 10e-6):
        self.env = Environment()
        self.vdd = vdd
        self.vss = vss
        self.paths = self.init_paths()
        self.time_step = time_step
        self.sim_time = sim_time
        self.clk = {'k_vco': 1.2566e8,
                    'fo': 1e7}
        self.vco = {'k_vco': 6.2832e9,
                    'fo': 1e6}
        self.divider = {'n': 3}
        self.pfd = {'gains': np.array([2.5e-5, -2.5e-5]),
                    'resistors': [],
                    'capacitors': [1.6e-11]
                    }
        self.lpd = {}
        self.components = {'clk': self.clk,
                           'vco': self.vco,
                           'divider': self.divider,
                           'pfd': self.pfd,
                           'lpd': self.lpd}

    def init_paths(self):
        """Populates paths dict
        Includes the path for outputs
        """
        base = os.getcwd()
        return {'base': base,
                'outputs': os.path.join(base, 'outputs'),
                }

    def get_running_dir(self):
        """Gets the running directory

        :returns: Returns the name of the running dir
        :rtype: None | str
        """
        output_dir = os.path.join(os.getcwd(), 'outputs')
        for output in os.listdir(output_dir):
            if output.startswith('RUNNING'):
                return os.path.join(output_dir,output)

        return None

    def get_logger(self, name):
        """Sets up a logger based on root

        It adds another file handler per module instance.

        :param name: Name of the module
        :type name: str
        """
        log = logging.getLogger(name)
        run_path = None
        for run in os.listdir(self.paths['outputs']):
            if run.startswith('RUNNING'):
                run_path = os.path.join(
                    self.paths['outputs'], run, f'{name}.log')

        fh = logging.FileHandler(run_path)
        fh.setLevel(logging.DEBUG)
        log.addHandler(fh)
        return log
