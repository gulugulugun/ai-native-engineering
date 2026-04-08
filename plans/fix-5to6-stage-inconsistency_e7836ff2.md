---
name: fix-5to6-stage-inconsistency
overview: 统一修复"方案文档仍是 5 阶段、执行层已是 6 阶段"的前后矛盾，涉及 8 处核心矛盾 + 5 处连带问题，共 13 处修改点，跨 7 个文件。
todos:
  - id: scan-stale-refs
    content: 使用 [subagent:code-explorer] 搜索 .codebuddy/ 下所有"5 个阶段""5 阶段""contract-proposal""第 3 阶段""第 4 阶段""第 5 阶段"的残留引用，产出完整修复清单
    status: completed
  - id: fix-scheme-doc
    content: 修复方案文档 ai-native-engineering-scheme.md：4.1 改 6 阶段流程图和人机分工表、插入 4.3 spec 章节、编号顺推 4.4~4.8、编码阶段输入改引 spec.md、第 5 章加 Skills/Commands/PostToolUse Hook、第 6 章加 spec
    status: completed
    dependencies:
      - scan-stale-refs
  - id: fix-skills
    content: 修复 4 个 Skills：requirement-analysis 门禁指向改 spec、coding 阶段号和前置条件、testing 阶段号、archiving 阶段号
    status: completed
    dependencies:
      - scan-stale-refs
  - id: fix-memory-ctx-prov
    content: 修复 MEMORY.md（全流程标题+阶段表改 6 阶段）、current-task.md（5 改 6）、design-provenance.md（5 改 6）
    status: completed
    dependencies:
      - scan-stale-refs
  - id: verify-consistency
    content: 再次搜索所有旧引用，确认 13 处不一致全部消除，运行 lint 检查所有修改文件无格式错误
    status: completed
    dependencies:
      - fix-scheme-doc
      - fix-skills
      - fix-memory-ctx-prov
---

## 用户需求

全面修复方案体系中的前后矛盾和不一致，确保"设计层（方案文档）"和"执行层（Rule / Skills / Commands / MEMORY）"完全对齐到 6 阶段流程。

## 产品概述

此前在多轮迭代中引入了 spec 阶段（从 5 阶段升级到 6 阶段），但只更新了 Rule、Skills、Commands 和 MEMORY 的部分字段，方案文档（设计真相源）没有同步更新，导致 8 处核心矛盾 + 5 处连带问题。本次任务是一次性修复所有不一致。

## 核心修复内容

**8 处核心矛盾：**

1. 方案文档 4.1 节写"5 个阶段"，流程图缺 spec
2. 方案文档无 spec 章节（4.2~4.6 只有 5 个阶段章节）
3. coding Skill 写"第 3 阶段"，前置条件引用已废弃的 `contract-proposal.md`
4. testing Skill 写"第 4 阶段"
5. archiving Skill 写"第 5 阶段"
6. requirement-analysis Skill 门禁指向 design 而非 spec
7. MEMORY.md 全流程仍写"5 个阶段"
8. current-task.md 仍写"5 阶段"

**5 处连带问题：**
A. 方案文档第 5 章 Hooks 表只写 2 个，缺 post_lint_check
B. 方案文档第 5 章 delivery-workflow 描述缺"6 阶段 Skill 链"
C. 方案文档第 5 章完全没有 Skills 层和 Commands 层
D. 溯源表第 37 行写"5 阶段流程"
E. 方案文档第 6 章实施路线写"需求分析 - 设计 - 编码 - 测试 - 归档"缺 spec

## 技术栈

纯 Markdown 文档修改，无代码编译或运行时依赖。

## 实现方案

### 修复策略

采用"真相源优先"策略：先修复方案文档（设计真相源），再修复执行层文件（Skills / MEMORY / current-task / 溯源表），确保所有文件统一到 6 阶段流程。

### 关键技术决策

1. **章节编号顺推规则**：方案文档插入 spec 章节后，原 4.3 方案设计变为 4.4，原 4.4 编码变为 4.5，原 4.5 测试变为 4.6，原 4.6 归档变为 4.7，原 4.7 反馈闭环变为 4.8
2. **spec 章节内容来源**：直接从已落地的 `skills/spec/SKILL.md` 提取并扩写，补场景示例和设计理由（参考 agent-skills、Superpower、gstack 三方对照），保持与其他章节一致的"问题 - 人机分工 - 输入约束交付物 - 场景示例 - 设计理由"结构
3. **废弃 contract-proposal.md 引用**：coding Skill 和方案文档编码阶段中对 `contract-proposal.md` 的引用改为 `spec.md`，因为接口定义已收入 spec 的第 2 章节
4. **第 5 章扩展**：新增 E（Skills 层）和 F（Commands 层）两个子节，并更新 Hooks 表加入 `post_lint_check`

### 实现注意事项

- 方案文档是最大的改动目标（约 15 处修改 + 1 个新章节插入），需要精确的行定位
- 修改完每个文件后立即检查 lint，确保 Markdown 格式无误
- 所有修改必须与已落地的 `delivery-workflow.mdc` Rule 中的 6 阶段表保持一致

## 目录结构

```
.codebuddy/
├── plans/
│   └── ai-native-engineering-scheme.md  # [MODIFY] 方案文档：4.1 流程图改 6 阶段、新增 4.3 spec 章节、编号顺推、第 5 章加 Skills/Commands/PostToolUse、第 6 章加 spec
├── skills/
│   ├── requirement-analysis/SKILL.md    # [MODIFY] 门禁指向从 design 改为 spec
│   ├── coding/SKILL.md                  # [MODIFY] 阶段号从 3 改为 4、前置条件从 contract-proposal.md 改为 spec.md + tasks.md
│   ├── testing/SKILL.md                 # [MODIFY] 阶段号从 4 改为 5、description 从第 4 阶段改为第 5 阶段
│   └── archiving/SKILL.md              # [MODIFY] 阶段号从 5 改为 6、description 从第 5 阶段改为第 6 阶段
├── context/
│   └── current-task.md                  # [MODIFY] "5 阶段"改为"6 阶段"
├── docs/
│   └── design-provenance.md             # [MODIFY] 第 37 行"5 阶段流程"改为"6 阶段流程"
└── MEMORY.md                            # [MODIFY] 全流程标题和阶段表改为 6 阶段
```

## Agent Extensions

### SubAgent

- **code-explorer**
- 用途：在修改方案文档前，搜索所有文件中残留的"5 个阶段""5 阶段""contract-proposal"等旧引用，确保修复无遗漏
- 预期结果：产出完整的旧引用清单，覆盖所有 `.codebuddy/` 下的文件