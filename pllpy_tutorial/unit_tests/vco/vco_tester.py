"""VCO Unit Test Suite

This module contains unit tests for the `Vco` class, testing the behavior of the Voltage-Controlled Oscillator (VCO) 
under different input conditions. The tests include verifying the accuracy of the VCO's output against known reference 
signals, such as a 1 GHz sine wave and a DC signal. The tests also assess the performance of the VCO by calculating the 
mean squared error (MSE) between the expected and actual outputs. Additionally, the module supports visualizing 
the input, target, and output signals using the `Scope` class, which can generate either local or web-based plots.

Tests:
    - `test_sine_1ghz`: Tests a 1 GHz sine wave input and compares the output against a reference sine wave.
    - `test_clk`: Tests a DC signal input and verifies that the frequency remains stable.
    - `test_show`: Displays the results using the `Scope` class and saves the plot as an HTML file or image.
"""

import numpy as np
from pll_py.components.vco import Vco
from pll_py.utils.settings import Settings
from pll_py.utils.comparators import mse
from pll_py.utils.scope import Scope
# pylint: disable=C0301

settings = Settings(name='VCO_Tester')
settings.update_from_file(setting_file_path='./unit_tests/ut_sett.json')
scope = Scope()
time_array = np.arange(0, settings.sim_time, settings.time_step)


def test_sine_1ghz():
    """
    Tests a 1 GHz sine wave input to ensure the VCO generates a variable output.

    The test compares the VCO's output to a reference sine wave and calculates the 
    mean squared error (MSE) between the output and the target. The test passes 
    if the MSE exceeds a threshold value (97%).

    The input, target, and output signals are optionally plotted using the `Scope` class.

    Asserts:
        MSE between the output and target must be greater than 97.
    """
    dut = Vco(settings=settings)

    vco_ref_sine = np.array(open(
        './unit_tests/vco/data/sine_1GHz_ref.csv', encoding='utf-8').readlines(), dtype=float)
    vco_out_sine_target = np.array(open(
        './unit_tests/vco/data/sine_1GHz_target.csv', encoding='utf-8').readlines(), dtype=float)

    dut.start(input_array=vco_ref_sine)
    out = dut.io['output']
    mse_out = mse(data_1=vco_out_sine_target, data_2=out)

    plot_mode = settings.global_plot_mode
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, vco_ref_sine,
                         'Test 1: VCO Input', plot_type=plot_mode)
        scope.add_signal(time_array, vco_out_sine_target,
                         'Test 1: VCO Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 1: VCO Output - mse: {mse_out:.2f}%', plot_type=plot_mode)

    print(f'\nVCO Test 1: Sine Accuracy mse: {mse_out:.2f}%')
    assert mse_out > 97


def test_clk():
    """
    Tests a DC signal to ensure the VCO's frequency remains stable.

    This test uses a DC input (constant value) and checks the VCO's response against 
    a target signal. The MSE is calculated between the expected output and the VCO output.
    The test passes if the MSE exceeds a threshold value (97%).

    The input, target, and output signals are optionally plotted using the `Scope` class.

    Asserts:
        MSE between the output and target must be greater than 97.
    """
    dut = Vco(settings=settings, clk=True)
    vco_ref_dc = np.ones(settings.sample_count, dtype=float)
    vco_out_dc_target = np.array(open(
        './unit_tests/vco/data/dc_target.csv', encoding='utf-8').readlines(), dtype=float)
    dut.start(input_array=vco_ref_dc)
    out = dut.io['output']
    mse_out = mse(data_1=vco_out_dc_target, data_2=out)

    plot_mode = settings.global_plot_mode
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, vco_ref_dc,
                         'Test 2: VCO Input', plot_type=plot_mode)
        scope.add_signal(time_array, vco_out_dc_target,
                         'Test 2: VCO Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 2: VCO Output - mse: {mse_out:.2f}%', plot_type=plot_mode)

    print(f'\nVCO Test 2: VCO CLK Accuracy mse: {mse_out:.2f}%')
    assert mse_out > 97


def test_show():
    """
    Displays the results of the tests using the `Scope` class and optionally saves the plot.

    This method generates a plot of the signals for each test, including the input, 
    target, and output signals, and saves the plot to a file if a `save_path` is provided. 
    The plot can either be displayed locally using `matplotlib` or interactively on the web using `Bokeh`.

    :param plot_mode: Specifies the plot type ('local' for `matplotlib` or 'web' for `Bokeh`).
    :param save_path: The path where the plot will be saved (if applicable). Default is `None`.
    """
    plot_mode = settings.global_plot_mode
    if plot_mode in ('local', 'web'):
        scope.show(plot_type=plot_mode,
                   save_path=f'unit_tests/vco/vco_unit_test_results.{"html" if plot_mode == "web" else ""}')
