cmake_minimum_required(VERSION 3.0.2)
project(moveit_msgs)

set(MSG_DEPS
  std_msgs
  actionlib_msgs
  sensor_msgs
  geometry_msgs
  trajectory_msgs
  shape_msgs
  object_recognition_msgs
  octomap_msgs)

find_package(catkin REQUIRED COMPONENTS message_generation ${MSG_DEPS})

set(MSG_FILES
AllowedCollisionEntry.msg
AllowedCollisionMatrix.msg
AttachedCollisionObject.msg
BoundingVolume.msg
CartesianPoint.msg
CartesianTrajectory.msg
CartesianTrajectoryPoint.msg
CollisionObject.msg
ConstraintEvalResult.msg
Constraints.msg
CostSource.msg
ContactInformation.msg
DisplayTrajectory.msg
DisplayRobotState.msg
GenericTrajectory.msg
Grasp.msg
GripperTranslation.msg
JointConstraint.msg
JointLimits.msg
LinkPadding.msg
LinkScale.msg
MotionPlanRequest.msg
MotionPlanResponse.msg
MotionPlanDetailedResponse.msg
MotionSequenceItem.msg
MotionSequenceRequest.msg
MotionSequenceResponse.msg
MoveItErrorCodes.msg
TrajectoryConstraints.msg
ObjectColor.msg
OrientationConstraint.msg
OrientedBoundingBox.msg
PlaceLocation.msg
PlannerInterfaceDescription.msg
PlannerParams.msg
PlanningScene.msg
PlanningSceneComponents.msg
PlanningSceneWorld.msg
PlanningOptions.msg
PositionConstraint.msg
RobotState.msg
RobotTrajectory.msg
VisibilityConstraint.msg
WorkspaceParameters.msg
KinematicSolverInfo.msg
PositionIKRequest.msg
)

set(SRV_FILES
GetMotionPlan.srv
ExecuteKnownTrajectory.srv
GetStateValidity.srv
GetCartesianPath.srv
GetPlanningScene.srv
GraspPlanning.srv
ApplyPlanningScene.srv
QueryPlannerInterfaces.srv
GetMotionSequence.srv
GetPositionFK.srv
GetPositionIK.srv
GetPlannerParams.srv
SetPlannerParams.srv
UpdatePointcloudOctomap.srv
SaveMap.srv
LoadMap.srv
SaveRobotStateToWarehouse.srv
ListRobotStatesInWarehouse.srv
GetRobotStateFromWarehouse.srv
CheckIfRobotStateExistsInWarehouse.srv
RenameRobotStateInWarehouse.srv
DeleteRobotStateFromWarehouse.srv
ChangeControlDimensions.srv
ChangeDriftDimensions.srv
)

set(ACT_FILES
ExecuteTrajectory.action
MoveGroup.action
MoveGroupSequence.action
Pickup.action
Place.action
)

add_action_files(DIRECTORY action FILES ${ACT_FILES})
add_message_files(DIRECTORY msg FILES ${MSG_FILES})
add_service_files(DIRECTORY srv FILES ${SRV_FILES})

generate_messages(DEPENDENCIES ${MSG_DEPS})

catkin_package(CATKIN_DEPENDS message_runtime ${MSG_DEPS})
