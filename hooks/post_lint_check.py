#!/usr/bin/env python3
"""PostToolUse hook: auto-lint after file modifications."""
import json
import os
import sys
from pathlib import Path

# 需要自动 lint 的文件扩展名
LINTABLE_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".vue", ".json"}


def main() -> None:
    raw = sys.stdin.read().strip() or "{}"
    payload = json.loads(raw)
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}

    # 只在文件写入/编辑工具之后触发
    write_tools = {"Write", "Edit", "write_to_file", "replace_in_file"}
    if tool_name not in write_tools:
        json.dump({"continue": True}, sys.stdout)
        return

    # 获取被修改的文件路径
    file_path = tool_input.get("filePath") or tool_input.get("target_file") or ""
    if not file_path:
        json.dump({"continue": True}, sys.stdout)
        return

    ext = Path(file_path).suffix.lower()
    if ext not in LINTABLE_EXTENSIONS:
        json.dump({"continue": True}, sys.stdout)
        return

    # 提醒 AI 检查 lint
    output = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"文件 `{file_path}` 已修改。请检查该文件的 lint 结果，确认无新增错误。",
        },
    }
    json.dump(output, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
