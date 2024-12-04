import scipy.io
import pandas as pd
import os

def mat_to_combined_csv(mat_file, output_file):
    # Load the .mat file
    data = scipy.io.loadmat(mat_file)

    # Initialize an empty DataFrame
    combined_df = pd.DataFrame()

    # Process 'stimulus' and 'emg' keys
    try:
        # Set subject to a constant value (e.g., 1 for all rows)
        num_rows = data['emg'].shape[0]  # Get the number of rows from the 'emg' data
        subject = pd.DataFrame({'subject': [1] * num_rows})  # Create a column with all values as 1

        # Convert and transpose 'stimulus'
        stimulus = pd.DataFrame(data['stimulus']).transpose()

        # Convert 'emg' to DataFrame
        emg = pd.DataFrame(data['emg'])

        # Rename columns for EMG data with plain numbers
        emg.columns = [i + 1 for i in range(emg.shape[1])]

        # Combine subject, stimulus, and emg into a single DataFrame
        combined_df = pd.concat([subject, stimulus, emg], axis=1)

        # Rename the columns
        combined_df.columns = ['subject', 'stimulus'] + [i + 1 for i in range(emg.shape[1])]

        # Save the combined DataFrame to a CSV file
        combined_df.to_csv(output_file, index=False)
        print(f"Combined data saved to {output_file}")
    except KeyError as e:
        print(f"KeyError: {e}. Ensure the .mat file contains 'stimulus' and 'emg' keys.")
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
mat_file = "/Users/amalfouda/Desktop/DSP_project_new/Project Dataset/subject_1.mat"
output_file = "./csv_files/combined_data.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Run the function
mat_to_combined_csv(mat_file, output_file)
