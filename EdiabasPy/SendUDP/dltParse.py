# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:14:56 2024

@author: testhouse
"""

import re

def count_errors_in_dlt_file(file_path):
    # Compile a regular expression pattern to match the desired error messages
    #error_pattern = re.compile(r'(FIFO-Underflow|SYNC-Stat-Error)(\. Value in FgChStat-Register| not present anymore)')
    error_pattern = re.compile(r'Register 0x0030001C changed')
    
    
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

# Example usage
file_name = r"D:\DLT_traces\Neuer Ordner\2024-02-26_15-08-35_13364_dlt-viewer-tmpfile.dlt"
errors_found = count_errors_in_dlt_file(file_name)
if errors_found is not None:
    print(f"Total errors found: {errors_found}")


