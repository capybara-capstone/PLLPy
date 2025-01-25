"""Divider Class"""
import math
from bokeh.plotting import show
from bokeh.layouts import gridplot
from components.settings import Settings
from components.buffer import Buffer

# pylint: disable=W1203


class Divider(Settings):
    """Models Feedback divider"""

    def __init__(self, settings: Settings):
        super().__init__()
        # Set up the environment 
        self.env = settings.env
        
        # Set immutable variables, get the divider value from the settings
        self.n = settings.divider["n"]
        self.name = 'Divider'
        self.log = None

        # In/out buffers
        self.input = Buffer(env=self.env, name=f'N={self.n} Divider Input')
        self.output = Buffer(env=self.env, name=f'N={self.n} Divider Output')

        # State variables
        self.transition_count = 0
        self.ton = False
        self.last_sample = 0
        self.setup()

    def setup(self):
        """Set up divider"""
        self.log = self.get_logger(self.name)
        self.log.info('Divider created with name %s and N %d',
                      self.name, self.n)

    def start(self):
        """Continous loop handling transition logic"""
        self.log.info('Starting %s',self.name)
        # self.last_sample = yield self.input.buffer.get()
        while True:
            current_sample = yield self.input.buffer.get()
            added = None
            self.log.debug(f'@{self.env.now}| {self.name} got sample {current_sample}')
            if (self.last_sample == self.vdd and current_sample == self.vss
                ) or (self.last_sample == self.vss and current_sample == self.vdd):
                if self.transition_count in (self.n * 2-1, self.n-1):
                    self.transition_count = 0 if self.transition_count == (
                        self.n * 2) - 1 else self.transition_count + 1
                    self.ton = not self.ton
                    self.output.put(self.vss if self.ton else self.vdd)
                    added = self.vss if self.ton else self.vdd
                else:
                    self.transition_count += 1
                    self.output.put(self.vdd if self.ton else self.vss)
                    added = self.vss if self.ton else self.vdd
            else:
                self.output.put(self.vdd if self.ton else self.vss)
                added = self.vss if self.ton else self.vdd
            self.log.debug(
                f'@{self.env.now}| {self.name} added sample {added}')
            self.last_sample = current_sample
            yield self.env.timeout(self.time_step)

    def unit_test(self):
        """Unit test for modules"""
        self.log.info('Running Unit Test')
        number_of_elements = math.floor(self.sim_time / self.time_step)
        for index, i in enumerate(range(0, number_of_elements)):
            if (1+math.sin(i/math.floor(number_of_elements/70))) > 1:
                self.input.buffer.put(self.vss)
                self.input.monitor.append((self.time_step*index, self.vss))
            else:
                self.input.buffer.put(self.vdd)
                self.input.monitor.append((self.time_step*index, self.vdd))

        self.env.process(self.start())

    def show(self, plot: bool = False):
        """Shows buffer occupancy

        :param plot: Flag to indicate if the function should
                     create a plot or return figures.
        :type plot: bool. Defualts to False

        :returns: If not plot, retuns an array of figures
        :return type: list[figure] || None

        """
        input_plot = self.input.get_buffer_waves()
        output_plot = self.output.get_buffer_waves()
        if plot:
            show(gridplot([[input_plot], [output_plot]]))
            return None
        return [[input_plot, output_plot]]
