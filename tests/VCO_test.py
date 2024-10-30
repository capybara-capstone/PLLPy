from PLL import VCO
import os
from tests.utils import *

tests_data_dir = os.path.dirname(os.path.abspath(__file__))

fields = ["out", "v_in"]
## Test function for when the input voltage is a sin wave (w/ frq 1e7 Hz)
def test_sin_example():
    df = read_test_csv(fields, f"{os.path.join(tests_data_dir, 'vco_3.csv')}")
    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.01) == True)


## Test function for when the input voltage is always 0
def test_v_in_zero_example():
    df = read_test_csv(fields, f"{os.path.join(tests_data_dir, 'vco_2.csv')}")
    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.00) == True)


## Test function for Simulink PLL_example's VCO in/out
def test_vco_PLL_example():
    df = read_test_csv(fields, f"{os.path.join(tests_data_dir, 'vco_1.csv')}")

    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.005) == True)


