#! /usr/bin/env python3
import requests
import json
import playsound
from unidecode import unidecode
import os
import urllib3
import shutil
from geometry_msgs.msg import Point
from std_msgs.msg import String

import rospy
import sys

class tts_converter:

    def __init__(self):
        self.tts_finish_pub = rospy.Publisher("tts_finish", Point, queue_size=1)
        
        self.tts_sub = rospy.Subscriber('run_tts', Point, queue_size=1)
        self.name_sub = rospy.Subscriber('name_student', String, self.callback)

        self.tts_finish = Point()

    def callback(self, name):
        print(name.data)
        global url, OUTPUT_MP3_FOLDER
        path, dirs, files = next(os.walk(OUTPUT_MP3_FOLDER))
        input_text = "Xin chào " + name.data
        print(input_text)
        mp3_file_name = unidecode(input_text).replace(' ', '_') + '.wav'
        output_mp3_file = os.path.join(OUTPUT_MP3_FOLDER, mp3_file_name)
        if mp3_file_name not in files:
            payload = {
                'speaker':4,
                'speed':0.8,
                'input': input_text
            }
            headers = {
                'apikey': 'WuGLgBxtGXfeUJYNyskfiq2y0fCZ3YtS'
            }

            response = requests.request('POST', url, data=payload, headers=headers).json()
            print(response["data"]["url"])
            mp3_file = response["data"]["url"]
            
            

            r = requests.get(mp3_file, allow_redirects=True)
            open(output_mp3_file, 'wb').write(r.content)

        try: 
            playsound.playsound(output_mp3_file)
            self.tts_finish.x = 1
            self.tts_finish_pub.publish(self.tts_finish)
        except Exception as e:
            print(e)


def main(args):
    global url, OUTPUT_MP3_FOLDER

    url = 'https://api.zalo.ai/v1/tts/synthesize'

    OUTPUT_MP3_FOLDER = '/home/huy1/catkin_build_ws/src/object_detect/src/mp3_file'
    rospy.init_node('tts', anonymous=True)
    ic = tts_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
