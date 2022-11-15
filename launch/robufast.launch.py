from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    OpaqueFunction,
)

from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def launch_setup(context, *args, **kwargs):

    mode = LaunchConfiguration("mode").perform(context)
    robot_namespace = LaunchConfiguration("robot_namespace").perform(context)
    joystick_type = LaunchConfiguration("joystick_type").perform(context)
    launch_gazebo = LaunchConfiguration("launch_gazebo").perform(context)

    devices_description = [
        get_package_share_directory("tirrex_robufast") + "/config/proflex.gps.yaml",
        get_package_share_directory("tirrex_robufast") + "/config/xsens.imu.yaml",
        get_package_share_directory("tirrex_robufast") + "/config/sick.lidar.yaml",
    ]

    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            get_package_share_directory("romea_mobile_base_bringup")
            + "/launch/mobile_base.launch.py"
        ),
        launch_arguments={
            "mode": mode,
            "robot_namespace": robot_namespace,
            "robot_type": "robucar",
            "joystick_type": joystick_type,
            "launch_gazebo": launch_gazebo,
            "devices_description": str(devices_description),
        }.items(),
    )

    return [robot]


def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(DeclareLaunchArgument("mode", default_value="simulation"))

    declared_arguments.append(
        DeclareLaunchArgument("robot_namespace", default_value="robufast")
    )

    declared_arguments.append(
        DeclareLaunchArgument("joystick_type", default_value="xbox")
    )

    declared_arguments.append(
        DeclareLaunchArgument("launch_gazebo", default_value="True")
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
