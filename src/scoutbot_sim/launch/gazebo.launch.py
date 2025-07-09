from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import Command, PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    pkg_sim = FindPackageShare('scoutbot_sim')
    pkg_description = FindPackageShare('scoutbot_description')

    world_path = PathJoinSubstitution([pkg_sim, 'worlds', 'basic_world.world'])
    urdf_xacro_path = PathJoinSubstitution([pkg_description, 'urdf', 'arm.urdf.xacro'])
    controller_config = PathJoinSubstitution([pkg_description, 'config', 'controller.yaml'])

    robot_description = Command(['xacro ',     
    PathJoinSubstitution([
        FindPackageShare('scoutbot_description'),
        'urdf',
        'arm.urdf.xacro'
        ])
    ])

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_path, '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # Spawn robot entity into Gazebo
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
                '-entity', 'scoutbot',
                '-topic', 'robot_description',
                '-x', '0', '-y', '0', '-z', '1.0'
            ],
            output='screen'
        ),

        # Controller manager
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                {'robot_description': robot_description},
                controller_config
            ],
            output='screen'
        ),

        # Load controllers with slight delay
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
                    output='screen'
                ),
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_controller'],
                    output='screen'
                )
            ]
        )
    ])
