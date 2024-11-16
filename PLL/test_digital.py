import numpy as np
from scipy import signal
from digital_lpd import *

def run_tests():
    fs = 1000  # Sampling frequency
    t = np.linspace(0, 1, fs, endpoint=False)
    
    # Test Case 1
    square_wave1 = (signal.square(2 * np.pi * 5 * t) + 1) / 2
    lpd = LPD(square_wave1, square_wave1, fs)
    lpd.get_wave_diff()
    assert np.all(lpd.up == 0) and np.all(lpd.down == 0), "Test Case 1 Failed"
    print('Test 1 PASSED')

    # # Test Case 2
    square_wave2 = (signal.square(2 * np.pi * 5 * t - np.pi/2) + 1) / 2
    # lpd = LPD(square_wave1, square_wave2, fs)
    # lpd.get_wave_diff()
    # lpd.get_phase_diff()  # Output phase diff should be ~90°
    # lpd.show_waves(fs)
    # assert (lpd.phase_diff == 90 or lpd.phase_diff == 89 or lpd.phase_diff == 91), f"Expected 90° got {lpd.phase_diff}"
    # print('Test 2 PASSED')
    
    # # Test Case 3
    # square_wave3 = (signal.square(2 * np.pi * 5 * t - np.pi) + 1) / 2
    # lpd = LPD(square_wave1, square_wave3, fs)
    # lpd.get_wave_diff()
    # lpd.get_phase_diff()  # Output phase diff should be ~180°
    # print('Test 3 PASSED')
    
    # Test Case 4
    fs_low = 500
    t_low = np.linspace(0, 1, fs_low, endpoint=False)
    square_wave_low = (signal.square(2 * np.pi * 5 * t_low) + 1) / 2
    lpd = LPD(square_wave_low, square_wave2[:fs_low], fs_low)
    lpd.show_waves(fs=fs_low)
    try:
        lpd.get_wave_diff()
        lpd.get_phase_diff()
        print('Test 4 PASSED')
    except:
        print('Test 4 FAILED')
    
    # Test Case 5
    constant_wave = np.ones(fs)
    lpd = LPD(constant_wave, square_wave1, fs)
    lpd.get_wave_diff()
    lpd.get_phase_diff()
    assert np.all(lpd.up == 0) and np.all(lpd.down == 0) and (lpd.phase_diff == None), "Test Case 6 Failed"
    print('Test 5 PASSED')
    
    # print("All test cases passed!")

if __name__ == '__main__':
    run_tests()