import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('trash_sorter')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    tb3_share = get_package_share_directory('turtlebot3_gazebo')

    models_path = os.path.join(pkg_share, 'models')
    tb3_models_path = os.path.join(tb3_share, 'models')
    existing_gz_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    gz_resource_path = f'{models_path}:{tb3_models_path}:{existing_gz_path}'

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=gz_resource_path
    )

    world_file = os.path.join(tb3_share, 'worlds', 'empty_world.world')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r ' + world_file}.items()
    )

    sdf_file = os.path.join(models_path, 'my_model', 'model.sdf')
    spawn_model = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'default',
            '-name', 'my_model',
            '-file', sdf_file,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5',
        ],
        output='screen'
    )

    can_sdf = os.path.join(models_path, 'can', 'model.sdf')
    spawn_can = Node(
    package='ros_gz_sim',
    executable='create',
    arguments=[
        '-world', 'default',
        '-name', 'soda_can_1',
        '-file', can_sdf,
        '-x', '-2.4095',
        '-y', '13.39',
        '-z', '3.275',
    ],
    output='screen'
)

    # TurtleBot3 waffle on top of the platform (platform top is z = 2.452)
    robot_sdf = os.path.join(tb3_models_path, 'turtlebot3_waffle', 'model.sdf')
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'default',
            '-name', 'turtlebot3_waffle',
            '-file', robot_sdf,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '2.47',
        ],
        output='screen'
    )

    # Colored trash for perception: (model folder, x, y)
    colored_trash = [('boot', 1.5, 0.5), ('fruit', 2.0, -0.6),
                    ('can_blue', 2.5, 1.2), ('can_magenta', 3.0, -1.5)]
    spawn_colored_trash = [
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-world', 'default',
                '-name', name,
                '-file', os.path.join(models_path, name, 'model.sdf'),
                '-x', str(x),
                '-y', str(y),
                '-z', '2.55',
            ],
            output='screen'
        )
        for name, x, y in colored_trash
    ]


    delayed_spawn = TimerAction(
        period=3.0,
        actions=[spawn_model, spawn_can]
    )

    delayed_robot_spawn = TimerAction(
        period=6.0,
        actions=[spawn_robot] + spawn_colored_trash
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', 'config_file:=' + os.path.join(
            tb3_share, 'params', 'turtlebot3_waffle_bridge.yaml')],
        output='screen'
    )

    camera_bridge = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen'
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_share, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_sim,
        delayed_spawn,
        delayed_robot_spawn,
        bridge,
        camera_bridge,
        robot_state_publisher
    ])