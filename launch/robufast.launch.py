from launch import LaunchDescription

from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    OpaqueFunction,
    GroupAction,
    SetEnvironmentVariable,
)

from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

from tirrex_demo import (
    get_log_directory,
    get_debug_directory,
    get_demo_timestamp,
    save_replay_configuration,
)


def launch_setup(context, *args, **kwargs):

    robot_namespace = "robufast"

    demo = "tirrex_robufast"
    demo_timestamp = get_demo_timestamp()

    mode = LaunchConfiguration("mode").perform(context)
    record = LaunchConfiguration("record").perform(context)
    demo_config_directory = LaunchConfiguration("demo_config_directory").perform(context)
    debug_directory = get_debug_directory(demo, demo_timestamp, record)
    log_directory = get_log_directory(demo, demo_timestamp, record)

    print(" demo_config_directory ", demo_config_directory)
    print(" debug_directory ", debug_directory)
    print(" log_directory ", log_directory)

    actions = []

    # in rolling : use launch_ros/launch_ros/actions/set_ros_log_dir.py instead
    actions.append(SetEnvironmentVariable("ROS_LOG_DIR", log_directory))

    actions.append(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                get_package_share_directory("tirrex_demo")
                + "/launch/demo.launch.py"
            ),
            launch_arguments={
                "demo": demo,
                "demo_timestamp": demo_timestamp,
                "mode": mode,
                "record": record,
                "robot_namespace": robot_namespace,
            }.items(),
        )
    )

    if record == "true":

        save_replay_configuration(
            demo,
            demo_timestamp,
            "robofast.launch.py",
            {"mode": "replay_"+mode},
        )

    return [GroupAction(actions)]


def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(DeclareLaunchArgument("mode", default_value="simulation"))

    declared_arguments.append(
        DeclareLaunchArgument(
            "demo_config_directory",
            default_value=get_package_share_directory("tirrex_robufast") + "/config",
        )
    )

    declared_arguments.append(DeclareLaunchArgument("record", default_value="false"))

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
