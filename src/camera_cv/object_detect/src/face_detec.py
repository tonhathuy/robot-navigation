#! /usr/bin/env python3
import sys
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)

import sys
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point
import actionlib
from move_base_msgs.msg import *
from actionlib_msgs.msg import *  
from std_msgs.msg import String

from pyimagesearch.centroidtracker_mine import CentroidTracker
import imutils

import json
import requests
import base64
import imutils


class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("face_detec", Image, queue_size=1)
        self.position_pub = rospy.Publisher("center_location", Point, queue_size=1)
        self.image_width_and_height = rospy.Publisher("image_ros_and_cols", Point, queue_size=1)
        self.blue_pub = rospy.Publisher('find_blue', Point, queue_size=1)
        # indicate that target is grabbed
        self.grab_finish_pub = rospy.Publisher('grab_finish', Point, queue_size=1)

        self.name_pub = rospy.Publisher("name_student", String, queue_size=10)

        self.image_info = Point()
        self.point = Point()
        self.bridge = CvBridge()
        self.find_blue = Point()
        self.grab_finish = Point()

        self.image_sub = rospy.Subscriber("usb_cam/image_raw", Image, self.callback, queue_size=1, buff_size=52428800)
        self.move_base_client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.tts_finish_sub = rospy.Subscriber('tts_finish', Point, self.finish_callback, queue_size=1)

    def finish_callback(self, finish):
        global name_student
        if finish.x == 1:
            list_student[name_student] = 1

    def callback(self, Image):
        global cv_image, x, y, count_pub_blue, center, x_range, y_range, x_goal_range, y_goal_range

        try:
            cv_image = self.bridge.imgmsg_to_cv2(Image, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        rows, cols, channels = cv_image.shape

        self.image_info.x = rows
        self.image_info.y = cols
        self.image_width_and_height.publish(self.image_info)

        def get_info(image_read):
            url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/search_face/post/'
            _, a_numpy = cv2.imencode('.jpg', image_read)
            a = a_numpy.tobytes()
            encoded = base64.encodebytes(a)
            image_encoded = encoded.decode('utf-8')

            # ###################################
            token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyMTE1ODk3MiwiZXhwIjozMTEyMDIxMTU4OTcyfQ.eyJ1c2VyX25hbWUiOiJ0ZXN0ZXIxIiwiZGV2aWNlIjoxODA4MDI5Ljg0MzM3MDc2NX0.ZUvTb6-Hz6eors43k2KHUCdnliy-PPiHkWc8a6KN5DxBo8vZ4X4iAexe9PcR20zD6pbzMsxauCTagfJgci_p-g'
            data = {'token': token, 'data': {'image_encoded': image_encoded,
                'class_id': '0', 'model': '0', 'classifier': '0'}}
            headers = {'Content-type': 'application/json'}
            data_json = json.dumps(data)
            response = requests.post(url, data=data_json, headers=headers)
            response = response.json()

            if len(response) > 2:
                get = list(response['data'].values())[6:8]
                name = str(get[-1])
            else:
                name = "Unknow"

            return name

        def find_center():

            global cv_image, x, y, count_pub_blue, center, x_range, y_range, x_goal_range, y_goal_range
            global ct, prototxt, model, net, url, list_student, name_student
            blob = cv2.dnn.blobFromImage(cv2.resize(cv_image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()
            rects = []

            cv2.line(cv_image, (x_range[0], 0), (x_range[0], 480), (0, 0, 0))
            cv2.line(cv_image, (x_range[1], 0), (x_range[1], 480), (0, 0, 0))
            cv2.line(cv_image, (0, y_range[0]), (640, y_range[0]), (0, 0, 0))
            cv2.line(cv_image, (0, y_range[1]), (640, y_range[1]), (0, 0, 0))
            
            # draw goal zone for finish indication
            # x_goal_range = np.array([200, 230])
            # y_goal_range = np.array([190, 210])

            cv2.line(cv_image, (x_goal_range[0], 0), (x_goal_range[0], 480), (0,248,220))
            cv2.line(cv_image, (x_goal_range[1], 0), (x_goal_range[1], 480), (0,248,220))
            cv2.line(cv_image, (0, y_goal_range[0]), (640, y_goal_range[0]), (0,248,220))
            cv2.line(cv_image, (0, y_goal_range[1]), (640, y_goal_range[1]), (0,248,220))

            for i in range(0, detections.shape[2]):
                if detections[0, 0, i, 2] > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([cols, rows, cols, rows])
                    rects.append(box.astype("int"))

                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(cv_image, (startX, startY), (endX, endY), (0, 255, 0), 2)

                    face = cv_image[startY:endY,startX:endX]
                    # print(index.shape)
                    if count_pub_blue == 0:

                        self.find_blue.x = 1
                        self.find_blue.y = 0
                        self.find_blue.z = 0
                        #self.blue_pub.publish(self.find_blue)
                        count_pub_blue += 1
                        #self.move_base_client.cancel_goal()  

            
        
            # publish center location
            # self.point.x = centroid[0]
            # self.point.y = centroid[1]
            
            # self.position_pub.publish(self.point)

            try:
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            except CvBridgeError as e:
                print(e)
            
            # check if object in gra zone, if yes, wait 20s for grabbing
            # if x_range[0]<centroid[0]<x_range[1] and y_range[0]<centroid[1]<y_range[1]:
            #     # ros.sleep(5000)
            #     rospy.loginfo("object in center!")
            #     rospy.sleep(20) 
            #     center = True

        find_center()

        

def main(args):
    global cv_image, x, y, count_pub_blue, center, x_range, y_range, x_goal_range, y_goal_range

    global ct, H, W, prototxt, model, net, url, list_student, name_student

    list_student = {"huy":1}
    ct = CentroidTracker()
    (H, W) = (None, None)
    # load our serialized model from disk
    print("[INFO] loading model...")
    prototxt = "/home/huy1/catkin_build_ws/src/object_detect/src/deploy.prototxt"
    model = "/home/huy1/catkin_build_ws/src/object_detect/src/res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    url = 'http://service.mmlab.uit.edu.vn/checkinService_demo/user_login/post/'
    x = 0
    y = 0
    count_pub_blue = 0
    center = False
    #set grab zone range
    x_range = np.array([310, 330])
    y_range = np.array([290, 310])
    #set goal zone range
    x_goal_range = np.array([300, 380])
    y_goal_range = np.array([30, 130])
    rospy.init_node('object_detection', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
        print("[INFO] loading model...")
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
