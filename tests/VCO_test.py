import pandas as pd
from PLL import VCO

def read_test_csv(filename: str):
    fields = ['out', 'v_in']
    df = pd.read_csv(f'{filename}', skipinitialspace=True, usecols=fields)
    return df


def verify_output(golden, actual, margin):
    if (golden.size != len(actual)):
        return False
    
    diff = 0
    for elem in range(0, golden.size):
        if (golden[elem] != actual[elem]):
            print(f"Difference found in element {elem}. Expected {golden[elem]}, found {actual[elem]}\n")
            diff+=1
    
    if (diff > margin*golden.size):
        return False
    
    return True


## Test function for when the input voltage is a sin wave (w/ frq 1e7 Hz)
def test_sin_example():
    df = read_test_csv("vco_3.csv")
    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.01) == True)


## Test function for when the input voltage is always 0
def test_v_in_zero_example():
    df = read_test_csv("vco_2.csv")
    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.00) == True)


## Test function for Simulink PLL_example's VCO in/out
def test_vco_PLL_example():
    df = read_test_csv("vco_1.csv")
    
    output_array = []
    VCO(df.v_in, output_array, 1e9)

    assert (verify_output(df.out, output_array, 0.005) == True)


