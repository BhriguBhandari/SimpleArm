from launch import LaunchDescription 
from launch.action import ExecuteProcess
from launch.substitution import PathJoinSubstition
from launch_ros.substitutions import FindPackageShare

def generate_launch_description(): 
    urdf_path = PathJoinSubstition([
        FindPackageShare('scoutbot_description'), 
        'urdf', 
        'arm.urdf.xacro'
    ])

    return LaunchDescription([
        ExecuteProcess( 
            cmd=[ 
                'ros2', 'run', 'gazebo_ros', 'spawn_entity.py', '-entity', 'scoutbot', '-topic', 'robot_description', '-x', '0', '-y', '0', '-z', '0.1'
            ], 
            output='screen'
        )
    ])