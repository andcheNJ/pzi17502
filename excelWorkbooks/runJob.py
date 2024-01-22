# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:36:45 2023

@author: testhouse
"""

import pandas as pd
import time



# df = pd.read_excel (r"E:\Scripts\excelWorkbooks\DTC_Files\Jobs1.xlsx")
# df = df.fillna('')
# size = len(df.index)
# for x in range(size):
#     #df1 =df[["job", "arguement", "delay"]]
#     print(df.job[x])
#     print(df.arguement[x])  
#     time.sleep(df.delay[x])
    
def runJob(fileLocation):
    df = pd.read_excel (fileLocation)
    df = df.fillna('')
    size = len(df.index)
    for x in range(size):      
        #df1 =df[["job", "arguement", "delay"]]
        if df.loops[x] == 1:
            print(df.sgbd[x] + "$" +  df.job[x] + "$"  + str(df.arguement[x]) , flush = True)
            time.sleep(df.delay[x])
        else:
            for w in range(df.loops[x]):
                print(df.sgbd[x] + "$" +  df.job[x] + "$"  + df.arguement[x] , flush = True)
                time.sleep(df.delay[x])



def runJob_1(fileLocation):
    df = pd.read_excel(fileLocation)
    df = df.fillna('')
    size = len(df.index)
    x = 0
    while x < size:
        if df.loops[x] == 1:
            print(df.sgbd[x] + "$" +  df.job[x] + "$"  + str(df.arguement[x]), flush=True)
            time.sleep(df.delay[x])
        else:
            for w in range(df.loops[x]):
                print(df.sgbd[x] + "$" +  df.job[x] + "$"  + df.arguement[x], flush=True)
                time.sleep(df.delay[x])

        # Check if goTo has a number and update the loop index accordingly
        if df.goTo[x] != '' and isinstance(df.goTo[x], (int, float)):
            x = int(df.goTo[x]) - 2  # Move to the specified index
        else:
            x += 1  # Move to the next index
