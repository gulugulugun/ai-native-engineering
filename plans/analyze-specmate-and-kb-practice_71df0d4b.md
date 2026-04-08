---
name: analyze-specmate-and-kb-practice
overview: 基于用户提供的 specmate 与开发知识库材料，结合 /data/workspace/specmate 源码与文档做一轮外部实践分析，并准备后续将可吸收机制映射到当前 AI 原生研发闭环方案与分享骨架。
todos:
  - id: evidence-mapping
    content: 用[subagent:code-explorer]补齐specmate与知识库源码证据
    status: completed
  - id: practice-screening
    content: 按四问归类直接吸收、条件吸收和仅参考项
    status: completed
    dependencies:
      - evidence-mapping
  - id: update-scheme-docs
    content: 更新方案文档与对外分享骨架的新增章节
    status: completed
    dependencies:
      - practice-screening
  - id: archive-analysis-result
    content: 回写current-task并沉淀Memory索引与主题文件
    status: completed
    dependencies:
      - update-scheme-docs
---

## User Requirements

基于用户提供的 `specmate` 与“开发知识库构建”材料，以及 `/data/workspace/specmate` 中已核验的源码与文档证据，完成一轮新的外部实践分析。

## Product Overview

本轮工作聚焦“分析与吸收”，不是开发新功能。需要把 `specmate` 的 4 步流程、分阶段 Commands/Skills、SubAgent 上下文隔离、P0/P1/P2 分级澄清、模板校验与归档机制，以及开发知识库的多源输入、多 Agent 编排、11 类文档、增量更新等内容，转译成适合当前体系的可落地结论。

## Core Features

- 结合材料与源码证据，确认哪些机制真实存在、哪些仅为材料口径
- 按“四问”完成筛选：解决的问题、所属层级、是否适配当前路线、沉淀位置
- 对照现有方案，区分“直接吸收、条件吸收、仅保留参考”
- 将结论同步到正式方案文档、对外分享骨架、当前任务交接与长期记忆
- 严格避免重复分析已完成的 KM、voucher、信贷 MIS、Harness CLI

## Tech Stack Selection

- 文档载体：沿用现有 `.codebuddy/` 下的 Markdown 方案、上下文与记忆体系
- 证据来源：`/data/workspace/specmate` 中的 README、docs、skills、agents、validation 与 knowledge-base 相关源码
- 组织方式：继续使用 `plans/`、`context/`、`memory/` 分层沉淀分析结果

## Implementation Approach

采用“材料描述 + 源码搜证 + 方案映射”的三段式方法：先核验 `specmate` 与知识库能力是否能被源码或官方文档支撑，再按当前外部实践筛选四问完成归类，最后把结论落到正式方案、分享骨架和长期记忆中。

关键决策：

- 将本轮输入拆成两组能力：一组是 `specmate` 的流程治理能力，另一组是开发知识库的知识底座能力，避免与已吸收的 Harness CLI、KM、voucher 混写。
- 只吸收与当前 `CodeBuddy + Rules/Skills/Hooks/Memory` 路线兼容的机制；对依赖特定生态或当前尚不具备条件的能力，只记录为观察项或后续验证项。
- 用户材料中的效率数据、提升比例等结果默认标注为“材料提供数据”；除非在代码或配套文档中再次找到佐证，不把它们写成已验证事实。

性能与可靠性：

- 搜证以定向读取为主，复杂度近似为 O(目标文件数)，避免全仓大范围遍历。
- 主要风险是高层宣讲与源码实现不一致；通过路径级证据、最小化搜索范围和已吸收项去重来控制误判。

## Implementation Notes

- 保持 `ai-native-engineering-scheme.md` v0.2 结构稳定，优先在已有“参考来源总表、吸收点、暂不吸收项”框架内增补内容。
- 明确区分“源码已验证机制”“材料表述”“待真实需求验证”，避免宣传口径直接进入正式方案。
- 遵守当前 Memory 约定：若形成长期有效结论，新增 `memory/` 主题文件并同步更新 `MEMORY.md` 索引。
- 本轮仅做分析资产更新，不直接修改现有 Rules、Skills、Hooks；如后续确认要吸收，再单独开实现任务。

## Architecture Design

本次变更属于文档与知识资产更新，结构上分为四层：

- 输入层：用户提供的实践材料、附图、`specmate` 只读源码与文档
- 分析层：机制拆解、四问筛选、适配边界判断、证据归档
- 沉淀层：正式方案文档、对外分享骨架、当前任务交接、长期记忆
- 约束层：保持现有 6 阶段体系主框架不变，只增补新的参考来源与吸收结论

## Directory Structure

本轮以 `.codebuddy/` 下的分析资产为主，`/data/workspace/specmate` 仅作为只读证据源。

- `/data/workspace/.codebuddy/plans/ai-native-engineering-scheme.md` [MODIFY] 正式方案文档。补充 `specmate` 与开发知识库两组实践的来源定位、可吸收点、适配边界、暂缓项，并与现有参考来源表和阶段设计保持一致。
- `/data/workspace/.codebuddy/plans/external-sharing-outline.md` [MODIFY] 对外分享骨架。增加“编码阶段的流程压缩与上下文治理”“复杂存量系统的知识底座”两段讲法、数据素材位和图示落点。
- `/data/workspace/.codebuddy/context/current-task.md` [MODIFY] 当前任务交接。记录本轮已分析来源、已确认结论、暂缓吸收项与后续待分析方向，确保跨会话不重复劳动。
- `/data/workspace/.codebuddy/MEMORY.md` [MODIFY] 长期记忆索引。若新增外部实践主题文件，补充索引与读取时机说明。
- `/data/workspace/.codebuddy/memory/external-practices.md` [NEW] 外部实践主题记忆。沉淀 `specmate`/开发知识库与当前方案的稳定对照结论、复用边界和适配判断。
- 只读证据锚点（不修改）：`/data/workspace/specmate/README.md`、`/data/workspace/specmate/docs/workflow-guide.md`、`/data/workspace/specmate/docs/knowledge-base-guide.md`、`/data/workspace/specmate/src/frontend/agents/specmate-clarify-design.md`、`/data/workspace/specmate/src/shared/commands/validate.ts`、`/data/workspace/specmate/src/shared/knowledge-base/commands/orchestrator.md`

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 补充 `specmate` 在 skills、agents、validation、knowledge-base 编排上的跨文件搜证，核对材料描述与源码实现是否一致。
- Expected outcome: 形成可直接引用到方案文档和记忆文件中的证据清单，减少误吸收、漏吸收和重复分析。