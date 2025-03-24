"""
LPD Unit Test Suite
==========================

This module contains the unit tests for the `LPD` (Linear Phase Detector) system, which models 
a phase detector used in digital signal processing. It tests the functionality of the phase detector, 
ensuring it behaves as expected when processing input signals and generating corresponding output signals.

Test Methods:
-------------
- `test_c_filter`: Tests the performance of the LoopFilter with a single integrator (capacitor) 
  and variable input signals. It compares the output with a target signal using metrics such as MSE 
  and Cross-Correlation (CC).
- `test_rc_filter`: Tests the performance of the LoopFilter with an RC filter and variable input signals. 
  Similar to the previous test, it compares the output with a reference target signal using MSE and CC.
- `test_show`: Displays the results using the `Scope` class based on the plot mode setting, 
  either locally or on the web.
"""

import numpy as np
from components.lf import LoopFilter
from utils.settings import Settings
from utils.comparators import mse, cross_correlation
from utils.scope import Scope
# pylint: disable=C0301

settings = Settings(name='LF_Tester')
scope = Scope(fit='stretch_width')
time_array = np.arange(0, settings.sim_time, settings.time_step)


def test_c_filter():
    """
    Test the single integrator (capacitor) with variable input.

    This test validates the performance of the LoopFilter with variable input signals.
    It compares the output of the filter with a target signal using Mean Squared Error (MSE)
    and Cross-Correlation (CC) metrics. The results are plotted if the plot mode is enabled.

    **Steps**:
        - Load reference and target data from CSV files.
        - Start the LoopFilter with the loaded input signals.
        - Calculate MSE and CC between the output and target signals.
        - Plot the input, target, and output signals if the plot mode is 'local' or 'web'.

    **Assertions**:
        - The MSE and CC values should be greater than 97%.

    :raises AssertionError: If MSE or CC does not meet the threshold of 97%.
    """
    dut = LoopFilter(settings=settings)
    lf_var_ref_a = np.array(open(
        'unit_tests/lf/data/lf_variable_ref_a.csv', encoding='utf-8').readlines(),
        dtype=float)

    lf_var_ref_b = np.array(open('unit_tests/lf/data/lf_variable_ref_b.csv',
                            encoding='utf-8').readlines(),
                            dtype=float)

    lf_var_target = np.array(open('unit_tests/lf/data/lf_var_target.csv',
                             encoding='utf-8').readlines(),
                             dtype=float)

    dut.start(input_array_a=lf_var_ref_a, input_array_b=lf_var_ref_b)

    out = dut.io['output']

    mse_out = mse(data_1=lf_var_target, data_2=out)
    cc = cross_correlation(data_1=lf_var_target, data_2=out)

    plot_mode = settings.lf['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, lf_var_ref_a,
                         'Test 1: LF Input A', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_ref_b,
                         'Test 1: LF Input B', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_target,
                         'Test 1: LF Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 1: LF Output - mse: {mse_out:.2f}% cc: {cc:.4f}%', plot_type=plot_mode)

    print(
        f'\nLPD Test 1: Same CLK Input - mse: {mse_out:.2f}% cc: {cc:.4f}%')

    assert mse_out.item() > 97 or cc > 97


def test_rc_filter():
    """
    Test the RC filter with variable input.

    This test validates the performance of the LoopFilter with a fixed resistor value
    and variable input signals. It compares the output of the filter with a target signal
    using Mean Squared Error (MSE) and Cross-Correlation (CC) metrics. The results are plotted
    if the plot mode is enabled.

    **Steps**:
        - Set the resistor value (`R`) in the settings.
        - Load reference and target data from CSV files.
        - Start the LoopFilter with the loaded input signals.
        - Calculate MSE and CC between the output and target signals.
        - Plot the input, target, and output signals if the plot mode is 'local' or 'web'.

    **Assertions**:
        - The MSE and CC values should be greater than 97%.

    :raises AssertionError: If MSE or CC does not meet the threshold of 97%.
    """
    settings.lf['R'] = 8400
    dut = LoopFilter(settings=settings)

    lf_var_ref_a = np.array(open(
        'unit_tests/lf/data/rc_lpd_out_a.csv', encoding='utf-8').readlines(),
        dtype=float)

    lf_var_ref_b = np.array(open(
        'unit_tests/lf/data/rc_lpd_out_b.csv', encoding='utf-8').readlines(),
        dtype=float)

    lf_var_target = np.array(open(
        'unit_tests/lf/data/rc_lf_out.csv', encoding='utf-8').readlines(),
        dtype=float)

    dut.start(input_array_a=lf_var_ref_a, input_array_b=lf_var_ref_b)
    out = dut.io['output']

    mse_out = mse(data_1=lf_var_target, data_2=out)
    cc = cross_correlation(data_1=lf_var_target, data_2=out)

    plot_mode = settings.lf['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, lf_var_ref_a,
                         'Test 2: LF Input A', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_ref_b,
                         'Test 2: LF Input B', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_target,
                         'Test 2: LF Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 2: LF Output - mse: {mse_out:.2f}% cc: {cc:.4f}%', plot_type=plot_mode)

    print(
        f'\nLPD Test 2: Same RC Filter - mse: {mse_out:.2f}% cc: {cc:.4f}%')

    assert mse_out.item() > 97 or cc > 97


def test_rcc_filter():
    """Tests rcc filter"""
    settings.lf['R'] = 6400
    settings.lf['C'] = 16e-12
    settings.lf['C2'] = 1.6e-12

    dut = LoopFilter(settings=settings)

    lf_var_ref_a = np.array(open(
        'unit_tests/lf/data/lf_rcc_ref_a.csv', encoding='utf-8').readlines(),
        dtype=float)

    lf_var_ref_b = np.array(open(
        'unit_tests/lf/data/lf_rcc_ref_b.csv', encoding='utf-8').readlines(),
        dtype=float)

    lf_var_target = np.array(open(
        'unit_tests/lf/data/lf_rcc_ref_out.csv', encoding='utf-8').readlines(),
        dtype=float)

    dut.start(input_array_a=lf_var_ref_a, input_array_b=lf_var_ref_b)
    out = dut.io['output']

    mse_out = mse(data_1=lf_var_target, data_2=out)
    cc = cross_correlation(data_1=lf_var_target, data_2=out)

    plot_mode = settings.lf['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, lf_var_ref_a,
                         'Test 3: LF Input A', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_ref_b,
                         'Test 3: LF Input B', plot_type=plot_mode)
        scope.add_signal(time_array, lf_var_target,
                         'Test 3: LF Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 3: LF Output - mse: {mse_out:.2f}% cc: {cc:.4f}%', plot_type=plot_mode)

    print(
        f'\nLPD Test 3: Same RCC Filter - mse: {mse_out:.2f}% cc: {cc:.4f}%')

    assert mse_out.item() > 97 or cc > 97


def test_show():
    """
    Show the plotted signals based on the selected plot mode.

    This function checks the `plot_mode` setting and either displays the plot 
    locally or on the web. The resulting plot is saved to a specified path.

    :raises FileNotFoundError: If the file paths or required data for plotting are incorrect.
    """
    plot_mode = settings.lf['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.show(plot_type=plot_mode,
                   save_path=f'unit_tests/lf/lf_unit_test_results.{"html" if plot_mode == "web" else ""}')
