import pandas as pd
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
