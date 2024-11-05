import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

def phase_difference(signal1, signal2, sampling_rate):

    fft1 = fft(signal1)
    fft2 = fft(signal2)
    primary_freq_index = np.argmax(np.abs(fft1))
    phase1 = np.angle(fft1[primary_freq_index])
    phase2 = np.angle(fft2[primary_freq_index])

    phase_diff = phase1 - phase2

    phase_diff = np.degrees(phase_diff) % 360
    if phase_diff > 180:
        phase_diff -= 360

    return phase_diff

if __name__ == "__main__":
    fs = 1000  # Sampling rate (Hz)
    t = np.linspace(0, 1, fs, endpoint=False)

    freq = 5  # Frequency in Hz
    signal1 = np.sin(2 * np.pi * freq * t)
    signal2 = np.sin(2 * np.pi * freq * t + np.pi/4)

    phase_diff = phase_difference(signal1, signal2, fs)
    time = np.arange(len(signal1)) / fs

    plt.figure(figsize=(14, 6))

    plt.subplot(3, 1, 1)
    plt.plot(time, signal1, label="Signal 1", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 1")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time, signal2, label="Signal 2", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal 2")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.axhline(phase_diff, color='green', linestyle='--', label=f"Phase Difference: {phase_diff:.2f}°")
    plt.xlabel("Frequency Component")
    plt.ylabel("Phase Difference (Degrees)")
    plt.title("Primary Frequency Phase Difference")
    plt.legend()

    plt.tight_layout()
    plt.show()
    print(f"Phase Difference: {phase_diff:.2f} degrees")
