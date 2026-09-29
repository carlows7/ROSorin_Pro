import sys, time, subprocess
import numpy as np
import cv2
import rclpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from ros_robot_controller_msgs.msg import ServosPosition, ServoPosition

V = 0.15
G = 0.8
rclpy.init()
n = rclpy.create_node('robot_sofia')
pub_v = n.create_publisher(Twist, '/controller/cmd_vel', 10)
pub_s = n.create_publisher(ServosPosition, '/ros_robot_controller/bus_servo/set_position', 10)
img_actual = {'img': None}

def recibir(msg):
    img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
    if msg.encoding == 'rgb8':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_actual['img'] = img.copy()

n.create_subscription(Image, '/depth_cam/rgb0/image_raw', recibir, 10)
time.sleep(1)

def parar():
    for _ in range(5):
        pub_v.publish(Twist())
        time.sleep(0.05)

def rueda(x, y, z, seg):
    seg = min(float(seg), 5.0)
    m = Twist()
    m.linear.x = float(x)
    m.linear.y = float(y)
    m.angular.z = float(z)
    fin = time.time() + seg
    while time.time() < fin:
        pub_v.publish(m)
        time.sleep(0.1)
    parar()

def servo(i, pos, minimo, maximo, seg=1.5):
    pos = max(minimo, min(maximo, int(float(pos))))
    m = ServosPosition()
    m.duration = float(seg)
    s = ServoPosition()
    s.id = i
    s.position = pos
    m.position.append(s)
    pub_s.publish(m)
    time.sleep(seg + 0.3)
    print('Servo', i, 'en', pos)

def imagen(espera=5):
    img_actual['img'] = None
    fin = time.time() + espera
    while time.time() < fin:
        rclpy.spin_once(n, timeout_sec=0.1)
        if img_actual['img'] is not None:
            return img_actual['img']
    return None

def buscar_rojo(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255)) | cv2.inRange(hsv, (170, 120, 70), (180, 255, 255))
    c, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not c:
        return None
    c = max(c, key=cv2.contourArea)
    if cv2.contourArea(c) < 800:
        return None
    x, y, w, h = cv2.boundingRect(c)
    centro = x + w // 2
    ancho = img.shape[1]
    if centro < ancho / 3:
        lado = 'IZQUIERDA'
    elif centro > 2 * ancho / 3:
        lado = 'DERECHA'
    else:
        lado = 'CENTRO'
    return lado, (x, y, w, h)

def ayuda():
    print('''
COMANDOS:
  robot bateria
  robot adelante SEG | atras SEG | izquierda SEG | derecha SEG
  robot girar_izq SEG | girar_der SEG | parar
  robot base POS          (250-750, centro 500)
  robot muneca POS        (200-800, centro 500)
  robot camara POS        (50-900, descanso 150)
  robot pinza abrir | pinza cerrar | pinza POS
  robot brazo_descanso
  robot buscar_rojo SEG
  robot seguir_rojo SEG
  robotfoto
''')

try:
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'ayuda'
    a = sys.argv[2] if len(sys.argv) > 2 else '1'
    if cmd == 'bateria':
        subprocess.run(['ros2', 'topic', 'echo', '--once', '/ros_robot_controller/battery'])
    elif cmd == 'adelante':
        rueda(V, 0, 0, a)
    elif cmd == 'atras':
        rueda(-V, 0, 0, a)
    elif cmd == 'izquierda':
        rueda(0, V, 0, a)
    elif cmd == 'derecha':
        rueda(0, -V, 0, a)
    elif cmd == 'girar_izq':
        rueda(0, 0, G, a)
    elif cmd == 'girar_der':
        rueda(0, 0, -G, a)
    elif cmd == 'parar':
        parar()
    elif cmd == 'base':
        servo(1, a, 250, 750)
    elif cmd == 'muneca':
        servo(5, a, 200, 800)
    elif cmd == 'camara':
        servo(4, a, 50, 900)
    elif cmd == 'pinza':
        pos = {'abrir': 300, 'cerrar': 550}.get(a, a)
        servo(10, pos, 200, 700)
    elif cmd == 'brazo_descanso':
        servo(1, 500, 0, 1000, 1.0)
        servo(5, 500, 0, 1000, 1.0)
        servo(4, 150, 0, 1000, 1.0)
        servo(10, 500, 0, 1000, 1.0)
    elif cmd == 'foto':
        img = imagen()
        if img is None:
            print('No llego imagen de la camara')
        else:
            r = buscar_rojo(img)
            if r:
                x, y, w, h = r[1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                print('Rojo en la foto:', r[0])
            cv2.imwrite('/home/ubuntu/foto.jpg', img)
            print('Foto guardada')
    elif cmd == 'buscar_rojo':
        fin = time.time() + min(float(a), 30)
        while time.time() < fin:
            img = imagen(1)
            if img is None:
                continue
            r = buscar_rojo(img)
            print('Rojo a la ' + r[0] if r else 'No veo rojo')
            time.sleep(0.5)
    elif cmd == 'seguir_rojo':
        fin = time.time() + min(float(a), 30)
        while time.time() < fin:
            img = imagen(1)
            if img is None:
                continue
            r = buscar_rojo(img)
            m = Twist()
            if r and r[0] == 'IZQUIERDA':
                m.angular.z = 0.5
            elif r and r[0] == 'DERECHA':
                m.angular.z = -0.5
            pub_v.publish(m)
            print(r[0] if r else 'No veo rojo')
        parar()
    else:
        ayuda()
finally:
    parar()
    n.destroy_node()
    rclpy.shutdown()
