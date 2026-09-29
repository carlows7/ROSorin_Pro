#!/bin/bash
# Copia el codigo del repo (carpetas robot y ejemplos) al robot
ROBOT="ubuntu@ubuntu.local"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
echo "== Copiando codigo al robot =="
ssh -4 "$ROBOT" "mkdir -p ~/ROSorin_Pro" && \
scp -4 -q -r "$REPO/robot" "$REPO/ejemplos" "$ROBOT":~/ROSorin_Pro/ && \
ssh -4 "$ROBOT" "chmod +x ~/ROSorin_Pro/robot/robot.sh" && echo "Codigo actualizado en el robot."
