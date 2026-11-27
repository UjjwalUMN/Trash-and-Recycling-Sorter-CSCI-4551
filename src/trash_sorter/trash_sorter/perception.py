import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# Each color: (lowest R, G, B), (highest R, G, B)
COLORS = {
    'red':     ((60, 0, 0), (255, 50, 50)),
    'green':   ((0, 60, 0), (50, 255, 50)),
    'blue':    ((0, 0, 60), (50, 50, 255)),
    'magenta': ((60, 0, 60), (255, 50, 255)),
}


class Perception(Node):

    def __init__(self):
        super().__init__('perception')
        self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)

    def image_callback(self, msg):
        image = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)

        for color, (low, high) in COLORS.items():
            mask = np.all((image >= low) & (image <= high), axis=2)
            rows, cols = np.nonzero(mask)
            if len(cols) > 40:
                self.get_logger().info(f'{color} at pixel ({int(cols.mean())}, {rows.max()})')


def main():
    rclpy.init()
    rclpy.spin(Perception())
    rclpy.shutdown()


if __name__ == '__main__':
    main()