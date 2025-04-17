import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # DualShock parameters
    joy_dev_dsc      = LaunchConfiguration('joy_dev_dsc')
    joy_vel_dsc      = LaunchConfiguration('joy_vel_dsc')
    ack_topic_dsc    = LaunchConfiguration('ack_topic_dsc')
    joy_config_dsc   = LaunchConfiguration('joy_config_dsc')
    config_filepath_dsc = LaunchConfiguration(
        'config_filepath_dsc',
        default=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('teleop_acker_joy'),
                'config', ''
            )),
            joy_config_dsc,
            TextSubstitution(text='.config.yaml')
        ]
    )

    # F710 parameters
    joy_dev_f710     = LaunchConfiguration('joy_dev_f710')
    joy_vel_f710     = LaunchConfiguration('joy_vel_f710')
    ack_topic_f710   = LaunchConfiguration('ack_topic_f710')
    joy_config_f710  = LaunchConfiguration('joy_config_f710')
    config_filepath_f710 = LaunchConfiguration(
        'config_filepath_f710',
        default=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('teleop_acker_joy'),
                'config', ''
            )),
            joy_config_f710,
            TextSubstitution(text='.config.yaml')
        ]
    )

    return LaunchDescription([
        # --- Declare all the launch arguments ---
        DeclareLaunchArgument('joy_dev_dsc',    default_value='/dev/input/dsc'),
        DeclareLaunchArgument('joy_vel_dsc',    default_value='cmd_vel_dsc'),
        DeclareLaunchArgument('ack_topic_dsc',  default_value='drive'),
        DeclareLaunchArgument('joy_config_dsc', default_value='ps4'),

        DeclareLaunchArgument('joy_dev_f710',    default_value='/dev/input/f710'),
        DeclareLaunchArgument('joy_vel_f710',    default_value='cmd_vel_f710'),
        DeclareLaunchArgument('ack_topic_f710',  default_value='opp_drive'),
        DeclareLaunchArgument('joy_config_f710', default_value='f710'),

        # --- DualShock joystick node ---
        
        Node(
            package='joy', executable='joy_node', name='joy_node_dsc',
            parameters=[{
                'dev': '/dev/input/dsc',
                'device_id': 1,    # joystick index from joy_enumerate_devices
                'deadzone': 0.3,
                'autorepeat_rate': 20.0,
            }],
            remappings=[('/joy','/joy_dsc')]
        ),

        # --- Teleop node for DualShock ---
        Node(
            package='teleop_acker_joy', executable='teleop_acker_node',
            name='teleop_acker_joy_node_dsc',
            parameters=[config_filepath_dsc, {'ack_topic': ack_topic_dsc}],
            remappings=[
                ('/joy', '/joy_dsc'),
                ('/cmd/vel', joy_vel_dsc),
            ],
        ),

        # --- F710 joystick node ---
         
        Node(
            package='joy', executable='joy_node', name='joy_node_f710',
            parameters=[{
                'dev': '/dev/input/f710',
                'device_id': 0,
                'deadzone': 0.3,
                'autorepeat_rate': 20.0,
            }],
            remappings=[('/joy','/joy_f710')]
        ),
        # --- Teleop node for F710 ---
        Node(
            package='teleop_acker_joy', executable='teleop_acker_node',
            name='teleop_acker_joy_node_f710',
            parameters=[config_filepath_f710, {'ack_topic': ack_topic_f710}],
            remappings=[
                ('/joy', '/joy_f710'),
                ('/cmd/vel', joy_vel_f710),
            ],
        ),
    ])

