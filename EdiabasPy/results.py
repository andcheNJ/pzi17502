# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:30:23 2023

@author: testhouse
"""

import os
from datetime import datetime
from xml.etree import ElementTree as ET
from typing import Union

class API:
    # Define your API class methods and constants here
    pass

def results_2(directory: str, save_name: str):
    result_dir = directory
    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = os.path.join(result_dir, f"{save_name}_{date}.txt")

    with open(file_name, 'a') as tw:
        if API.apiResultSets() is not None:
            s = API.apiResultSets()

            for set in range(s + 1):
                if API.apiErrorCode() == API.EDIABAS_ERR_NONE:
                    tw.write(f"Date and Time  {datetime.now()}:\n")
                    tw.write(f"SET {set}:\n")

                    if API.apiResultNumber(set=set) is not None:
                        i = API.apiResultNumber(set=set)

                        for index in range(1, i + 1):
                            if API.apiErrorCode() == API.EDIABAS_ERR_NONE:
                                if API.apiResultName(index=index, set=set) is not None:
                                    data = API.apiResultName(index=index, set=set)
                                    tw.write(f"{' ' if index == 1 else '         '}RESULT {index}:  ")

                                    if API.apiResultFormat(data=data, set=set) is not None:
                                        format = API.apiResultFormat(data=data, set=set)

                                        if format == API.APIFORMAT_INTEGER:
                                            intG = API.apiResultInt(data=data, set=set)
                                            tw.write(f"Integer Data: {data} = {intG}\n")

                                        elif format == API.APIFORMAT_TEXT:
                                            t = API.apiResultText(data=data, set=set)
                                            tw.write(f"Text Data: {data} = \"{t}\"\n")

                                        elif format == API.APIFORMAT_CHAR:
                                            c = API.apiResultChar(data=data, set=set)
                                            tw.write(f"Char Data: {data} = {c}\n")

                                        elif format == API.APIFORMAT_BYTE:
                                            b = API.apiResultByte(data=data, set=set)
                                            tw.write(f"Byte Data: {data} = {b}\n")

                                        elif format == API.APIFORMAT_WORD:
                                            w = API.apiResultWord(data=data, set=set)
                                            tw.write(f"Word Data: {data} = {w}\n")

                                        elif format == API.APIFORMAT_LONG:
                                            l = API.apiResultLong(data=data, set=set)
                                            tw.write(f"Long Data: {data} = {l}\n")

                                        elif format == API.APIFORMAT_DWORD:
                                            dw = API.apiResultDWord(data=data, set=set)
                                            tw.write(f"Dword Data: {data} = {dw}\n")

                                        elif format == API.APIFORMAT_REAL:
                                            r = API.apiResultReal(data=data, set=set)
                                            tw.write(f"Real Data: {data} = {r}\n")

                                        elif format == API.APIFORMAT_BINARY:
                                            yb, length = API.apiResultBinary(data=data, set=set)
                                            tw.write(f"Binary Data: {data} = {length}\n")

                                            for x in range(length):
                                                if yb[x] < 16:
                                                    hex_val = f"{yb[x]:X}"
                                                    hex_val1 = f"0{hex_val}"
                                                    tw.write(f" {hex_val1}")
                                                else:
                                                        hex_val = f"{yb[x]:X}"
                                                        tw.write(f" {hex_val}")

                                        tw.write("\n")

                                else:
                                    print("Error in API.apiResultFormat")

                            else:
                                print("Error in API.apiResultName")

                        else:
                            print("Error in API.apiErrorCode")

                else:
                    print("Error in API.apiResultNumber")

            else:
                print("Error in API.apiErrorCode")

    print("Results saved to:", file_name)


                                               
