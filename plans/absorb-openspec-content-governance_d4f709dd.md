---
name: absorb-openspec-content-governance
overview: 将 voucher/mkt 团队 OpenSpec 实践中验证过的 3 个内容治理策略融入我们现有的 Skill/Template 体系，并同步更新方案文档和 booklet。
todos:
  - id: add-specs-dir
    content: 新建 .codebuddy/specs/ 目录及 README.md，定义 spec 主线的命名规则和更新流程
    status: completed
  - id: update-skills
    content: 修改 archiving Skill（增加 spec 主线合并步骤 + 知识排除原则）和 design Skill（增加任务依赖关系图指引）
    status: completed
    dependencies:
      - add-specs-dir
  - id: update-templates
    content: 修改 tasks-batch-template.md（增加任务依赖关系部分）和 memory-capture-template.md（增加知识排除原则）
    status: completed
  - id: update-scheme
    content: 更新方案文档 ai-native-engineering-scheme.md：参考来源表增加 voucher/mkt OpenSpec 条目，设计和归档阶段补充 3 个策略说明
    status: completed
    dependencies:
      - add-specs-dir
      - update-skills
      - update-templates
  - id: update-booklet
    content: 同步更新 booklet 四个文件（ch03 设计+归档阶段、ch04 飞轮机制、ch06 溯源表、appendix 外部实践），确保与方案文档口径一致
    status: completed
    dependencies:
      - update-scheme
---

## 用户需求

将 voucher/mkt 团队 OpenSpec 实践中验证过的 3 个内容治理策略融入现有 `.codebuddy/` 方案体系，同时同步更新所有相关文档。

## 核心特性

### 1. Spec 活文档机制

归档阶段增加"合并 spec 关键能力描述到持久化主线文件"步骤，新建 `.codebuddy/specs/` 目录存放能力主线文档。让 AI 在后续需求中能看到已部署能力的演进视图，而不是每次从零理解。

### 2. 任务依赖关系图

在 `tasks-batch-template.md` 末尾增加 `## 任务依赖关系` 部分，用 ASCII DAG 格式标注任务间的前后依赖和可并行关系。design Skill 生成 tasks.md 时引导产出此部分。

### 3. 知识排除原则

在 Memory 沉淀模板和 archiving Skill 中增加排除规则：代码能直接表达的流程逻辑不进 Memory/知识文档，只文档化 AI 读代码后仍不理解的隐性知识。

### 4. 文档同步更新

方案文档、booklet（ch03/ch04/ch06/appendix）全部同步更新，确保方案文档-booklet-skill-template 四者口径一致。溯源表标注这 3 个策略来自 voucher/mkt 团队 OpenSpec 实践。

## 技术栈

纯 Markdown 文档修改，无代码实现。涉及 `.codebuddy/` 目录下的 Skill 定义、模板文件、方案文档和 booklet 文档。

## 实现方案

### 总体策略

3 个内容治理策略分别融入对应的 Skill 和 Template 中，遵循现有的 6 阶段工作流架构，不引入新的执行机制或外部依赖。所有改动通过修改现有 Markdown 文件实现，新建仅限于 `specs/` 目录及其说明文件。

### 关键决策

1. **Spec 活文档的存储位置**：选择 `.codebuddy/specs/<capability-name>.md`，而不是放在各项目目录下。理由：spec 主线是跨项目的能力视图（一个能力可能跨前后端），放在 `.codebuddy/` 集中管理与现有 Memory/Rules 同级，便于 AI 统一读取。

2. **任务依赖关系的表达格式**：采用 mkt 已验证的 ASCII 文本 DAG 格式（如 `T1.1, T1.2 (并行) → T2.1 ← T1.1`），而不是 Mermaid 图。理由：ASCII 格式更紧凑，AI 解析更可靠，与 mkt 实践一致。

3. **知识排除原则的落地方式**：同时写入 `memory-capture-template.md`（模板层面引导）和 `archiving` Skill（执行层面约束），双重保障。不修改 `archiving-delta-template.md`，因为那是 delta 草稿格式模板，排除原则应在更上游的决策环节生效。

### 实现注意事项

- 修改 `archiving` Skill 时，新增步骤要插入到"步骤 4：确认后执行真实归档"之后（作为步骤 5），不改变已有步骤的编号逻辑
- `design` Skill 中只需在"步骤 4：生成批次化 tasks.md"中追加一条关于依赖关系图的指引，不改变现有 5 字段格式
- 方案文档更新时，在 3.1 参考来源总表中增加 voucher/mkt OpenSpec 条目，在 4.4 方案设计阶段和 4.7 归档阶段分别补充对应说明
- booklet 更新保持与方案文档一致的口径

## 目录结构

```
.codebuddy/
├── specs/                                    # [NEW] 能力 Spec 主线目录
│   └── README.md                             # [NEW] 目录说明：什么是 spec 主线、命名规则、归档时如何更新
├── skills/
│   ├── archiving/
│   │   └── SKILL.md                          # [MODIFY] 增加步骤 5"合并 spec delta 到主线" + 知识排除原则
│   └── design/
│       └── SKILL.md                          # [MODIFY] 步骤 4 追加任务依赖关系图指引
├── templates/
│   ├── tasks-batch-template.md               # [MODIFY] 末尾增加 ## 任务依赖关系 部分
│   └── memory-capture-template.md            # [MODIFY] 增加知识排除原则（什么不该记）
├── plans/
│   └── ai-native-engineering-scheme.md       # [MODIFY] 更新参考来源表 + 设计/归档阶段说明
└── booklet/
    ├── ch03-workflow.md                      # [MODIFY] 更新设计阶段（依赖关系图）+ 归档阶段（spec 主线）
    ├── ch04-core-mechanisms.md               # [MODIFY] 飞轮机制增加知识排除原则 + spec 主线说明
    ├── ch06-provenance.md                    # [MODIFY] 溯源表增加 3 个策略的来源标注
    └── appendix.md                           # [MODIFY] 外部实践总览增加 voucher/mkt OpenSpec 条目
```

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 在修改 booklet 和方案文档前，批量读取所有待修改文件的完整内容，确认插入位置和上下文
- Expected outcome: 获取所有文件的精确内容，避免修改时遗漏上下文或插入位置错误

### SubAgent

- **archiving-delta-synthesizer**
- Purpose: 修改完成后，按 delta-first 策略整理所有变更点，生成变更摘要供人审查
- Expected outcome: 产出一份清晰的变更清单，列出每个文件的具体改动点