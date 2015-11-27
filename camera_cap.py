import time
import io
import threading
import numpy as np
import cv2


class Camera(object):
    thread = None
    cap = cv2.VideoCapture()
    frame = None
    width = None
    height = None

    def __init__(self):
        # Get the width and height of frame
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
        # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

    def initialize(self):
        # if self.cap.isOpened() != True:
        #     self.cap.open(0) # Capture video from camera

        #     # Get the width and height of frame
        #     self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        #     self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None :
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    def destroy(self):
        # Release everything if job is finished
        # out.release()
        self.width =  None
        self.height = None
        self.cap.release()
        cv2.destroyAllWindows()

    @classmethod
    def _thread(cls):
        while(cls.cap.isOpened()):
            ret, frame = cls.cap.read()
            if ret == True:
                cls.frame = frame

                # write the flipped frame
                # out.write(frame)

                cv2.imshow('frame',frame)

                if time.time() - cls.last_access > 10:
                    break
            else:
                break
        cls.destroy(cls)

   