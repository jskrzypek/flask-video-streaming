# camera.py
import numpy as np
import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.cat_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades/haarcascade_frontalcatface.xml')
        self.face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.0.0/share/OpenCV/haarcascades/haarcascade_eye.xml')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if success == True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # if self.cat_cascade.empty() != True:
            #     cats = self.cat_cascade.detectMultiScale(image, 1.3, 5)
            #     for (x,y,w,h) in cats:
            #         cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            if self.face_cascade.empty() != True:
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                    if self.face_cascade.empty() != True:
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = image[y:y+h, x:x+w]
                        eyes = self.eye_cascade.detectMultiScale(roi_gray)
                        for (ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            ret, jpeg = cv2.imencode('.jpg', image)
            if ret == True:
                return jpeg.tobytes()
            return b''
        else:
            return b''