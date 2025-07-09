#!/usr/bin/env python3 

import rclpy #ROS2 Python Library 
from rclpy.node import Node #Base Class for all ROS2 Nodes
from sensor_msgs.msg import JointState #Standard message to describe joint angles 
import math #For sine wave generation

class JointStatePublisher(Node): 
    def __init__(self): 
        super().__init__('joint_state_publisher')
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.start_time = self.get_clock().now().seconds_nanoseconds() [0]

    def timer_callback(self): 
        now = self.get_clock().now().seconds_nanoseconds()[0]
        t = now - self.start_time

        msg = JointState() 
        msg.header.stamp = self.get_clock().now().to_msg() 
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        msg.position = [ 
            math.sin(t), 
            math.sin(t/2),
            math.sin(t/3),
            math.sin(t/4),
            math.sin(t/5),
            math.sin(t/6) 
        ]
        self.publisher.publish(msg)

def main(args=None):
        rclpy.init(args=args)
        node = JointStatePublisher()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
