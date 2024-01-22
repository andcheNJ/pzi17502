# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 21:16:19 2023

@author: Andrew
"""
import search3
#import plotData as pl
import re



here = r'D:\Kameratest\CameraTestApp_release\KameratestApp\bin\Debug\Test_results'
#ecu = r"D:\Kameratest\excelWorkbooks\DTC_Files\ICBox_DTCs.xlsx"
#output = r'D:\Kameratest\excelWorkbooks\DTC_Files\Test.xlsx'
output = r'E:\DTC_Reports'



# def natural_sort(l): 
#     convert = lambda text: int(text) if text.isdigit() else text.lower()
#     alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
#     return sorted(l, key=alphanum_key)



# appended_data = []
# for x in range(10):
#     path = search3.find_all("ErrorReport.txt", here)
#     path1 = natural_sort(path)
#     df = search3.readListDTCs("ICBox")

#     p = path1[x].replace('\'', '')
#     search3.createDTCexcel(df, p, output)
    

#ecu = 



    
def runDTCanalysis(ecu, filename, word):
    
    df = search3.readListDTCs(ecu)
    
    count = word.split("_")
    count1 = int(count[0])
    
    outputFile = output + "\\" + filename + ".xlsx"
    
    searchFile = here + "\\" + filename + "\\" + word + "\\" + "ErrorReport.txt"
    
    search3.createDTCexcel_1(df, searchFile, outputFile, count1)
