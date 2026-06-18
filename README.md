# MCG 5353 Panda Gazebo MoveIt Base Package

This repository contains the working base package used in the final robotics sessions.
Students should clone this package, build it, verify that Panda runs in Gazebo with MoveIt, then create their own project packages around it.

## Package

- `mcg5353_panda_gazebo_moveit`

This package starts:

- Gazebo Classic world
- Panda robot model
- `ros2_control` controllers
- MoveIt `move_group`
- RViz MotionPlanning panel

## Install requirements

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-joint-state-broadcaster \
  ros-humble-joint-trajectory-controller \
  ros-humble-position-controllers \
  ros-humble-moveit
```

## Clone and build

```bash
cd ~/ros2_ws/src
git clone git@github.com:ake1999/mcg5353_panda_gazebo_moveit_pick_place_projects.git

cd ~/ros2_ws
colcon build --symlink-install --packages-select mcg5353_panda_gazebo_moveit
source install/setup.bash
```

## Run Gazebo + MoveIt

```bash
ros2 launch mcg5353_panda_gazebo_moveit panda_moveit_gazebo.launch.py
```

Wait until controllers are active and RViz opens. In RViz, choose planning group `panda_arm`, then Plan and Execute.

## Debug checks

```bash
ros2 control list_controllers
ros2 action list | grep panda
ros2 topic echo /joint_states --once
gz model -m panda -p
```

Expected controllers:

- `joint_state_broadcaster` active
- `panda_arm_controller` active
- `panda_hand_controller` active

## Student projects

Students should create their own ROS 2 packages that depend on this base package.
Do not edit files in `/opt/ros/humble/share/...`.
