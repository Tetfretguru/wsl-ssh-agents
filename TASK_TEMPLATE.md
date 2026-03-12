# Task Template

Use this when creating a new task JSON.

```json
{
  "task_id": "task-YYYYMMDD-001",
  "thread_id": "thread-abc-001",
  "target": "laptop-b",
  "request": "Natural language user request",
  "approvals": [],
  "steps": [
    {
      "id": "step-name",
      "type": "remote_cmd",
      "command": "echo hello"
    }
  ]
}
```

Step types:

- `remote_cmd`: run command on target host via SSH.
- `remote_fetch`: run command and save stdout to artifact file.
- `local_cmd`: run command on local orchestrator host.
