import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class JointSubscriber(Node):
    def __init__(self):
        super().__init__('joint_subscriber')
        self.subscription = self.create_subscription(
            String,
            'joint_cmd',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received command: "{msg.data}"')
        # In real life: parse this string and send it to ESP32 via serial

def main(args=None):
    rclpy.init(args=args)
    node = JointSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
