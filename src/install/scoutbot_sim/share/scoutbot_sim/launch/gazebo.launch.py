from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command 
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description(): 
    world_path = PathJoinSubstitution([
        FindPackageShare('scoutbot_sim'), 
        'worlds', 
        'basic_world.world'
    ])

    urdf_path = PathJoinSubstitution([
        FindPackageShare('scoutbot_description'), 
        'urdf', 
        'arm.urdf.xacro'
    ])

    return LaunchDescription([
        #Start Gazebo 
        ExecuteProcess( 
            cmd=['gazebo', '--verbose', world_path, '-s', 'libgazebo_ros_factory.so'], 
            output='screen'
        ), 

        #Publish URDF on robot_description 
        Node( 
            package='robot_state_publisher', 
            executable='robot_state_publisher', 
            parameters=[{ 
                'robot_description': Command(['xacro', urdf_path])              
            }]
        ), 

        #Spawn robot in Gazebo 
        ExecuteProcess( 
            cmd=[ 
                'ros2', 'run', 'gazebo_ros', 'spawn_entity.py', '-entity', 'scoutbot', '-topic', 'robot_description', '-x', '0', '-y', '0', '-z', '0.1'
            ], 
            output='screen'
        )
    ])