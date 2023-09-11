#!/usr/bin/env python

from __future__ import print_function

import rospy

import sys
import copy
import math
import moveit_commander

import moveit_msgs.msg
from moveit_msgs.msg import Constraints, JointConstraint, PositionConstraint, OrientationConstraint, BoundingVolume
from sensor_msgs.msg import JointState
from moveit_msgs.msg import RobotState
import geometry_msgs.msg
from geometry_msgs.msg import Quaternion, Pose
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

import time
import threading

from niryo_moveit.srv import PointToPointService, PointToPointServiceRequest, PointToPointServiceResponse

group_name = "arm"
move_group = moveit_commander.MoveGroupCommander(group_name)
move_group.set_planning_time(0.04)

joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']

# Between Melodic and Noetic, the return type of plan() changed. moveit_commander has no __version__ variable, so checking the python version as a proxy
if sys.version_info >= (3, 0):
    def planCompat(plan):
        return plan[1]
else:
    def planCompat(plan):
        return plan
        
"""
    Given the start angles of the robot, plan a trajectory that ends at the destination pose.
"""
def plan_trajectory(move_group, destination_pose, start_joint_angles): 
    current_joint_state = JointState()
    current_joint_state.name = joint_names
    current_joint_state.position = start_joint_angles

    moveit_robot_state = RobotState()
    moveit_robot_state.joint_state = current_joint_state
    move_group.set_start_state(moveit_robot_state)

    move_group.set_pose_target(destination_pose)
    plan = move_group.plan()

    if not plan:
        exception_str = """
            Trajectory could not be planned for a destination of {} with starting joint angles {}.
            Please make sure target and destination are reachable by the robot.
        """.format(destination_pose, destination_pose)
        raise Exception(exception_str)

    return planCompat(plan)


"""
    Creates a point-to-point with finish_pose as the destination pose.

    https://github.com/ros-planning/moveit/blob/master/moveit_commander/src/moveit_commander/move_group.py
"""
def plan_point_to_point(req):
    response = PointToPointServiceResponse()

    current_robot_joint_configuration = req.joints_input.joints

    # Pre grasp - position gripper directly above target object
    plan = plan_trajectory(move_group, req.finish_pose, current_robot_joint_configuration)

    # If the trajectory has no points, planning has failed and we return an empty response
    if not plan.joint_trajectory.points:
        move_group.clear_pose_targets()
        return response

    # If trajectory planning worked for all pick and place stages, add plan to response
    response.trajectory = plan
    move_group.clear_pose_targets()

    return response

def moveit_server():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('niryo_moveit_server')

    s = rospy.Service('niryo_moveit', PointToPointService, plan_point_to_point)
    print("Ready to plan")
    rospy.spin()


if __name__ == "__main__":
    moveit_server()
