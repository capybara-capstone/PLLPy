"""LPD class"""
import math
from bokeh.plotting import show
from bokeh.layouts import gridplot
from components.buffer import Buffer
from components.settings import Settings


class Lpd(Settings):
    """Linear Phase Detector"""

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.name = 'LPD'
        self.input_a = Buffer(env, 'LPD Input A')
        self.input_b = Buffer(env, 'LPD Input B')
        self.output_up = Buffer(env, 'LPD Output UP')
        self.output_down = Buffer(env, 'LPD Output DOWN')
        self.last = [0, 0]
        self.results = [0, 0]

        self.input_b.buffer.put(0)
        self.output_up.buffer.put(0)
        self.output_down.buffer.put(0)

    def start(self):
        """Starts lpd"""
        print(f"Starting {self.name}")
        while True:
            input_a = yield self.input_a.buffer.get()
            input_b = yield self.input_b.buffer.get()

            rising_edge_detected = 0

            if input_a == 0:
                self.results[0] = 0
                self.last[0] = 0
            elif input_a == 1:
                if self.last[0] == 0:  # rising edge detected
                    self.results[0] = 1
                    rising_edge_detected = 1
                self.last[0] = 1

            if input_b == 1 and rising_edge_detected == 0:
                self.results[0] = 0
            self.output_up.put(self.results[0])

            # down logic
            rising_edge_detected = 0
            if input_b == 0:
                self.results[1] = 0
                self.last[1] = 0

            elif input_b == 1:
                if self.last[1] == 0:  # rising edge detected
                    self.results[1] = 1
                    rising_edge_detected = 1
                self.last[1] = 1

            if input_a == 1 and rising_edge_detected == 0:
                self.results[1] = 0

            self.output_down.put(self.results[1])

            yield self.env.timeout(self.time_step)

    def unit_test(self):
        """Unit test for modules"""
        print(f"@ {self.env.now}| Testing Phase Detector")
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
        output_up_plot = self.output_up.get_buffer_waves()
        output_down_plot = self.output_down.get_buffer_waves()
        if plot:
            show(gridplot([[input_a_plot, output_up_plot],
                           [input_b_plot, output_down_plot]]))
            return None
        else:
            return [[input_a_plot, output_up_plot],
                    [input_b_plot, output_down_plot]]
