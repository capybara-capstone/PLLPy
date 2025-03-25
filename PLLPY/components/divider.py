"""Divider Class: Feedback Divider

This class models a feedback divider, typically used in digital signal processing. 
It divides the input signal based on the configured divider value `n`, toggling 
the output signal between two voltage levels (`vdd` and `vss`) upon detecting transitions.

The divider operates with a feedback mechanism to generate a periodic output based on 
transitions in the input signal. The class also allows monitoring of the input and output signals.

Attributes:
    - `n` (int): The divider's divisor value used for the transition counting.
    - `vdd` (float): The high voltage output level.
    - `vss` (float): The low voltage output level.
    - `upper_limit` (int): The upper transition count limit (`2*n - 1`).
    - `lower_limit` (int): The lower transition count limit (`n - 1`).
    - `io` (dict): Input and output signal buffers, where keys are 'input' and 'output' and values are deques of signal values.
    - `transition_count` (int): The current transition count.
    - `ton` (bool): The state of the output signal (`True` for high, `False` for low).
    - `last_sample` (float): The last value of the input sample for edge detection.

Methods:
    - `__init__(self, settings)`: Initializes the Divider with the provided settings.
    - `_process_and_monitor(self, current_sample: float)`: Processes the current input sample, 
      updates the transition count, and monitors input/output signals.
    - `_process(self, current_sample: float)`: Processes the current input sample and generates 
      the output signal without monitoring.
    - `start(self, input_array: list[float] | ndarray)`: Starts the divider processing, processing the entire input array.
    - `unit_test(self)`: Runs the unit test for the Divider using pytest.
"""
import os
from collections import deque
import pytest
# pylint: disable=W1203


class Divider:
    """
    Feedback Divider Class.

    The `Divider` class models a feedback divider used in digital circuits. It processes 
    the input signal and generates an output signal that toggles between two voltage levels (`vdd` 
    and `vss`) based on a transition-detection mechanism. The divider counts the number of transitions 
    and produces an output based on the configured divider value `n`. The class supports monitoring 
    of input and output signal values.

    :param settings: Configuration object containing the divider settings, including `n`, 
                     `vdd` (high voltage), and `vss` (low voltage).

    **Attributes**:
        - `n` (int): The divider's divisor value used for the transition counting.
        - `vdd` (float): The high voltage output level.
        - `vss` (float): The low voltage output level.
        - `upper_limit` (int): The upper transition count limit (`2*n - 1`).
        - `lower_limit` (int): The lower transition count limit (`n - 1`).
        - `io` (dict): Input and output signal buffers.
        - `transition_count` (int): The current transition count.
        - `ton` (bool): The state of the output signal (`True` for high, `False` for low).
        - `last_sample` (float): The last value of the input sample for edge detection.
    """

    def __init__(self, settings):
        """
        Initialize the Feedback Divider with the provided settings.

        This constructor sets up the divider `n` value, voltage levels (`vdd` and `vss`),
        and initializes the transition counters, limits, and output state. It prepares 
        the `io` buffer for monitoring input and output signal values during processing.

        :param settings: The configuration object containing `divider` settings and voltage levels.

        **Attributes**:
            - `n` (int): The divider's divisor value used for the transition counting.
            - `vdd` (float): The high voltage output level.
            - `vss` (float): The low voltage output level.
            - `upper_limit` (int): The upper transition count limit (`2*n - 1`).
            - `lower_limit` (int): The lower transition count limit (`n - 1`).
            - `io` (dict): Input and output signal buffers.
            - `transition_count` (int): The current transition count.
            - `ton` (bool): The state of the output signal (`True` for high, `False` for low).
            - `last_sample` (float): The last value of the input sample for edge detection.
        """
        self.n: float = settings.divider['n']
        self.vdd: float = settings.vdd
        self.vss: float = settings.vss
        self.sample_count: int = settings.sample_count

        self.upper_limit: float = self.n * 2 - 1
        self.lower_limit: float = self.n - 1

        self.io = {'input': deque([]), 'output': deque([])}

        self.transition_count: int = 0
        self.ton: bool = False
        self.last_sample: int = 0

    def _process_and_monitor(self, current_sample: float):
        """
        Process the current input sample, update the transition count, and monitor input/output.

        This method detects transitions in the input signal and toggles the output signal 
        between `vdd` and `vss` based on the feedback mechanism. It also stores the input 
        and output samples in the `io` buffer for monitoring purposes. The divider's state 
        alternates between `vdd` and `vss` based on the number of transitions counted, 
        subject to the configured divider value `n`.

        :param current_sample: The current input signal value to be processed.

        :return: The output signal value (`vdd` or `vss`) after processing the input sample.

        **Returns**:
            - float: The output signal, which is either `vdd` or `vss` based on the divider logic.
        """
        vdd = self.vdd
        vss = self.vss

        is_transition = ((self.last_sample == vdd and current_sample == vss) or
                         (self.last_sample == vss and current_sample == vdd))

        result = None

        if is_transition:
            if self.transition_count in (self.lower_limit, self.upper_limit):
                if self.transition_count == self.upper_limit:
                    self.transition_count = 0
                else:
                    self.transition_count += 1

                self.ton = not self.ton
                self.last_sample = current_sample
                result = vss if self.ton else vdd
            else:
                self.transition_count += 1
                self.last_sample = current_sample
                result = vdd if self.ton else vss
        else:
            self.last_sample = current_sample
            result = vdd if self.ton else vss

        self.io['input'].append(current_sample)
        self.io['output'].append(result)

        return result

    def _process(self, current_sample: float):
        """
        Process the current input sample and generate the output signal without monitoring.

        This method detects transitions in the input signal and toggles the output signal 
        between `vdd` and `vss` based on the feedback mechanism. Unlike `_process_and_monitor`, 
        this method does not store the input/output values for monitoring but directly returns 
        the output signal. The divider alternates its output between `vdd` and `vss` based on 
        the number of transitions and the configured divider value `n`.

        :param current_sample: The current input signal value to be processed.

        :return: The output signal value (`vdd` or `vss`) after processing the input sample.

        **Returns**:
            - float: The output signal, which is either `vdd` or `vss` based on the divider logic.
        """
        vdd = self.vdd
        vss = self.vss

        is_transition = ((self.last_sample == vdd and current_sample == vss) or
                         (self.last_sample == vss and current_sample == vdd))

        result = None

        if is_transition:
            if self.transition_count in (self.lower_limit, self.upper_limit):
                if self.transition_count == self.upper_limit:
                    self.transition_count = 0
                else:
                    self.transition_count += 1

                self.ton = not self.ton
                self.last_sample = current_sample
                result = vss if self.ton else vdd
            else:
                self.transition_count += 1
                self.last_sample = current_sample
                result = vdd if self.ton else vss
        else:
            self.last_sample = current_sample
            result = vdd if self.ton else vss

        return result

    def start(self, input_array: list[float]):
        """
        Start the divider processing on an input array.

        This method processes the entire input array, calling `_process` for each 
        individual sample and storing the output in the `io` buffer.

        It places the output directly into the io['output'].

        :param input_array: A list or np.array of input signal values.

        :return: None
        """
        self.io['output'] = deque([], maxlen=self.sample_count)
        self.io['input'] = input_array
        for sample in input_array:
            self.io['output'].append(self._process(current_sample=sample))

    def unit_test(self,  test_path):
        """
        Unit test for the Divider class.

        Runs the unit tests for the Divider class using pytest. The results of the tests 
        are displayed in the console.

        :return: None
        """
        print("Testing Divider")
        if os.path.isfile(path=test_path):
            return pytest.main(["-s", "--durations=0", test_path])
        return f'File {test_path} does not exist'
