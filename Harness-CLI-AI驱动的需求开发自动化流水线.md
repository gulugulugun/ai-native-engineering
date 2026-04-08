---
title: Harness CLI — AI 驱动的需求开发自动化流水线
author: zipsu
source: https://km.woa.com/articles/show/656720
date: 2026-04-03
tags:
  - 自动化
  - CLI
  - Harness
fetched: 2026-04-08
---

# Harness CLI — AI 驱动的需求开发自动化流水线

> 导语：针对当前 AI 辅助开发中缺乏流程固化、无法向前回溯的问题，开发了一款 CLI 工具。通过多状态机驱动 + 执行结果校验机制，将对话式编码升级为可控、可追溯、可回溯的开发流水线，提升开发过程的规范性和可靠性。

推荐先阅读实践，对这个工具有个大致了解：[CLI实践](https://doc.weixin.qq.com/doc/w3_AcIAdQaWACYCN2WsVcledSCukPPjR?scode=AJEAIQdfAAoce2h2ePAcIAdQaWACY&isEnterEdit=1&qt_source=Other&qt_report_identifier=1774593452873)

## 目录

1. 项目背景与动机
2. 核心理念与理论基础
3. 系统架构总览
4. 数据流与运行时架构
5. 状态机引擎详解
6. 九大状态深度解读
7. 三大核心机制
8. 门禁（Gate）质量体系
9. Prompt 工程设计
10. 可观测性：轨迹追踪系统
11. 使用方式
12. 未来改进方向

## 1. 项目背景与动机

### 1.1 问题现状

自己在日常需求开发中，存在以下痛点：

| 痛点 | 描述 | 影响 |
| --- | --- | --- |
| 🔴 需求理解偏差 | AI 编码助手直接开始编码，缺少需求澄清环节 | 返工率高，产出不符合预期 |
| 🔴 质量无保障 | AI 生成的代码缺少系统性审查 | 缺陷遗漏到后期才被发现 |
| 🟡 流程不可控 | AI 的执行过程是黑盒，难以干预和回溯 | 问题定位困难，不知道问题出现在哪一次描述中 |
| 🟡 上下文丢失 | 长对话中 AI 容易"遗忘"前期决策 | 产出与计划不一致 |
| 🟡 人工介入多 | 每个阶段需要人工盯守和手动推进 | 效率低，无法规模化 |

### 1.2 关联分析

![](images/harness-cli/Pasted%20image%2020260408111539.png)
图 1-1：痛点关联分析图

会陷入到需求描述->AI开发代码->需求描述这样一种死循环中。

### 1.3 设计目标

将非结构化的需求开发过程，转化为可控、可追溯、可回溯的自动化流水线。

知道当前在执行什么、之前我执行了什么、当前有问题能够带着问题回溯到之前操作重新执行
![](images/harness-cli/Pasted%20image%2020260408111546.png)

图 1-2：设计原则思维导图

### 1.4 从"对话式编码"到"工程化交付"

![](images/harness-cli/Pasted%20image%2020260408111553.png)
图 1-3：传统模式 vs Harness CLI 模式

## 2. 核心理念与理论基础

### 2.1 Agent Harness 理论

Harness CLI 基于 Agent Harness 理论（如下展示了几篇说明博客）

- [工程技术：在智能体优先的世界中利用 Codex | OpenAI](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
- [Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

![](images/harness-cli/Pasted%20image%2020260408111603.png)

图 2-1：计算机 → Agent 类比映射

简单来说，harness的作用就是调度和组织相关任务在大模型上执行

### 2.2 Agent Harness的支柱
![](images/harness-cli/Pasted%20image%2020260408111614.png)
图 2-2：Agent Harness 五大支柱

| Harness 支柱 | 理论定义 | 当前实现 | 实现文件 |
| --- | --- | --- | --- |
| Plan | 任务分解与里程碑 | 9 状态状态机 + 里程碑分解 | state_machine.sh |
| Tools | 原子化工具集 | CodeBuddy CLI 统一执行 | utils.sh → invoke_codebuddy() |
| Context | 上下文管理 | Prompt 模板 + 文件注入 + 变量渲染 | utils.sh → render_prompt() |
| Verify | 验证机制 | JSON 规则 + AI 检查 + 人工确认 | gate_checker.sh + 9份 JSON |
| Trace | 轨迹捕获 | JSONL 日志 | trace_logger.sh |

## 3. 系统架构总览

### 3.1 四层架构图
![](images/harness-cli/Pasted%20image%2020260408111623.png)

图 3-1：Harness CLI 四层架构图

用户交互层命令说明：

四层架构最上面一层是"用户交互层"，它负责接收用户在命令行里的操作，并把这些操作转成对状态机、任务目录和质量模块的调用。对用户来说，这一层就是 Harness CLI 的全部入口；对系统来说，这一层负责把"我要做什么"翻译成"系统下一步该执行什么"。

下面列举部分命令：

- **init**：初始化一个新任务。作用是为需求创建独立的任务目录、初始 state.json 和 trace.jsonl，并把任务名称、来源链接、设计稿、代码库路径等基础上下文写入系统。可以把它理解为"立项建档"。
- **run**：自动推进完整流水线。从当前状态开始连续执行后续阶段，并在每一步后做 Gate 检查；如果通过就继续，失败就停止或按规则回流。它适合在任务信息已经比较完整时一键跑通全流程。
- **step**：只执行单个指定状态。适合你想精细控制流程时使用，例如先只跑 INTAKE 看需求摘要是否合理，再决定是否进入 DISCOVER。它本质上是"手动挡模式"。
- **resume**：从中断位置恢复执行。它会读取任务目录中的 state.json，找到上一次停止的状态并继续往下走，适合处理中途中断、网络异常或人工暂停后的续跑场景。
- **status**：查看当前任务处于哪个状态，以及已经完成了哪些阶段。它解决的是"现在跑到哪了、下一步该做什么"的可见性问题。
- **rollback**：把任务回退到指定状态重新处理。它用于发现前面某一步做错了、方案需要重来、或者验证阶段要求回到更早层级时的人工干预，是系统可回溯能力的重要入口。
- **rollback --step**：执行步骤级回溯。除了修改当前状态外，还会清理该状态之后生成的产物文件，让任务回到一个更干净、更符合历史现场的节点，适合做深度返工。
- **rollback --list-steps**：查看完整步骤执行历史。它帮助用户在回溯前先看清楚系统按什么顺序执行过哪些步骤、在哪些节点发生过回流或中断。
- **trace**：查看执行轨迹。它面向过程审计与问题排查，能帮助你理解每个状态何时进入、是否通过 Gate、在哪里回流，以及整个任务链路的运行情况。

从职责上看，用户交互层中的这些命令大致可以分成四类：

- **创建入口**：init
- **执行入口**：run、step、resume
- **观察入口**：status、trace、list
- **回溯入口**：rollback、rollback --step、rollback --list-steps

### 3.2 模块依赖关系
![](images/harness-cli/Pasted%20image%2020260408111634.png)

图 3-2：模块间调用与数据依赖关系

### 3.3 文件与模块规模

| 模块 | 文件 | 职责 |
| --- | --- | --- |
| 用户层 | harness.sh | 命令解析、参数校验、路由分发 |
| 状态机引擎层 | state_machine.sh | 状态定义、转换、执行、回流 |
| 质量检查层 | gate_checker.sh | 规则加载、多层检查 |
| 基础设施层 | trace_logger.sh | 轨迹记录、摘要展示 |
| 基础设施层 | utils.sh | 状态 IO、Prompt 渲染、CLI 调用 |
| 基础设施层 | prompts/*.md | 10 份 Prompt 模板 |
| 基础设施层 | gates/*.json | 9 份 Gate 规则 |
| 外部依赖 | - | CodeBuddy CLI |

## 4. 数据流与运行时架构

### 4.1 完整数据流

![](images/harness-cli/Pasted%20image%2020260408111641.png)
图 4-1：数据流

### 4.2 state.json 结构详解

```json
{
  "task_id": "story-001",
  "task_name": "XXX",
  "current_status": "BUILD_LOOP",
  "current_milestone": "M2-API接口",
  "source_url": "https://tapd...",
  "design_url": "",
  "codebase_path": "./src",
  "model": "",
  "p0_case_url": "https://case.wwtest.woa.com/...",
  "test_contract_version": "v1.0",
  "last_gate_result": "PASS",
  "blocked": false,
  "blocking_reason": "",
  "rollback_target": "",
  "clarification_readiness": "HIGH",
  "step_history": [
    {"state": "INTAKE", "status": "completed", "timestamp": "..."},
    {"state": "DISCOVER", "status": "completed", "timestamp": "..."}
  ],
  "created_at": "2026-03-23T14:16:49Z",
  "updated_at": "2026-03-24T09:30:00Z"
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| task_id | string | 任务唯一标识 |
| task_name | string | 需求名称 |
| current_status | string | 当前所处状态（9 种之一） |
| current_milestone | string | BUILD_LOOP 阶段的当前里程碑 |
| source_url | string | 需求来源链接 |
| design_url | string | 设计稿链接 |
| codebase_path | string | 目标代码库路径 |
| p0_case_url | string | P0 用例链接（case.wwtest.woa.com），可选 |
| blocked | boolean | 是否被阻塞 |
| blocking_reason | string | 阻塞原因 |
| rollback_target | string | 回流目标状态 |
| clarification_readiness | string | 需求澄清就绪度 (HIGH/MEDIUM/LOW) |
| step_history | array | 步骤执行历史（支持步骤级回溯） |

### 4.3 阶段产出
![](images/harness-cli/Pasted%20image%2020260408111716.png)

图 5-2：目标状态和对应产物

## 5. 状态机引擎详解

### 5.1 状态全景流程图

| # | 状态 | Worker 角色 | 核心产出 | Gate检查项数 | 回流目标 |
| --- | --- | --- | --- | --- | --- |
| 1 | INTAKE | orchestrator | brief.md, source-index.md, clarification-log.md | 7 项 | — |
| 2 | DISCOVER | discovery-worker | requirements.md, open-questions.md, risk-list.md | 4 项 | → INTAKE |
| 3 | SPEC_LOCK | spec-worker | product-plan.md, technical-plan.md, decision-log.md | 一致性检查 | — |
| 4 | TEST_CONTRACT | test-worker | test-case.md, acceptance-checklist.md, quality-gates.md, p0_cases_report.md | P0覆盖检查 | — |
| 5 | PLAN_LOCK | planning-worker | milestones.md, commit-strategy.md | DoD检查 | — |
| 6 | BUILD_LOOP | execution-worker + reviewer | 代码文件, execution-process.md, milestone-review.md | 5 项 | → PLAN_LOCK |
| 7 | VERIFY_GATE | verification-worker | verification-report.md, gap-list.md | 4 项 | 多目标 |
| 8 | FIX_LOOP | repair-worker | bug-fix-log.md, root-cause.md | 修复检查 | — |
| 9 | DONE | orchestrator | final-summary.md | 一致性检查 | — |

状态说明：

- **INTAKE**：这是任务的录入与建档阶段，重点是把需求背景、目标用户、来源链接、设计稿和代码仓路径等基础信息补齐，并通过澄清追问把模糊描述变成可执行任务。这个阶段的目标不是马上产出方案，而是先确保"要做什么"已经说清楚。
- **DISCOVER**：这是需求细化阶段，主要挖出边界条件、异常流程、潜在风险和仍待确认的问题。它相当于在正式设计之前先做一次业务排雷，避免后面写方案和写代码时基于错误假设往前走。
- **SPEC_LOCK**：这是规格锁定阶段，要求产品方案和技术方案形成闭环，并把关键决策记录到 decision-log.md。对于一个技术方案来说这个阶段来说能够确定方案选型。
- **TEST_CONTRACT**：TDD（测试驱动开发）这是测试先行阶段，核心逻辑是通过测试用例驱动代码实现，确保软件功能的正确性与可维护性，用例、验收清单和质量门槛要先于编码被定义出来。支持两种模式：模式 A 由 AI 从文档中自动生成测试用例；模式 B 从 P0 用例管理平台（case.wwtest.woa.com）的链接中通过浏览器自动化提取已有的 P0 测试用例。它的意义在于把"做成什么样算完成"前置，避免 BUILD 阶段因为验收标准模糊而反复返工。
- **PLAN_LOCK**：这是实施计划锁定阶段，重点把方案拆成可执行的里程碑，明确每一步的完成定义（DoD）以及建议的提交策略。它回答的是"先做什么、后做什么、每步做到什么程度算过关"。
- **BUILD_LOOP**：这是按里程碑推进实现的主执行阶段，开发 Worker 负责落代码，Reviewer 负责即时审查。它不是一次性写完再统一验收，而是每完成一个阶段性成果就做一次小闭环，尽量把问题消灭在局部。
- **VERIFY_GATE**：这是全局验证阶段，会站在规格、测试与交付目标的角度判断当前阶段实现是否真正达标。这里不仅会给出是否通过，还会根据问题性质决定是回到修复、重规划，还是回到更早的需求/方案层重新处理。
- **FIX_LOOP**：这是针对验证问题的修复阶段，要求不仅修 bug，还要记录根因和修复动作，避免同类问题重复出现。这个阶段强调的是"修复 + 复盘"。
- **DONE**：这是任务收尾与归档阶段，沉淀最终总结、交付结果和过程结论。走到这里意味着需求已经形成完整闭环，后续无论是复盘、审计还是二次迭代，都有清晰依据可追溯。

![](images/harness-cli/Pasted%20image%2020260408111730.png)
图 5-1：状态流转图

### 5.2 完整决策树

![](images/harness-cli/Pasted%20image%2020260408111752.png)
图 5-2：完整决策树（含所有分支路径）

## 6. 状态深度解读

### 6.1 INTAKE — 需求理解阶段

角色：需求工程师 | Prompt：intake.md
![](images/harness-cli/Pasted%20image%2020260408111807.png)
图 6-1：INTAKE 阶段

Prompt 核心三步：

1. **阅读提炼**：从输入源提炼需求目标、核心功能、涉及模块
2. **多维度自检**：对每个维度标注 ✅(充分) / ⚠️(部分缺失) / ❌(严重缺失)
3. **生成文档**：brief.md + source-index.md + clarification-log.md

- **brief.md**：这次需求是什么，需求摘要
- **source-index.md**：这些信息从哪来，信息来源清单（需求链接、设计稿、代码库路径、历史需求）
- **clarification-log.md**：还有哪些地方没说清 / 会卡住后续

Gate 检查（intake_gate.json）：

- 需求目标是否已明确
- 主要用户对象是否已指明
- 目标系统/模块范围是否已确定
- 设计稿或其他端（android/mac/win）参考实现有无标注
- clarification-log.md 包含完整 6 项维度检查
- 待澄清问题已标注影响范围

### 6.2 DISCOVER — 需求发现阶段

角色：产品分析师 | Prompt：discover.md (43行)

![](images/harness-cli/Pasted%20image%2020260408111816.png)
图 6-2：Discovery 阶段

Prompt 核心四步：

1. **功能目标列表**：从 brief.md 的需求摘要出发，明确列出所有功能目标及其验证标准
2. **场景深挖**：拆解核心路径（正常流程）、异常路径（各种失败/边界情况）
3. **风险评估**：识别技术风险、业务风险、依赖风险，标注等级和缓解方案
4. **问题记录**：记录尚未确认的待澄清问题，标注是否阻塞后续阶段

- **requirements.md**：需求要做什么——完整的功能目标列表、用户场景（核心路径 + 异常路径 + 边界条件）、涉及入口清单、对齐参考实现、假设项。它是后续 SPEC_LOCK 设计方案的输入基础。
- **open-questions.md**：还有哪些没确认的问题——每个问题标注优先级、影响范围、是否阻塞，并附带当前假设。阻塞性问题必须在进入技术设计（SPEC_LOCK）前确认清楚。
- **risk-list.md**：可能踩什么坑——按技术风险、业务风险、依赖风险分类，每项标注等级（🔴高/🟡中/🟢低）和缓解方案。它帮助后续阶段提前做好防护，避免在 BUILD_LOOP 阶段才暴露问题。

Gate 检查（discover_gate.json）：

- 核心功能路径是否完整覆盖
- 异常场景是否已列出
- 阻塞性问题是否已标注
- 需求是否可验证（有明确的验证标准）

交互式问题解答（answer 命令）：

DISCOVER 阶段完成后，如果 open-questions.md 中存在阻塞性问题（标记为 是否阻塞: 是），CLI 会自动检测并暂停流程，提示用户处理：

```
⚠️  发现 3 个阻塞性问题，需要先解答才能进入技术设计

下一步操作：
  方式一：bash harness.sh answer --task-id <ID>    # AI 自动搜索代码库解答
  方式二：vim open-questions.md                     # 手动编辑
  方式三：bash harness.sh step --task-id <ID> --state SPEC_LOCK  # 带假设跳过
```

answer 命令（参考了 gpt-engineer 的 clarify 循环 + aider 的 /ask 模式设计）：

- AI 会逐个分析阻塞性问题，在代码库中搜索相关函数/接口定义
- 找到证据后自动更新 open-questions.md，将阻塞状态改为「已确认」
- 找不到答案的问题保持阻塞状态，提示需要人工确认

### 6.3 SPEC_LOCK — 规格锁定阶段

角色：系统架构师 | Prompt：spec_lock.md

产出三件套：

- **product-plan.md**：功能清单 + 交互规则 + 数据模型 + UI 规格 + 非功能性需求
- **technical-plan.md**：模块划分 + 接口设计 + 数据结构 + 异常处理 + 日志规范
- **decision-log.md**：关键技术决策 + 选择理由 + 替代方案 + 风险

自检环节：生成完毕后以审查者角色自检产品规格与技术方案一致性

### 6.4 TEST_CONTRACT — 测试契约阶段

角色：QA 工程师 | Prompt：test_contract.md / test_contract_p0_extract.md

核心理念：TDD 思想，测试驱动开发，通过测试用例完善需求理解
![](images/harness-cli/Pasted%20image%2020260408111830.png)
图 6-4-1：用例优先级

双模式支持：TEST_CONTRACT 阶段支持两种测试用例来源，用户可在执行时交互选择：
![](images/harness-cli/Pasted%20image%2020260408111840.png)
图 6-4-1：双执行模式

三种指定 P0 链接的方式：

```bash
# 方式1: 初始化时指定
bash harness.sh init --task-id xxx --name "功能名" --p0-url "https://case.wwtest.woa.com/..."

# 方式2: step 命令临时传入
bash harness.sh step --task-id xxx --state TEST_CONTRACT --p0-url "https://case.wwtest.woa.com/..."

# 方式3: 执行时交互选择模式 B，手动输入链接
bash harness.sh step --task-id xxx --state TEST_CONTRACT
# → 选择 2) 从 P0 用例链接提取（模式 B）
# → 输入链接
```

### 6.5 PLAN_LOCK — 计划锁定阶段

角色：项目经理 | Prompt：plan_lock.md
![](images/harness-cli/Pasted%20image%2020260408111849.png)
图 6-5：PLAN_LOCK 阶段

每个里程碑包含：目标功能范围 / 依赖输入 / 变更模块 / 风险说明 / DoD / 验证方法 / 提交粒度 / 回退策略

#### 产出文档说明

PLAN_LOCK 阶段会在 tasks/<task-id>/ 目录下生成以下两个文档：

##### 1. milestones.md — 里程碑执行计划（必需）

这是 PLAN_LOCK 阶段的核心产出，也是 Gate 门禁的必需文件。该文档将需求拆分为 3-5 个可独立执行和验证的里程碑，按依赖关系排序。

文档结构：

```markdown
## M1: [里程碑名称]

**目标功能范围**: 具体要实现什么功能
**依赖输入**: 需要先完成哪个里程碑（M1 无依赖则标明"无"）
**变更模块**: 需要改动的文件清单
**风险说明**: 该里程碑可能遇到的技术风险
**完成定义 (DoD)**:
- [ ] 具体的完成条件 1
- [ ] 具体的完成条件 2
- [ ] ...
**验证方法**: 如何检验里程碑是否完成
**提交粒度**: 建议拆成几个 commit
**回退策略**: 实施失败时的回滚方案

## M2: [里程碑名称]
... (同上结构)
```

拆分原则：

- 每个里程碑控制在 1-5 个文件的改动范围（功能粒度）
- P0 功能必须分配到明确的里程碑（当之前有输入了 P0 用例）
- 里程碑之间的依赖关系必须清晰
- 每个里程碑完成后应能独立验证
- 排序遵循：基础模块（会话气泡） → 核心业务逻辑 → 边界处理

输入依赖：参考以下前序阶段产出：

- product-plan.md（产品规格，来自 SPEC_LOCK）
- technical-plan.md（技术方案，来自 SPEC_LOCK）
- test-case.md（测试用例，来自 TEST_CONTRACT，可选）
- acceptance-checklist.md（验收清单，来自 TEST_CONTRACT，可选）

##### 2. commit-strategy.md — 提交策略

该文档为每个里程碑定义推荐的 Git 提交策略，确保 BUILD_LOOP 阶段代码提交规范、可追溯。

文档内容包括：

- commit message 格式：约定统一的提交信息格式（如 feat(module): 描述）
- 每个 commit 承载的内容范围：明确每次提交应包含哪些改动，避免大杂烩提交
- 代码审查重点：标注每个里程碑中需要重点 Review 的关键改动点

示例：

```markdown
## M1: 基础设施搭建

### 提交策略
| # | Commit Message | 内容范围 | Review 重点 |
|---|---------------|---------|------------|
| 1 | feat(model): 新增用户权限数据模型 | schema 定义 + migration | 字段设计合理性 |
| 2 | feat(api): 添加权限管理 API 骨架 | 路由 + Controller 框架 | 接口设计是否符合 RESTful |
```

#### Gate 检查项

PLAN_LOCK Gate（gates/plan_lock_gate.json）执行以下检查：

| 检查项 | 说明 |
| --- | --- |
| 文件存在性 | milestones.md 必须存在 |
| P0 功能覆盖 | P0 功能是否已分配到明确的里程碑（可选） |
| 里程碑粒度 | 单个里程碑改动范围是否控制在 1-3 个文件 |
| 可独立验证 | 每个里程碑完成后是否可以独立验证 |
| 依赖关系清晰 | 里程碑之间的依赖关系是否明确无环 |

Gate 失败处理：VERIFY_GATE 阶段判定 REPLAN_REQUIRED 时也会回流到 PLAN_LOCK，要求重新调整里程碑计划。

### 6.6 BUILD_LOOP — 构建循环阶段

最复杂的阶段，包含逐里程碑执行 + 即时审查子循环（详见 7.2 节）

### 6.7 VERIFY_GATE — 质量门禁阶段

角色：Verification Worker | 五种判定：
![](images/harness-cli/Pasted%20image%2020260408112443.png)
图 6-7：VERIFY_GATE 阶段

这是全局验证阶段，会站在规格、测试与交付目标的角度判断当前实现是否真正达标。这里不仅会给出是否通过，还会根据问题性质决定是回到修复、重规划，还是回到更早阶段重新处理。

### 6.8 FIX_LOOP — 修复循环

角色：修复工程师 | Prompt：fix_loop.md

核心原则：不要一看到 bug 就直接改代码。先判断问题出在哪一层，再决定改哪里。
![](images/harness-cli/Pasted%20image%2020260408112837.png)
图 6-8：FIX_LOOP 阶段

核心四步：

#### 第 1 步：根因分类

对 gap-list.md 中的每个问题进行根因分类，判定问题属于哪一层级：

| 根因分类 | 说明 | 处理方式 | 示例 |
| --- | --- | --- | --- |
| 🐛 Implementation Issue（实现问题） | 代码有 bug、逻辑错误、功能遗漏 | 直接修复代码 | 空指针异常、条件判断遗漏、接口参数错误 |
| 📋 Planning Issue（计划问题） | 里程碑拆分不合理、DoD 不清晰 | 回流 → PLAN_LOCK | 里程碑依赖关系错误、DoD 无法验证 |
| 📐 Specification Issue（规格问题） | 规格模糊、矛盾、缺失 | 回流 → SPEC_LOCK | 接口定义与产品规格不一致、缺少异常处理规格 |
| 🔎 Discovery Issue（需求问题） | 需求理解错误、场景遗漏 | 回流 → DISCOVER | 完全没有覆盖某个用户场景、业务规则理解有误 |

关键判断逻辑：如果一个问题既像实现问题又像规格问题，优先归类到更上层（规格 > 实现），因为上层修复能从根本上解决问题，避免反复修补。

#### 第 2 步：修复 Implementation Issues

对所有分类为 Implementation Issue 的问题，逐一执行：

1. 定位问题代码 — 找到引发问题的具体文件和函数
2. 实施修复 — 修改代码，修复 bug 或补全遗漏逻辑
3. 验证修复有效 — 确认修复后功能正常，且不引入新问题

#### 第 3 步：记录修复过程

产出两份文档：

**bug-fix-log.md** — 修复记录

```markdown
## 修复记录

### Issue 1: [问题描述]
- **根因分类**: Implementation Issue
- **问题定位**: [具体代码位置，如 src/api/handler.ts:42]
- **修复方法**: [具体改了什么，怎么改的]
- **验证**: [如何确认修复有效，跑了什么测试]

### Issue 2: [问题描述]
...
```

**root-cause.md** — 根因分析总结

```markdown
## 根因分析总结

| # | 问题 | 根因分类 | 需要回流? | 回流目标 |
|---|------|----------|-----------|---------|
| 1 | API 返回格式错误 | Implementation | 否 | - |
| 2 | 缺少批量操作接口 | Specification | 是 | SPEC_LOCK |
| 3 | 并发场景未考虑 | Discovery | 是 | DISCOVER |

## 回流建议
- **SPEC_LOCK**: 需补充批量操作接口的规格定义
- **DISCOVER**: 需重新审视并发使用场景的需求边界
```

#### 第 4 步：标明回流路径

如果存在非 Implementation Issue 的问题，Repair Worker 需要在 root-cause.md 中明确指出：

- 需要回流到哪个阶段
- 为什么需要回流（不是代码层面能修的）
- 回流后需要重点关注什么

状态机会根据 root-cause.md 中的回流建议，在 Gate 通过后自动触发回流。

#### Gate 检查

Gate 规则（gates/fix_loop_gate.json）：

```json
{
  "state": "FIX_LOOP",
  "required_files": ["bug-fix-log.md", "root-cause.md"],
  "checks": [
    "所有 Implementation Issue 是否已修复",
    "需要回流的问题是否已标明回流目标",
    "修复是否未引入新问题"
  ],
  "rollback_target": "VERIFY_GATE",
  "on_fail": "继续修复"
}
```

| 检查项 | 说明 |
| --- | --- |
| 文件存在性 | bug-fix-log.md 和 root-cause.md 必须存在 |
| 修复完整性 | 所有 Implementation Issue 是否已逐一修复 |
| 回流标注 | 非 Implementation Issue 是否已标明回流目标和原因 |
| 无副作用 | 修复是否未引入新问题 |

Gate 通过后：回到 VERIFY_GATE 重新进行全局验证，确认修复后的代码满足规格和测试要求。Gate 失败处理：继续在 FIX_LOOP 内修复，直到所有 Implementation Issue 处理完毕。

### 6.9 DONE — 归档阶段

产出 final-summary.md：需求概述 + 功能列表 + 里程碑状态 + 设计决策 + 测试结果 + 遗留问题 + 执行轨迹统计

## 7. 三大核心机制

### 7.1 需求细化
![](images/harness-cli/Pasted%20image%2020260408112903.png)
图 7-1：需求追问

### 7.2 即时代码审查
![](images/harness-cli/Pasted%20image%2020260408112926.png)
图 7-2：代码审查

多维度审查：

1. **功能完整性** — 所有功能点实现、边界条件处理、DoD 满足
2. **代码质量** — 编译运行、逻辑 bug、错误处理（大字体、暗黑模式等）、命名结构
3. **规格一致性** — 符合 product-plan、接口与 technical-plan 一致、无范围蔓延
4. **测试可达性** — P0 用例可执行、无不可测试实现

最多 3 轮审查修复循环，超过则留给 VERIFY_GATE 最终判定

### 7.3 步骤级回溯（Step-Level Rollback）
![](images/harness-cli/Pasted%20image%2020260408112933.png)
图 7-3：支持回溯

产物清理映射（每个状态对应的文件）：

| 状态 | 产出文件 |
| --- | --- |
| INTAKE | brief.md, source-index.md, clarification-log.md |
| DISCOVER | requirements.md, open-questions.md, risk-list.md |
| SPEC_LOCK | product-plan.md, technical-plan.md, decision-log.md |
| TEST_CONTRACT | test-case.md, acceptance-checklist.md, quality-gates.md, p0_cases_report.md |
| PLAN_LOCK | milestones.md, commit-strategy.md |
| BUILD_LOOP | execution-process.md, milestone-review.md |
| VERIFY_GATE | verification-report.md, gap-list.md |
| FIX_LOOP | bug-fix-log.md, root-cause.md |
| DONE | final-summary.md |

## 8. 状态检查体系

### 8.1 三层检查流程
![](images/harness-cli/Pasted%20image%2020260408112942.png)
图 8-1：三重检查

### 8.2 完整质量检查规则
![](images/harness-cli/Pasted%20image%2020260408112954.png)
| 状态 | 必需文件 | 检查项示例 | 回流目标 |
| --- | --- | --- | --- |
| INTAKE | brief.md, source-index.md, clarification-log.md | 需求目标明确？用户已指明？6维自检完整？ | null |
| DISCOVER | requirements.md, open-questions.md, risk-list.md | 核心路径完整？异常场景列出？需求可验证？ | →INTAKE |
| SPEC_LOCK | product-plan.md, technical-plan.md, decision-log.md | 产品+技术一致？无过度设计？ | — |
| TEST_CONTRACT | test-case.md, acceptance-checklist.md, quality-gates.md, p0_cases_report.md | 每功能有P0验收？有阻断条件？ | — |
| PLAN_LOCK | milestones.md, commit-strategy.md | P0覆盖？单里程碑1-3文件？可独立验证？ | — |
| BUILD_LOOP | execution-process.md, milestone-review.md | 范围不超？DoD满足？审查APPROVE？ | →PLAN_LOCK |
| VERIFY_GATE | verification-report.md | P0全过？符合规格？无阻断缺陷？ | →BUILD_LOOP |
| FIX_LOOP | bug-fix-log.md, root-cause.md | 问题全修？回流路径标明？ | — |
| DONE | final-summary.md | P0过？文档一致？缺陷闭环？ | — |

### 8.3 Gate JSON 示例

INTAKE Gate：

```json
{
  "state": "INTAKE",
  "required_files": ["brief.md", "source-index.md", "clarification-log.md"],
  "checks": [
    "需求目标是否已明确（不是一句模糊描述）",
    "主要用户对象是否已指明",
    "目标系统/模块范围是否已确定",
    "clarification-log.md 是否包含完整的 6 项维度检查"
  ],
  "rollback_target": null
}
```

## 9. Prompt 工程设计

### 9.1 模板渲染机制
![](images/harness-cli/Pasted%20image%2020260408113006.png)
图 9-1：prompt 执行

### 9.3 角色化 Prompt 设计
![](images/harness-cli/Pasted%20image%2020260408113021.png)
图 6-5：角色化 Prompt
![](images/harness-cli/Pasted%20image%2020260408113025.png)
| Prompt 文件 | 角色 | 核心指令 |
| --- | --- | --- |
| intake.md | Orchestrator | 阅读提炼 → 6维自检 → 生成3文档 |
| discover.md | Discovery Worker | 功能目标 + 场景 + 风险评估 |
| spec_lock.md | Spec Worker | 产品方案 + 技术方案 + 自检 |
| test_contract.md | Test Worker | 模式A: 从文档生成 P0/P1/P2 用例 + 验收条件 |
| test_contract_p0_extract.md | Test Worker | 模式B: 从 P0 链接提取用例 + agent-browser 自动化 |
| plan_lock.md | Planning Worker | 3-5 里程碑 + DoD + 提交策略 |
| build_loop.md | Execution Worker | 逐里程碑实现 + 局部自检 |
| review_milestone.md | Reviewer | 4维审查 + APPROVE/REQUEST/REWORK |
| verify_gate.md | Verification Worker | P0验证 + 5种判定 |
| fix_loop.md | Repair Worker | 根因分类 + 修复 + 回流建议 |
| done.md | Orchestrator | 归档总结 + 一致性检查 |

## 10. 可观测性：执行轨迹追踪

### 10.1 轨迹记录结构

每条记录是一个 JSON 对象，写入 trace.jsonl（每行一条）：

```json
{
  "ts": "2026-03-23T14:16:49Z",
  "actor": "orchestrator",
  "state": "INTAKE",
  "action": "enter",
  "result": "ok",
  "reason": "...",
  "rollback_target": "PLAN_LOCK"
}
```

### 10.3 执行轨迹摘要示例

```
━━━ 执行轨迹摘要 ━━━
总记录数:    15
涉及状态:    7
Gate 通过:   6 / 失败: 1
回流次数:    1

时间线:
  13:01:05 🔵 INTAKE      ▶ enter → ok
  13:03:22 🟢 INTAKE      ✦ execute → ok
  13:03:45 ✅ INTAKE      ◆ gate_check → pass
  13:05:22 🔵 DISCOVER    ▶ enter → ok
  ...
  13:35:42 ❌ BUILD_LOOP  ◆ gate_check → fail
  13:36:00 🔙 BUILD_LOOP  ↩ rollback → PLAN_LOCK
```

## 11. 使用方式

### 11.1 部分命令列表

| 命令 | 用途 | 必需参数 | 可选参数 |
| --- | --- | --- | --- |
| init | 初始化新任务 | --task-id, --name | --source, --design, --codebase, --p0-url |
| run | 运行完整流水线 | --task-id | --auto |
| step | 单步执行 | --task-id, --state | --p0-url（仅 TEST_CONTRACT 阶段） |
| resume | 从中断恢复 | --task-id | — |
| status | 查看状态 | --task-id | — |
| rollback | 回滚 | --task-id, --to | --step, --list-steps |
| trace | 查看轨迹 | --task-id | — |
| list | 列出任务 | — | — |
| gate | 查看Gate清单 | — | --state |

### 11.2 典型使用流程
![](images/harness-cli/Pasted%20image%2020260408113037.png)
图 11-2：使用流程

## 12. 未来改进方向

| 方向 | 描述 |
| --- | --- |
| prompt和gate.json优化 | 每个阶段执行能力以及执行效果验证的优化 |
| 接入openclaw | 企微操作项目开发、查看进度等 |
| 可视化 | 整个流程可视化：状态流转、轨迹时间线 |
| 团队协作 | 多人任务分配机制 |
| 自定义状态 | 用户自定义状态和转换规则 |
| CI/CD 集成 | 与团队已有的CI/CD工具集成，在开发阶段执行代码审查 |
