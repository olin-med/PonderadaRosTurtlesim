import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen, Spawn, Kill
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios
import time

class TurtleDriver(Node):
    def __init__(self):
        super().__init__('turtle_driver_node')
        self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.update_timer = self.create_timer(1, self.drive_turtle)
        self.pen_service = self.create_client(SetPen, '/turtle1/set_pen')
        self.spawn_service = self.create_client(Spawn, 'spawn')
        self.terminate_service = self.create_client(Kill, 'kill')

        self.pen_red = 255
        self.pen_green = 210
        self.pen_blue = 20
        self.pen_thickness = 15
        self.pen_disabled = False

        self.create_new_turtle()
        self.apply_initial_pen_settings()

    def create_new_turtle(self):
        self.get_logger().info('Waiting for spawn service...')
        self.spawn_service.wait_for_service()
        spawn_request = Spawn.Request()
        spawn_request.x = 20.0
        spawn_request.y = 20.0
        spawn_request.theta = 0.0
        spawn_request.name = 'turtle2'
        future = self.spawn_service.call_async(spawn_request)
        rclpy.spin_until_future_complete(self, future)
        try:
            response = future.result()
            self.turtle_identifier = response.name
            self.get_logger().info(f'Successfully spawned turtle named: {self.turtle_identifier}')
        except Exception as e:
            self.get_logger().error('Spawn failed due to: %r' % (e,))

    def drive_turtle(self):
        move_cmd = Twist()
        speed = 1.3
        turn_radius = 0.7
        move_cmd.linear.x = speed
        move_cmd.linear.y = 0.0
        move_cmd.angular.z = speed / turn_radius
        self.velocity_publisher.publish(move_cmd)

    def apply_initial_pen_settings(self):
        self.get_logger().info('Waiting for SetPen service...')
        self.pen_service.wait_for_service()
        pen_req = SetPen.Request()
        pen_req.r = self.pen_red
        pen_req.g = self.pen_green
        pen_req.b = self.pen_blue
        pen_req.width = self.pen_thickness
        pen_req.off = self.pen_disabled
        future = self.pen_service.call_async(pen_req)
        rclpy.spin_until_future_complete(self, future)
        try:
            future.result()
            self.get_logger().info('Pen settings applied successfully.')
            self.get_logger().info('Press "Q" to terminate the turtle.')
        except Exception as e:
            self.get_logger().error('Failed to set pen settings: %r' % (e,))

    def terminate_turtle(self):
        if rclpy.ok():
            self.get_logger().info('Waiting for Kill service...')
            self.terminate_service.wait_for_service()
            terminate_request = Kill.Request()
            terminate_request.name = self.turtle_identifier
            future = self.terminate_service.call_async(terminate_request)
            rclpy.spin_until_future_complete(self, future)
            try:
                future.result()
                self.get_logger().info(f'Turtle named {self.turtle_identifier} terminated. Closing terminal in 15 seconds.')
            except Exception as e:
                self.get_logger().error('Termination failed: %r' % (e,))
        else:
            self.get_logger().info('ROS shutting down, no need to kill the turtle')

def main(args=None):
    rclpy.init(args=args)
    driver_node = TurtleDriver()
    shutdown_flag = False
    terminal_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())
        while rclpy.ok():
            if select.select([sys.stdin], [], [], 0)[0]:
                if sys.stdin.read(1) == 'q':
                    driver_node.get_logger().info('Q key pressed, terminating turtle...')
                    driver_node.terminate_turtle()
                    time.sleep(15)
                    break
            rclpy.spin_once(driver_node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, terminal_settings)
        if not shutdown_flag:
            shutdown_flag = True
            rclpy.shutdown()

if __name__ == '__main__':
    main()
