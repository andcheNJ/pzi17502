# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:45:11 2024

@author: Temes3
"""

import tkinter as tk
from tkinter import filedialog
from recordVid import recordVideo  # Assuming your class is saved in recordVideo.py

class VideoRecorderGUI:
    def __init__(self, master):
        self.master = master
        self.recorder = recordVideo()
        
        # Set title
        master.title("Video Recorder")
        
        # Start button
        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()
        
        # Stop button
        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()
        
        # Pause button
        self.pause_button = tk.Button(master, text="Pause Recording", command=self.pause_recording)
        self.pause_button.pack()

        # Resume button
        self.resume_button = tk.Button(master, text="Resume Recording", command=self.resume_recording)
        self.resume_button.pack()

        # Save location entry
        self.save_location_label = tk.Label(master, text="Save Location:")
        self.save_location_label.pack()
        self.save_location_entry = tk.Entry(master)
        self.save_location_entry.pack()
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_location)
        self.browse_button.pack()
        
        # Number of hours per video
        self.hours_label = tk.Label(master, text="Hours per Video:")
        self.hours_label.pack()
        self.hours_entry = tk.Entry(master)
        self.hours_entry.pack()
    
    def start_recording(self):
        save_location = self.save_location_entry.get()
        hours_per_video = float(self.hours_entry.get())  # Assuming valid float input
        self.recorder = recordVideo(save_location=save_location, hours_per_video=hours_per_video)
        self.recorder.start_vid()
        print(f"Recording started... Saving to {save_location} for {hours_per_video} hours per video.")


    def stop_recording(self):
        # Here, insert logic to stop recording
        print("Recording stopped...")
        self.recorder.terminate()
    
    def pause_recording(self):
        # Here, insert logic to pause recording
        print("Recording paused...")
        self.recorder.pause_Recording()

    def resume_recording(self):
        # Here, insert logic to resume recording
        print("Recording resumed...")
        self.recorder.resume_Recording()

    def browse_location(self):
        # Open a dialog to choose save location
        directory = filedialog.askdirectory()
        self.save_location_entry.delete(0, tk.END)  # Remove current entry
        self.save_location_entry.insert(0, directory)  # Insert the selected directory

def main():
    root = tk.Tk()
    gui = VideoRecorderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
