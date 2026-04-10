---
name: archiving
description: 新需求的归档与沉淀阶段。当测试验证完成、需要提炼经验并更新 Rules 和 Memory 时自动触发。这是 Implement 流程的第 6 阶段。
allowed-tools: Read, Write, Edit, Task
---

# 归档与沉淀阶段

你正在执行 Implement 流程的**第 6 阶段：归档与沉淀**。

本阶段不直接把经验写进基线，而是先生成**只包含变化点**的归档草稿，再由人评审 diff，确认后再真正更新 Rules / Memory / 模板。

## 前置条件

测试阶段已完成且人已验收。

## 核心升级

- 归档优先走 **delta-first**：先整理变化点，再做真实写入。
- 增量整理优先交给子代理 `archiving-delta-synthesizer`（或等价的 `Task / Subagent` 调用）做上下文隔离。
- 只评审变化点，不重写整份 Rules / Memory / 模板基线。

## 执行步骤

### 1. 读取本次过程产物与现有基线

1. 回顾本次需求的全部过程产物：`requirement-analysis.md`、`spec.md`、`tasks.md`、`test-cases.md`、关键代码改动、验证结果。
2. 读取现有 Rules、Memory 和可复用模板，确认哪些内容已经被沉淀，避免重复写入。

### 2. 生成归档 delta 草稿

1. 优先调用子代理 `archiving-delta-synthesizer`；如果运行环境不支持显式点名子代理，则用 CodeBuddy 原生 `Task / Subagent` 能力按同等职责隔离执行。
2. 子代理只负责整理 `.codebuddy/context/archiving.delta.md`，不得直接修改基线文件。
3. 草稿必须遵循 `.codebuddy/templates/archiving-delta-template.md`，按三类目标输出：
   - **Rules**：新的长期约束、禁忌、坑点
   - **Memory**：`Pattern / Pitfall / Preference / Architecture`
   - **Templates**：可重复复用的结构与模板

### 3. 只展示变化点并请求确认

1. 读取 `.codebuddy/context/archiving.delta.md`。
2. 向人展示本次建议新增 / 修订 / 不纳入沉淀的条目，而不是整篇重写后的全文。
3. **STOP**，等待人确认哪些条目真正成立、哪些需要删除或改写。

### 4. 确认后执行真实归档

1. 仅对已确认的条目更新对应 Rules / Memory / 模板。
2. 没有通过确认的条目，不得写入基线。
3. 如果 delta 为空，明确说明"本次无值得长期沉淀的新增经验"，然后结束归档阶段。

### 5. 合并 Spec 到能力主线

> 来源：voucher/mkt 团队 OpenSpec 的 `specs/` 活文档机制。

1. 检查本次 `spec.md` 中是否定义了可独立描述的**能力**（如"待处理订单查询"、"保证金明细查看"）。
2. 如果有，检查 `.codebuddy/specs/` 目录下是否已有对应的主线文件：
   - **已有** → 在"关键行为"中追加/修改本次变更的行为描述，在"变更历史"中追加一行记录。
   - **没有** → 按 `.codebuddy/specs/README.md` 中的模板新建主线文件。
3. 合并时**只追加变化点**，不重写已有内容。
4. 如果本次需求是纯 bug 修复或配置变更，不涉及能力新增/修改，跳过此步骤。

## 知识排除原则

> 来源：voucher/mkt 团队 OpenSpec 知识文档提炼策略。

以下内容**不应**写入 Memory 或知识文档：
- **代码能直接表达的流程逻辑**——通过读代码即可理解的，以代码为准，不做二次文档化。
- **一次性聊天内容**——临时讨论、调试过程。
- **证据不足的推测**。

只沉淀同时满足以下条件的知识：
1. AI 读代码后仍不理解的隐性知识
2. 业务强相关的领域规则
3. 相对稳定、短期内不会频繁变化的约定

## 注意

- 只沉淀长期有效、可复用的经验。
- 临时讨论、一次性聊天不写入 Memory。
- 所有沉淀都要有证据；证据不足的条目只能放进"本次不纳入沉淀"。
- 归档阶段优先更新变化点，不要整篇重写现有文档。

## 完成

归档完成后，本次 Implement 流程结束。反馈闭环生效——本次沉淀的 Rules / Memory / 模板将在下一个需求中自动生效。
