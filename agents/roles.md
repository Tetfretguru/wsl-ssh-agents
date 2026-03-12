# Roles

## orquestador (Laptop A)

- Receives user intent and creates a task document.
- Validates policy before each action.
- Delegates remote steps to `destino` via SSH.
- Consolidates outputs and writes final status.

## destino (Laptop B)

- Executes approved remote commands.
- Returns command output and exit codes.
- Does not delete data unless approval is attached to task.

## busqueda (Laptop A)

- Focuses on discovery operations (files, status, logs, checks).
- Can run local checks before/after remote execution.

## Shared contract

- Every task has `task_id` and `thread_id`.
- Every step produces an auditable event.
- End states are exactly: `done`, `failed`, `needs_approval`.
