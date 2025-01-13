# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:00:43 2023

@author: testhouse
"""

import clr  # pip install pythonnet - to use this library

clr.AddReference(r"E:\Scripts\EdiabasPy\DiagnosticModuleDLL\DiagnosticModule.dll") 
from DiagnosticModule import EdiabasSingleton



# Instantiate the C# class
csharp_instance =  EdiabasSingleton()

# Call the C# function
directory = r"E:\DTC_Reports"
saveName = "test1"
_huSgbd = "HU_MGU"

csharp_instance.Job(_huSgbd, "fs_lesen_expert", ", ");              # run an ediabas job of your choice 
#csharp_instance.Job("IPB_APP1","steuern_routine","ID;0x1031;STR;0x07")
csharp_instance.Results_1(directory, saveName)                      # save the results 

def call_csharp_function():
    clr.AddReference(r"E:\Scripts\EdiabasPy\DiagnosticModuleDLL\DiagnosticModule.dll")
    from DiagnosticModule import EdiabasSingleton

    # Instantiate the C# class
    csharp_instance = EdiabasSingleton()

    # Call the C# function
    directory = r"D:\DTC_Reports"
    saveName = "test"
    _huSgbd = "HU_MGU"
    csharp_instance.Job(_huSgbd, "fs_lesen_expert", ", ")
    csharp_instance.Results_1(directory, saveName)
