import rclpy
import time

from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import String

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


POSES = {

    "HOME": [
        0.0,
        -1.57,
        1.57,
        -1.57,
        -1.57,
        0.0
    ],

    "LEFT": [
        1.0,
        -1.57,
        1.57,
        -1.57,
        -1.57,
        0.0
    ],

    "RIGHT": [
        -1.0,
        -1.57,
        1.57,
        -1.57,
        -1.57,
        0.0
    ],

    "FORWARD": [
        0.0,
        -1.0,
        1.0,
        -1.0,
        -1.0,
        0.0
    ],

    "UP": [
        0.0,
        -0.7,
        0.7,
        -0.7,
        -1.57,
        0.0
    ],

    "INSPECT": [
        0.5,
        -1.2,
        1.8,
        -1.8,
        -1.57,
        0.0
    ]
}


class RobotController(Node):

    def __init__(self):

        super().__init__('robot_controller')

        self.subscription = self.create_subscription(
            String,
            '/eeg_command',
            self.command_callback,
            10
        )

        self.action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )

        self.last_command = None
        self.last_execution_time = 0.0
        self.cooldown_seconds = 2.5
        
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

    def command_callback(self, msg):

        command = msg.data

        current_time = time.time()

        if command == self.last_command:

            self.get_logger().info(
                f"Ignoring duplicate command {command}"
            )

            return

        if (
            current_time -
            self.last_execution_time
        ) < self.cooldown_seconds:

            self.get_logger().info(
                "Cooldown active"
            )

            return

        self.get_logger().info(
            f"Received {command}"
        )

        if command not in POSES:

            self.get_logger().warn(
                f"Unknown command {command}"
            )

            return

        self.send_goal(
            POSES[command]
        )

        self.last_command = command

        self.last_execution_time = current_time

        self.get_logger().info(
            f"Received {command}"
        )

        if command not in POSES:

            self.get_logger().warn(
                f"Unknown command {command}"
            )

            return

        self.send_goal(
            POSES[command]
        )

        self.last_command = command

        self.last_execution_time = current_time

    def send_goal(self, positions):

        goal_msg = FollowJointTrajectory.Goal()

        goal_msg.trajectory.joint_names = self.joint_names

        point = JointTrajectoryPoint()

        point.positions = positions

        point.time_from_start.sec = 3

        goal_msg.trajectory.points.append(point)

        self.action_client.wait_for_server()

        self.action_client.send_goal_async(
            goal_msg
        )

        self.get_logger().info(
            "Trajectory sent"
        )


def main(args=None):

    rclpy.init(args=args)

    node = RobotController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()