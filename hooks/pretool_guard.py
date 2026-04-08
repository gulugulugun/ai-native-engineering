#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


DESTRUCTIVE_COMMAND_PATTERNS = [
    r"(^|\s)rm\s+-rf\s+/($|\s)",
    r"(^|\s)mkfs(\.|\s)",
    r":\(\)\{:\|:\&\};:",
    r"(^|\s)(shutdown|reboot|poweroff)(\s|$)",
    r"dd\s+if=.*\s+of=/dev/",
]

ASK_COMMAND_PATTERNS = [
    r"git\s+push\s+.*--force",
    r"git\s+reset\s+.*--hard",
    r"git\s+clean\s+.*-f",
    r"curl\b.*\|\s*(bash|sh)",
    r"wget\b.*\|\s*(bash|sh)",
]

PROCESS_ARTIFACT_NAMES = {
    "requirement-analysis.md",
    "spec.md",
    "design-notes.md",
    "tasks.md",
    "test-cases.md",
}

WRITE_TOOL_NAMES = {"Write", "Edit", "write_to_file", "replace_in_file"}
DELETE_TOOL_NAMES = {"Delete", "delete_file"}
COMMAND_TOOL_NAMES = {"Bash", "execute_command"}


def emit(decision: str, reason: Optional[str] = None) -> None:
    output = {
        "continue": decision != "deny",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        },
    }
    if reason:
        output["hookSpecificOutput"]["permissionDecisionReason"] = reason
        if decision == "deny":
            output["stopReason"] = reason
    json.dump(output, sys.stdout, ensure_ascii=False)


def resolve_path(raw_path: Optional[str], cwd: str, workspace_root: Path) -> Optional[Path]:
    if not raw_path:
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path(cwd) / path
    try:
        return path.resolve()
    except Exception:
        return workspace_root / raw_path


def main() -> None:
    raw = sys.stdin.read().strip() or "{}"
    payload = json.loads(raw)
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    cwd = str(payload.get("cwd") or os.environ.get("CODEBUDDY_PROJECT_DIR") or "/data/workspace")
    workspace_root = Path(os.environ.get("CODEBUDDY_PROJECT_DIR") or "/data/workspace").resolve()

    if tool_name in COMMAND_TOOL_NAMES:
        command = str(tool_input.get("command") or "")
        for pattern in DESTRUCTIVE_COMMAND_PATTERNS:
            if re.search(pattern, command):
                emit("deny", f"检测到高危命令，已阻止执行: {command}")
                return
        for pattern in ASK_COMMAND_PATTERNS:
            if re.search(pattern, command):
                emit("ask", f"检测到高风险命令，请人工确认后再执行: {command}")
                return
        emit("allow")
        return

    if tool_name in WRITE_TOOL_NAMES | DELETE_TOOL_NAMES:
        file_path = tool_input.get("filePath") or tool_input.get("target_file")
        resolved = resolve_path(file_path, cwd, workspace_root)
        if resolved is None:
            emit("allow")
            return

        resolved_str = str(resolved)
        git_dir = str((workspace_root / ".git").resolve())
        codebuddy_dir = str((workspace_root / ".codebuddy").resolve())

        if resolved_str == git_dir or resolved_str.startswith(git_dir + os.sep):
            emit("deny", f"禁止直接修改 Git 元数据目录: {resolved}")
            return

        if tool_name in DELETE_TOOL_NAMES and (
            resolved_str == codebuddy_dir or resolved_str.startswith(codebuddy_dir + os.sep)
        ):
            emit("deny", f"禁止删除 `.codebuddy` 目录下的文件: {resolved}")
            return

        if tool_name in DELETE_TOOL_NAMES and resolved.name in PROCESS_ARTIFACT_NAMES:
            emit("ask", f"目标是流程产物文件，请确认是否继续删除: {resolved}")
            return

        if not (resolved == workspace_root or resolved_str.startswith(str(workspace_root) + os.sep)):
            emit("ask", f"目标路径不在当前工作区内，请确认是否继续: {resolved}")
            return

        emit("allow")
        return

    emit("allow")


if __name__ == "__main__":
    main()
