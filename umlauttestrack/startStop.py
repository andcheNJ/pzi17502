# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:03:54 2024

@author: testhouse
"""

import requests

def post_start_stop():
    url = "http://192.168.1.2:8080/api/startStop"
    headers = {"accept": "*/*"}
    # As your curl command has `-d ""`, it indicates an empty data payload.
    # In the requests.post call, we can represent this with an empty dictionary for the data parameter.
    response = requests.post(url, headers=headers, data={})

    # Check if the response status code is successful
    if response.status_code == 200:
        print("Request successful.")
        # Uncomment the following line if you want to print the response content
        # print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")

# Example usage
post_start_stop()
