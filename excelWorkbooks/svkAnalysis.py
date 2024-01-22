# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:07:48 2023

@author: testhouse
"""



def hex_data_to_info(hex_data):
   
    # Exclude the first six elements
    hex_data = [hex_str.upper() for hex_str in hex_data[6:]]
    result_info = []
    i = 0  # iterator for the current position in the hex chunks

    while i < len(hex_data):
        if i + 13 <= len(hex_data):
            # Extract the display bytes
            dspl = hex_data[i] + hex_data[i+1]
            result_info.append(f"DSPL_{dspl}")
            i += 2  # Move past the DSPL

            # Skip the next 4 bytes as they are not needed
            i += 4
            
            # Process the HWEL part
            hwel_hex = ''.join(hex_data[i:i+4])  # Get the BTLD hex part
            hwel_version_major = int(hex_data[i+4], 16)
            hwel_version_minor = int(hex_data[i+5], 16)
            hwel_sequence = int(hex_data[i+6], 16)
            result_info.append(f"HWEL_{hwel_hex}_{hwel_version_major:03d}_{hwel_version_minor:03d}_{hwel_sequence:03d}")
            i += 8  # Move past the HWEL and padding '08'

            # Process the BTLD part
            btld_hex = ''.join(hex_data[i:i+4])  # Get the BTLD hex part
            btld_version_major = int(hex_data[i+4], 16)
            btld_version_minor = int(hex_data[i+5], 16)
            btld_sequence = int(hex_data[i+6], 16)
            result_info.append(f"BTLD_{btld_hex}_{btld_version_major:03d}_{btld_version_minor:03d}_{btld_sequence:03d}")
            i += 8  # Move past the BTLD and padding '08'

            # Process the SWFL part
            swfl_hex = ''.join(hex_data[i:i+4])  # Get the SWFL hex part
            swfl_version_major = int(hex_data[i+4], 16)
            swfl_version_minor = int(hex_data[i+5], 16)
            swfl_sequence = int(hex_data[i+6], 16)
            result_info.append(f"SWFL_{swfl_hex}_{swfl_version_major:03d}_{swfl_version_minor:03d}_{swfl_sequence:03d}")
            i += 7  # Move past the SWFL
        else:
            i += 1  # Move to the next byte if the offset is not found

    return ', '.join(result_info)

dec_array = [[98, 241, 65, 1, 0, 4, 0, 144, 1, 0, 3, 1, 0, 0, 183, 240, 1, 1, 1, 6, 0, 0, 183, 216, 1, 3, 1, 8, 0, 0, 183, 241, 1, 7, 1, 0, 176, 1, 0, 3, 1, 66, 5, 2, 5, 255, 255, 255, 6, 66, 5, 2, 4, 5, 1, 50, 8, 66, 5, 5, 3, 6, 19, 50, 0, 177, 1, 0, 3, 1, 66, 5, 2, 5, 6, 1, 2, 6, 66, 5, 2, 4, 5, 1, 50, 8, 66, 5, 5, 3, 6, 19, 50, 0, 178, 1, 0, 3, 1, 66, 5, 2, 5, 6, 1, 2, 6, 66, 5, 2, 4, 5, 1, 50, 8, 66, 5, 5, 3, 6, 19, 50]]
hex_data = [hex(x)[2:] for x in dec_array[0]]
dec_list = str(dec_array[0])

hex_str = str(hex_data)
out = hex_data_to_info(hex_data)

print(out)