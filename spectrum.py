import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt

# Load the EMG data from CSV
emg = pd.read_csv('/Users/amalfouda/Desktop/dsp_project/Project-1/csv_files/emg.csv')  

fs = 100  

# High-pass filter setup
def high_pass_filter(data, cutoff=10, fs=100, order=8):
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

# Apply the high-pass filter to the first three channels
filtered_emg = emg.copy()
for i in range(3):  # Apply filter to the first three channels
    filtered_emg.iloc[:, i] = high_pass_filter(emg.iloc[:, i], cutoff=10, fs=fs)

# Function to compute and plot spectrum
def plot_spectrum(emg_channel, channel_number, fs, title_prefix):
    # Number of samples
    n = len(emg_channel)
    
    # Compute FFT
    fft_values = np.fft.fft(emg_channel)
    fft_freq = np.fft.fftfreq(n, d=1/fs)  # Frequency bins
    
    # Only take the positive half of the spectrum
    positive_freq = fft_freq[:n // 2]
    positive_fft = np.abs(fft_values[:n // 2])
    
    plt.plot(positive_freq, positive_fft, label=f'Channel {channel_number}')
    plt.title(f'{title_prefix} - Channel {channel_number}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()

plt.figure(figsize=(15, 15))

for i in range(3):  
    # Before filtering
    plt.subplot(3, 2, 2 * i + 1)
    plot_spectrum(emg.iloc[:, i], i + 1, fs, title_prefix="Before Filtering")
    
    # After filtering
    plt.subplot(3, 2, 2 * i + 2)
    plot_spectrum(filtered_emg.iloc[:, i], i + 1, fs, title_prefix="After Filtering")

plt.tight_layout()
plt.show()
