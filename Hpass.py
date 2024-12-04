import pandas as pd
from scipy.signal import butter, filtfilt

def high_pass_filter(data, cutoff=10, fs=100, order=8):
    nyquist = 0.5 * fs
    if cutoff >= nyquist:
        raise ValueError(f"Cutoff frequency must be less than Nyquist frequency ({nyquist} Hz).")
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def filter_emg_combined(input_file, output_file, cutoff=10, fs=100, order=10):
    try:
        # Read the input CSV file
        combined_data = pd.read_csv(input_file)
        
        if combined_data.empty:
            raise ValueError("The input file is empty or contains no valid data.")
        
        # Extract `subject` and `stimulus` columns
        metadata = combined_data[['subject', 'stimulus']]
        
        # Extract the columns tagged `1` to `10` for filtering
        emg_data = combined_data.iloc[:, 2:]  # Skip the first two columns
        
        # Apply the high-pass filter to the EMG data
        filtered_emg_data = emg_data.apply(
            lambda col: high_pass_filter(col.dropna(), cutoff=cutoff, fs=fs, order=order)
        )
        
        # Combine `subject`, `stimulus`, and the filtered data into a new DataFrame
        filtered_combined_data = pd.concat([metadata, filtered_emg_data], axis=1)
        
        # Save the filtered data to a new CSV file
        filtered_combined_data.to_csv(output_file, index=False)
        print(f"Filtered EMG data saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
