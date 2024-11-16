from PLL import pfd
import os
from tests.utils import *

tests_data_dir = os.path.dirname(os.path.abspath(__file__))

#def test_sin_example():
#    df = read_test_csv(f"{os.path.join(tests_data_dir, 'vco_3.csv')}")
#     
#    output_array = []
#    VCO(df.v_in, output_array, 1e9)
#
#    assert (verify_output(df.out, output_array, 0.01) == True)
#

def test_conly():
    fields = ["time","out","in1","in2"]
    df = read_test_csv(fields, f"{os.path.join(tests_data_dir, 'C_only.csv')}")
#    df = pd.read_csv(f"{os.path.join(tests_data_dir, 'C_only.csv')}", skipinitialspace=True, usecols=["time","out","in1","in2"]) 



    output_array = []
    output_array.append(0)
    state_vector = 0
    output_array, state_vector = pfd(df.in1, df.in2, output_array, 1, 0, 1e-11, 4e-6, state_vector)

    '''
    fig, axs = plt.subplots(4)
    axs[0].plot(df.in1)
    axs[1].plot(df.in2)
    axs[2].plot(output_array)
    axs[3].plot(df.out)
    plt.show()

    '''
    

    assert(verify_output(df.out, output_array, 0.01) == True)
