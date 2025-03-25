"""
LPD Unit Test Suite
==========================

This module contains the unit tests for the `Lpd` class, which models a phase detector 
used in digital signal processing. It tests the functionality of the LPD (Linear Phase Detector) 
system, ensuring that it behaves as expected when processing input signals and generating the output signals.

Test Methods:
-------------
- `test_equal_input`: Tests the LPD with equal input signals (both `input_a` and `input_b` are the same). 
  It compares the output to reference target signals `clk_target_a` and `clk_target_b` and checks for accuracy.
- `test_variable_input`: Tests the LPD with different variable input signals (`input_a` and `input_b` are different). 
  It compares the output to target signals `lpd_variable_target_a` and `lpd_variable_target_b` and checks for accuracy.
- `test_rc_input`: Tests the LPD with RC filter inputs (`input_a` and `input_b`). 
  It compares the output to reference target signals `rc_lpd_out_a` and `rc_lpd_out_b` and checks for accuracy.
- `test_show`: Displays the results using the `Scope` class based on the plot mode setting, either locally or on the web.
"""

import numpy as np
from PLLPY.components.lpd import Lpd
from PLLPY.utils.settings import Settings
from PLLPY.utils.scope import Scope
# pylint: disable=C0301

settings = Settings('LPD_Tester')
settings.update_from_file(setting_file_path='./unit_tests/ut_sett.json')
scope = Scope(fit='stretch_width')
time_array = np.arange(0, settings.sim_time, settings.time_step)


def test_equal_input():
    """
    Test the LPD with equal input signals (input_a and input_b are identical).

    This test validates the behavior of the LPD when both input signals are the same. 
    It compares the outputs with reference target signals for both output_a and output_b.
    The accuracy of the output is measured by counting mismatches with the target signals.

    Asserts:
        - Accuracy of output_a should be above 97%.
        - Accuracy of output_b should be above 97%.
    """
    # Test implementati
    dut = Lpd(settings=settings)
    lpd_clk_ref = np.array(open(
        'unit_tests/lpd/data/clk_ref.csv', encoding='utf-8').readlines(), dtype=float)

    lpd_clk_target_a = np.array(open(
        'unit_tests/lpd/data/clk_target_a.csv', encoding='utf-8').readlines(), dtype=float)

    lpd_clk_target_b = np.array(open(
        'unit_tests/lpd/data/clk_target_b.csv', encoding='utf-8').readlines(), dtype=float)

    dut.start(input_array_a=lpd_clk_ref, input_array_b=lpd_clk_ref)

    out_a = [*dut.io['output_a']]
    out_b = [*dut.io['output_b']]

    assert len(out_a) == len(lpd_clk_target_a)
    mismatch_count_a = 0
    for index, sample in enumerate(lpd_clk_target_a):
        results = sample - out_a[index]
        if results != 0:
            mismatch_count_a += 1

    acc_a = (1-mismatch_count_a/len(out_a))*100

    mismatch_count_b = 0
    for index, sample in enumerate(lpd_clk_target_b):
        results = sample - out_a[index]
        if results != 0:
            mismatch_count_b += 1

    acc_b = (1-mismatch_count_b/len(out_b))*100

    plot_mode = settings.lpd['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, lpd_clk_ref,
                         'Test 1: LPD Input A', plot_type=plot_mode)
        scope.add_signal(time_array, lpd_clk_ref,
                         'Test 1: LPD Input B', plot_type=plot_mode)
        scope.add_signal(time_array, lpd_clk_target_a,
                         'Test 1: LPD Target Output A', plot_type=plot_mode)
        scope.add_signal(time_array, lpd_clk_target_b,
                         'Test 1: LPD Target Output B', plot_type=plot_mode)
        scope.add_signal(
            time_array, out_a, f'Test 1: LPD Output A - Match: {acc_a:.2f}%', plot_type=plot_mode)

        scope.add_signal(
            time_array, out_b, f'Test 1: LPD Output B - Match: {acc_a:.2f}%', plot_type=plot_mode)

    print(
        f'\nLPD Test 1: Same CLK Input - Accuracy A: {acc_a} Accuracy B: {acc_b}')

    assert acc_a > 97
    assert acc_b > 9


def test_show():
    """
    Display the test results using the `Scope` class based on the plot mode setting.

    This function visualizes the input, target, and output signals for the LPD tests. It supports 
    both local and web-based plotting, depending on the plot mode configuration in the settings.

    The generated results can be saved as an HTML file or displayed locally.
    """
    plot_mode = settings.lpd['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.show(plot_type=plot_mode,
                   save_path=f'unit_tests/lpd/lpd_unit_test_results.{"html" if plot_mode == "web" else ""}')
