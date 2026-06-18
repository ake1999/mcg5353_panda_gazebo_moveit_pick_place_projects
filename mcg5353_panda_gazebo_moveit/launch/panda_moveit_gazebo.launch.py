import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    pkg_share = get_package_share_directory("mcg5353_panda_gazebo_moveit")

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("mcg5353_panda_gazebo_moveit"),
                "launch",
                "panda_gazebo.launch.py",
            ])
        )
    )

    moveit_config = (
        MoveItConfigsBuilder(
            "panda",
            package_name="mcg5353_panda_gazebo_moveit",
        )
        .robot_description(file_path="config/panda_gazebo.urdf.xacro")
        .robot_description_semantic(file_path="config/panda.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(), {"use_sim_time": True}],
        arguments=["--ros-args", "--log-level", "info"],
    )

    rviz_config = os.path.join(pkg_share, "rviz", "panda_moveit_gazebo.rviz")
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            {"use_sim_time": True},
        ],
    )

    delayed_moveit = TimerAction(
        period=7.0,
        actions=[move_group, rviz],
    )

    return LaunchDescription([
        gazebo_launch,
        delayed_moveit,
    ])
