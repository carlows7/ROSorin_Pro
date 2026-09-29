# ROSorin_Pro

Programas para el robot **Hiwonder ROSOrin Mecanum Pro** (Jetson Orin, ROS2): ruedas mecanum, brazo de 6 servos, cámara de profundidad Aurora, LIDAR y módulo de voz WonderEcho Pro.

## Estructura

| Carpeta | Contenido |
|---|---|
| `robot/` | `robot.py` (programa maestro de comandos) y `robot.sh` (lanzador que carga ROS2) |
| `ejemplos/` | Retos sueltos: `mover.py`, `brazo.py`, `camara.py`, `mirar.py` |
| `mac/` | `instalar.sh` (configuración inicial) y `subir_al_robot.sh` (copia el código al robot) |

## Conexión

- El robot está en modo LAN (Wi‑Fi de casa). Nombre en la red: `ubuntu.local`
- Usuario `ubuntu` · clave `ubuntu`
- Respaldo por cable USB‑C: `ssh ubuntu@192.168.55.1`
- Modo hotspot de fábrica (si se restaura): red `HW-...`, clave `hiwonder`, IP `192.168.149.1`

## Primera vez (en cada Mac, conectada al Wi‑Fi de casa)

```bash
cd ~/ROSorin_Pro
bash mac/instalar.sh
```

## Uso diario

```bash
robotsync            # copia los cambios del repo al robot
robot ayuda          # lista de comandos
robot adelante 1
robot pinza abrir
robotfoto
robot seguir_rojo 15
```

## Mapa del robot

| Topic | Uso |
|---|---|
| `/controller/cmd_vel` | Ruedas (`geometry_msgs/Twist`) |
| `/ros_robot_controller/bus_servo/set_position` | Servos del brazo (`ServosPosition`) |
| `/depth_cam/rgb0/image_raw` | Cámara RGB |
| `/scan` | LIDAR |
| `/asr_node/voice_words` | Voz reconocida |
| `/ros_robot_controller/battery` | Batería (mV) |

| Servo | Parte | Descanso |
|---|---|---|
| 1 | Base | 500 |
| 2 | Hombro | 725 |
| 3 | Codo | 50 |
| 4 | Muñeca arriba/abajo (cámara) | 150 |
| 5 | Muñeca rotación | 500 |
| 10 | Pinza | 500 |

## Trabajar en equipo (misma terminal)

```bash
ssh -4 ubuntu@ubuntu.local
tmux new -s equipo        # la primera persona
tmux attach -t equipo     # la segunda persona
```

Regla: solo una persona mueve el robot a la vez.
