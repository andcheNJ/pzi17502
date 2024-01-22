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
