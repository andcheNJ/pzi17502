# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:36:44 2024

@author: testhouse
"""

import re
import os
import pandas as pd
from datetime import datetime

directory_path = r'E:\DLT_Traces'
excel_filename = r'E:\DLT_Traces\error_counts.xlsx'
def count_errors_in_dlt_file(file_path):
    error_pattern = re.compile(r'Register 0x0030001C changed')
    error_count = 0
    try:
        with open(file_path, 'rb') as file:
            for line in file:
                decoded_line = line.decode('latin-1')
                if error_pattern.search(decoded_line):
                    error_count += 1
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    return error_count

def count_errors_in_directory(directory_path):
    file_errors = {}
    
    for file in os.listdir(directory_path):
        full_file_path = os.path.join(directory_path, file)
        if os.path.isfile(full_file_path) and file.endswith('.dlt'):
            print(f"Processing file: {file}")  # Show current file being processed
            error_count = count_errors_in_dlt_file(full_file_path)
            if error_count is not None:
                file_errors[file] = error_count
    
    return file_errors
# Function to append row to Excel
def append_row_to_excel(filepath, row):
    try:
        # Try to read the existing Excel file
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        # If the file does not exist, create a new DataFrame
        df = pd.DataFrame(columns=['Filename', 'Timestamp', 'Number of Errors'])
    # Convert the row to a DataFrame and append it
    row_df = pd.DataFrame([row])  # Convert row to a DataFrame with a single row
    df = pd.concat([df, row_df], ignore_index=True)  # Use concat instead of append
    df.to_excel(filepath, index=False)

# Example usage

file_errors = count_errors_in_directory(directory_path)
for file, errors in file_errors.items():
    print(f"{file}: {errors} errors")
    
    # Count errors in the newly created DLT file
    #error_count = count_errors_in_dlt_file(current_filename)
    #write the data to excel
    if errors is not None:
        # Prepare the row to be appended
        row = {
            'Filename': file,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Number of Errors': errors
        }
        # Append the row to the Excel file
        append_row_to_excel(excel_filename, row)
