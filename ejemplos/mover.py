# Reto 1: mover las ruedas mecanum (adelante, atras, lados, girar)
import time
import rclpy
from geometry_msgs.msg import Twist

rclpy.init()
nodo = rclpy.create_node('mover_sofia')
pub = nodo.create_publisher(Twist, '/controller/cmd_vel', 10)

def mover(x, y, giro, segundos, nombre):
    print(nombre)
    msg = Twist()
    msg.linear.x = x
    msg.linear.y = y
    msg.angular.z = giro
    fin = time.time() + segundos
    while time.time() < fin:
        pub.publish(msg)
        time.sleep(0.1)
    pub.publish(Twist())
    time.sleep(0.5)

time.sleep(1)
mover(0.15, 0.0, 0.0, 1.5, 'Adelante')
mover(-0.15, 0.0, 0.0, 1.5, 'Atras')
mover(0.0, 0.15, 0.0, 1.5, 'Izquierda (de lado)')
mover(0.0, -0.15, 0.0, 1.5, 'Derecha (de lado)')
mover(0.0, 0.0, 0.8, 2.0, 'Girar')
pub.publish(Twist())
print('Listo!')
nodo.destroy_node()
rclpy.shutdown()
