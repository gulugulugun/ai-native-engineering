---
description: "快速修复模式（跳过需求分析和设计，直接编码 → 验证 → 归档）"
argument-hint: "[问题描述]"
---

# Fast-fix 快速修复

用户要求快速修复一个 bug 或做一个小改动。

## 问题描述

$ARGUMENTS

## 执行指令

1. 直接定位问题并编码修复。
2. 运行 lint 和相关验证，附带命令输出证据。
3. 如果发现新的坑点或规则，按四分类归档：
   - **Pattern**：可复用的修复模式
   - **Pitfall**：踩过的坑
   - **Preference**：命名约定
   - **Architecture**：架构决策

现在开始修复。
