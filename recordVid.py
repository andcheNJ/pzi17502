# -*- coding: utf-8 -*-
"""
Created on Sat May 21 18:35:42 2022

@author: Andrew
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:06:40 2022

@author: Andrew
"""

import cv2, numpy as np
import time
from datetime import datetime
import os

i = 1;
hours = 0
j = 1

win_name = 'Recording'

start_time = time.time()
capture_duration = 10    # number of hours per video

# Connect camera capture and reduce frame size ---③

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS,30)

frame_width = int(cap.get(3))

frame_height = int(cap.get(4))

frame_size = (frame_width, frame_height)

#dirName = r'D:\Videos\vidDir_' + str(j)
sai = datetime.now()
dirName = r'E:\Videos\testVids_' +  sai.strftime("%Y%m%d_time%H%M%S")
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

# output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (frame_width , frame_height))
outVid = dirName  +  '\output_' + str(i) + '.avi'
output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'), 30, (frame_width, frame_height))
while cap.isOpened():
    e1 = cv2.getTickCount()
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
        output = cv2.VideoWriter(outVid, cv2.VideoWriter_fourcc(*'XVID'), 30, (frame_width, frame_height))
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Esc, 종료
        break


else:
    print("can't open camera.")

cap.release()
cv2.destroyAllWindows()
output.release()
