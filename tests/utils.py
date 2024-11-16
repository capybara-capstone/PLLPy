import pandas as pd

def read_test_csv(fields: list, filename: str):
#    fields = ['out', 'v_in']
    df = pd.read_csv(f'{filename}', skipinitialspace=True, usecols=fields)
    return df


def verify_output(golden, actual, margin):
#    if (golden.size != len(actual)):
#        print("Length Difference!\n")
#        return False
    
    diff = 0
    maxFound = 1e-10
    for elem in range(0, golden.size):
        #if (elem >= actual.size):
         #   return
        if(golden[elem]>maxFound):
            maxFound = golden[elem]
        error_percent = abs(golden[elem] - actual[elem])/maxFound
        if (error_percent>margin):
            print(f"Difference found in element {elem}. Expected {golden[elem]}, found {actual[elem]}\n")
            diff+=1
    
    if (diff > margin*golden.size):
        return False
    
    return True
