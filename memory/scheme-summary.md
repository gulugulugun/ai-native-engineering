# AI 原生研发闭环体系方案摘要

> 从 MEMORY.md 拆分 | 正式方案文档：`.codebuddy/plans/ai-native-engineering-scheme.md`
>
> **一句话目标**：通过 Rules + Hooks + Memory + MCP + 阶段化工作流，把 AI 从"代码补全工具"提升为"可治理的研发执行体"——每个阶段有固定输入、明确约束和标准交付物，过程可追溯、结果可验证、经验可沉淀。

## 设计依据分层

- **内容来源（4 层）**：① 自身基础（约束条件）→ ② 同业务实践 KM/voucher/信贷 MIS（流程+结构设计）→ ③ 业内实践 agent-skills/Superpower/CE/gstack（具体机制）→ ④ Harness 思想（认知坐标）
- **落地方式**：参考 OpenHarness 把方案"翻译"成 AI 可执行指令

## 全流程设计（6 个阶段）

```
需求与分析 → 规范定义(spec) → 方案设计 → 编码实现 → 测试与验证 → 归档与沉淀 → 反馈闭环
```

| 阶段 | 人的角色 | AI 的角色 | 核心交付物 |
|------|---------|----------|-----------|
| 需求与分析 | **主导** | 辅助：结构化需求、提取规则 | `requirement-analysis.md` |
| 规范定义(spec) | **主导** | 辅助：生成 spec 草案 | `spec.md` |
| 方案设计 | **主导** | 辅助：拆任务清单 | `tasks.md` |
| 编码实现 | 辅助 | **主导**：按任务逐步生成代码 | 符合 spec 的前后端代码 |
| 测试与验证 | 辅助 | **主导**：生成用例、执行测试 | `test-cases.md` + 验证结果 |
| 归档与沉淀 | **主导** | 辅助：提炼规则和记忆更新 | Rules / Memory / 模板更新 |

## 体系支撑能力（已落地）

| 层 | 已落地产物 | 作用 |
|----|-----------|------|
| Rules | **5 条**：workspace-architecture（含配置表）/ xpage-frontend-guardrails / xdc-backend-contract-guardrails / delivery-workflow（v3）/ git-workflow | 项目约束 + 任务分类 + Git 规范 |
| Skills | **7 个**：requirement-analysis / spec（含场景判断）/ design / coding（含契约校验）/ testing / archiving + ui-guide | 全流程阶段执行指令 + UI 正向模板 |
| Commands | **2 个**：`/implement` / `/fast-fix` | 用户快捷入口 |
| Hooks | 3 个：session_start_context / pretool_guard / post_lint_check | 上下文注入 + 风险控制 + lint 提醒 |
| Memory | MEMORY.md（索引）+ 主题文件 + context + templates | 长期知识 + 任务上下文 |
| MCP | XContract（可用）/ 工蜂 Git（部分可用）/ iWiki（待接入） | 外部系统接入 |

## 实施路线与当前状态

- [x] **第一阶段：最小可用原型**（2026-04-03）— Rules 4 条 + Hooks 2 个 + 模板 3 个
- [x] **方案调研与外部实践对照**（2026-04-06）— Harness + KM/voucher + agent-skills/Superpower/CE/gstack
- [x] **方案落地到执行指令**（2026-04-06）— 6 阶段 Skills + Commands + PostToolUse Hook
- [x] **同业务实践对照与改进**（2026-04-07）— 信贷 MIS 参考 → 配置表+UI Guide+场景判断+契约校验+Git 规范
- [x] **Memory 拆分**（2026-04-07）— 从 434 行单文件拆为索引+3 个主题文件
- [ ] **第二阶段：真实需求验证**（下一步）— 选一个真实需求走完整全流程
- [ ] **第三阶段：持续沉淀** — 常用模板和轻量 SOP
- [ ] **第四阶段：扩展增强** — 工蜂 Git 自动化、iWiki MCP、Custom Subagents

## CodeBuddy 能力备忘

- **Agent Teams**：支持多智能体协作（成员间直接通信 + 共享任务列表）
- **Custom Subagents**：`.codebuddy/agents/` 下自定义（12+ 配置维度，agentic/manual 两种模式）
- **当前决策**：暂不引入 Sub Agent，Skill 链已覆盖 6 阶段串行流程

## Harness Engineering 思想参考

> 来源: OpenAI 博文 + OpenHarness 仓库

`Harness Engineering` 是底层思想参考，不是正式命名。核心：模型提供智能，Harness 提供约束、反馈和控制系统。映射到 CodeBuddy：Rules = 约束、Hooks = 控制、Memory = 反馈。
