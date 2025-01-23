"""Sim class"""
import logging
import logging.config
import configparser
import os
from datetime import datetime
import time
from tqdm import tqdm
from components.pll import Pll
from components.settings import Settings
from components.divider import Divider
# pylint: disable=W0718


class Sim():
    """Sim class"""

    def __init__(self, name='SIM'):
        self.settings = None
        self.name = name
        self.log = None
        self.components = {}
        self.sim_setup()
        self.env = self.settings.env

    def sim_setup(self):
        """Setups elements before sim starts"""
        # Logger setup
        logger_config_path = os.path.join(os.getcwd(), 'utils', 'logging.ini')
        config = configparser.ConfigParser()
        config.read(logger_config_path)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_output = os.path.join(
            os.getcwd(), 'outputs', f'RUNNING - {current_time}')
        os.makedirs(current_output, exist_ok=True)
        sim_path = os.path.join(current_output, 'sim.log')
        config.set('handler_fileHandler', 'args', f"('{sim_path}',)")
        with open(logger_config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        self.settings = Settings()
        logging.config.fileConfig(os.path.join(logger_config_path))
        self.log = logging.getLogger(self.name)

    def add_components(self, component):
        """Adds component instance to PLL components dict

        :param components: Components instances to be added
                           Index is the components name.
        :type components: object | list[Object]
        """
        try:
            self.components[component.name] = component
            self.log.info('Component %s added to %s',
                          component.name, self.name)
        except Exception as e:
            self.log.error(
                'Component %s NOT added to %s', component.name, self.name)
            self.log.error('ERROR: %s', e)

        return component

    def progress(self):
        """Progress bar logic"""
        progress_bar = tqdm(total=self.settings.sim_time/self.settings.time_step,
                            desc='LOCKING PLL',
                            position=0)
        while True:
            progress_bar.update(1)
            yield self.env.timeout(self.settings.time_step)

    def add_divider(self, name: str = None):
        """Adds a divider to the simulation"""
        divider = Divider(self.env)
        if name is not None:
            divider.name = name
        self.add_components(component=divider)

    def add_pll(self, name: str = None):
        """Adds pll to similation"""
        pll = Pll(self.settings)
        if name is not None:
            pll.name = name
        self.add_components(component=pll)

    def start(self):
        """Starts simulation"""
        for component in self.components.values():
            if isinstance(component, Pll):
                print('STARTING SIMULATION')
                # start_time = time.time()
                self.env.process(self.progress())
                component.start()
                end_time = time.time()
                output_dir = os.path.join(os.getcwd(), 'outputs')
                for output in os.listdir(output_dir):
                    if output.startswith('RUNNING'):
                        finished_path = os.path.join(
                            output_dir, output.replace('RUNNING - ', 'FINISHED - '))
                        os.rename(os.path.join(output_dir, output),
                                  finished_path)
                # print('SIMULATION FINISHED')
                # elapsed = end_time - start_time
                # print(f'Total simulation time {elapsed:.2f} Seconds')
            else:
                component.unit_test()
                self.env.run(until=self.settings.sim_time)
                component.show(plot=True)
