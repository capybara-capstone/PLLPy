"""Divider Class"""
import math
from bokeh.plotting import show
from bokeh.layouts import gridplot
from components.settings import Settings
from components.buffer import Buffer


class Divider(Settings):
    """Models Feedback divider"""

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.name = 'Divider'
        self.n = self.dividor['n']
        self.input = Buffer(env=self.env, name=f'N={self.n} Divider Input')
        self.output = Buffer(env=self.env, name=f'N={self.n} Divider Output')
        self.transition_count = 0
        self.ton = False
        self.last_sample = 0

    def start(self):
        """Continous loop handling transition logic"""
        print(f"Starting {self.name}")
        # self.last_sample = yield self.input.buffer.get()
        while True:
            current_sample = yield self.input.buffer.get()
            if (self.last_sample == self.vdd and current_sample == self.vss) or (self.last_sample == self.vss and current_sample == self.vdd):
                if self.transition_count in (self.n * 2-1, self.n-1):
                    self.transition_count = 0 if self.transition_count == (
                        self.n * 2) - 1 else self.transition_count + 1
                    self.ton = not self.ton
                    self.output.put(self.vss if self.ton else self.vdd)
                else:
                    self.transition_count += 1
                    self.output.put(self.vdd if self.ton else self.vss)
            else:
                self.output.put(self.vdd if self.ton else self.vss)

            self.last_sample = current_sample
            yield self.env.timeout(self.time_step)

    def unit_test(self):
        """Unit test for modules"""
        print(f"@ {self.env.now}| Testing Divider")
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
        else:
            return [[input_plot, output_plot]]
