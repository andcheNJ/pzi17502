# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:51:44 2024

@author: testhouse
"""

s = ['current software: CID : DSPL_090, HWEL_00B7F0_007_001_003, BTLD_00B7D8_007_001_050, SWFL_00B7F1_007_030_050\nexpected software: DSPL_090, BTLD_0000B7D8_007_001_050, SWFL_0000B7F1_007_030_055\nsoftware check: failed\n']
print(s[0])

# Extracting the 'current software' part
current_software_str = s[0].split('\n')[0]  # This splits the string by newlines and gets the first part
print(current_software_str)
