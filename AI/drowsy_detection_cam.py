import torch
import numpy as np
import cv2
from matplotlib import pyplot as plt
import uuid
import os 
import time
import ultralytics
from ultralytics import YOLO
from playsound import playsound

model = YOLO('best11.pt')
cap = cv2.VideoCapture(0)
eyecount = 0
mouthcount = 0
last_warned = time.time() 
warning_active = False

while cap.isOpened():
    ret, frame = cap.read()
    
    current_time = time.time()
    font = cv2.FONT_HERSHEY_DUPLEX
    results_list = model(frame)
    
    for results in results_list:
        confs = results.boxes.cls
        confs = confs.type(torch.int32)
        for check in confs:
            if check == 0:
                eyecount = eyecount + 1
                #print("eyecount1:" , eyecount)
            elif check == 3:
                mouthcount = mouthcount + 1
                #print("mouthcount2:", mouthcount)
            elif check == 1:
                if(eyecount > 0):
                    eyecount = eyecount - 1
                #print("eyecount3:" , eyecount)
            elif check == 2:
                if(mouthcount > 0):
                    mouthcount = mouthcount - 1
                #print("mouthcount4:", mouthcount)
        
        if 40 > eyecount >= 20:
            if not warning_active and current_time - last_warned > 5:  # 5초마다 경고
                cv2.putText(frame, "drowsy dectection eyecount", (50,50), font, 1.0, (0, 0, 0), 1)
                playsound("beep-1.wav", block=False)
                last_warned = current_time
                warning_active = True 
        else:
            warning_active = False 
        if eyecount >= 40:
            cv2.putText(frame, "drowsy dectection eyecount", (50,50), font, 1.0, (0, 0, 0), 1)
            playsound("drowsy.wav", block=False)
            eyecount = 0
        if mouthcount >= 25:
            cv2.putText(frame, "drowsy dectection mouthcount", (50,50), font, 1.0, (0, 0, 0), 1)
            playsound("drowsy.wav", block=False)
            mouthcount = 0
        #annotated_image = results.plot()
        #cv2.imshow('YOLO', annotated_image)
        cv2.imshow('YOLO', frame)
    
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()

