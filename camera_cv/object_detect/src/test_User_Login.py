import base64
import urllib.parse
import requests
import json
import timeit
# url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/user_login/post/'
#url = 'http://192.168.28.73:81/user_login/post/'
url = 'https://aiclub.uit.edu.vn/checkin/checkinService_demo/user_login/post/'
#------------------------------------
data ={'user_name':'admin', 'password': 'admin'}
headers = {'Content-type': 'application/json'}
data_json = json.dumps(data)
response = requests.post(url, data = data_json, headers=headers)
print(response)
response = response.json()
print(response)
