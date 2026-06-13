import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('eeg_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_command(self, command):
        msg = Twist()

        if command == 0:  # LEFT
            msg.angular.z = 0.5

        elif command == 1:  # RIGHT
            msg.angular.z = -0.5

        elif command == 2:  # FORWARD
            msg.linear.x = 0.5

        elif command == 3:  # BACK
            msg.linear.x = -0.5

        else:  # STOP
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)