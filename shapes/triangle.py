#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import math

def triangle(side):
    global vel,pub,rate
    rospy.init_node('triangle',anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate(30)
    vel = Twist()
    rotations = 0

    while rotations < 3:
        triangle_side(side)
        rotations += 1

def triangle_side(side):
    t0 = rospy.Time.now().to_sec()
    dist = 0
    linear_speed = 0.2
    vel.linear.x = linear_speed
    sys.stdout.flush()
    while True:
        rospy.loginfo("Turtle sliding")
        pub.publish(vel)
        rate.sleep()
        t1 = rospy.Time.now().to_sec()
        dist = linear_speed * (t1-t0)
        if dist > side:
            break
    
    vel.linear.x = 0
    pub.publish(vel)
    
    turn()

def turn():
    angular_speed = 0.2
    vel.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    angle = 0
    while True:
        rospy.loginfo("Turtle rotating")
        if angle > (math.pi/3 * 2):
            break
        pub.publish(vel)
        t1 = rospy.Time.now().to_sec()
        angle = ((t1-t0) * angular_speed)
        rate.sleep()

    vel.angular.z = 0
    pub.publish(vel)

if __name__ == '__main__':
    try:
        triangle(float(sys.argv[1]))
    except rospy.ROSInterruptException:
        pass