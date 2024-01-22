# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 21:03:57 2022

@author: Andrew
"""
import cv2, numpy as np
import time
from datetime import datetime
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
        # img_train = cv2.imread(self.trainp)
        # vcObject = cv2.VideoCapture(self.path, cv2.CAP_DSHOW)
        # vcObject.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # vcObject.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # frame_width = int(vcObject.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frame_height = int(vcObject.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # vwObject = cv2.VideoWriter(self.output, fourcc, 10, (frame_width + img_train.shape[1], frame_height))

        # orb = cv2.ORB_create()
        # kp_train, des_train = orb.detectAndCompute(img_train, None)
        # Prozesszeit = 0
        # i = 0
        # tick_sum = 0
        # avg_prozesszeit = 0
        # global cap
        # global key
        self.close = False
     

        i = 1;
        hours = 0
        # j = 1

        win_name = 'Recording'

        start_time = time.time()
        capture_duration = 10    # number of hours per video

        # Connect camera capture and reduce frame size ---③

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # cap.set(cv2.CAP_PROP_FPS,30)

        frame_width = int(cap.get(3))

        frame_height = int(cap.get(4))

        # frame_size = (frame_width, frame_height)

        #dirName = r'D:\Videos\vidDir_' + str(j)
        sai = datetime.now()
        dirName = r'E:\Logitech\testVids_' +  sai.strftime("%Y%m%d_time%H%M%S")
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")

        # output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (frame_width , frame_height))
        outVid = dirName  +  '\output_' + str(i) + '.avi'
        output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'), 15, (frame_width, frame_height))
        while cap.isOpened():
            # e1 = cv2.getTickCount()
            ret, frame = cap.read()

            duration = time.time() - start_time
            minutes = int(duration / 60)
            hours = int(minutes / 60)
            # if minutes == 60:
            #     minutes = 0
            #     hours += 1
            seconds = duration % 60
            seconds = round(seconds, 2)
            now = datetime.now()
            # write text to the frame
            cv2.putText(frame, now.strftime("date: %Y/%m/%d time: %H:%M:%S") + '  ' + 'hours: ' + str(hours) + '  min: ' + str(
                minutes % 60) + '  sec: ' + str(seconds), (20, frame_height - 20), 0, 0.5, (255, 255, 255), 1,
                        cv2.LINE_AA)

            # 결과 출력
            cv2.imshow(win_name, frame)
            # print(round(seconds % 20))

            if round(hours) < capture_duration:

                output.write(frame)
            #        i += 1

            # print(seconds)
            elif round(hours) == capture_duration and minutes % 60 == 0 and round(seconds,0) == 0:
                output.release()
                i += 1
                capture_duration += 10
                outVid = dirName  +  '\output_' + str(i) + '.avi'
                output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'),15, (frame_width, frame_height))
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Esc, 종료
                break
                
                  
            if _FINISH:
               break

            # global stop_threads
            # if stop_threads:
            #         break

            # print('thread running')
            # stop_threads = False
        
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