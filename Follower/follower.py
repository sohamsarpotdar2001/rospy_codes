#!/usr/bin/env python3

import turtlesim.srv
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class Turtlesim:
    def __init__(self):
        rospy.init_node("turtlesim_motion_pose",anonymous=True)
        self.pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
        self.pose_sub = rospy.Subscriber("/turtle1/pose",Pose,self.poseCallback)
        rospy.wait_for_service("spawn")
        self.spawner = rospy.ServiceProxy("spawn", turtlesim.srv.Spawn)
        self.spawner(8,2,0,"turtle2")
        self.pub2 = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size=10)
        self.pose_sub2 = rospy.Subscriber("/turtle2/pose",Pose,self.poseCallback_turtle2)
        self.pose = Pose()
        self.pose2 = Pose()
        self.rate = rospy.Rate(30)

    def poseCallback(self,pose_message):
        self.pose = pose_message
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def poseCallback_turtle2(self,pose_message):
        self.pose2 = pose_message
        self.pose2.x = round(self.pose2.x, 4)
        self.pose2.y = round(self.pose2.y, 4)

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
        goal_pose.x = 8
        goal_pose.y = 2
        lineartolerance = 0.1
        vel = Twist()
        vel2 = Twist()
        while rospy.is_shutdown:
            rospy.sleep(0.1)
            while self.distance(goal_pose) >= lineartolerance:
                vel.linear.x = self.linear_vel(goal_pose)
                vel.linear.y = 0
                vel.linear.z = 0
                vel.angular.x = 0
                vel.angular.y = 0
                vel.angular.z = self.angular_vel(goal_pose)
                self.pub.publish(vel)
                self.rate.sleep()
            vel.linear.x = 0
            vel.angular.z = 0
            self.pub.publish(vel)
            a = input()
            if(a == "w"):
                vel2.linear.x = 2
                self.pub2.publish(vel2)
            if(a == "a"):
                vel2.angular.z = 2
                self.pub2.publish(vel2)
            if (a == "s"):
                vel2.linear.x = -2
                self.pub2.publish(vel2)
            if (a == "d"):
                vel2.angular.z = -2
                self.pub2.publish(vel2)
            goal_pose.x = self.pose2.x
            goal_pose.y = self.pose2.y
        rospy.spin()

if __name__ == "__main__":
    try:
        x = Turtlesim()
        x.go_to_goal()
    except rospy.ROSInterruptException:
        pass