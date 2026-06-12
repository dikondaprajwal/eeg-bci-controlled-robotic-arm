import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class EEGCommandNode(Node):

    def __init__(self):
        super().__init__('eeg_command_node')

        self.publisher = self.create_publisher(
            String,
            '/eeg_command',
            10
        )

        self.timer = self.create_timer(
            3.0,
            self.publish_command
        )

        self.commands = [
            "LEFT",
            "RIGHT",
            "FORWARD",
            "HOME"
        ]

        self.index = 0

    def publish_command(self):

        msg = String()

        msg.data = self.commands[self.index]

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published {msg.data}'
        )

        self.index = (self.index + 1) % len(self.commands)


def main(args=None):

    rclpy.init(args=args)

    node = EEGCommandNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()