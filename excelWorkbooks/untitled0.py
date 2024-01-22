# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:05:56 2023

@author: testhouse
"""

def is_valid_date(date_list):
    # Check if the date list has exactly 3 elements
    if len(date_list) != 3:
        return False

    day, month, year = date_list

    # Check year range if needed (example: 00-99)
    if not (0 <= year <= 99):
        return False

    # Check if the month is valid (1-12)
    if not (1 <= month <= 12):
        return False

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

    return valid_day

# Example usage
SENSOR_PROD_DATUM = [[12, 5, 21], [31, 2, 20]]  # Example data
for date in SENSOR_PROD_DATUM:
    print(is_valid_date(date))
