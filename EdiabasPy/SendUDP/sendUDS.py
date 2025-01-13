# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:01:55 2024

@author: testhouse
"""

import subprocess
import time
#ip_address = "169.254.61.64:6801"
ip_address = "169.254.61.64"              #BCP
#ip_address = "169.254.167.64:13400"         #IPB
# Define the base command without the variable parts : python script to use and the ip address 
python = r"C:\Users\testhouse\anaconda3\envs\ecutest\python.exe"
base_command = [python, "E:/Scripts/EdiabasPy/SendUDP/sendhsfz_2.py", "--ip-addr", ip_address]

# Define a list of tuples with the variable parts of the command, durations, and messages
# For example: (command_parts, duration_in_seconds, "Message to print")
commands_with_duration_messages = [
    (["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 20, "PAD sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 20, "wohnen sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "03", "03", "88"], 40, "stnd sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 20, "wohnen sent"),
    #(["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 5, "PAD sent"),
    # Add more commands, durations, and messages here
]
while True:
    for command_parts, duration, message in commands_with_duration_messages:
        # Combine the base command with the variable parts
        full_command = base_command + command_parts
        
        # Print the command being sent for debugging
        #print("Sending command:", " ".join(full_command))yxcy
        
        # Execute the command and capture output
        result = subprocess.run(full_command, capture_output=True, text=True)
        
        # Print the specific message for this command
        print(message)
        
        # Check if there's output (reply from the command) and print it
        if result.stdout:
            print("Reply:", result.stdout.strip())
        if result.stderr:
            print("Error:", result.stderr.strip())
        
        # Wait for the specified duration before sending the next command
        print(f"Waiting for {duration} seconds...")
        time.sleep(duration)

print("All commands sent.")
