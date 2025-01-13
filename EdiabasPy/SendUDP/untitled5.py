# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:01:55 2024

@author: testhouse
"""

import subprocess
import time

# Define the base command without the variable parts
base_command = ["python", "E:/Scripts/EdiabasPy/SendUDP/sendhsfz_2.py", "--ip-addr", "169.254.167.64:13400"]

# Define a list of tuples with the variable parts of the command, durations, and messages
# For example: (command_parts, duration_in_seconds, "Message to print")
commands_with_duration_messages = [
    (["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 5, "PAD sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 5, "wohnen sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "03", "03", "88"], 5, "stnd sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 5, "wohnen sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 5, "PAD sent"),
    # Add more commands, durations, and messages here
]

for command_parts, duration, message in commands_with_duration_messages:
    # Combine the base command with the variable parts
    full_command = base_command + command_parts
    
    # Print the command being sent for debugging
    print("Sending command:", " ".join(full_command))
    
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
