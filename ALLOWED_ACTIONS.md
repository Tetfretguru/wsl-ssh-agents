# Allowed Actions

## Allowed by default

- Read/search files.
- Start and inspect services (`docker compose up`, `docker ps`, `docker logs`).
- Run health checks (`curl`, process checks).
- Gather and return artifacts.

## Requires explicit approval

- Any delete/remove/prune/truncate operation.
- Any command matching blocked policy patterns.

## Required output contract

- Agents must return one of: `done`, `failed`, `needs_approval`.
- Agents must include evidence paths for completed tasks.
