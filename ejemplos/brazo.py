# Reto 2: mover base, rotacion de muneca y pinza del brazo
import time
import rclpy
from ros_robot_controller_msgs.msg import ServosPosition, ServoPosition

rclpy.init()
nodo = rclpy.create_node('brazo_sofia')
pub = nodo.create_publisher(ServosPosition, '/ros_robot_controller/bus_servo/set_position', 10)

def mover(nombre, servos, segundos=1.5):
    print(nombre)
    msg = ServosPosition()
    msg.duration = float(segundos)
    for id_servo, pos in servos.items():
        s = ServoPosition()
        s.id = id_servo
        s.position = pos
        msg.position.append(s)
    pub.publish(msg)
    time.sleep(segundos + 0.5)

time.sleep(1)
mover('Base a la izquierda', {1: 400})
mover('Base a la derecha', {1: 600})
mover('Base al centro', {1: 500})
mover('Girar muneca', {5: 350})
mover('Girar muneca al otro lado', {5: 650})
mover('Muneca al centro', {5: 500})
mover('Abrir pinza', {10: 300})
mover('Cerrar pinza', {10: 550})
mover('Pinza normal', {10: 500})
print('Listo!')
nodo.destroy_node()
rclpy.shutdown()
