# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:58:38 2023

@author: testhouse
"""
#curl -X PUT "http://192.168.1.2:8080/api/clamps/30f" -H  "accept: application/json" -H  "Content-Type: application/json" -d "\"on\""
import requests

def send_put_request(clampName, state):
    if state not in ["on", "off"]:
        raise ValueError("Invalid state. Only 'on' or 'off' are allowed.")
    
    url = f"http://192.168.1.2:8080/api/clamps/{clampName}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = f"\"{state}\""
    
    response = requests.put(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("Request was successful")
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)

# Example usage
def set_status_all(state):
    send_put_request('30',state)
    send_put_request('30b', state)
    send_put_request('30f', state)
    
    
    
#set_status_all('on')