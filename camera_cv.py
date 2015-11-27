import time
import io
import threading
import numpy as np
import cv2



# Release everything if job is finished


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                return None

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        # cap = cv2.VideoCapture(0) # Capture video from camera
        cap = cv2.VideoCapture("%02d.jpg") # Capture video from camera
        # cap = cv2.VideoCapture("/Users/jskrzypek/Downloads/One\ Piece/001\ East\ Blue\ Saga/003\ Syrup\ Village\ Arc/opdubnew011.mp4") # Capture video from camera
        # cap.open()
        # println(cap.isOpened())

        # Get the width and height of frame
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
        # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cls.frame = cv2.flip(frame,0)

                # write the flipped frame
                # out.write(frame)

                cv2.imshow('frame',frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                    break

                if time.time() - cls.last_access > 10:
                    break
            else:
                break
        # with picamera.PiCamera() as camera:
        #     # camera setup
        #     camera.resolution = (320, 240)
        #     camera.hflip = True
        #     camera.vflip = True

        #     # let camera warm up
        #     camera.start_preview()
        #     time.sleep(2)

        # stream = io.BytesIO()
        # for foo in camera.capture_continuous(stream, 'jpeg',
        #                                      use_video_port=True):
        #     # store frame
        #     stream.seek(0)
        #     cls.frame = stream.read()

        #     # reset stream for next frame
        #     stream.seek(0)
        #     stream.truncate()

        #     # if there hasn't been any clients asking for frames in
        #     # the last 10 seconds stop the thread
        #     if time.time() - cls.last_access > 10:
        #         break
        cap.release()
        # cv2.destroyAllWindows()
        cls.thread = None
