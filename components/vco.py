"""VCO Class"""
from math import pi, sin, cos, floor
from bokeh.plotting import show
from bokeh.layouts import gridplot
from components.settings import Settings
from components.buffer import Buffer


class Vco(Settings):
    """Models a voltage controlled oscilator.

    The higher voltage at the input the faster the frequency
    of the output.
    """

    def __init__(self, env, name='VCO', clk=False):
        super().__init__()
        self.env = env
        self.name = name
        self.clk_flag = clk
        self.input = Buffer(env, f'{self.name} Input')
        self.output = Buffer(env, f'{self.name} Output')
        self.gain = self.clk['k_vco'] if self.clk else self.vco['k_vco']
        self.frequency = self.clk['fo'] if self.clk else self.vco['fo']
        self.last = 0

        if self.clk_flag:
            self.input.buffer.put(0)

    def start(self):
        """Start VCO"""
        print(f"Starting {self.name}")
        while True:
            current_sample = yield self.input.buffer.get()
            new_voltage = current_sample * 2 * pi * self.gain
            angular_frequency = self.frequency * 2 * pi
            multiply = new_voltage+angular_frequency
            total_integral = self.last + (multiply * self.time_step)
            sin_out = cos(total_integral)
            self.output.put(self.vss if sin_out < 0 else self.vdd)
            if self.clk_flag:
                self.input.put(0)
            self.last = total_integral
            yield self.env.timeout(self.time_step)

    def unit_test(self):
        """Unit test for modules"""
        print(f"@ {self.env.now}| Testing VCO")
        number_of_elements = floor(self.sim_time / self.time_step)
        time = 0
        for i in range(0, number_of_elements):
            sample = 1+sin(i/floor(number_of_elements/10))
            self.input.buffer.put(sample)
            self.input.monitor.append((time, sample))
            time += self.time_step
        self.env.process(self.start())

    def show(self, plot: bool = False):
        """Shows buffer occupancy"""
        input_plot = self.input.get_buffer_waves()
        output_plot = self.output.get_buffer_waves()
        if plot:
            show(gridplot([[input_plot], [output_plot]]))
            return None
        else:
            return [[input_plot], [output_plot]]
