# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:57:25 2024

@author: testhouse
"""
import xml.etree.cElementTree as ET
import zipfile
import os
def process_pdx(pdx_path):
    if not os.path.exists(pdx_path):
        raise FileNotFoundError(f"PDX file does not exist or could not be found: {pdx_path}")

    with zipfile.ZipFile(pdx_path) as pdx:
        pdx_str = pdx.read("index.xml").decode("utf-8")
        pdx_root = ET.fromstring(pdx_str)

    short_name = pdx_root.find('.//SHORT-NAME').text if pdx_root.find('.//SHORT-NAME') is not None else 'Unknown'
    dspl = 'Unknown'  # Default value

    if 'PHUD' in short_name:
        dspl = 'DSPL_0Bx'  
    elif 'HUD' in short_name:
        dspl = 'DSPL_00A0'  
    elif 'CID' in short_name:
        dspl = 'DSPL_0090' 

    btld_ver = btld_sgbm = swfl_ver = swfl_sgbm = 'Unknown'

    for el in pdx_root.iter():
        if el.text is not None:
            if "swe/btld" in el.text:
                btld_ver = el.text.split('.')[-1].upper()  # Convert to uppercase
                btld_sgbm = el.text.split('.')[-3].split('_')[-1].upper()  # Convert to uppercase
            elif "swe/swfl" in el.text:
                swfl_ver = el.text.split('.')[-1].upper()  # Convert to uppercase
                swfl_sgbm = el.text.split('.')[-3].split('_')[-1].upper()  # Convert to uppercase

    btld_output = f"BTLD_{btld_sgbm}_{btld_ver}" if btld_sgbm != 'Unknown' and btld_ver != 'Unknown' else "BTLD_Unknown"
    swfl_output = f"SWFL_{swfl_sgbm}_{swfl_ver}" if swfl_sgbm != 'Unknown' and swfl_ver != 'Unknown' else "SWFL_Unknown"

    software = f"{dspl}, {btld_output}, {swfl_output}"
    return software

# Example usage:
# pdx_path = 'path/to/your/pdx_file.pdx'
# print(process_pdx(pdx_path))
# Example usage:
#pdx_path = r"E:\SW\17_CID\CID_MID__25__I360_1.009_047_050\CID_MID__25__I360_1.009_047_050.pdx"
#pdx_path = r"E:\SW\15_PHUD\PHUD__50_ECO__I360_1.009_047_050.pdx"
pdx_path = r"E:\SW\18_HUD\HUD__HX_SLP3D__I350_1.008_042_052.pdx"
print(process_pdx(pdx_path))
