from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command 
from launch_ros.substitutions import FindPackageShare
import os 
import yaml

def generate_launch_description(): 
    pkg = FindPackageShare("scoutbot_description")
    urdf_path = PathJoinSubstitution([pkg, "urdf", "arm.urdf.xacro"])
    controller_yaml_path = os.path.join(
        os.getenv("AMENT_PREFIX_PATH").split(":")[0], 
        "src", "scoutbot_description", "config", "controller.yaml"
    )

    with open(controller_yaml_path, 'r') as f: 
        controller_params = yaml.safe_load(f)

    return LaunchDescription([
        Node( 
            package="gazebo_ros", 
            executable="gzserver", 
            output="screen"
        ), 
        Node( 
            package="gazebo_ros", 
            executable="gzclient", 
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
        Node(
            package="gazebo_ros", 
            executable="spawn_entity.py", 
            arguments=[ 
                "-entity", "simple_arm", 
                "-topic", "robot_description"
            ], 
            output="screen"
        ), 
        Node(
            package="controller_manager", 
            executable="ros2_control_node", 
            parameters=[
                {"robot_description": Command(["xacro ", urdf_path])}, 
                controller_params
            ], 
            output="screen"
        ), 
        Node( 
            package="controller_manager", 
            executable="spawner", 
            arguments=["joint_state_publisher"], 
            output="screen"
        ), 
        Node( 
            package="controller_manager", 
            executable="spawner", 
            arguments=["arm_position_controller"], 
            output="screen"
       )
    ])