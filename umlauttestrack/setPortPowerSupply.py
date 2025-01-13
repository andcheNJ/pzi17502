# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:34:36 2023

@author: testhouse
"""

import utils
import json

# function must be named 'func'
#portName example 'Port D' PowerSupplyId '0' 
def func(portName, powerSupplyId):
    
    baseUrl = "http://192.168.1.2:8080/api"
    
    # get portId
    r = utils.request3times('GET', f"{baseUrl}/ports")
    
    if r is not None and r.status_code == 200:
        portsData = r.json()
        #print(portsData)
    else:
        return 'Could not get any ports data from RestAPI'
    
    for port in portsData:
        if port['name'] == portName:
            portId = port['id']
            uMessAvailable = port.get('uMessAvailable')
            break
    else:
        return f'Could not find any port with name {portName}'
    
    # put powerSupplyId
    if uMessAvailable:
        if powerSupplyId == 4:
            data = {"uMessStatus": True, "powerSupplyId": -1}
        else:
            data = {"uMessStatus": False, "powerSupplyId": powerSupplyId}
    else:
        data = {"powerSupplyId": powerSupplyId}
        
    r = utils.request3times(
            'PUT', f"{baseUrl}/ports/{portId}",
            data=json.dumps(data),
            verifyData=True)
    if r is None or r.status_code != 200:
        return f'Failed to set power supply id {powerSupplyId} for port id {portId} ({portName})'
    
    return ''
    if r.status_code == 200:
        print('wake up')
        portsData = r.json()
        return ''
    else:
        return 'Request could not be sent or received correctly. Status code {r.status_code}'
    
func('Port D', 0)