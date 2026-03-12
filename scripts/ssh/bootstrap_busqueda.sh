#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <alias> <user@host>"
  exit 1
fi

ALIAS_NAME="$1"
SSH_TARGET="$2"

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

if [[ ! -f "$HOME/.ssh/id_ed25519" ]]; then
  echo "[busqueda] Generating ed25519 key"
  ssh-keygen -t ed25519 -f "$HOME/.ssh/id_ed25519" -N ""
else
  echo "[busqueda] Existing key found"
fi

if command -v ssh-copy-id >/dev/null 2>&1; then
  echo "[busqueda] Copying key to $SSH_TARGET"
  ssh-copy-id "$SSH_TARGET"
else
  echo "[busqueda] ssh-copy-id not found. Copy key manually:"
  echo "cat ~/.ssh/id_ed25519.pub | ssh $SSH_TARGET 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'"
fi

if ! grep -q "Host $ALIAS_NAME" "$HOME/.ssh/config" 2>/dev/null; then
  cat >> "$HOME/.ssh/config" <<EOF

Host $ALIAS_NAME
  HostName ${SSH_TARGET#*@}
  User ${SSH_TARGET%@*}
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
EOF
fi

chmod 600 "$HOME/.ssh/config" 2>/dev/null || true

echo "[busqueda] Testing SSH alias $ALIAS_NAME"
ssh -o BatchMode=yes "$ALIAS_NAME" "hostname && uname -a" || {
  echo "Passwordless login not ready yet. Retry after validating authorized_keys and sshd on destination."
  exit 2
}

echo "Done. Alias '$ALIAS_NAME' is ready."
