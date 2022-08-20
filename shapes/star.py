#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import math

def star(side):
    global vel,pub,rate
    rospy.init_node('square',anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()
    rotations = 0

    while rotations < 4:
        star_side(side)
        rotations += 1


def star_side(side):
    t0 = rospy.Time.now().to_sec()
    dist = 0    
    linear_speed = 0.3
    angular_speed = 0.3
    vel.linear.x = linear_speed
    vel.angular.z = angular_speed

    while dist < ((linear_speed/angular_speed)*(math.pi/2)):
        rospy.loginfo("Turtle slides")
        pub.publish(vel)
        rate.sleep()
        t1 = rospy.Time.now().to_sec()
        angle = (t1-t0) * angular_speed
        dist = (linear_speed/angular_speed) * angle

    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    
    turn()

def turn():
    angular_speed = 0.2
    vel.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    angle = 0
    while True:
        rospy.loginfo("Turtle rotates")
        if angle > (math.pi):
            break
        pub.publish(vel)
        t1 = rospy.Time.now().to_sec()
        angle = (t1-t0) * angular_speed
        rate.sleep()

    vel.angular.z = 0
    pub.publish(vel)

if __name__ == '__main__':
    try:
        star(float(sys.argv[1]))
    except rospy.ROSInterruptException:
        pass
