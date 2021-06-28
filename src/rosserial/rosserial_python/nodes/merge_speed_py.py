#!/usr/bin/env python
import sys
import rospy
import message_filters
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Float64

def callback(speed_l, speed_r):
    topic = 'chatter'
    rospy.loginfo("I will publish to the topic %s", topic)
    print("[INFO] okie")

def main(args):
    print("[INFO] loading merge...")
    rospy.init_node('merge_speed_py', anonymous=True)
    image_sub = message_filters.Subscriber("speed_left", Vector3Stamped)
    depth_sub = message_filters.Subscriber("speed_right", Vector3Stamped)
    sync = message_filters.TimeSynchronizer([image_sub, depth_sub], 1)
    sync.registerCallback(callback)
    print("[INFO TEST]")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
