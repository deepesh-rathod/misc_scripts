import pandas as pd
import os

def merge_csv_to_excel(csv_folder, output_file):
    """
    Merge multiple CSV files from a folder into a single Excel file.
    
    Parameters:
    - csv_folder: The path to the folder containing the CSV files.
    - output_file: The path to the output Excel file.
    """
    
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    # Create a new Excel writer
    with pd.ExcelWriter(output_file) as writer:
        for csv_file in csv_files:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join(csv_folder, csv_file))
            
            # Write the DataFrame to the Excel writer with the sheet name as the CSV file name (without the .csv extension)
            df.to_excel(writer, sheet_name=os.path.splitext(csv_file)[0], index=False)

# Example usage
merge_csv_to_excel('./scheduling_events', 'scheduling_events.xlsx')