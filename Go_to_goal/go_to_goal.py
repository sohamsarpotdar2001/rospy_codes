#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class Turtlesim:
    def __init__(self):
        rospy.init_node("turtlesim_motion_pose",anonymous=True)
        self.pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
        self.pose_sub = rospy.Subscriber("/turtle1/pose",Pose,self.poseCallback)
        self.pose = Pose()
        self.rate = rospy.Rate(30)

    def poseCallback(self,pose_message):
        self.pose = pose_message
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def distance(self,goal):
        return math.sqrt((goal.x - self.pose.x) ** 2 + (goal.y - self.pose.y) ** 2)

    def linear_vel(self,goal,k_l = 1.5):
        return k_l * self.distance(goal)

    def steering_angle(self,goal):
        return math.atan2(goal.y - self.pose.y, goal.x - self.pose.x)

    def angular_vel(self,goal, k_a = 6):
        return k_a * (self.steering_angle(goal) - self.pose.theta)
        
    def go_to_goal(self):
        goal_pose = Pose()
        goal_pose.x = float(input("Set your x goal: "))
        goal_pose.y = float(input("Set your y goal: "))
        lineartolerance = 0.1
        vel = Twist()

        while self.distance(goal_pose) >= lineartolerance:
            vel.linear.x = self.linear_vel(goal_pose)
            vel.linear.y = 0
            vel.linear.z = 0
            vel.angular.x = 0
            vel.angular.y = 0
            vel.angular.z = self.angular_vel(goal_pose)
            print(self.pose)
            self.pub.publish(vel)
            self.rate.sleep()
        vel.linear.x = 0
        vel.angular.z = 0
        self.pub.publish(vel)
        rospy.spin() 

if __name__ == "__main__":
    try:
        x = Turtlesim()
        x.go_to_goal()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated")