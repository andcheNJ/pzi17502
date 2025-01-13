# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:39:10 2023

@author: testhouse
"""

import requests
from enum import Enum

class PowerSupplyNames(Enum):
    FIX = 'fix'
    EXT = 'ext'
    MESS = 'mess'

def get_power_supplies_info():
    url = "http://192.168.1.2:8080/api/powerSupplies"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    power_supplies = response.json()

    formatted_data = []
    for ps in power_supplies:
        formatted_data.append(f"Name: {ps['name']}, Voltage: {ps['voltage']}, Current: {ps['current']}, IsControllable: {ps['isControllable']}")

    return formatted_data

def get_power_supply_details(value):
    name = 'fix'
    match value:
        case 1:
            name = 'fix'
        case 2:
            name = 'mess'
        case 3:
            name = 'ext'

            
    url = "http://192.168.1.2:8080/api/powerSupplies"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    power_supplies = response.json()

    for ps in power_supplies:
        if ps['name'].lower() == name.lower():
            voltage_formatted = f"{ps['voltage'] / 100:.2f}V"
            current_formatted = f"{ps['current'] / 100:.2f}A"
            print(voltage_formatted + "$" + current_formatted , flush=True)
            return f"Voltage: {voltage_formatted}, Current: {current_formatted}"

    return "Power supply not found"

def get_power_supply_details_1(power_supply_name: PowerSupplyNames):
    url = "http://192.168.1.2:8080/api/powerSupplies"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    power_supplies = response.json()

    name = power_supply_name.value
    for ps in power_supplies:
        if ps['name'].lower() == name.lower():
            print(ps['voltage'] + "$" + ps['voltage'] , flush=True)
            return ps['voltage'], ps['current']

    return None, None


# Example usage:
print(get_power_supply_details(1))
