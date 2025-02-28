"""Phase Loop Filter Class.

This class models a phase loop filter (LPF) used in phase-locked loops (PLLs).
The filter processes two input signals (`input_a` and `input_b`) to compute a 
filtered output value based on a resistor-capacitor (RC) network. The filter also 
provides methods for both processing and monitoring the input/output signal.

It is commonly used in PLLs to filter the phase difference between two signals 
and provide a control voltage for a Voltage-Controlled Oscillator (VCO).
"""

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
        self.pull_up: float = float(settings.lf['pull_up'])
        self.pull_down: float = -1 * float(settings.lf['pull_down'])

        self.last: list = [0, 0]
        self.output_value: int = 0

        if self.r is None:
            self.alpha: float = 1.0
            self.beta: float = self.time_step / self.c
        else:
            self.alpha: float = np.exp(-self.time_step / (self.r * self.c))
            self.beta: float = 1.0 - self.alpha

    def _process_and_monitor(self, current_sample_a: float, current_sample_b: float) -> float:
        """
        Process and monitor the input signals, returning the filtered output value.

        This method calculates the output of the phase loop filter based on the current input
        samples (`current_sample_a` and `current_sample_b`). The current difference is filtered 
        using the alpha and beta coefficients. It also stores the input and output values in the 
        `io` dictionary for monitoring purposes.

        :param current_sample_a: The current input signal `a` to be processed.
        :param current_sample_b: The current input signal `b` to be processed.

        :return: The filtered output value based on the input samples.

        **Returns**:
            - float: The filtered output value after applying the phase loop filter.
        """
        up_current = current_sample_a * self.pull_up
        down_current = current_sample_b * self.pull_down
        net_current = up_current + down_current
        self.output_value = self.alpha * self.output_value + self.beta * net_current
        self.last = [current_sample_a, current_sample_b]

        self.io['output'].append(self.output_value)
        return self.output_value

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
        self.output_value = self.alpha * self.output_value + self.beta * net_current
        self.last = [input_a, input_b]
        return self.output_value

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
        n_samples = self.sample_count
        output = np.empty(n_samples, dtype=np.float64)
        net_current = input_array_a * self.pull_up + input_array_b * self.pull_down
        output[0] = self.alpha * self.output_value + self.beta * net_current[0]
        if n_samples > 1:
            for i in range(1, n_samples):
                output[i] = self.alpha * output[i-1] + \
                    self.beta * net_current[i]

        self.io['output'] = output

    def unit_test(self):
        """
        Unit test for modules.

        This method runs unit tests for the LoopFilter class using pytest, which will display 
        the results in the console.

        :return: None

        **Returns**:
            - None
        """
        print("Testing LoopFilter")
        return pytest.main(["-s", "--durations=0", "unit_tests/lf/lf_tester.py"])
