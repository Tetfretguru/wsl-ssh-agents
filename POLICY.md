# Policy

This project is execution-first, but safety-constrained.

## Non-negotiable rule

- No destructive action without explicit user approval.
- Destructive means delete/remove/prune/truncate/wipe data resources.

## Default behavior

- If a command matches a blocked pattern, task status is `needs_approval`.
- Agent must return a specific approval request (what, where, why).
- Agent should offer a safe alternative when possible.

## Approval model

- Approval is task-scoped, not global.
- Approval must include:
  - task id
  - command scope
  - reason

## Practical examples

- Blocked by default: `rm -rf`, `docker rm`, `docker system prune`, `truncate -s 0`.
- Allowed: read-only search, logs collection, `docker compose up -d`, health checks.
