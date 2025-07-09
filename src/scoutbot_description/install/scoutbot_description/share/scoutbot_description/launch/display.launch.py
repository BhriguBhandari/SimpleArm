from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_path = FindPackageShare("scoutbot_description")
    urdf_path = PathJoinSubstitution([pkg_path, "urdf", "arm.urdf.xacro"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": Command(["xacro ", urdf_path])
            }]
        ),
        Node( 
            package="joint_state_publisher", 
            executable="joint_state_publisher", 
            name="joint_state_publisher", 
            output="screen",
        ), 
        Node( 
            package="joint_state_publisher_gui", 
            executable="joint_state_publisher_gui", 
            name="joint_state_publisher_gui", 
            output="screen", 
            parameters=[{ 
                "robot_description": Command(["xacro ", urdf_path])
            }]
        ), 
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
        )
    ])
