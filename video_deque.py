# video_deque.py
from PIL import Image
from fs.memoryfs import MemoryFS
import fs.path
import PIL
import io
import numpy as np
import cv2
import collections
import datetime
import tempfile
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class VideoDeque(object):
    def __init__(self):
        self.frame_deque = collections.deque(maxlen=100)
        self.face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades/haarcascade_eye.xml')
    
    def enque_frame(self, frame):
        frame_io = io.BytesIO()
        frame.save(frame_io)
        self.frame_deque.append(frame_io)
        print('new length is '+str(len(self.frame_deque)))

    
    def deque_frame(self):
        print('deque length is '+str(len(self.frame_deque)))
        if len(self.frame_deque) <= 0:
             return None
        print('dequeing image')
        frame_io = self.frame_deque.popleft()
        nparr = np.array(frame_io.getbuffer(), np.ubyte)
        image = cv2.imdecode(nparr,1)
        print(image.size)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.face_cascade.empty() != True:
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            print('faces length is '+str(len(self.frame_deque)))
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                if self.face_cascade.empty() != True:
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = image[y:y+h, x:x+w]
                    eyes = self.eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        else:
            print('face cascade not open')
        imagergb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', imagergb)
        if ret == True:
            return jpeg.tobytes()
        print('cv2 failed')
        return b''