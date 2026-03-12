# WSL SSH Agents

Practical repo to operate WSL-to-WSL remote work over SSH with OpenCode as orchestrator.

## What this repo gives you

- Role-based operation: `orquestador` (Laptop A), `destino` (Laptop B), `busqueda` (Laptop A).
- Real tasks over SSH: search files, start Docker services, collect outputs.
- Full traceability: JSONL events + agent conversation log per task.
- Safety guardrails: destructive commands are blocked unless explicit user approval is present.

## Quickstart

1) On Laptop B (destination WSL), bootstrap SSH server:

```bash
bash scripts/ssh/bootstrap_destino.sh
```

2) On Laptop A (search/orchestrator WSL), setup client key and host alias:

```bash
bash scripts/ssh/bootstrap_busqueda.sh laptop-b user@192.168.1.50
```

3) Copy examples and adapt your host inventory:

```bash
cp inventory/hosts.example.json inventory/hosts.json
cp policy/policy.example.json policy/policy.json
```

4) Run a sample task:

```bash
python3 scripts/runner/control_plane.py \
  --task examples/tasks/find_file.json \
  --hosts inventory/hosts.json \
  --policy policy/policy.json
```

5) Inspect outputs:

- `logs/tasks/<task_id>/events.jsonl`
- `logs/tasks/<task_id>/conversation.md`
- `artifacts/<task_id>/...`

## Core rule

No delete without explicit user approval. See `POLICY.md`.
