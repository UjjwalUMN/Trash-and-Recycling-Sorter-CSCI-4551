import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('trash_sorter')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    models_path = os.path.join(pkg_share, 'models')
    existing_gz_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    gz_resource_path = f'{models_path}:{existing_gz_path}' if existing_gz_path else models_path

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=gz_resource_path
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    sdf_file = os.path.join(models_path, 'my_model', 'model.sdf')
    spawn_model = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'empty',
            '-name', 'my_model',
            '-file', sdf_file,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5',
        ],
        output='screen'
    )

    delayed_spawn = TimerAction(
        period=3.0,
        actions=[spawn_model]
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_sim,
        delayed_spawn,
    ])