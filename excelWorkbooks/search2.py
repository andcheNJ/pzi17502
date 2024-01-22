# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:41:36 2022

@author: testhouse
"""

#import csv
#import sys
import pandas as pd

#df = pandas.read_csv(r"D:\Kameratest\excelWorkbooks\IDC_DTCs.csv")
#print(df)

# choose the ECU tested 
#df = pd.read_excel (r"D:\Kameratest\excelWorkbooks\IDC_DTCs.xlsx")
df = pd.read_excel (r"D:\Kameratest\excelWorkbooks\ICBox_DTCs.xlsx")
#df = pd.read_excel (r"D:\Kameratest\excelWorkbooks\Kombi_DTCs.xlsx" , sheet_name="FS")
#df = pd.read_excel (r"D:\Kameratest\excelWorkbooks\Kombi_DTCs.xlsx" , sheet_name="IS")
#df = pd.read_csv(r"D:\Kameratest\excelWorkbooks\IDC_DTCs.txt", sep="   ")
#print (df)
#df['DTC Dezimal'].astype('str')
#print(df['DTC Dezimal'].dtypes)

# the ID of the DTC to search for 

s = {12057514, 12057531}

x=df.loc[df['DTC Dezimal'].isin(s)]
print(x)

# a = 20 

# b = '{' + str(a) + '}'

# print(b)

#print(df)
#print(df.loc['12057514'])
#
#a = hex(12057514)
#b = a.replace('0x', '').upper()
#print(df['DTC Dezimal'])
#c = df['DTC Dezimal'].astype('object')
#print(c)
#t= df.loc[df.index.isin([s])]
#print(df['DTC Dezimal'].astype('object').index.isin(s))
#print(df.loc[df['DTC Dezimal']].astype('object').isin([s]))

         #.str.match(s)])
#print(df[df['DTC Hex'].str.match(s)])
#print(df.info())

#print(df.loc['A76306'])