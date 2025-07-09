from launch import LaunchDescription
from launch_ros.actions import ExecuteProcess
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description(): 
    world_path = PathJoinSubstitution([
        FindPackageShare('scoutbot_sim'), 
        'worlds', 
        'basic_world.world'
    ])

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_path],
            output='screen'
        )
    ])

    return LaunchDescription([
        gazebo
    ])

