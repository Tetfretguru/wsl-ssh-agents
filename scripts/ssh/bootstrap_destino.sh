#!/usr/bin/env bash
set -euo pipefail

echo "[destino] Installing OpenSSH server"
sudo apt-get update
sudo apt-get install -y openssh-server

echo "[destino] Ensuring SSH drop-in config exists"
sudo mkdir -p /etc/ssh/sshd_config.d
sudo tee /etc/ssh/sshd_config.d/opencode.conf >/dev/null <<'EOF'
PubkeyAuthentication yes
PasswordAuthentication yes
PermitRootLogin no
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

echo "[destino] Restarting ssh service"
if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl restart ssh || true
  sudo systemctl enable ssh || true
fi
sudo service ssh restart || true

echo "[destino] SSH status"
if command -v systemctl >/dev/null 2>&1; then
  systemctl status ssh --no-pager || true
fi

echo "[destino] Network hints"
hostname -f || true
ip -4 addr show || true
echo "Done. If WSL uses dynamic IP, configure mirrored mode or Windows port forwarding."
