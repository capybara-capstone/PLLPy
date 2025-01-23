"""Phase Loop Filter Class"""
import math
from scipy import signal
import numpy as np
from bokeh.plotting import show
from bokeh.layouts import gridplot
from components.settings import Settings
from components.buffer import Buffer

# pylint: disable=W0612 disable=W1203


class Pfd(Settings):
    """Loop filder class"""

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.name = 'PFD'
        self.input_a = Buffer(env, 'Loop Filter Input A')
        self.input_b = Buffer(env, 'Loop Filter Input B')
        self.output = Buffer(env, 'Loop Filter Output')
        self.capacitors = self.pfd['capacitors']
        self.resistors = self.pfd['resistors']
        self.gains = self.pfd['gains']
        self.h = signal.TransferFunction([1.0,],
                                         [self.capacitors[0], 0,]
                                         )
        self.gain_histogram = Buffer(env, 'Loop Filter Gain')
        self.last = [0, 0]
        self.state = 0
        self.log = None

        self.setup()

    def setup(self):
        """Set up dividor"""
        self.log = self.get_logger(self.name)
        self.log.info(
            'Loop Filter created with name %s', self.name)

    def start(self):
        """Start Loop filter"""
        # init_a = yield self.input_a.buffer.get()
        # init_b = yield self.input_b.buffer.get()
        # self.last = [init_a, init_b]
        self.log.info('Starting %s', self.name)
        while True:
            current_sample_a = yield self.input_a.buffer.get()
            current_sample_b = yield self.input_b.buffer.get()

            self.log.debug(
                f'@{self.env.now}| {self.name} got sample A {current_sample_a} B {current_sample_b}')

            scaled_input = np.dot(np.array([self.last, [current_sample_a, current_sample_b]]),
                                  self.gains)
            self.gain_histogram.put(scaled_input[1])

            time_out, signal_out, xout = signal.lsim(self.h,
                                                     U=scaled_input,
                                                     T=[self.env.now,
                                                        self.env.now+self.time_step],
                                                     X0=self.state)
            self.last = [current_sample_a, current_sample_b]
            self.output.put(signal_out[1])
            self.state = xout[1]
            self.log.debug(
                f'@{self.env.now}| {self.name}  added {signal_out[1]}')

            yield self.env.timeout(self.time_step)

    def unit_test(self):
        """Unit test"""
        number_of_elements = math.floor(self.sim_time / self.time_step)
        for index, i in enumerate(range(0, number_of_elements)):
            if (1+math.sin(i/math.floor(number_of_elements/31))) > 1:
                self.input_a.buffer.put(self.vdd)
                self.input_b.buffer.put(self.vss)
                self.input_a.monitor.append((self.time_step*index, self.vdd))
                self.input_b.monitor.append((self.time_step*index, self.vss))

            else:
                self.input_a.buffer.put(self.vss)
                self.input_b.buffer.put(self.vdd)
                self.input_a.monitor.append((self.time_step*index, self.vss))
                self.input_b.monitor.append((self.time_step*index, self.vdd))

        self.env.process(self.start())

    def show(self, plot: bool = False):
        """Shows buffer occupancy

        :param plot: Flag to indicate if the function should
                     create a plot or return figures.
        :type plot: bool. Defualts to False

        :returns: If not plot, retuns an array of figures
        :return type: list[figure] || None

        """
        input_a_plot = self.input_a.get_buffer_waves()
        input_b_plot = self.input_b.get_buffer_waves()
        output_plot = self.output.get_buffer_waves()
        gain_plot = self.gain_histogram.get_buffer_waves()
        if plot:
            show(gridplot([[input_a_plot, input_b_plot],
                           [output_plot, gain_plot]
                           ]))
            return None
        else:
            return [[input_a_plot, input_b_plot],
                    [output_plot, gain_plot]]
