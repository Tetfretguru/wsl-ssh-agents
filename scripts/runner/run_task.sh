#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <task.json>"
  exit 1
fi

TASK_FILE="$1"

python3 scripts/runner/control_plane.py \
  --task "$TASK_FILE" \
  --hosts inventory/hosts.json \
  --policy policy/policy.json
