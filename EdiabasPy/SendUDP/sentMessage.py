# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:36:09 2024

@author: testhouse
"""

import socket
import struct
import sys
from time import sleep

# Constants from sendhsfz.py
TESTER_TOOL_ADDRESS = 0xF4
CONTROL_DIAGNOSIS = 0x01
BCP_IP="169.254.61.64"
DEFAULT_PORT = 13400

def send_pwf(ip_addr, diag_addr, payload):
    """
    Sends a packet to the specified IP address and diagnostic address with the given payload.
    
    :param ip_addr: IP address of the device to send the packet to.
    :param diag_addr: Diagnostic address of the device.
    :param payload: List of bytes representing the UDS data.
    """
    try:
        target_addr = socket.gethostbyname(ip_addr)
    except:
        print(f"Cannot resolve \"{ip_addr}\"", file=sys.stderr)
        return

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server.connect((target_addr, DEFAULT_PORT))
    except Exception as e:
        print(f"Cannot connect to {target_addr}:{DEFAULT_PORT}", file=sys.stderr)
        return

    # Send the packet
    server.send(
        struct.pack(">IH", len(payload) + 2, CONTROL_DIAGNOSIS) +
        bytes([TESTER_TOOL_ADDRESS, diag_addr]) +
        bytes(payload)
    )

    # Close the connection
    server.close()

if __name__ == "__main__":
    # Convert the payload from hex string to bytes
    payload_wohnen = [0x31,0x01,0x10,0x31,0x05, 0x05, 0x73]  # Example payload equivalent to '05 05 73'
    #payload_wohnen = [0x31,0x01,0x10,0x31,0x05]
    payload_PAD = [0x31,0x01,0x10,0x31,0x07, 0x07, 0xD1]
    #payload_PAD = [0x31,0x01,0x10,0x31,0x07]
    payload_stnd = [0x31,0x01,0x10,0x31,0x03, 0x03, 0x88]
    #payload_stnd = [0x31,0x01,0x10,0x31,0x03]
    #payload_parken = [0x31,0x01,0x10,0x31,0x01]
    diag_addr = 16  # Example diagnostic address, needs to be adjusted according to actual use#
    while True:
        
        send_pwf(BCP_IP, diag_addr, payload_wohnen)
        print("Wohnen sent")
      
        sleep(20)
        
        send_pwf(BCP_IP, diag_addr, payload_stnd)
        print("STANDFUNKTIONEN_KUNDE_NICHT_IM_FZG sent")
        
        # send_pwf(BCP_IP, diag_addr, payload_parken)
        # print("parken sent")
        
        sleep(35)
        
        send_pwf(BCP_IP, diag_addr, payload_wohnen)
        print("Wohnen sent")
      
        sleep(20)
        
        send_pwf(BCP_IP, diag_addr, payload_PAD)
        print("PAD sent")
      
        sleep(20)
        
