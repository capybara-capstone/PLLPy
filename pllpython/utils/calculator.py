"""Calculator Module

This module defines the Calculator class for computing jitter metrics
based on input signals.
"""

import numpy as np
from .scope import Scope

scope = Scope()


class Calculator:
    """A calculator class for computing jitter and phase noise metrics."""

    def __init__(self, settings):
        """
        Initialize the Calculator.

        :param settings: Configuration settings object with attributes like time_step and global_plot_mode.
        """
        self.settings = settings

    def calculate_jitter(self, input_array, start_time: int = None, stop_time: int = None, plot: bool = True):
        """
        Compute jitter and phase noise from an input signal.

        :param input_array: Input signal array.
        :param start_time: Optional; Start index for slicing the input array.
        :param stop_time: Optional; Stop index for slicing the input array.
        :param plot: Optional; If True, plots the signals and phase noise spectrum.
        :return: Tuple containing jitter and standard deviation of jitter.
        """
        if start_time is not None and stop_time is not None:
            start_sample = round(start_time / self.settings.time_step)
            stop_sample = round(stop_time / self.settings.time_step)
            input_array = input_array[start_sample:stop_sample]
        total_time = 0
        cross_zero = []
        last_cross = 0

        for index, sample in enumerate(input_array[1:], 1):
            total_time += self.settings.time_step
            if sample != input_array[index-1]:
                cross_zero.append(total_time - last_cross)
                last_cross = total_time
        mean_cross = np.mean(cross_zero)
        jitter_sequence = np.divide(np.subtract(
            cross_zero, mean_cross), mean_cross)

        phase_noise = np.fft.fft(jitter_sequence)
        cross_period = (self.settings.time_step *
                        len(input_array)) / len(cross_zero)
        phase_noise_freq = np.fft.fftfreq(len(phase_noise), cross_period)

        jitter = np.sqrt(np.mean(np.square(jitter_sequence)))
        std_dev = np.mean(np.absolute(jitter_sequence))

        bin_size = phase_noise_freq[1] - phase_noise_freq[0]
        phase_noise = np.divide(phase_noise, bin_size)

        index_min = np.argmin(abs(phase_noise))
        phase_noise[index_min] = phase_noise[index_min+1]

        if plot:
            scope.add_signal(np.arange(0, len(input_array)*self.settings.time_step, self.settings.time_step), input_array,
                             name='Input', x_label='Time', y_label='Voltage', plot_type=self.settings.global_plot_mode)

            scope.add_signal(phase_noise_freq, 10*np.log(abs(phase_noise), out=abs(phase_noise), where=abs(phase_noise) > 0),
                             'Phase Noise', 'Frequency Offset (Hz)', 'Phase Noise (dB/Hz)', self.settings.global_plot_mode)

            scope.show(plot_type=self.settings.global_plot_mode)

        return jitter, std_dev
