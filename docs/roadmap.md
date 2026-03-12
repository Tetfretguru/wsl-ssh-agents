# Roadmap

## Phase 1: SSH baseline

- Bootstrap destination SSH server in WSL.
- Bootstrap search/orchestrator SSH client in WSL.
- Validate passwordless SSH and host alias.

## Phase 2: Task runner

- Execute task JSONs with local/remote steps.
- Persist events and conversation logs per task.

## Phase 3: Multi-agent workflow

- Standardize A->B handoff messages.
- Keep end states strict: done, failed, needs_approval.

## Phase 4: Guardrails

- Enforce policy deny list for destructive actions.
- Require explicit approval for blocked scopes.

## Phase 5: Service playbooks

- Add reusable playbooks for Docker service lifecycle.
- Add fetch/report patterns for logs and diagnostics.
