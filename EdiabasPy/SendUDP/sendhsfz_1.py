# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:22:51 2024

@author: testhouse
"""

import subprocess
import datetime

def send_udp_packet(ip_addr, diag_addr, payload):
    # Assuming sendhsfz.py takes similar arguments to construct and send a UDP packet.
    # You might need to adjust the command and arguments according to the actual sendhsfz.py script.
    command = [
        'D:\Kameratest\EdiabasPy\SendUDP\sendhsfz_2.py',  # Update this path to where sendhsfz.py is located in your environment.
        '--ip-addr', ip_addr,
        '--diag-addr', *diag_addr,
        *payload
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL)

def main():
    BCP_IP = "169.254.22.84"
    # Example usage of send_udp_packet function
    # This sends a packet with the example payload '05 05 73', similar to the 'sendpwf 05 05 73' command in the bash script.
    send_udp_packet(BCP_IP, ['16', '31', '01', '10', '31'], ['05', '05', '73'])

if __name__ == "__main__":
    main()
