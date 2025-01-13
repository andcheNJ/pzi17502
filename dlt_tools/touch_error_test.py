# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:43:59 2024

@author: testhouse
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:23:35 2024

@author: testhouse
"""
from openpyxl import load_workbook  # You need openpyxl to handle existing Excel files
import pandas as pd
from datetime import datetime
import re
import time
from dltmodules.dlt_export import DltExport
from dltmodules import connector
from dltmodules import dlt_filter
import subprocess
from webcam import WebcamRecorder  # Import the WebcamRecorder class
import threading

ip_address_IDC = "169.254.157.47"      #IDC
#ip_address_IDC = "169.254.1.99"         #IDCevo
ip_address = "169.254.61.64"              #BCP
screen = True
amount = 1000000000
csv = ''
base_filename = r'E:\DLT_Traces\IDC23\loop'
excel_filename = r'E:\DLT_Traces\IDC23\error_counts.xlsx'
python = r"C:\Users\testhouse\anaconda3\envs\ecutest\python.exe"
base_command = [python, "E:/Scripts/EdiabasPy/SendUDP/sendhsfz_2.py", "--ip-addr", ip_address]

video_filename = r'E:\Videos\IDC23\output_3.avi'
base_filename_pic = r'E:\TestPics\IDC23\loop'
picture_filename = 'picture.jpg'

# Define a list of tuples with the variable parts of the command, durations, and messages
# For example: (command_parts, duration_in_seconds, "Message to print")
commands_with_duration_messages = [
    (["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 20, "PAD sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 20, "wohnen sent"),
    #(["--diag-addr", "16", "31", "01", "10", "31", "03", "03", "88"], 40, "stnd sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "02", "02", "D9"], 40, "parken sent"),
    (["--diag-addr", "16", "31", "01", "10", "31", "05", "05", "73"], 20, "wohnen sent"),
    #(["--diag-addr", "16", "31", "01", "10", "31", "07", "07", "D1"], 5, "PAD sent"),
    # Add more commands, durations, and messages here
]
# Start logging dlt with variables provided
def start_logging(filename):
    exportOptions = DltExport(None, screen, csv, filename, amount)
    c = connector.DltConnectorThread(ip_address_IDC, exp=exportOptions, buffering=False)
    c.start_reading()
    return c
# Stop the logging and save
def stop_logging(c):
    c.stop_reading()

# Function to count errors in DLT file
def count_errors_in_dlt_file(file_path):
    #error_pattern = re.compile(r'Register 0x0030001C changed')
    error_pattern = re.compile(r'DEL NEIGHBOUR:INCOMPLETE|NEW NEIGHBOUR:FAILED')
    error_count = 0
    try:
        with open(file_path, 'rb') as file:
            for line in file:
                decoded_line = line.decode('latin-1')
                if error_pattern.search(decoded_line):
                    error_count += 1
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    return error_count

# Function to append row to Excel
def append_row_to_excel(filepath, row):
    try:
        # Try to read the existing Excel file
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        # If the file does not exist, create a new DataFrame
        df = pd.DataFrame(columns=['Filename', 'Timestamp', 'Number of Errors'])
    # Convert the row to a DataFrame and append it
    row_df = pd.DataFrame([row])  # Convert row to a DataFrame with a single row
    df = pd.concat([df, row_df], ignore_index=True)  # Use concat instead of append
    df.to_excel(filepath, index=False)
    
def append_row_to_excel_sheet(filepath, row, sheet_name='Sheet1'):
    # Create a DataFrame from the row
    row_df = pd.DataFrame([row])

    try:
        # Try to open the existing workbook
        book = load_workbook(filepath)
        # If the sheet exists, load it, else create a new sheet
        if sheet_name in book.sheetnames:
            writer = pd.ExcelWriter(filepath, engine='openpyxl')  # Specify the ExcelWriter
            writer.book = book  # Load the existing workbook
            writer.sheets = {ws.title: ws for ws in book.worksheets}  # Load existing sheets
            # Get the last row in the existing Excel sheet
            # If the sheet is not empty, start at the first empty row after the existing content.
            startrow = writer.sheets[sheet_name].max_row
            # Append without writing index
            row_df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False, header=False)
        else:
            # The sheet does not exist, we can just write to it as a new sheet
            row_df.to_excel(filepath, sheet_name=sheet_name, index=False)
        writer.save()
        writer.close()
    except FileNotFoundError:
        # If the file does not exist, simply use DataFrame.to_excel to create it
        row_df.to_excel(filepath, sheet_name=sheet_name, index=False)


recorder = WebcamRecorder(video_filename, picture_filename)

# Start recording before the while loop
threading.Thread(target=recorder.start_recording).start()

try:
    iteration = 0
    while iteration < 300:
        iteration += 1
        current_filename = f"{base_filename}_{iteration}.dlt"
        c = start_logging(current_filename)
        
        for command_parts, duration, message in commands_with_duration_messages:
            full_command = base_command + command_parts
            print("Sending command:", " ".join(full_command))
            result = subprocess.run(full_command, capture_output=True, text=True)
            print(message)
            if result.stdout:
                print("Reply:", result.stdout.strip())
            if result.stderr:
                print("Error:", result.stderr.strip())

            if message == "PAD sent":
                # Schedule the picture to be taken 19 seconds after "PAD sent"
                picture_filename = f"{base_filename_pic}_{iteration}.jpg"
                threading.Timer(19, recorder.capture_picture, [picture_filename]).start()

            print(f"Waiting for {duration} seconds...")
            time.sleep(duration)    
        stop_logging(c)
        
        error_count = count_errors_in_dlt_file(current_filename)
        if error_count is not None:
            row = {
                'Filename': current_filename,
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Number of Errors': error_count
            }
            append_row_to_excel(excel_filename, row)

finally:
    # Stop recording after the while loop
    recorder.stop_recording()