from Hpass import filter_emg_combined
from extract_filtered_data import extract_data
import os

# File paths
raw_emg_file = '/Users/amalfouda/Desktop/DSP_project_new/csv_files/combined_data.csv'
filtered_emg_file = '/Users/amalfouda/Desktop/DSP_project_new/csv_files/filtered_combined_data.csv'
output_directory = '/Users/amalfouda/Desktop/DSP_project_new/csv_files/segments'

# Sampling frequency
fs = 100

def main():
   
    if not os.path.exists(raw_emg_file):
        print(f"Error: The file {raw_emg_file} does not exist.")
        return
    
    os.makedirs(os.path.dirname(filtered_emg_file), exist_ok=True)

    print("Filtering combined EMG data...")
    try:
        filter_emg_combined(
            input_file=raw_emg_file, 
            output_file=filtered_emg_file, 
            cutoff=10, 
            fs=fs, 
            order=10
        )
        print(f"Filtered combined EMG data saved to {filtered_emg_file}")
    except Exception as e:
        print(f"Error during filtering: {e}")
        return

    print("Extracting segments from filtered EMG data...")
    try:
        extract_data(
            input_file=filtered_emg_file,
            output_dir=output_directory,
            stimulus_column='stimulus',
            target_stimuli=[1, 2],
            columns_to_process=range(1, 11)  
        )
        print(f"Segments saved to {output_directory}")
    except Exception as e:
        print(f"Error during segment extraction: {e}")

if __name__ == '__main__':
    main()
