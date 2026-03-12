# North Star

Build a practical, low-friction OpenCode-operated repo for WSL-to-WSL remote execution over SSH.

## In scope

- Execute useful user requests remotely (search, start services, collect outputs).
- Keep agent conversations and execution logs auditable.
- Enforce safety policy, especially no deletion without explicit approval.

## Out of scope

- Heavy platform engineering or distributed consensus systems.
- Abstract orchestration not tied to direct operational value.

## Success criteria

- User requests map to runnable task files.
- Execution yields reproducible logs and artifacts.
- Unsafe destructive actions are blocked by default.
