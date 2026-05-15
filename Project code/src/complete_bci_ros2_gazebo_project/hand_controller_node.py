import rclpy

from rclpy.node import Node

from std_msgs.msg import String

from trajectory_msgs.msg import (
    JointTrajectory,
    JointTrajectoryPoint
)

class HandController(Node):

    def __init__(self):

        super().__init__('hand_controller')

        self.subscription = self.create_subscription(
            String,
            '/bci_command',
            self.command_callback,
            10
        )

        self.publisher = self.create_publisher(
            JointTrajectory,
            '/hand_controller/joint_trajectory',
            10
        )

    def command_callback(self, msg):

        command = msg.data

        if command == 'GRASP':
            self.grasp()

        elif command == 'RELEASE':
            self.release()

    def grasp(self):

        traj = JointTrajectory()

        traj.joint_names = [
            'FFJ3',
            'MFJ3',
            'RFJ3',
            'LFJ3',
            'THJ4'
        ]

        point = JointTrajectoryPoint()

        point.positions = [1.0, 1.0, 1.0, 1.0, 0.8]

        point.time_from_start.sec = 1

        traj.points.append(point)

        self.publisher.publish(traj)

    def release(self):

        traj = JointTrajectory()

        traj.joint_names = [
            'FFJ3',
            'MFJ3',
            'RFJ3',
            'LFJ3',
            'THJ4'
        ]

        point = JointTrajectoryPoint()

        point.positions = [0.0, 0.0, 0.0, 0.0, 0.0]

        point.time_from_start.sec = 1

        traj.points.append(point)

        self.publisher.publish(traj)

def main(args=None):

    rclpy.init(args=args)

    node = HandController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
