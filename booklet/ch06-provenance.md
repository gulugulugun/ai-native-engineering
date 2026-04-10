# 第 6 章：产物溯源全表

> **本章核心问题**：每个具体产物的设计来源是什么？
>
> **用途**：当你需要修改某个 Rule、Skill、Hook 或模板时，先查本表，找到当初的设计依据，避免"改了但不知道为什么当初这么写"。

---

## 6.1 方案内容来源（4 层）

| 层 | 来源 | 贡献了什么 |
|---|------|-----------|
| 1. 自身基础 | 四项目现状 + XPage/XDC/XContract 技术边界 + CodeBuddy 原生能力 | 约束条件 |
| 2. 同业务实践 | KM 团队（tobytang）：流程编排 | 阶段化工作流 + 固定交付物 + 契约先行 + 测试左移 |
| 2. 同业务实践 | voucher 团队（cavanwan）：知识体系 | 代码第一性 + 任务提案桥梁 + 反馈飞轮 + 人机分工模型 |
| 2. 同业务实践 | 信贷 MIS 团队（[iWiki 文档](https://iwiki.woa.com/p/4018105585)） | 配置驱动 + Agent 三角协作 + UI Guide + 契约校验 + 场景判断 + Git 规范 |
| 2. 同业务实践 | Harness CLI（zipsu） | 验证回流 + 代码库搜证 + DoD + 需求就绪度 |
| 2. 同业务实践 | specmate | 上下文隔离 + 澄清分级 + 批次执行 |
| 3. 业内优秀实践 | agent-skills（addyosmani） | 反合理化 + 五轴审查 + Skill 结构 |
| 3. 业内优秀实践 | Superpower（obra） | 完成前验证 + TDD + 任务粒度 + 禁止占位符 |
| 3. 业内优秀实践 | CE（EveryInc） | 做完即沉淀 + 80/20 原则 |
| 3. 业内优秀实践 | gstack（garrytan/YC） | 前提挑战 + 四分类 + 安全护栏 |
| 3. 业内优秀实践 | Claude Code system prompt | 避免过度工程 + 未读勿改 + 最小复杂度 |
| 4. 底层思想 | Harness Engineering + OpenHarness | 约束 + 反馈 + 控制系统的认知坐标 |

## 6.2 落地方式来源

| 载体 | 面向 | 写法参考 |
|------|------|---------|
| Rules | AI | OpenHarness `CLAUDE.md`：祈使句、精简、可执行 |
| Skills | AI（按阶段加载） | CodeBuddy 原生 Skills 系统 + OpenHarness 按需加载 |
| Commands | 用户入口 | CodeBuddy Slash Commands 文档 + agent-skills 7 命令启发 |
| Hooks | AI 运行时 | OpenHarness `PreToolUse`/`PostToolUse` 拦截模式 |
| Memory | AI 上下文 | OpenHarness 索引 + 主题文件拆分 |

---

## 6.3 Rules 溯源

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `delivery-workflow` 的祈使句风格 | OpenHarness `CLAUDE.md` | — |
| `delivery-workflow` 的 6 阶段流程 | — | 方案文档（4 层来源共同推导） |
| `delivery-workflow` 的禁止项（禁止 TBD、模糊引用） | Superpower `writing-plans` | — |
| `delivery-workflow` 的任务分类 | — | 我们自己第一版设计 |
| `delivery-workflow` 的"完成前必须出示证据" | Superpower `verification-before-completion` | — |
| `delivery-workflow` 的"主动挑战前提假设" | gstack `/office-hours` | — |
| `delivery-workflow` 的四分类归档 | gstack `/learn` | — |
| `delivery-workflow` 的验证回流 | Harness CLI `VERIFY_GATE` + `FIX_LOOP` | — |
| `workspace-architecture` | — | 自身项目现状 + 信贷 MIS（配置表结构） |
| `xpage-frontend-guardrails` | — | XPage 平台约束 + 踩坑经验 |
| `xdc-backend-contract-guardrails` | — | XDC 框架约束 + 契约驱动实践 |
| `git-workflow` | — | 通用 Git 最佳实践 + 信贷 MIS Git 规范 |

## 6.4 Skills 溯源

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| Skills 整体架构（6 阶段各一个 Skill） | CodeBuddy 原生 Skills + OpenHarness 按需加载 | 方案全流程设计 |
| `requirement-analysis` 的前提挑战 | gstack `/office-hours` | — |
| `requirement-analysis` 的四要素 + 穷举策略 | — | KM 团队 |
| `requirement-analysis` 的代码库搜证 | Harness CLI `answer` 命令 | — |
| `requirement-analysis` 的就绪度评级 | Harness CLI `clarification_readiness` | — |
| `spec` 独立于 design | agent-skills + Superpower + gstack（三方一致） | — |
| `spec` 的 5 必选章节结构 | agent-skills `spec-driven-development` | 适配契约驱动场景 |
| `spec` §1 目标 | agent-skills "Goals" | — |
| `spec` §2 接口定义 | agent-skills "Commands"（适配为接口定义） | XDC/OpenAPI 实践 |
| `spec` §3 文件规划 | agent-skills "Structure" + Superpower | — |
| `spec` §4 测试策略 | agent-skills "Tests" | KM 团队测试左移 |
| `spec` §5 约束与边界 | agent-skills "Boundaries" + gstack | — |
| `spec` 场景判断（纯前端/纯后端/全栈） | 信贷 MIS 团队 | — |
| `spec` 禁止 TBD | Superpower `writing-plans` | — |
| `spec` 是唯一锚点 | 我们自创（三方实质一致） | — |
| `design` 的澄清分级（P0/P1/P2） | specmate | — |
| `design` 的批次执行 | specmate `planning.md` | — |
| `design` 的 DoD + 回退策略 | Harness CLI 里程碑结构 | — |
| `design` 的任务提案思路 | — | voucher 团队 SDD |
| `coding` 的契约校验前置 | 信贷 MIS 团队 | — |
| `coding` 的逐任务不跳步 | agent-skills 反合理化 + Superpower 任务粒度 | — |
| `coding` 的完成前验证 | Superpower `verification-before-completion` | — |
| `coding` 的 6 条避免过度工程禁止项 | Claude Code system prompt | — |
| `coding` 的完成条件含人审查 | agent-skills 五轴审查 | — |
| `testing` 的测试左移 | — | KM 团队 |
| `testing` 的证据要求 | Superpower `verification-before-completion` | — |
| `testing` 的回流机制 | Harness CLI VERIFY_GATE + FIX_LOOP | — |
| `archiving` 的反馈闭环 | — | voucher 团队飞轮 |
| `archiving` 的 Spec 主线合并 | voucher/mkt 团队 OpenSpec `specs/` 活文档 | — |
| `archiving` 的知识排除原则 | voucher 团队知识提炼四原则 | — |
| `archiving` 的做完即沉淀 | CE `/ce:compound` | — |
| `archiving` 的四分类 | gstack `/learn` | — |
| `archiving` 的 delta-first | 开发知识库"基准文档增量更新" | — |
| `ui-guide` | 信贷 MIS 团队 UI Guide | — |

## 6.5 Hooks 溯源

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `session_start_context` 的项目检测 + 注入 | OpenHarness `claudemd.py` | — |
| `session_start_context` 的"引导走流程选择" | 我们自创 | — |
| `pretool_guard` 的高危命令拦截 | OpenHarness `hooks/` PreToolUse | — |
| `pretool_guard` 的安全护栏思路 | gstack `careful`/`freeze`/`guard` | — |
| `post_lint_check` | CodeBuddy Hooks 文档 PostToolUse | 方案"改完立即检查 lint" |

## 6.6 SubAgents 溯源

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| SubAgent 上下文隔离思路 | specmate | — |
| `design-clarifier` | CodeBuddy Agent 系统 | 方案设计阶段搜证需求 |
| `batch-implementer` | CodeBuddy Agent 系统 | 编码阶段批次执行需求 |
| `archiving-delta-synthesizer` | CodeBuddy Agent 系统 | 归档阶段 delta-first 需求 |

## 6.7 Memory / Templates / Commands 溯源

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `MEMORY.md` 索引 + 主题文件 | OpenHarness memory 索引思路 | — |
| `memory-capture-template` 四分类 | gstack `/learn` | — |
| `memory-capture-template` 知识排除原则 | voucher 团队知识提炼四原则 | — |
| `handoff-template` | 我们自己第一版设计 | — |
| `tasks-batch-template` | specmate `planning.md` 启发 | — |
| `archiving-delta-template` | 开发知识库增量更新启发 | — |
| `clarifications-draft-template` | specmate P0/P1/P2 启发 | — |
| `/implement` 命令 | CodeBuddy Slash Commands | 方案 Implement 流程 |
| `/fast-fix` 命令 | CodeBuddy Slash Commands | 方案 Fast-fix 流程 |
| `settings.json` | CodeBuddy Hooks 文档 | 注册 3 个 Hook |

---

## 6.8 方案文档各章节内容来源

| 章节 | 主要内容来源 |
|------|------------|
| 问题定义 | 自身痛点 + KM 统计数据 + agent-skills 反合理化观察 |
| 设计依据 | 本表 6.1 + 6.2 |
| 人机分工模型 | voucher 团队实践 |
| 需求分析阶段 | KM（四要素+穷举）+ gstack（前提挑战）+ Harness CLI（搜证+就绪度） |
| 规范定义阶段 | agent-skills（5 章节）+ Superpower（禁止 TBD）+ 信贷 MIS（场景判断） |
| 方案设计阶段 | KM（契约先行）+ voucher（任务提案）+ Harness CLI（DoD）+ specmate（澄清分级） |
| 编码实现阶段 | voucher（Rules 即规范）+ Superpower（粒度+验证）+ gstack（护栏）+ Claude Code（最小复杂度） |
| 测试验证阶段 | KM（测试左移）+ Superpower（证据验证）+ Harness CLI（回流） |
| 归档沉淀阶段 | voucher（飞轮）+ CE（复利）+ gstack（四分类）+ 开发知识库（增量更新） |
| 反馈闭环 | voucher（飞轮效应）+ CE（80/20 复利） |

---

> **使用方式**：修改某个产物前，先在本表中找到它的写法来源和内容来源。如果来源是外部实践，查阅[附录](appendix.md)中的外部实践对照精要了解当初的吸收判断。
