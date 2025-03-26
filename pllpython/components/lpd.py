"""LPD class: Linear Phase Detector.

The LPD class models a linear phase detector used for signal processing.
It detects the phase difference between two input signals and generates
corresponding output signals. The phase detector has the ability to monitor 
the input and output signals during simulation and provides the ability 
to process inputs without monitoring.

The class extends the `Settings` class to retrieve configuration parameters 
such as sample count.
"""
import os
from collections import deque
import pytest

# pylint: disable=W1203


class Lpd:
    """
    Linear Phase Detector (LPD).

    This class models a Linear Phase Detector, which detects phase differences
    between two input signals (`input_a` and `input_b`) and produces output
    signals (`output_a` and `output_b`). It supports monitoring of input and 
    output values, and simulates the behavior of the phase detector based on 
    the provided settings.

    :param settings: Configuration object that contains parameters such as 
        `sample_count` to set up the size of the input/output buffers.

    **Attributes**:
        - `io` (dict): A dictionary containing deques for monitoring input 
          (`input_a`, `input_b`) and output (`output_a`, `output_b`) signals 
          during simulation.
        - `ff_up_q` (int): The flip-flop state for `output_a`.
        - `ff_down_q` (int): The flip-flop state for `output_b`.
        - `last_up` (int): The previous value of `input_a` for edge detection.
        - `last_down` (int): The previous value of `input_b` for edge detection.
    """

    def __init__(self, settings):
        """
        Initialize the Linear Phase Detector (LPD) with given settings.

        This method sets up the input/output buffers (as deques) and initializes
        the flip-flop states and edge detection values. The simulation parameters 
        (such as `sample_count`) are fetched from the provided `settings` object.

        :param settings: The configuration object containing simulation parameters 
            like `sample_count`.

        **Attributes**:
            - `io` (dict): Input and output buffers for signal monitoring.
            - `ff_up_q` (int): The current state of `output_a`.
            - `ff_down_q` (int): The current state of `output_b`.
            - `last_up` (int): Stores the last value of `input_a`.
            - `last_down` (int): Stores the last value of `input_b`.
        """
        self.io = {
            'input_a': deque([], maxlen=settings.sample_count),
            'input_b': deque([], maxlen=settings.sample_count),
            'output_a': deque([], maxlen=settings.sample_count),
            'output_b': deque([], maxlen=settings.sample_count)
        }

        self.sample_count = settings.sample_count
        self.ff_up_q: float = 0
        self.ff_down_q: float = 0
        self.last_up: float = 0
        self.last_down: float = 0

    def _process_and_monitor(self, input_a: float, input_b: float) -> tuple:
        """
        Process two input signals and monitor their outputs.

        This method detects edges (rising edges) in both input signals and 
        updates the flip-flop states accordingly. The method also stores the 
        input and output signals in the monitoring buffers (`io`).

        :param input_a: The first input signal to the phase detector.
        :param input_b: The second input signal to the phase detector.

        :return: A tuple containing the current output values `(output_a, output_b)`.

        **Returns**:
            - tuple: Contains two values:
              - `output_a` (int): The output for the first signal after processing.
              - `output_b` (int): The output for the second signal after processing.
        """
        edge_a = input_a == 1 and self.last_up == 0
        edge_b = input_b == 1 and self.last_down == 0

        self.last_up = input_a
        self.last_down = input_b

        reset = self.ff_up_q and self.ff_down_q

        if reset:
            self.ff_up_q = 0
        elif edge_a:
            self.ff_up_q = 1

        if reset:
            self.ff_down_q = 0
        elif edge_b:
            self.ff_down_q = 1

        self.io['input_a'].append(input_a)
        self.io['input_b'].append(input_b)
        self.io['output_a'].append(self.ff_up_q)
        self.io['output_b'].append(self.ff_down_q)

        return self.ff_up_q, self.ff_down_q

    def _process(self, input_a: float, input_b: float) -> tuple:
        """
        Process two input signals without monitoring.

        This method detects edges (rising edges) in both input signals and 
        updates the flip-flop states accordingly, but it does not store the 
        input/output values in monitoring buffers.

        :param input_a: The first input signal to the phase detector.
        :param input_b: The second input signal to the phase detector.

        :return: A tuple containing the current output values `(output_a, output_b)`.

        **Returns**:
            - tuple: Contains two values:
              - `output_a` (int): The output for the first signal after processing.
              - `output_b` (int): The output for the second signal after processing.
        """
        edge_a = input_a == 1 and self.last_up == 0
        edge_b = input_b == 1 and self.last_down == 0

        self.last_up = input_a
        self.last_down = input_b

        reset = self.ff_up_q and self.ff_down_q

        if reset:
            self.ff_up_q = 0
        elif edge_a:
            self.ff_up_q = 1

        if reset:
            self.ff_down_q = 0
        elif edge_b:
            self.ff_down_q = 1

        return self.ff_up_q, self.ff_down_q

    def start(self, input_array_a: list[float], input_array_b: list[float]) -> None:
        """
        Same as process but optimized for preloaded input.

        This method processes preloaded input arrays and stores the output values
        in the monitoring buffers. It iterates over the `input_array_a` and 
        `input_array_b` signals and updates the output arrays accordingly.

        :param input_array_a: A list of input signals for `input_a`.
        :param input_array_b: A list of input signals for `input_b`.

        **Returns**:
            - None
        """
        self.io['input_a'] = input_array_a
        self.io['input_b'] = input_array_b
        for index, __ in enumerate(range(self.sample_count)):
            out_a, out_b = self._process(
                input_a=input_array_a[index], input_b=input_array_b[index])
            self.io['output_a'].append(out_a)
            self.io['output_b'].append(out_b)

    def unit_test(self,  test_path):
        """
        Unit test for modules.

        This method runs the unit tests for the Linear Phase Detector class using 
        the `pytest` framework.

        **Returns**:
            - None
        """
        print("Testing LPD")
        if os.path.isfile(path=test_path):
            return pytest.main(["-s", "--durations=0", test_path])
        return f'File {test_path} does not exist'