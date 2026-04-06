#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


def detect_project(cwd: str) -> tuple[str, list[str]]:
    rules = [
        "优先遵守项目 Rules，再结合当前任务上下文做分析和实现。",
        "如本轮任务跨前后端，优先检查契约与接口一致性。",
    ]

    if "/queryopenorderlist/" in cwd:
        return (
            "当前位于 `queryopenorderlist`（XPage 前端模板）",
            rules
            + [
                "`src/index.ts` 是路由唯一真相源。",
                "平台内路由跳转优先使用 `window.wxpay.router`，不要直接依赖 `vue-router`。",
                "API 调用优先使用契约生成客户端，非契约场景再用 `window.wxpay.request`。",
            ],
        )
    if "/xdc_wxpay/" in cwd:
        return (
            "当前位于 `xdc_wxpay`（XDC Node 后端模板）",
            rules
            + [
                "接口变更优先修改契约，再生成或对齐代码。",
                "`controller/` 以契约生成结构为准，业务逻辑优先放 `entity/`。",
                "业务异常优先使用 `BizError` 和标准错误码语义。",
            ],
        )
    if "/payclient-oa-depositmisview/" in cwd:
        return (
            "当前位于 `payclient-oa-depositmisview`（旧前端）",
            rules
            + [
                "该项目主要作为迁移参考，不要把旧实现机械复制到 XPage 新模板。",
            ],
        )
    if "/lqp/" in cwd:
        return (
            "当前位于 `lqp`（旧后端集合）",
            rules
            + [
                "该项目主要作为迁移参考，不要直接照搬 Egg / Service 分层到 XDC 新模板。",
            ],
        )
    return (
        "当前位于工作区通用目录",
        rules + ["先识别目标项目，再应用对应规则与模板。"],
    )


def main() -> None:
    raw = sys.stdin.read().strip() or "{}"
    payload = json.loads(raw)
    cwd = str(payload.get("cwd") or os.environ.get("CODEBUDDY_PROJECT_DIR") or "/data/workspace")
    workspace_root = Path(os.environ.get("CODEBUDDY_PROJECT_DIR") or "/data/workspace")
    current_task = workspace_root / ".codebuddy" / "context" / "current-task.md"

    project_title, hints = detect_project(cwd)
    if current_task.exists():
        hints.append(f"如任务有临时约束或交接信息，优先读取 `{current_task}`。")

    additional_context = project_title + "。\n- " + "\n- ".join(hints)
    output = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        },
    }
    json.dump(output, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
