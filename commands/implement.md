---
description: "启动 Implement 全流程（6 阶段：需求分析 → spec → 设计 → 编码 → 测试 → 归档）"
argument-hint: "[需求描述]"
---

# Implement 全流程

用户要求执行一个新需求的完整开发流程。

## 需求描述

$ARGUMENTS

## 执行指令

按以下 6 个阶段顺序执行，每个阶段完成后请人确认再进入下一阶段：

1. **需求与分析**：使用 `requirement-analysis` Skill，产出 `requirement-analysis.md`
2. **规范定义**：使用 `spec` Skill，产出 `spec.md`（目标 + 接口 + 文件规划 + 测试策略 + 约束）
3. **方案设计**：使用 `design` Skill，先做代码搜证与澄清，再产出**批次化** `tasks.md`
4. **编码实现**：使用 `coding` Skill，按 `tasks.md` **逐批次执行**；每批结束后暂停，等人回复“继续”
5. **测试与验证**：使用 `testing` Skill，产出 `test-cases.md` + 验证结果
6. **归档与沉淀**：使用 `archiving` Skill，先产出 `.codebuddy/context/archiving.delta.md` 供确认，再更新 Rules / Memory / 模板

现在从第 1 阶段开始。
