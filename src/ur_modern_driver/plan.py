#!/usr/bin/env python
import time
import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from math import pi
from random import random
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from OSC import OSCClient, OSCMessage

from geometry_msgs.msg import PoseStamped
import numpy as np
import time

import thread

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

client = None



poses = [
np.radians([77.32632695, -69.73220526, 121.29976102, -141.59751593, -90.06095192, 168.36293361]),
]



def printRoll():
    while True:
        roll =  np.degrees(group.get_current_rpy())[0]
        
        try:
            clientOSC.send( OSCMessage("/roll", roll ) )
        except:
            pass
        time.sleep(0.1)

def move(i):
    global joints_pos
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    joint_states = rospy.wait_for_message("joint_states", JointState)
    joints_pos = joint_states.position
    print joints_pos

    g.trajectory.points = [
        JointTrajectoryPoint(positions=joints_pos, velocities=[0]*6, time_from_start=rospy.Duration(0.0)),
        JointTrajectoryPoint(positions=poses[i], velocities=[0]*6, time_from_start=rospy.Duration(5.0)),
        ]
    return g

   
def main():
    global client, group, clientOSC
    try:
        rospy.init_node("test_move", anonymous=True, disable_signals=True)
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        print "Waiting for server..."
        client.wait_for_server()
        print "Connected to server"
        parameters = rospy.get_param(None)

        print "============ Starting tutorial setup"

        moveit_commander.roscpp_initialize(sys.argv)
        time.sleep(0.5)
        robot = moveit_commander.RobotCommander()
        group = moveit_commander.MoveGroupCommander("manipulator")


        g = move(0)

        while True:
            client.send_goal(g)
            if not(client.wait_for_result()):
                break


    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()
