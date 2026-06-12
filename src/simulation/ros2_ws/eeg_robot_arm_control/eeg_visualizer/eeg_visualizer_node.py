import rclpy

from rclpy.node import Node
from std_msgs.msg import String


class EEGVisualizerNode(Node):

    def __init__(self):

        super().__init__(
            'eeg_visualizer_node'
        )

        self.subscription = (
            self.create_subscription(
                String,
                '/eeg_status',
                self.status_callback,
                10
            )
        )

    def status_callback(self, msg):

        print()

        print("=" * 60)
        print("EEG BRAIN CONTROL STATUS")
        print("=" * 60)
        print(msg.data)
        print("=" * 60)


def main(args=None):

    rclpy.init(args=args)

    node = EEGVisualizerNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()