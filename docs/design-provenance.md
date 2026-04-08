# 设计决策溯源表

> 记录方案中每个关键设计点和落地产物的来源，方便后续修改时快速定位"当初为什么这么写"和"参考了谁"。

## 一、方案内容来源（4 层）

| 层 | 来源 | 贡献了什么 |
|---|------|-----------|
| 1. 自身基础 | 四项目现状 + XPage/XDC/XContract 技术边界 + CodeBuddy 原生能力 | 约束条件——能做什么、不能做什么 |
| 2. 同业务实践 | KM 团队（tobytang）：流程编排 | 阶段化工作流 + 固定交付物 + 契约先行 + 风险前置 + 测试左移 |
| 2. 同业务实践 | voucher 团队（cavanwan）：知识体系 | 结构化知识体系 + 代码第一性 + 任务提案桥梁 + 反馈飞轮 + 人机分工模型 |
| 3. 业内优秀实践 | agent-skills（addyosmani） | 19 个工程技能 + 7 个 Slash Commands（/spec /plan /build /test /review /code-simplify /ship）+ 反合理化机制 + 验证门禁 + 五轴代码审查 |
| 3. 业内优秀实践 | Superpower（obra） | 流程纪律 + TDD 红绿循环 + 任务粒度 2-5 min + 完成前验证必须有证据 + 禁止占位符 |
| 3. 业内优秀实践 | CE / Compound Engineering（EveryInc） | 知识复利 + 做完即沉淀 + 80/20 计划审查原则 |
| 3. 业内优秀实践 | gstack（garrytan / YC） | 需求阶段主动挑战假设 + 学习记录四分类（Patterns/Pitfalls/Preferences/Architecture）+ 安全护栏 |
| 3. 业内优秀实践 | Claude Code system prompt（通过 `system_prompts_leaks` 仓库提取） | 避免过度工程 + 最小复杂度 + 删除优于保留 + 边界验证 + 未读勿改 + 优先编辑 |
| 4. Harness 思想 | Harness Engineering + OpenHarness | 约束 + 反馈 + 控制系统的认知坐标 |

## 二、方案落地方式来源

| 载体 | 面向 | 写法参考来源 |
|------|------|------------|
| 方案文档 `ai-native-engineering-scheme.md` | 人 | 自研结构，参考 KM/voucher 的"问题→推导→设计"叙事方式 |
| Rules | AI | OpenHarness 的 CLAUDE.md 写法：祈使句、精简、可执行 |
| Skills | AI（按阶段自动加载） | CodeBuddy 原生 Skills 系统 + OpenHarness 的 Skill 按需加载 |
| Commands | 用户快捷入口 | CodeBuddy Slash Commands 文档 + agent-skills 的 7 命令结构启发 |
| Hooks | AI 运行时 | OpenHarness 的 PreToolUse / PostToolUse 拦截模式 + CodeBuddy Hooks 文档 |
| Memory | AI 上下文 | OpenHarness 的索引 + 主题文件拆分思路 |

## 三、具体产物溯源

### Rules

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `delivery-workflow.mdc` 的祈使句风格 | OpenHarness CLAUDE.md | — |
| `delivery-workflow.mdc` 的 6 阶段流程 | — | 方案文档（4 层来源共同推导） |
| `delivery-workflow.mdc` 的禁止项（禁止 TBD、禁止模糊引用） | Superpower `writing-plans` SKILL.md | — |
| `delivery-workflow.mdc` 的任务分类（Implement / Fast-fix / Review-only） | — | 我们自己第一版就有的分类，本轮正式写入 Rule |
| `delivery-workflow.mdc` 的"完成前必须出示证据" | Superpower `verification-before-completion` SKILL.md | — |
| `delivery-workflow.mdc` 的"主动挑战前提假设" | gstack `/office-hours`（Premise Challenge） | — |
| `delivery-workflow.mdc` 的四分类归档 | gstack `/learn` | — |
| `workspace-architecture.mdc` | — | 我们自身项目现状（四项目识别 + 技术栈 + 禁止事项） |
| `xpage-frontend-guardrails.mdc` | — | XPage 平台约束 + 我们踩坑经验 |
| `xdc-backend-contract-guardrails.mdc` | — | XDC 框架约束 + 契约驱动实践 |

### Hooks

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `session_start_context.py` 的项目检测 + 提示注入结构 | OpenHarness `claudemd.py`（向上遍历发现 + 注入 system prompt） | — |
| `session_start_context.py` 的"引导 AI 走流程选择" | 我们自创（OpenHarness 没有这个，它的 Hook 只做拦截不做引导） | — |
| `pretool_guard.py` 的高危命令拦截 | OpenHarness `hooks/` 子系统（PreToolUse 事件 + block_on_failure） | — |
| `pretool_guard.py` 的安全护栏思路 | gstack `careful` / `freeze` / `guard` 三级护栏 | — |

### Memory / Templates

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `memory-capture-template.md` 的四分类 | gstack `/learn`（Patterns / Pitfalls / Preferences / Architecture） | — |
| `handoff-template.md` 的结构 | 我们自己第一版设计 | — |
| `current-task.md` 的结构 | handoff 模板变体 + OpenHarness memory 索引思路 | — |
| `MEMORY.md` 的格式 | 我们自己既有格式 | — |
| Memory 后续拆分方向（索引 + 主题文件） | OpenHarness `memory/manager.py`（add/remove/search API + MEMORY.md 当索引） | — |

### Skills

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| Skills 整体架构（6 个阶段各一个 Skill） | CodeBuddy 原生 Skills 系统 + OpenHarness 的 Skill 按需加载思路 | 方案文档全流程设计 |
| 每个 Skill 的 YAML frontmatter（`name` / `description` / `allowed-tools`） | CodeBuddy Skills 文档 | — |
| `spec` Skill 的独立阶段设计 | agent-skills `/spec`（Define 阶段）+ Superpower `brainstorming`（强制 spec）+ gstack `/office-hours`（设计文档优先） | 3 个主流框架一致：spec 和 plan 必须分开 |
| `spec` Skill 的 5 个必选章节整体结构 | agent-skills `spec-driven-development`（原 6 章节：Goals/Commands/Structure/Style/Tests/Boundaries，我们去掉 Style 因为已有 Rules 覆盖） | 适配我们的契约驱动场景 |
| `spec` §1 目标（Goals） | agent-skills `spec-driven-development` 的 "Goals" 章节 | — |
| `spec` §2 接口定义（API / Interface） | agent-skills `spec-driven-development` 的 "Commands" 章节（我们适配为"接口定义"以匹配 XDC/OpenAPI） | 我们自身的契约驱动实践 |
| `spec` §3 文件规划（File Plan） | agent-skills `spec-driven-development` 的 "Structure" 章节 + Superpower `writing-plans`（要求先 map files and responsibilities 再写任务） | — |
| `spec` §4 测试策略（Test Strategy） | agent-skills `spec-driven-development` 的 "Tests" 章节 | KM 团队（测试左移：测试用例在编码前就基于规则生成） |
| `spec` §5 约束与边界（Constraints） | agent-skills `spec-driven-development` 的 "Boundaries" 章节 + gstack `/office-hours`（要求明确标注 Out of Scope） | — |
| `spec` "本阶段只定义做什么，不拆任务、不写代码" | Superpower `brainstorming`（"Do not implement any code"）+ gstack `/office-hours`（"This skill only generates design documents"） | — |
| `spec` "禁止 TBD/待定/后续补充" | Superpower `writing-plans`（"Never use placeholders: TBD, TODO, implement later"） | — |
| `spec` "spec 是后续所有阶段的唯一锚点" | 我们自创——agent-skills/Superpower 的 review 都要求"根据 spec 检查代码"，实际含义一致，但"唯一锚点"是我们的显式表达 | — |
| `spec.md` 文件名和统一产出格式 | 我们自创——agent-skills 产出 PRD 文档，Superpower 产出 `docs/superpowers/specs/YYYY-MM-DD--design.md`，gstack 产出 `~/.gstack/projects/{slug}/...design-{datetime}.md`，我们简化为统一的 `spec.md` | — |
| `requirement-analysis` Skill 的执行步骤 | — | KM 团队（四要素 + 穷举补全）+ gstack（前提挑战） |
| `design` Skill 的执行步骤（职责收窄为"规划怎么做"） | Superpower `writing-plans`（spec 和 plan 分离）+ agent-skills `/plan` | voucher 团队（任务提案桥梁） |
| `coding` Skill 的执行步骤和禁止项 | Superpower `writing-plans` + `verification-before-completion` | voucher 团队（Rules 即规范） |
| `coding` Skill 的完成条件（含人审查关键逻辑） | agent-skills `code-review-and-quality`（五轴审查：正确性/可读性/安全性/性能/测试覆盖） | 弥补 Review 环节缺失 |
| `coding` Skill 的 6 条新增禁止项（避免过度工程/过早抽象/无用兼容/过度防御/未读先改/不必要新建） | Claude Code system prompt（`system_prompts_leaks` 仓库提取） | Google 工程文化的最小复杂度原则 |
| `testing` Skill 的执行步骤 | Superpower `verification-before-completion`（必须附带证据） | KM 团队（测试左移） |
| `archiving` Skill 的四分类 | gstack `/learn` | voucher 团队（知识飞轮） |

### Slash Commands

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `/implement` 命令 | CodeBuddy Slash Commands 文档（`.codebuddy/commands/*.md`） | 方案文档 Implement 流程 |
| `/fast-fix` 命令 | CodeBuddy Slash Commands 文档 | 方案文档 Fast-fix 流程 |

### PostToolUse Hook

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `post_lint_check.py`（文件修改后自动提醒 lint） | CodeBuddy Hooks 文档（PostToolUse 事件） | 方案文档编码阶段"改完代码后立即检查 lint" |

### 配置文件

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `settings.json`（Hook 注册配置） | CodeBuddy Hooks 文档（settings.json 配置结构） | 注册 SessionStart / PreToolUse / PostToolUse 三个 Hook |

### 文档文件

| 产物 | 写法来源 | 内容来源 |
|------|---------|---------|
| `docs/design-provenance.md`（本文件） | 我们自创 | 记录所有产物的设计来源，方便后续修改时定位 |
| `docs/architecture-diagrams.drawio` | CodeBuddy drawio-diagrams Skill | 全流程图 + 体系架构图 + 方案来源层次图 |

## 四、方案文档各章节的内容来源

| 章节 | 主要内容来源 |
|------|------------|
| 2. 问题定义 | 自身痛点 + KM 团队统计数据 + agent-skills 反合理化观察 |
| 3. 设计依据 | 本表的第一、二节 |
| 4.1 人机分工模型 | voucher 团队实践 |
| 4.2 需求与分析 | KM 团队（四要素结构化 + 穷举补全）+ gstack（前提挑战） |
| 4.3 方案设计 | KM 团队（契约先行）+ voucher 团队（任务提案桥梁） |
| 4.4 编码实现 | voucher（Rules 即规范）+ Superpower（任务粒度 + 完成验证）+ gstack（安全护栏） |
| 4.5 测试与验证 | KM 团队（测试左移）+ Superpower（完成前验证） |
| 4.6 归档与沉淀 | voucher（知识飞轮）+ CE（做完即沉淀）+ gstack（四分类） |
| 4.7 反馈闭环 | voucher（飞轮效应）+ CE（80/20 复利）+ gstack（学习记录管理） |
| 5. 体系支撑 | 自身已落地产物 |
| 6. 实施路线 | 自研 |

---

> 最后更新：2026-04-06
