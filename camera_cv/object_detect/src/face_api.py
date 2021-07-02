# USAGE
# python detect_faces_video.py

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import base64
import urllib.parse
import requests
import json
import timeit
import sys
import threading
from multiprocessing import Process, Queue

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(
    '/home/huy/cvbridge_build_ws/src/object_detect/src/deploy.prototxt', '/home/huy/cvbridge_build_ws/src/object_detect/src/res10_300x300_ssd_iter_140000.caffemodel')
# url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/user_login/post/'
# url = 'http://192.168.28.73:81/user_login/post/'
url = 'https://aiclub.uit.edu.vn/checkin/checkinService_demo/user_login/post/'

# ------------------------------------
data = {'user_name': 'tester1', 'password': 'tester1'}
headers = {'Content-type': 'application/json'}
data_json = json.dumps(data)
response = requests.post(url, data=data_json, headers=headers)
# print(response)
response = response.json()
print(response['token'])
token = response['token']

# url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/search_face/post/'
url = 'https://aiclub.uit.edu.vn/checkin/checkinService_demo/search_face/post/'
####################################
# q = Queue()


def get_info(image_read):
	url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/search_face/post/'
	_, a_numpy = cv2.imencode('.jpg', image_read)
	a = a_numpy.tobytes()
	encoded = base64.encodebytes(a)
	image_encoded = encoded.decode('utf-8')

	# ###################################

	data = {'token': token, 'data': {'image_encoded': image_encoded,
	    'class_id': '0', 'model': '0', 'classifier': '0'}}
	headers = {'Content-type': 'application/json'}
	data_json = json.dumps(data)
	response = requests.post(url, data=data_json, headers=headers)
	response = response.json()
	return (response)

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
video_capture = cv2.VideoCapture(0)
prev_frame_time = 0
while True:
	# frame = imutils.resize(frame, width=1000)

    ret, frame = video_capture.read()

    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = str(int(fps))
    font = cv2.FONT_HERSHEY_SIMPLEX 
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

	# loop over the detections
    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10

            
            face = frame[startY:endY,startX:endX]
            result = get_info(face)
            print(result)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
        # cv2.putText(frame, text, (startX, y),
        # 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
