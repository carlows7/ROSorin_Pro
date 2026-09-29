# Reto 3: buscar objetos rojos con la camara y guardar foto
import time
import numpy as np
import cv2
import rclpy
from sensor_msgs.msg import Image

rclpy.init()
nodo = rclpy.create_node('camara_sofia')
estado = {'ultima': None}

def recibir(msg):
    img = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
    if msg.encoding == 'rgb8':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    estado['ultima'] = img.copy()

nodo.create_subscription(Image, '/depth_cam/rgb0/image_raw', recibir, 10)

print('Buscando objetos rojos por 10 segundos...')
fin = time.time() + 10
foto = None
while time.time() < fin:
    rclpy.spin_once(nodo, timeout_sec=0.1)
    img = estado['ultima']
    if img is None:
        continue
    foto = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255)) | cv2.inRange(hsv, (170, 120, 70), (180, 255, 255))
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contornos:
        c = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(c) > 800:
            x, y, w, h = cv2.boundingRect(c)
            centro = x + w // 2
            ancho = img.shape[1]
            lado = 'IZQUIERDA' if centro < ancho / 3 else ('DERECHA' if centro > 2 * ancho / 3 else 'CENTRO')
            print('Rojo detectado a la', lado)
            cv2.rectangle(foto, (x, y), (x + w, y + h), (0, 255, 0), 3)
            time.sleep(0.5)

if foto is not None:
    cv2.imwrite('/home/ubuntu/foto.jpg', foto)
    print('Foto guardada en /home/ubuntu/foto.jpg')
else:
    print('No llego ninguna imagen de la camara')
nodo.destroy_node()
rclpy.shutdown()
