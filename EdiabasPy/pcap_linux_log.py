# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:34:50 2024

@author: testhouse
"""

import subprocess
import os
from datetime import datetime
import threading
import tracemalloc


# to get detailed traces of object allocations
tracemalloc.start()

# Flag to control the capturing loop
stop_capturing = True

def run_command_in_git_bash(command):
    git_bash_executable = os.path.expandvars(r"C:\Program Files\Git\bin\bash.exe")
    # Use Popen for real-time output
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        try:
            # Print output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        finally:
            process.terminate()  # Ensure process is terminated
            process.wait()       # Wait for the process to terminate
            if process.stdout:
                process.stdout.close()  # Explicitly close the stdout stream


def start_tracing(interface, filesize_limit, output_dir):
    global stop_capturing
    stop_capturing = False  # Reset the flag each time tracing starts
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    # This function now runs in a dedicated thread
    def tracing_thread():
        while not stop_capturing:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pcap_trace_{timestamp}.gzip"
            tshark_command = f'"C:/Program Files/Wireshark/tshark" -i "{interface}" -a filesize:{filesize_limit} -w - | "C:/Program Files/Git/usr/bin/gzip.exe" -9 -f > "{output_dir}/{filename}"'
            print(f"Starting capture with command: {tshark_command}")
            run_command_in_git_bash(tshark_command)
    
    thread = threading.Thread(target=tracing_thread)
    thread.start()

def stop_tracing():
    global stop_capturing
    stop_capturing = True

# Example external control functions
def begin_trace():
    start_tracing("Messtechnik", 2000000, "E:\DLT_Traces\IDCevo_Pcap")

def end_trace():
    stop_tracing()

# Start the managing function if directly run
if __name__ == "__main__":
    begin_trace()
    input("Press Enter to stop tracing...\n")
    end_trace()