# camera.py
import numpy as np
import cv2
import collections
import time


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.__is_running = False
        self.video = cv2.VideoCapture(0)
        self.frame_deque = collections.deque(maxlen=100)
        time.sleep(1)
        self.start()
    
    def __del__(self):
        self.video.release()
    
    def enque_frame(self):
        print('reading from camera')
        success, frame = self.video.read()
        if success == True:
            print('new length is '+str(len(self.frame_deque)))
            self.frame_deque.append(frame)           

    def deque_frame(self):
        print('deque length is '+str(len(self.frame_deque)))
        if len(self.frame_deque) <= 0:
             return None
        ret, jpeg = cv2.imencode('.jpg', image)
        if ret == True:
            return jpeg.tobytes()
        return None

    def start(self):
        print('starting video queue')
        self.__is_running = True
        while self.__is_running:
            self.enque_frame()
            time.sleep(1)

    def stop(self):
        print('starting video queue')
        self.__is_running = False