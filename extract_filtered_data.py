import pandas as pd
import os

def extract_data(input_file, output_dir, stimulus_column='stimulus', target_stimuli=[1, 2], columns_to_process=range(1, 11), num_slots=10):
    """
    Extract data segments and format them into fixed slots in rows.
    
    Args:
        input_file: Path to the input CSV file.
        output_dir: Path to save the output CSV files.
        stimulus_column: The name of the stimulus column.
        target_stimuli: List of target stimuli values.
        columns_to_process: Range of columns to process.
        num_slots: Number of slots for each row (segment).
    """
    try:
        # Read the input CSV file
        data = pd.read_csv(input_file)
        
        if data.empty:
            raise ValueError("The input file is empty or contains no valid data.")
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        for column_name in map(str, columns_to_process):  
            if column_name not in data.columns:
                print(f"Column '{column_name}' not found in the dataset. Skipping...")
                continue
            
            segments = {stimulus_value: [] for stimulus_value in target_stimuli}
            current_segment = []
            current_stimulus = None

            # Loop through the stimulus column and extract corresponding segments from the target column
            for index, stim_value in enumerate(data[stimulus_column]):
                if stim_value in target_stimuli:
                    if current_stimulus != stim_value:
                        if current_segment:
                            # Add the current segment to the corresponding stimulus list
                            segments[current_stimulus].append(current_segment)
                        current_segment = []
                        current_stimulus = stim_value
                    current_segment.append(data[column_name].iloc[index])
                else:
                    if current_segment:
                        segments[current_stimulus].append(current_segment)
                        current_segment = []
                        current_stimulus = None

            if current_segment:
                segments[current_stimulus].append(current_segment)

            # Create a combined DataFrame for this column
            combined_segments = []
            for stim_value, stim_segments in segments.items():
                for segment in stim_segments:
                    # Format the segment into fixed slots
                    formatted_segment = segment[:num_slots] + [None] * (num_slots - len(segment))
                    combined_segments.append(formatted_segment)

            # Convert the combined segments into a DataFrame
            combined_df = pd.DataFrame(combined_segments)
            combined_df.columns = [f"Slot {i + 1}" for i in range(num_slots)]  # Assign slot names

            # Save the combined data for this column into a single CSV file
            output_file = f"{output_dir}/column_{column_name}_fixed_slots.csv"
            combined_df.to_csv(output_file, index=False)
            print(f"Saved combined segments with fixed slots for column '{column_name}' to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
