#!/bin/bash
# Ejecutar UNA vez desde la carpeta del repo en tu Mac:  bash mac/instalar.sh
ROBOT="ubuntu@ubuntu.local"
REPO="$(cd "$(dirname "$0")/.." && pwd)"

if ! nc -z -G 3 ubuntu.local 22 2>/dev/null; then
  echo "ERROR: No encuentro el robot. Revisa que el robot este encendido y tu Mac en el mismo Wi-Fi de casa."
  exit 1
fi

echo "== Acceso sin contrasena (si la pide, escribe: ubuntu) =="
[ -f "$HOME/.ssh/id_ed25519" ] || ssh-keygen -t ed25519 -N "" -f "$HOME/.ssh/id_ed25519" -q
ssh-copy-id -o AddressFamily=inet -o StrictHostKeyChecking=accept-new "$ROBOT" >/dev/null 2>&1 || ssh-copy-id -o AddressFamily=inet "$ROBOT"

echo "== Creando atajos en tu Mac =="
sed -i '' '/# robot_kit_sofia/,/^robotfoto/d' "$HOME/.zshrc" 2>/dev/null
cat >> "$HOME/.zshrc" << ZSH
# robot_kit_sofia
ROSORIN_REPO="$REPO"
robot() { ssh -4 ubuntu@ubuntu.local "bash ~/ROSorin_Pro/robot/robot.sh \$*"; }
robotsync() { bash "\$ROSORIN_REPO/mac/subir_al_robot.sh"; }
robotfoto() { robot foto && scp -4 -q ubuntu@ubuntu.local:~/foto.jpg ~/Desktop/foto_robot.jpg && open ~/Desktop/foto_robot.jpg; }
ZSH

bash "$REPO/mac/subir_al_robot.sh"
echo ""
ssh -4 "$ROBOT" "bash ~/ROSorin_Pro/robot/robot.sh bateria"
echo ""
echo "LISTO! Abre una Terminal nueva (Cmd+N) y prueba:  robot ayuda"
