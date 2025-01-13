# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:05:05 2024

@author: testhouse
"""

import os
import re
from datetime import datetime
import pandas as pd

def count_errors_in_dlt_file(file_path):
    # Compile a regular expression pattern to match the desired error messages
    error_pattern = re.compile(r'NEIGHBOUR:INCOMPLETE')
    # error_pattern = re.compile(r'Register 0x0030001C changed')
    
    # Initialize a counter for the errors
    error_count = 0
    
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            for line in file:
                # Decode each line with 'latin-1' encoding
                decoded_line = line.decode('latin-1')
                
                # If a line matches the error pattern, increment the error count
                if error_pattern.search(decoded_line):
                    error_count += 1
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
    return error_count

def find_dlt_files(directory):
    dlt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.dlt'):
                dlt_files.append(os.path.join(root, file))
    return dlt_files

def analyze_dlt_files_in_folder(folder_path):
    dlt_files = find_dlt_files(folder_path)
    total_error_count = 0
    results = []

    for file_path in dlt_files:
        print(f"Processing file: {file_path}")
        errors_found = count_errors_in_dlt_file(file_path)
        if errors_found is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append({'Filename': file_path, 'Timestamp': timestamp, 'Number of Errors': errors_found})
            total_error_count += errors_found

    return total_error_count, results

def save_results_to_excel(results, output_file):
    df = pd.DataFrame(results)

    if os.path.exists(output_file):
        # Load existing workbook
        existing_df = pd.read_excel(output_file)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_excel(output_file, index=False)

# Example usage
folder_path = r"E:\DLT_Traces\IDC23\CDD_BHTC"
output_file = r"E:\DLT_traces\IDC23\CDD_BHTC\analysis_results_failed.xlsx"
total_errors, results = analyze_dlt_files_in_folder(folder_path)

print(f"Total errors found in all .dlt files: {total_errors}")

save_results_to_excel(results, output_file)
print(f"Results saved to {output_file}")
