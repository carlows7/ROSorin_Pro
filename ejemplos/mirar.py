# Mueve la muneca (servo 4) para apuntar la camara. Uso: python3 mirar.py 300
import sys
import time
import rclpy
from ros_robot_controller_msgs.msg import ServosPosition, ServoPosition

pos = max(0, min(1000, int(sys.argv[1])))
rclpy.init()
nodo = rclpy.create_node('mirar_sofia')
pub = nodo.create_publisher(ServosPosition, '/ros_robot_controller/bus_servo/set_position', 10)
time.sleep(1)
msg = ServosPosition()
msg.duration = 1.5
s = ServoPosition()
s.id = 4
s.position = pos
msg.position.append(s)
pub.publish(msg)
time.sleep(2)
print('Muneca en', pos)
nodo.destroy_node()
rclpy.shutdown()
