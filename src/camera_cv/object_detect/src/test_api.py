#!/usr/bin/python3
from ctypes import *
import cv2
import numpy as np
import sys
import os
import time
import json
import requests
import base64
import imutils

url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/user_login/post/'

def get_token():
    
    #url = 'http://192.168.28.73:81/user_login/post/'
    # ------------------------------------
    data = {'user_name': 'tester1', 'password': 'tester1'}
    headers = {'Content-type': 'application/json'}
    data_json = json.dumps(data)
    response = requests.post(url, data=data_json, headers=headers)
    # print(response)
    response = response.json()
    # print(response['token'])
    token = response['token']
    return token


if __name__=="__main__":
    img = cv2.imread('/home/huy/cvbridge_build_ws/src/object_detect/src/test.jpg')
    token = get_token()

    # print(token)

    _, a_numpy = cv2.imencode('.jpg', img)
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
    print(response)