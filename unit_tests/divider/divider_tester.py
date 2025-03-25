"""Divider unit test suite
==========================

This module contains the unit tests for the `Divider` class, which models a feedback divider
used in digital signal processing. It tests the functionality of the divider, ensuring that
it behaves as expected when processing an input signal and generating the output signal.

Test methods:
-------------
- `test_n_60`: Tests the divider with `n = 60` using reference and target data.
- `test_show`: Displays the results using the `Scope` class based on the plot mode setting.

"""

import numpy as np
from components.divider import Divider
from utils.settings import Settings
from utils.comparators import mse, cross_correlation
from utils.scope import Scope
# pylint: disable=C0301

settings = Settings(name='Divider_Tester')
settings.set_time(sim_time=4e-6, time_step=1e-11)

scope = Scope(fit='stretch_width')
time_array = np.arange(0, settings.sim_time, settings.time_step)


def test_n_60():
    """Test divider with n = 60.

    This test validates the behavior of the `Divider` class when the divisor value `n` is set 
    to 60. The test reads input signal data from a reference file (`div_ref.csv`) and compares 
    the output signal against a target file (`div_target.csv`). The mean squared error (MSE) and 
    cross-correlation (CC) are calculated to evaluate the performance of the divider.

    The results are plotted if the plot mode is set to either 'local' or 'web', and the MSE and 
    CC are displayed for further analysis. The test passes if the MSE is greater than 97% or the 
    cross-correlation exceeds 94%.

    **Steps**:
        1. Initialize the `Divider` with settings.
        2. Load the reference and target data from CSV files.
        3. Process the input signal through the divider.
        4. Calculate MSE and CC between the output and the target data.
        5. Optionally, plot the results.

    **Parameters**:
        None

    **Returns**:
        None

    **Raises**:
        AssertionError: If MSE or CC does not meet the thresholds.

    """
    dut = Divider(settings=settings)

    div_ref = np.array(open('unit_tests/divider/data/div_ref.csv',
                            encoding='utf-8').readlines(),
                       dtype=float)

    div_target = np.array(open('unit_tests/divider/data/div_target.csv',
                               encoding='utf-8').readlines(),
                          dtype=float)

    dut.start(input_array=div_ref)

    out = dut.io['output']

    mse_out = mse(data_1=div_target, data_2=out)
    cc = cross_correlation(data_1=div_target, data_2=out, mode='valid')

    plot_mode = settings.divider['plot_mode']
    if plot_mode in ('local', 'web'):
        scope.add_signal(time_array, div_ref,
                         'Test 1: Divider Input A', plot_type=plot_mode)
        scope.add_signal(time_array, div_target,
                         'Test 1: LF Target Output', plot_type=plot_mode)
        scope.add_signal(
            time_array, out, f'Test 1: LF Output - mse: {mse_out:.2f}% cc: {cc:.4f}%', plot_type=plot_mode)

    print(
        f'\nLPD Test 1: N 60 Input - mse: {mse_out:.2f}% cc: {cc:.4f}%')

    # Assert that the MSE is greater than 94% or cross-correlation is greater than 94%
    assert mse_out.item() > 94 or cc > 94


def test_show():
    """Show the plotted results.

    This method checks if the plot mode is set to either 'local' or 'web'. If so, it triggers 
    the display of the results using the `Scope` class, saving the plot in the appropriate 
    format (HTML for web or PNG for local).

    **Steps**:
        1. Check the plot mode setting.
        2. Call `scope.show()` to display the plot.

    **Parameters**:
        None

    **Returns**:
        None

    **Raises**:
        None

    **Example**:
        >>> test_show()
    """
    plot_mode = settings.divider['plot_mode']
    if plot_mode in ('local', 'web'):
        save_path = f'unit_tests/divider/divider_unit_test_results.{"html" if plot_mode == "web" else "png"}'
        scope.show(plot_type=plot_mode, save_path=save_path)
