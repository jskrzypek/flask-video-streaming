#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
from video_deque import VideoDeque
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

# @app.route('/')
# def index():
#     return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.deque_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed',methods=['GET'])
def video_feed():
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame',methods=['POST'],)
def upload_frame():
    start = datetime.datetime.now()
    jsonBody = request.get_json(silent=True)
    content = jsonBody.get('content')
    video.enque_frame(content)
    # return json.dumps(result)
    # retval = jsonify({'results': {'caras': caras}})
    return jsonify({'results': 'enque_frame success'})

if __name__ == '__main__':
    video = VideoDeque()
    app.run(host='0.0.0.0', debug=True)
