# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:35:15 2024

@author: testhouse
"""

import cv2
import time
from datetime import datetime

class WebcamRecorder:
    def __init__(self, video_filename, picture_filename):
        self.video_filename = video_filename
        self.picture_filename = picture_filename
        self.cap = cv2.VideoCapture(0)
        self.out = None
        self.recording = False
        self.start_time = None

    def start_recording(self):
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        self.out = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))
        self.recording = True
        self.start_time = time.time()

        while self.recording:
            ret, frame = self.cap.read()
            if ret:
                # Add date and time overlay
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                elapsed_time = time.time() - self.start_time
                elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                text = f"Date: {current_time} | Time since start: {elapsed_time_str}"
                cv2.putText(frame, text, (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

                self.out.write(frame)
                cv2.imshow('Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_recording()
            else:
                break

    def stop_recording(self):
        self.recording = False
        if self.out is not None:
            self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()

    def capture_picture(self):
        ret, frame = self.cap.read()
        if ret:
            # Add date and time overlay
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = f"Date: {current_time}"
            frame_height, frame_width, _ = frame.shape
            cv2.putText(frame, text, (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            cv2.imwrite(self.picture_filename, frame)
            print(f"Picture saved to {self.picture_filename}")
