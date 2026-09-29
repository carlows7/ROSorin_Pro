#!/bin/bash
# Lanzador: carga ROS2 y ejecuta robot.py con los argumentos recibidos
source /opt/ros/*/setup.bash
source ~/ros2_ws/install/setup.bash 2>/dev/null
python3 ~/ROSorin_Pro/robot/robot.py "$@"
