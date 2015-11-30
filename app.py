#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from video_deque import VideoDeque
from camera_cv2 import VideoCamera
import logging
import datetime
import time

# import unicode

app = Flask(__name__)
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)  # set the desired logging level here
app.logger.info('app started')

video = None
cv_video = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/00.jpg')
def test_img():
    return open('00.jpg', 'rb').read()

def gen(camera):
    while True:
        frame = camera.deque_frame()
        if frame == None: 
            print('Nothing to deque')
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed',methods=['GET'])
def video_feed():
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cv_feed',methods=['GET'])
def cv_feed():
    return Response(gen(cv_video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame',methods=['POST'])
def upload_frame():
    start = datetime.datetime.now()
    frame = request.files.get('frame')
    cv_video.enque_frame(frame)
    return jsonify({'results': 'enque_frame success'})

if __name__ == '__main__':
    video = VideoCamera()
    cv_video = VideoDeque()
    app.run(host='0.0.0.0', debug=True, threaded=True)
    video.stop()