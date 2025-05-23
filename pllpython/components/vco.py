"""VCO Class: Models a Voltage-Controlled Oscillator (VCO).

The VCO class models a voltage-controlled oscillator, where the frequency of
the output is controlled by the input voltage. The higher the input voltage,
the faster the frequency of the output. The output is generated by the 
oscillator's internal mechanism that processes the input over time, with 
additional monitoring capabilities for inputs and outputs.
"""
import os
from collections import deque
from math import pi, cos, sqrt
import pytest
import numpy as np
from random import gauss
from scipy import signal
# pylint: disable=W1203


class Vco:
    """
    Models a voltage-controlled oscillator (VCO).

    The VCO generates an output waveform based on the input voltage, with 
    frequency determined by the control voltage. The higher the input voltage, 
    the faster the frequency of the output waveform. This class also provides 
    an optional monitoring feature to track input and output values during 
    simulation.

    :param settings: Configuration object containing parameters for VCO
        operation like `k_vco`, `fo`, `vss`, `vdd`, and `time_step`.
    :param clk: Boolean flag to determine whether to use clock settings.
        Defaults to `False`.

    **Attributes**:
        - `k_vco_time` (float): Scaling factor for the VCO, depending on the 
          control voltage and the time step.
        - `angular_time` (float): The angular frequency of the oscillator.
        - `vss` (float): The lower bound of the VCO output.
        - `vdd` (float): The upper bound of the VCO output.
        - `last` (float): The last computed value used for calculating the next 
          output.
        - `io` (dict): A dictionary containing deques for storing input and 
          output samples, used for monitoring the system.
    """

    def __init__(self, settings: object, clk: bool = False):
        """
        Initialize the VCO with given settings and clock option.

        This method sets up the VCO's internal parameters like scaling factors, 
        output bounds, and initializes the monitoring data structures if 
        necessary. The time step and control parameters are configured based 
        on the provided settings.

        :param settings: The configuration object that contains various 
            parameters like `clk`, `vco`, and `time_step`.
        :param clk: If `True`, the clock settings will be used to configure 
            the VCO. If `False`, the VCO settings are used. Defaults to 
            `False`.

        **Attributes**:
            - `k_vco_time` (float): The time scaling factor for the VCO.
            - `angular_time` (float): The angular frequency of the VCO.
            - `vss` (float): The lower voltage bound of the output.
            - `vdd` (float): The upper voltage bound of the output.
            - `last` (float): The last accumulated value used for output generation.
            - `io` (dict): A dictionary containing deques for storing input and 
              output samples during simulation.
        """
        self.sample_count: int = settings.sample_count
        self.k_vco_time: float = float(settings.clk['k_vco'] * 2 * pi *
                                       settings.time_step if clk else settings.vco['k_vco'] *
                                       2 * pi * settings.time_step)
        self.angular_time: float = float(settings.clk['fo'] * 2 * pi *
                                         settings.time_step if clk else settings.vco['fo'] *
                                         2 * pi * settings.time_step)
        self.vss: float = float(settings.vss)
        self.vdd: float = float(settings.vdd)
        self.last: float = 0
        self.last_output: int = 0
        self.io = {'input': deque([], maxlen=settings.sample_count),
                   'output': deque([], maxlen=settings.sample_count)}
 

        #input and output needed for noise
        self.k_vco: float = float(settings.clk['k_vco'] * 2 * pi 
                                         if clk else settings.vco['k_vco'] * 2 * pi) 
        self.fo: float = float(settings.clk['fo'] * 2 * pi
                                         if clk else settings.vco['fo'] *
                                         2 * pi)
        self.h0: float = float(settings.clk['white_phase_noise_spectral_density'] 
                        if clk else settings.vco['white_phase_noise_spectral_density'])
        self.n1: float = float(settings.clk['low_frequency_phase_noise'] 
                        if clk else settings.vco['low_frequency_phase_noise'])
        self.white_noise: float = float(0)
        self.add_noise_flag: int = 0

        self.low_freq_noise: float = 0
        self.filter_numerator: float = [1]
        self.filter_denominator: float = [1, 1]
        self.filter_conditions: float = [0] #signal.lfilter_zi(self.filter_numerator, 
                                            #self.filter_denominator)


        


    def _process_and_monitor(self, input_a: float) -> float:
        """
        Process a single input sample and monitor the results.

        This method processes a given input sample, updates the internal state 
        of the VCO, computes the output waveform, and stores the input/output 
        values in the monitoring buffers (if monitoring is enabled). The output 
        is determined by the phase of the oscillator.

        :param input_a: The input control voltage to the VCO.

        :return: The output value of the VCO after processing the input.

        **Returns**:
            - float: The output value of the VCO after processing the input.
        """
        self.last += (input_a * self.k_vco_time + self.angular_time)
        sin_out = cos(self.last + self.white_noise + self.low_freq_noise)
        out = self.vss + (self.vdd - self.vss) * (sin_out < 0)
        
        if self.last_output != out:
            self.add_white_noise(input_a)
            self.add_low_freq_noise(input_a)

        self.last_output = out
        self.io['input'].append(input_a)
        self.io['output'].append(out)

        return out

    def _process(self, input_a: float) -> float:
        """
        Process a single input sample without monitoring.

        This method processes the input control voltage, computes the output 
        waveform, and returns the result without storing any monitoring data.

        :param input_a: The input control voltage to the VCO.

        :return: The output value of the VCO after processing the input.

        **Returns**:
            - float: The output value of the VCO after processing the input.
        """
        self.last += (input_a * self.k_vco_time + self.angular_time)
        sin_out = cos(self.last + self.white_noise + self.low_freq_noise)
        out = self.vss + (self.vdd - self.vss) * (sin_out < 0)

        if self.last_output != out:
            self.add_white_noise(input_a)
            self.add_low_freq_noise(input_a)


        self.last_output = out

        return out

    def start(self, input_array: np.ndarray):
        """
        Process an array of input samples with maximum vectorization.

        This implementation is fully vectorized but changes the behavior
        of the oscillator compared to the original sequential algorithm, as it
        calculates all phase accumulations at once rather than sequentially.

        It saves the output directly into io.['output]
        :param input_array: Array of input control voltages to the VCO.

        :return: Array of output values of the VCO after processing the inputs.

        **Returns**:
            - np.ndarray: Array of output values of the VCO after processing 
              the inputs.
        """
        self.io['input'] = input_array
        increments = input_array * self.k_vco_time + self.angular_time
        phase_values = np.cumsum(increments) + self.last
        self.last = phase_values[-1]
        cos_values = np.cos(phase_values)
        self.io['output'] = self.vss + (self.vdd - self.vss) * (cos_values < 0)

    def add_white_noise(self, input_a):
        """
        This function adds white noise to the output. Inputs are setup in the settings.py file.

        :return: a value to be added to the integral in the VCO

        **Returns**:
            - float
        """
        if self.h0 != 0:
            target_frequency = (self.k_vco*input_a) + self.fo
            random_number = gauss(0, sqrt(self.h0/2))
            self.white_noise = random_number * sqrt(target_frequency)


    def add_low_freq_noise(self, input_a):
        """
        This function adds white noise to the output. Inputs are setup in the settings.py file.

        :return: a value to be added to the integral by the VCO

        **Returns**:
            - float
        """
        if self.n1 != 0:
            target_frequency = (self.k_vco*input_a) + self.fo
            random_number = gauss(0, sqrt(self.n1/2))
            pre_filter_noise = [self.low_freq_noise, random_number * sqrt(target_frequency)]
            result, self.filter_conditions = signal.lfilter(self.filter_numerator, 
                        self.filter_denominator, pre_filter_noise, zi = self.filter_conditions)
            self.low_freq_noise = result[1]


    def unit_test(self, test_path):
        """
        Unit test for the VCO class.

        Runs the unit tests for the VCO class using pytest. The results of the tests 
        are displayed in the console.

        :return: None

        **Returns**:
            - None
        """
        print("Testing VCO")
        if os.path.isfile(path=test_path):
            return pytest.main(["-s", "--durations=0", test_path])
        return f'File {test_path} does not exist'
