from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg = FindPackageShare("mcg5353_panda_gazebo_moveit")
    gazebo_ros = FindPackageShare("gazebo_ros")

    robot_xacro = PathJoinSubstitution(
        [pkg, "config", "panda_gazebo.urdf.xacro"])
    world = PathJoinSubstitution(
        [pkg, "worlds", "panda_table.world"])
        

    robot_description = {
        "robot_description": Command(["xacro ", robot_xacro])
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [gazebo_ros, "launch", "gazebo.launch.py"])),
        launch_arguments={"world": world, "pause": "true"}.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description, {"use_sim_time": True}],
    )
    
    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "panda",
        ],
        output="screen",
    )
    

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["panda_arm_controller"],
    )

    hand_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["panda_hand_controller"],
    )

    delayed_controllers = TimerAction(
        period=4.0,
        actions=[joint_state_broadcaster,
                 arm_controller, hand_controller],
    )

    unpause_gazebo = TimerAction(
        period=8.0,
        actions=[ExecuteProcess(
            cmd=["ros2", "service", "call", "/unpause_physics", "std_srvs/srv/Empty"],
            output="screen",
        )],
    )

    return LaunchDescription([
        gazebo, robot_state_publisher,
        spawn_robot, delayed_controllers, unpause_gazebo,
    ])
