import base64
import urllib.parse
import requests
import json
import timeit
import sys
# url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/search_face/post/'
url = 'https://aiclub.uit.edu.vn/checkin/checkinService_demo/search_face/post/'

####################################
image_path = "/home/huy/cvbridge_build_ws/src/object_detect/src/test.jpg"
image = open(image_path, 'rb')
image_read = image.read()
encoded = base64.encodestring(image_read)
image_encoded = encoded.decode('utf-8')

####################################
token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyMTE0NTYwNywiZXhwIjozMTEyMDIxMTQ1NjA3fQ.eyJ1c2VyX25hbWUiOiJhZG1pbiIsImRldmljZSI6MTc5NDY2NC42ODE0MjcxMzN9.um3C21q_bKaGm__nlYDm3wU5scYJeEu3JVh8CFW6fSs-85912fKBL9UQsmOpdCNZdgTdNoGE1pq1l-Mbd1dqMQ'
data ={'token': token, 'data':{'image_encoded': image_encoded, 'class_id': '0', 'model': '0', 'classifier': '0'}}
headers = {'Content-type': 'application/json'}
data_json = json.dumps(data)
response = requests.post(url, data = data_json, headers=headers)
print(response)
response = response.json()
print(response)
