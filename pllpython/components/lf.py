"""Phase Loop Filter Class.

This class models a phase loop filter (LPF) used in phase-locked loops (PLLs).
The filter processes two input signals (`input_a` and `input_b`) to compute a 
filtered output value based on a resistor-capacitor (RC) network. The filter also 
provides methods for both processing and monitoring the input/output signal.

It is commonly used in PLLs to filter the phase difference between two signals 
and provide a control voltage for a Voltage-Controlled Oscillator (VCO).
"""
import os
from collections import deque
import pytest
import numpy as np

# pylint: disable=W0612 disable=W1203


class LoopFilter:
    """
    Phase Loop Filter (LPF) Class.

    This class models a phase loop filter used in phase-locked loops (PLLs). It takes two 
    input signals (`input_a` and `input_b`), processes them through a resistor-capacitor 
    (RC) network, and computes a filtered output signal. The filter uses two primary 
    components: a resistor `R` and a capacitor `C`, as well as pull-up and pull-down 
    currents that modify the output based on the input signals.

    The filter works by integrating the current difference between `input_a` and `input_b` 
    over time. It uses the alpha-beta filter algorithm to produce the output signal based on 
    the time step `time_step`, resistance `R`, and capacitance `C`.

    :param settings: Configuration object containing the filter settings, including `lf` 
                     parameters like resistor `R`, capacitor `C`, and current values.

    **Attributes**:
        - `time_step` (float): The simulation time step used for processing the signals.
        - `r` (float): The resistor value in the RC filter circuit.
        - `c` (float): The capacitor value in the RC filter circuit.
        - `pull_up` (float): The pull-up current coefficient for `input_a`.
        - `pull_down` (float): The pull-down current coefficient for `input_b`.
        - `last` (list): The last values of `input_a` and `input_b`.
        - `output_value` (float): The current output value of the filter.
        - `alpha` (float): The filter's alpha coefficient, used in the recursive computation.
        - `beta` (float): The filter's beta coefficient, used in the recursive computation.
        - `io` (dict): A dictionary storing input and output signals for monitoring.
    """

    def __init__(self, settings):
        """
        Initialize the Phase Loop Filter with the given settings.

        The constructor initializes the time step, resistor, capacitor, and pull-up/pull-down 
        currents. It computes the alpha and beta coefficients based on the resistor and 
        capacitor values, or defaults to an alternative method if `r` is None.

        :param settings: Configuration object containing the filter settings, including `lf` parameters 
                         like `R`, `C`, `pull_up`, `pull_down`, and `sample_count`.

        **Attributes**:
            - `time_step` (float): Time step used for signal processing.
            - `r` (float): Resistor value.
            - `c` (float): Capacitor value.
            - `pull_up` (float): Pull-up current coefficient.
            - `pull_down` (float): Pull-down current coefficient.
            - `alpha` (float): Computed alpha value for filtering.
            - `beta` (float): Computed beta value for filtering.
            - `last` (list): Stores the previous values of `input_a` and `input_b`.
            - `output_value` (float): The output value of the filter.
            - `io` (dict): Dictionary for storing input/output signals.
        """
        self.settings = settings
        self.io = {
            'input_a': deque([], maxlen=settings.sample_count),
            'input_b': deque([], maxlen=settings.sample_count),
            'output': deque([], maxlen=settings.sample_count)
        }

        self.time_step: float = float(settings.time_step)
        self.sample_count: int = settings.sample_count
        self.r: float = float(
            settings.lf['R']) if settings.lf['R'] is not None else None
        self.c: float = float(settings.lf['C'])
        self.c2: float = float(
            settings.lf['C2']) if settings.lf['C2'] is not None else None
        self.pull_up: float = float(settings.lf['pull_up'])
        self.pull_down: float = -1 * float(settings.lf['pull_down'])

        self.last_inputs: list = [0.0, 0.0]
        self.last_outputs: list = [0.0, 0.0]
        self.output_value: int = 0

        if self.r is None:
            self.alpha: float = 1.0
            self.beta: float = self.time_step / self.c
        else:
            if self.c2 is None:
                self.alpha: float = np.exp(-self.time_step / (self.r * self.c))
                self.beta: float = 1.0 - self.alpha
            else:
                rc = self.r*self.c
                rcc2 = self.r*self.c*self.c2
                cc2 = self.c+self.c2
                k = 2.0/self.time_step
                self.b0 = rc * k + 1
                self.b1 = -rc * k + 1
                self.b2 = 0

                self.a0 = rcc2 * k**2 + cc2 * k
                self.a1 = -2 * rcc2 * k**2
                self.a2 = rcc2 * k**2 - cc2 * k

    def update_settings(self, settings):
        """Update Settings"""
        self.settings = settings

    def _process(self, input_a: float, input_b: float) -> float:
        """
        Process the input signals and return the filtered output value.

        This method is similar to `_process_and_monitor` but does not store the input/output
        values for monitoring. It calculates the output value by applying the alpha and beta
        coefficients to the current input samples (`current_sample_a` and `current_sample_b`).

        :param current_sample_a: The current input signal `a` to be processed.
        :param current_sample_b: The current input signal `b` to be processed.

        :return: The filtered output value based on the input samples.

        **Returns**:
            - float: The filtered output value after applying the phase loop filter.
        """
        up_current = input_a * self.pull_up
        down_current = input_b * self.pull_down
        net_current = up_current + down_current

        if self.c2 is None:
            self.output_value = self.alpha * self.output_value + self.beta * net_current
            if self.settings.lf['min_sat'] is not None and self.settings.lf['max_sat'] is not None:
                if self.output_value < self.settings.lf['min_sat']:
                    self.output_value = self.settings.lf['min_sat']
                elif self.output_value > self.settings.lf['max_sat']:
                    self.output_value = self.settings.lf['max_sat']
        else:
            self.output_value = (self.b0 * net_current +
                                 self.b1 * self.last_inputs[0] +
                                 self.b2 * self.last_inputs[1] -
                                 self.a1 * self.last_outputs[0] -
                                 self.a2 * self.last_outputs[1]) / self.a0
            self.last_inputs = [net_current, self.last_inputs[0]]
            if self.settings.lf['min_sat'] is not None and self.settings.lf['max_sat'] is not None:
                if self.output_value < self.settings.lf['min_sat']:
                    self.output_value = self.settings.lf['min_sat']
                elif self.output_value > self.settings.lf['max_sat']:
                    self.output_value = self.settings.lf['max_sat']
            self.last_outputs = [self.output_value, self.last_outputs[0]]
        self.io['output'].append(self.output_value)

    def start(self, input_array_a: list[float], input_array_b: list[float]):
        """
        Process preloaded input signals and compute the filtered output.

        This method processes an array of input signals (`input_array_a` and `input_array_b`) 
        using the preloaded signals and computes the output for each sample.

        :param input_array_a: List of input signals `a` to be processed.
        :param input_array_b: List of input signals `b` to be processed.

        **Returns**:
            - None
        """
        self.io['input_a'] = np.array(input_array_a)
        self.io['input_b'] = np.array(input_array_b)
        for index, __ in enumerate(range(self.sample_count)):
            self._process(
                input_a=input_array_a[index], input_b=input_array_b[index])
        self.io['output'] = np.array(self.io['output'])

    def unit_test(self, test_path):
        """
        Unit test for modules.

        This method runs unit tests for the LoopFilter class using pytest, which will display 
        the results in the console.

        :return: None

        **Returns**:
            - None
        """
        print("Testing LoopFilter")
        if os.path.isfile(path=test_path):
            return pytest.main(["-s", "--durations=0", test_path])
        return f'File {test_path} does not exist'
