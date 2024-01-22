# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:53:15 2023

@author: Andrew
"""

import pandas as pd
import re
import numpy as np
#import search2
#import openpyxl
#import xlsxwriter
import appendExcel
#import appendExcel_1
import os



DTCs = []
isPresent = []
i= 1
ls =[] 
# with open(r'C:\Users\Temes3\Documents\search_folder\ErrorReport.txt') as file:
#     file_contents = file.read()
#     print(file_contents)
# df1 = pd.read_excel (r"C:\Users\Andrew\imageMatching\excelFiles\IDC_DTCs.xlsx" , sheet_name="FS") 
   
# with open(r"C:\Users\Andrew\imageMatching\excelFiles\ErrorReport.txt", 'r') as fp:
#     for l_no, line in enumerate(fp):
#         # search string
#         if 'F_ORT_NR' in line:
#             # print('string found in a file')
#             # print('Line Number:', l_no)
#             # print('Line:', line)
#             # print(re.findall(r'\d+', line))
#             DTCs.append(re.findall(r'\d+', line)[0])
            
#         if 'F_VORHANDEN_NR' in line:
#             # print('string found in a file')
#             # print('Line Number:', l_no)
#             # print('Line:', line)
#             # print(re.findall(r'\d+', line))
#             isPresent.append(re.findall(r'\d+', line)[0])
            
#             # don't look for next lines
#             #break
# # print(DTCs) 
# # print(isPresent)  

# x = np.array(DTCs)
# y = np.array(isPresent)
# #print(x)
# df = pd.DataFrame({'DTCs':x, 'isPresent':y})

# df2 = df[df['isPresent'] == '12' ]

# f = [int(i) for i in df['DTCs']]

# x=df1.loc[df1['DTC_Decimal'].isin(f)]

# print(x)
# #x.loc[0,0] = i
# x['TestLoop'] = i



# b = [int(i) for i in df2['DTCs']]

# c=x.loc[x['DTC_Decimal'].isin(b)]

# print(c)
# c['TestLoop'] = i
# #x.loc[0,0] = i

# filename = r'C:\Users\Andrew\imageMatching\excelFiles\OCC.xlsx'
 

# appendExcel.append_df_to_excel(filename, x , sheet_name='Sheet1', index= False)
# appendExcel.append_df_to_excel(filename, c, sheet_name='Sheet2', index= False)

# i+=1
# with pd.ExcelWriter(filename ,mode='a', engine="openpyxl",if_sheet_exists="overlay") as writer:  
#     x.to_excel(writer, sheet_name='Sheet1')
    
# with pd.ExcelWriter(filename ,mode='a', engine="openpyxl",if_sheet_exists="overlay") as writer:  
#     c.to_excel(writer, sheet_name='Sheet2')
    
# writer.close()

#finds certain variables ina test file and stores them in an excel file

def readListDTCs(ecu):
    
    if ecu == "IDC23":
            path = r"D:\Kameratest\excelWorkbooks\DTC_Files\IDC_DTCs.xlsx"
    
    elif ecu == "ICBox":
            path = r"D:\Kameratest\excelWorkbooks\DTC_Files\ICBox_DTCs.xlsx"
    
    elif ecu == "MGU21" or ecu == "MGU18":
            path = r"D:\Kameratest\excelWorkbooks\DTC_Files\MGU_DTCs.xlsx"
            
    elif ecu == "MGU22":
            path = r"D:\Kameratest\excelWorkbooks\DTC_Files\MGU22_DTCs.xlsx"
        
    df1 = pd.read_excel (path , sheet_name="FS")
    return df1

# searches for DTCs in search file and saves them to an excel output file 
def createDTCexcel(df1, searchFile, outputFile):
    global i
    DTCs = []
    isPresent = []
  
    # with open(r'C:\Users\Temes3\Documents\search_folder\ErrorReport.txt') as file:
    #     file_contents = file.read()
    #     print(file_contents)
    #df1 = pd.read_excel (ecu , sheet_name="FS") 
       
    with open(searchFile, 'r') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if 'F_ORT_NR' in line:
                # print('string found in a file')
                # print('Line Number:', l_no)
                # print('Line:', line)
                # print(re.findall(r'\d+', line))
                DTCs.append(re.findall(r'\d+', line)[0])
                
            if 'F_VORHANDEN_NR' in line:
                # print('string found in a file')
                # print('Line Number:', l_no)
                # print('Line:', line)
                # print(re.findall(r'\d+', line))
                isPresent.append(re.findall(r'\d+', line)[0])
                
                # don't look for next lines
                #break
    # print(DTCs) 
    # print(isPresent)  
    
    x = np.array(DTCs)
    y = np.array(isPresent)
    #print(x)
    df = pd.DataFrame({'DTCs':x, 'isPresent':y})
    
    df2 = df[df['isPresent'] == '13' ]
    
    f = [int(i) for i in df['DTCs']]
    
    x=df1.loc[df1['DTC_Decimal'].isin(f)]
    
    print(x)
    #x.loc[:,0] = i
    #x['TestLoop'] = i
    x.insert(5,'TestLoop',i , allow_duplicates = True )
    
    
    
    b = [int(i) for i in df2['DTCs']]
    
    c=x.loc[x['DTC_Decimal'].isin(b)]
    
    print(c)
    #c['TestLoop'] = i
    #c.loc[0,0] = i
   #c.insert(5,'TestLoop', i , allow_duplicates = True)
    
    filename = outputFile
     
    #write to excel file 
    appendExcel.append_df_to_excel(filename, x , sheet_name='storedDTCs', index= False)
    appendExcel.append_df_to_excel(filename, c, sheet_name='presentDTCs', index= False)
    
    i+=1
    
# searches for DTCs in search file and saves them to an excel output file. Here i is received from the C# App
def createDTCexcel_1(df1, searchFile, outputFile, i):
    #global i
    DTCs = []
    isPresent = []
  

    with open(searchFile, 'r') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if 'F_ORT_NR' in line:
                # print('string found in a file')
                # print('Line Number:', l_no)
                # print('Line:', line)
                # print(re.findall(r'\d+', line))
                DTCs.append(re.findall(r'\d+', line)[0])
                
            if 'F_VORHANDEN_NR' in line:
                # print('string found in a file')
                # print('Line Number:', l_no)
                # print('Line:', line)
                # print(re.findall(r'\d+', line))
                isPresent.append(re.findall(r'\d+', line)[0])
                
                # don't look for next lines
                #break
    # print(DTCs) 
    # print(isPresent)  
    
    x = np.array(DTCs)
    y = np.array(isPresent)
    #print(x)
    df = pd.DataFrame({'DTCs':x, 'isPresent':y})
    
    df2 = df[df['isPresent'] == '13' ]
    
    f = [int(i) for i in df['DTCs']]
    
    x=df1.loc[df1['DTC_Decimal'].isin(f)]
    
    #print(x)

    #x['TestLoop'] = i
    x.insert(5,'TestLoop',i , allow_duplicates = True )
    
    
    
    
    b = [int(i) for i in df2['DTCs']]
    
    c=x.loc[x['DTC_Decimal'].isin(b)]
    
    #print(c)
    #c['TestLoop'] = i
    #c.insert(5,'TestLoop',i , allow_duplicates = True )

    
    filename = outputFile
     
    #write to excel file 
    appendExcel.append_df_to_excel(filename, x , sheet_name='storedDTCs', index= False)
    appendExcel.append_df_to_excel(filename, c, sheet_name='presentDTCs', index= False)
    
    # i+=1
        
    
    
    
# find a specific file in given directory    
def findFile(fileName, searchHere, index):
    global ls
    #ls.clear()
    for dirpath, dirnames, filenames in os.walk(searchHere):
        for filename in filenames:
            if filename == fileName:
                filename = os.path.join(dirpath, filename)
                #print(filename)
                #print(dirpath)
                fn = '\'' + filename + '\''
                ls.append(fn)
    return ls

# another find file function but not really tested
def gather_files(folder, ending):
    contents = os.walk(folder)
    files = []
    for (dirpath, dirnames, filenames) in contents:
        files += ([file.splitext()[0] for file in filenames if file.lower().endswith(ending)])
    return files

# finds all files specified by the name variable and returns a list of the paths
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
    


