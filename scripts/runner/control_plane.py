#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


def now_iso():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_event(events_path, event):
    with open(events_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=True) + "\n")


def append_conversation(conv_path, speaker, message):
    with open(conv_path, "a", encoding="utf-8") as f:
        f.write(f"- {now_iso()} {speaker}: {message}\n")


def blocked_by_policy(command, policy):
    if not policy.get("deny_delete_without_approval", True):
        return False, None
    for pattern in policy.get("blocked_patterns", []):
        if re.search(pattern, command):
            return True, pattern
    return False, None


def run_local(command):
    return subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
    )


def run_remote(ssh_target, command):
    remote = f"bash -lc {shlex.quote(command)}"
    return subprocess.run(
        ["ssh", ssh_target, remote],
        text=True,
        capture_output=True,
    )


def main():
    parser = argparse.ArgumentParser(description="OpenCode lightweight control plane")
    parser.add_argument("--task", required=True, help="Path to task json")
    parser.add_argument("--hosts", required=True, help="Path to hosts json")
    parser.add_argument("--policy", required=True, help="Path to policy json")
    parser.add_argument("--logs-dir", default="logs/tasks", help="Task logs root")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Artifacts root")
    args = parser.parse_args()

    task = load_json(args.task)
    hosts = load_json(args.hosts)
    policy = load_json(args.policy)

    task_id = task.get("task_id") or f"task-{dt.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    thread_id = task.get("thread_id", task_id)
    target_name = task["target"]
    ssh_target = hosts[target_name]["ssh_target"]

    run_dir = Path(args.logs_dir) / task_id
    art_dir = Path(args.artifacts_dir) / task_id
    run_dir.mkdir(parents=True, exist_ok=True)
    art_dir.mkdir(parents=True, exist_ok=True)

    events_path = run_dir / "events.jsonl"
    conv_path = run_dir / "conversation.md"
    approvals = task.get("approvals", [])

    append_conversation(conv_path, "agent-A", f"Start task {task_id} thread {thread_id}")
    write_event(events_path, {
        "ts": now_iso(),
        "task_id": task_id,
        "thread_id": thread_id,
        "status": "started",
        "target": target_name,
    })

    for idx, step in enumerate(task.get("steps", []), start=1):
        step_id = step.get("id", f"step-{idx}")
        step_type = step.get("type", "remote_cmd")
        command = step.get("command", "")

        if command:
            blocked, pattern = blocked_by_policy(command, policy)
            if blocked and step_id not in approvals:
                msg = f"Blocked by policy pattern '{pattern}' on step '{step_id}'"
                append_conversation(conv_path, "agent-A", msg)
                write_event(events_path, {
                    "ts": now_iso(),
                    "task_id": task_id,
                    "step_id": step_id,
                    "status": "needs_approval",
                    "command": command,
                    "pattern": pattern,
                })
                print(f"needs_approval: step={step_id} pattern={pattern}")
                return 2

        append_conversation(conv_path, "agent-A", f"Dispatch {step_id} to agent-B ({step_type})")

        if step_type == "remote_cmd":
            result = run_remote(ssh_target, command)
        elif step_type == "local_cmd":
            result = run_local(command)
        elif step_type == "remote_fetch":
            result = run_remote(ssh_target, command)
            artifact_name = step.get("artifact", f"{step_id}.txt")
            with open(art_dir / artifact_name, "w", encoding="utf-8") as f:
                f.write(result.stdout)
        else:
            result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr=f"unknown step type: {step_type}")

        write_event(events_path, {
            "ts": now_iso(),
            "task_id": task_id,
            "step_id": step_id,
            "step_type": step_type,
            "command": command,
            "returncode": result.returncode,
            "stdout_preview": (result.stdout or "")[:800],
            "stderr_preview": (result.stderr or "")[:800],
        })

        if result.returncode != 0:
            append_conversation(conv_path, "agent-B", f"Step {step_id} failed rc={result.returncode}")
            write_event(events_path, {
                "ts": now_iso(),
                "task_id": task_id,
                "status": "failed",
                "failed_step": step_id,
            })
            print(f"failed: step={step_id}")
            return 1

        append_conversation(conv_path, "agent-B", f"Step {step_id} ok")

    write_event(events_path, {
        "ts": now_iso(),
        "task_id": task_id,
        "status": "done",
    })
    append_conversation(conv_path, "agent-A", "Task done")
    print(f"done: task_id={task_id}")
    print(f"events={events_path}")
    print(f"conversation={conv_path}")
    print(f"artifacts={art_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
