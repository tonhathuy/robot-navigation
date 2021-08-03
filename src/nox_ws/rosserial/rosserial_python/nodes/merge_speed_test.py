#! /usr/bin/env python
import sys

import rospy
from geometry_msgs.msg import Vector3Stamped
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64

global speed_act_left
global speed_act_right


def callback_left(speed_l):
    #global speed_act_left
    #speed_act_left = speed_l.vector.x
    rospy.loginfo("left   : %s", speed_l.vector.x)

def callback_right(speed_r):
    #global speed_act_right
    #speed_act_right = speed_l.vector.y
    rospy.loginfo("right: %s", speed_r.vector.y)


def main(args):
    rospy.init_node('merge_speed_py', anonymous=True)
    image_sub = rospy.Subscriber("speed_left", Vector3Stamped, callback_left)
    depth_sub = rospy.Subscriber("speed_right", Vector3Stamped, callback_right)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
