# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:42:36 2024

@author: testhouse
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 21:03:57 2022

@author: Andrew
"""
import cv2, numpy as np
import time
from datetime import datetime, timedelta
import multiprocessing as mp
import queue        #needed for Exception Handling of mp.queue
import threading
import sys
from multiprocessing.pool import ThreadPool
import os

_FINISH = False
# key = cv2.waitKey(1)  & 0xFF

class recordVideo:
 
    
    def __init__(self):


        self.screenon = False
        self.pause = mp.Queue()
        self.commandq = mp.Queue(maxsize=1)
        self.display_status_q = mp.Queue(maxsize=1)
        self.off_counter_q = mp.Queue(maxsize=1)
        #self.status_rec, self.status_send = mp.Pipe(duplex=False)
        #self.offcnt_rec, self.offcnt_send = mp.Pipe(duplex=False)
        self.process = mp.Process(target=self.videoFeed)
        self.t = threading.Thread(target=self.videoFeed)

        self.status_cnt = 0
        self.starttime = time.time()
        # threading.Thread.__init__(self, *args, **keywords) 
        # self.killed = False
        self.x = 1
        global s 
        self.s = 1

        


    # creates videoobject and handles outputpath
    def videoFeed(self):

        self.close = False
     

        # Initial parameters
        capture_duration = 10  # Total hours per video
        frame_rate = 15
        win_name = 'Recording'
        
        # Connect camera capture
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, frame_rate)
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (frame_width, frame_height)
        
        # Create output directory
        sai = datetime.now()
        dirName = r'D:\Videos\testVids_' + sai.strftime("%Y%m%d_time%H%M%S")
        os.makedirs(dirName, exist_ok=True)
        print(f"Directory {dirName} created")
        
        # Initialize video writer
        i = 1
        start_time = time.time()
        outVid = os.path.join(dirName, f'output_{i}.avi')
        output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'), frame_rate, frame_size)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break
        
            # Calculate elapsed time
            duration = time.time() - start_time
            minutes = int(duration / 60)
            hours = int(minutes / 60)
            seconds = duration % 60
        
            # Calculate elapsed time for the duration overlay
            elapsed_time = time.time() - start_time
            elapsed_td = timedelta(seconds=elapsed_time)
            elapsed_str = str(elapsed_td).split('.')[0]  # Remove microseconds for cleaner display
        
            # Add timestamp and duration overlay
            now = datetime.now()
            timestamp = now.strftime("date: %Y/%m/%d time: %H:%M:%S")
            duration_text = f"Duration: {elapsed_str}"
            overlay_text = f"{timestamp} | {duration_text}"
            cv2.putText(frame, overlay_text, (20, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
            # Show the frame in a window
            cv2.imshow(win_name, frame)
        
            # Write the frame to the video file
            output.write(frame)
        
            # Check for video splitting condition
            if round(hours) == capture_duration and minutes % 60 == 0 and round(seconds, 0) == 0:
            #if round(minutes) == capture_duration and round(seconds, 0) == 0:
                
                # Release and create a new video file
                output.release()
                i += 1
                capture_duration += 10
                outVid = os.path.join(dirName, f'output_{i}.avi')
                output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'), frame_rate, frame_size)
                if not output.isOpened():
                    print("Failed to open new video file for writing.")
                    break
        
            # Check for exit key
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

                
                  
            if _FINISH:
               break

        
        else:
            print("can't open camera.")
            
        

        cap.release()                          
        cv2.destroyAllWindows()
        output.release()
        
        
        
    def start_vid(self):
        # self.process = mp.Process(target=self.videoFeed)
        # self.process.start()
        self.t = threading.Thread(target=self.videoFeed)
        self.t.start()
        # self.t.join()
        print("start")
        # self.t = threading.Thread(target=self.videoFeed)
        # self.t.start()
        
    def resume_Recording(self):
        self.pause.put(obj=False, block=True, timeout=None)
        print("Resume Recording")
    
    def pause_Recording(self):
        self.pause.put(obj=True, block=True, timeout=None)
        print("Pause Recording")
    
    def terminate(self):
        
        global _FINISH
        # global key
        
        self.t = threading.Thread(target=self.videoFeed)
        # self.t.start()
        # pool = ThreadPool(processes=1)
        # pool.apply_async(self.videoFeed)
        _FINISH = True
        # pool.terminate()
        # pool.join()
        # self.t.join()
        # key = 27

    
    
    def addVar(self, var):
        
        var += 1
        
        return var
      

    

        

        
    def __commandHandlanger__(self, looptime): #handle the commands on client side
        try:
            command = self.commandq.get(block=False)
            if command == 1:
                return self.display_status_q.put((self.screenon, looptime), block=False)
            elif command == 2:
                return self.off_counter_q.put((self.status_cnt,looptime), block=False)
        except queue.Empty:
            return -1
    
    
    def commandoManager(self, commandoNr): #handle the commands on server side (ECU-Test)
        try:
            self.commandq.put(commandoNr, block=True, timeout=1) #send command id to __commandHandlanger__
            if commandoNr == 1:
                try:
                    return  self.display_status_q.get(block=True, timeout=1)
                except queue.Empty:
                    return (False, -1)
            elif commandoNr == 2:
                try:
                    return self.off_counter_q.get(block=True, timeout = 1)
                except queue.Empty:
                    return (False, -1)
        except queue.Full:
            print("command Queue is Full")
            return -1