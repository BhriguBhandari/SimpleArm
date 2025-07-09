from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command 
from launch_ros.substitutions import FindPackageShare
import os 
import yaml
from ament_index_python.packages import get_package_share_directory 
from launch.actions import ExecuteProcess
from launch.actions import TimerAction 

def generate_launch_description(): 
    pkg = FindPackageShare("scoutbot_description")
    urdf_path = PathJoinSubstitution([pkg, "urdf", "arm.urdf.xacro"])

    controller_yaml_path="/home/bbhanda/scoutbot_ws/src/scoutbot_description/config/controller.yaml"

    return LaunchDescription([
        ExecuteProcess( 
            cmd=['gzserver', "--verbose"], 
            output="screen"
        ), 
        ExecuteProcess( 
            cmd=["gzclient"], 
            output="screen"
        ), 
        Node( 
            package="robot_state_publisher", 
            executable="robot_state_publisher", 
            output="screen", 
            parameters=[{
                "robot_description": Command(["xacro ", urdf_path])
            }]
        ), 
        TimerAction(
            period=5.0, 
            actions=[
                Node(
                    package="gazebo_ros", 
                    executable="spawn_entity.py", 
                    arguments=[ 
                        "-entity", "simple_arm", 
                        "-topic", "robot_description", 
                        "-x", "0", "-y", "0", "-z", "0"
                    ], 
                    output="screen"
                )
            ]
        ),
        TimerAction( 
            period=5.0, 
            actions =[ 
                Node(
                    package="controller_manager", 
                    executable="ros2_control_node", 
                    parameters=[{
                        "robot_description": Command(["xacro ", urdf_path])
                        }, 
                        controller_yaml_path
                    ],
                    output="screen"
                ), 
            ] 
        ), 
        TimerAction( 
            period=5.0, 
            actions =[ 
                Node( 
                    package="controller_manager", 
                    executable="spawner", 
                    arguments=["arm_position_controller"], 
                    output="screen"
                ), 
            ] 
        ), 
        TimerAction( 
            period=5.0, 
            actions =[ 
       Node( 
           package="controller_manager", 
           executable="spawner", 
           arguments=["joint_state_broadcaster"], 
           output="screen"
                ), 
            ] 
        )
    ]    
)