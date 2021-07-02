#! /usr/bin/env python

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

# --- Define our Class
def imgmsg_to_cv2(img_msg):
    if img_msg.encoding != "bgr8":
        rospy.logerr("This Coral detect node has been hardcoded to the 'bgr8' encoding.  Come change the code if you're actually trying to implement a new camera")
    dtype = np.dtype("uint8") # Hardcode to 8 bits...
    dtype = dtype.newbyteorder('>' if img_msg.is_bigendian else '<')
    image_opencv = np.ndarray(shape=(img_msg.height, img_msg.width, 3), # and three channels of data. Since OpenCV works with bgr natively, we don't need to reorder the channels.
                    dtype=dtype, buffer=img_msg.data)
    # If the byt order is different between the message and the system.
    if img_msg.is_bigendian == (sys.byteorder == 'little'):
        image_opencv = image_opencv.byteswap().newbyteorder()
    return image_opencv
def cv2_to_imgmsg(cv_image):
    img_msg = Image()
    img_msg.height = cv_image.shape[0]
    img_msg.width = cv_image.shape[1]
    img_msg.encoding = "rgb8"
    img_msg.is_bigendian = 0
    img_msg.data = cv_image.tostring()
    img_msg.step = len(img_msg.data) // img_msg.height # That double line is actually integer division, not a comment
    return img_msg

class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("face_detec", Image, queue_size=1)
        self.position_pub = rospy.Publisher("center_location", Point, queue_size=1)
        self.image_width_and_height = rospy.Publisher("image_ros_and_cols", Point, queue_size=1)
        self.blue_pub = rospy.Publisher('find_blue', Point, queue_size=1)
        # indicate that target is grabbed
        self.grab_finish_pub = rospy.Publisher('grab_finish', Point, queue_size=1)

        self.name_pub = rospy.Publisher("name_student", String)

        self.image_info = Point()
        self.point = Point()
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
            cv_image = imgmsg_to_cv2(Image, "bgr8")
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
                    if face.shape[0]!= 0 and face.shape[1]!=0:
                        name_student = get_info(face)
                        print(name_student)
                        if name_student != "Unknow":
                            if name_student not in list_student:
                                list_student[name_student] = 0
                                self.name_pub.publish(name_student)
                                print('chua vao')
                                rospy.sleep(5)
                            elif list_student[name_student] == 0:
                                self.name_pub.publish(name_student)
                                print('bug')
                                rospy.sleep(5) 
                    print("list", list_student)
                    if count_pub_blue == 0:

                        self.find_blue.x = 1
                        self.find_blue.y = 0
                        self.find_blue.z = 0
                        #self.blue_pub.publish(self.find_blue)
                        count_pub_blue += 1
                        #self.move_base_client.cancel_goal()  

            objects = ct.update(rects)
            # print(objects.items())

            for (objectID, centroid) in objects.items():
            # (objectID, centroid) =  objects.items()[0]
                text = "ID {}".format(objectID)
                cv2.putText(cv_image, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(cv_image, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                cv2.line(cv_image, (320, 300), (int(centroid[0]), int(centroid[1])), (255, 237, 79), 2)
        
            # publish center location
            # self.point.x = centroid[0]
            # self.point.y = centroid[1]
            
            # self.position_pub.publish(self.point)

            try:
                self.image_pub.publish(cv2_to_imgmsg(cv_image))
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
    prototxt = "/home/huy/cvbridge_build_ws/src/object_detect/src/deploy.prototxt"
    model = "/home/huy/cvbridge_build_ws/src/object_detect/src/res10_300x300_ssd_iter_140000.caffemodel"
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
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
