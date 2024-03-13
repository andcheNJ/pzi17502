# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:01:28 2024

@author: testhouse
"""

def interpret_byte_array(byte_array):
    # Dictionary to map byte values to their corresponding strings
    byte_to_string = {
        0x0001: "PHUD50 ECO",
        0x0002: "PHUD50 VIS-1",
        0x0003: "PHUD50 VIS-2",
        0x0004: "PHUD40 EVO",
        0x0005: "FHUD"
    }

    # Combine the first two bytes to form a single number
    combined_bytes = (byte_array[0] << 8) + byte_array[1]

    # Return the corresponding string, if exists
    return byte_to_string.get(combined_bytes, "Unknown")

# Example usage
example_byte_array = [0, 5, 20]
result = interpret_byte_array(example_byte_array)
result

def is_valid_date(date_list):
    # Check if the date list has exactly 3 elements
    if len(date_list) != 3:
        return False, None

    year, month, day = date_list

    # Adjust year to include century if needed (example: 20 -> 2020)
    if 0 <= year <= 99:
        year += 2000

    # Check if the month is valid (1-12)
    if not (1 <= month <= 12):
        return False, None

    # Check if the day is valid
    # Assuming 31 days for months 1, 3, 5, 7, 8, 10, 12
    # 30 days for months 4, 6, 9, 11 and
    # 28 or 29 days for month 2 (leap year not considered)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        valid_day = 1 <= day <= 31
    elif month in [4, 6, 9, 11]:
        valid_day = 1 <= day <= 30
    else:  # February
        valid_day = 1 <= day <= 29

    # Format the date in DD.MM.YYYY format
    formatted_date = f"{day:02d}.{month:02d}.{year}"

    return valid_day, formatted_date

# Example usage
date_list = [31, 2, 20]
is_valid, formatted_date = is_valid_date(date_list)
print(is_valid, formatted_date)

import re
# function must be named 'func'

def convert_to_hex_and_extract(six_bytes):
    # Convert each byte to its hex representation
    hex_values = [format(byte, '02X') for byte in six_bytes]

    # Combine the hex values into a single string
    combined_hex = ''.join(hex_values)

    # Return the last 7 characters of the combined hex string
    return combined_hex[-7:]



def func(input_string):
    pattern = r'^\d[A-Fa-f0-9]{5}\d$'
    return bool(re.match(pattern, input_string))

# Example usage
six_bytes = [0, 255, 5, 168, 226, 82]
result = convert_to_hex_and_extract(six_bytes)
result

result2 = func(result)

def convert_to_hex_and_extract_1(six_bytes):
    # Convert each byte to its hex representation
    hex_values = [format(byte, '02X') for byte in six_bytes]

    # Combine the hex values into a single string
    combined_hex = ''.join(hex_values)

    # Return the last 7 characters of the combined hex string
    bmw_number = combined_hex[-7:]
    pattern = r'^\d[A-Fa-f0-9]{5}\d$'
    return bool(re.match(pattern, bmw_number))

def check_software_data_with_initial_validation(initial_data, software_data):
    # Helper function to extract parts
    def extract_parts(data_list):
        parts_dict = {}
        for item in data_list:
            prefix, value = item.split('_', 1)
            if prefix in parts_dict:
                parts_dict[prefix].append(value)
            else:
                parts_dict[prefix] = [value]
        return parts_dict
    
    # Parse initial and software data
    initial_parts = extract_parts(initial_data.split(', '))
    software_parts = extract_parts(software_data.split(', '))
    
    # Check for DSPL_0Bx validity in initial data
    if any(dspl.startswith('0B') for dspl in software_parts['DSPL']):
        btld_swfl_combinations = set()  # Set to hold unique BTLD and SWFL combinations for DSPL_0Bx
        for i, dspl in enumerate(initial_parts['DSPL']):
            if dspl.startswith('0B'):
                btld_swfl_combinations.add((initial_parts['BTLD'][i], initial_parts['SWFL'][i]))
        if len(btld_swfl_combinations) > 1:
            return False  # Initial data contains DSPL_0Bx with different BTLD and SWFL values
    
    # Check DSPL data
    for dspl in software_parts['DSPL']:
        # Check if DSPL data is in initial data
        if dspl not in initial_parts['DSPL']:
            return False  # DSPL data not found in initial set
        
        # If DSPL data is found, check BTLD and SWFL parts
        dspl_index = initial_parts['DSPL'].index(dspl)
        # Ensure BTLD and SWFL match for the corresponding DSPL
        if initial_parts['BTLD'][dspl_index] != software_parts['BTLD'][0] or initial_parts['SWFL'][dspl_index] != software_parts['SWFL'][0]:
            return False  # BTLD or SWFL data does not match
    
    # If all checks passed
    return True

# Example usage
initial_data = "DSPL_090, HWEL_00B7F0_001_001_001, BTLD_00B7D8_001_003_001, SWFL_00B7F1_001_007_001, DSPL_0B0, HWEL_42525_255_255_255, BTLD_42524_005_001_050, SWFL_42553_006_019_050, DSPL_0B1, HWEL_42525_006_001_002, BTLD_42524_005_001_050, SWFL_42553_006_019_050, DSPL_0B2, HWEL_42525_006_001_002, BTLD_42524_005_001_050, SWFL_42553_006_019_050"
software_data = "DSPL_090, HWEL_00B7F0_001_001_001, BTLD_00B7D8_001_003_001, SWFL_00B7F1_001_007_001"

# Call the function with updated requirement
result = check_software_data_with_initial_validation(initial_data, software_data)
print(f"Match found and initial data valid: {result}")
