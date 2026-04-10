---
name: ai-native-engineering-booklet
overview: 将 .codebuddy/ 下的 AI 原生研发闭环体系方案梳理为多文件小册（.codebuddy/booklet/），标准版深度（15000-25000字），每章独立可读，讲清每个设计点的来源、推理和好处，配架构图。
todos:
  - id: create-index
    content: 创建 `00-index.md` 目录索引页，含章节导航、阅读建议和 Mermaid 章节依赖图
    status: pending
  - id: write-ch1-why
    content: 撰写第一章 `01-why.md`：三个核心问题的推理链叙事 + 项目现状对比表 + 问题-解法映射图
    status: pending
    dependencies:
      - create-index
  - id: write-ch2-philosophy
    content: 撰写第二章 `02-design-philosophy.md`：四层参考来源解析 + 吸收策略 + 人机分工原则 + 落地方式选择
    status: pending
    dependencies:
      - create-index
  - id: write-ch3-workflow
    content: 撰写第三章 `03-workflow.md`：全流程全景图 + 六阶段三段式详解（每阶段含溯源标注）
    status: pending
    dependencies:
      - write-ch1-why
      - write-ch2-philosophy
  - id: write-ch4-mechanisms
    content: 撰写第四章 `04-key-mechanisms.md`：契约先行 / 验证回流 / 反合理化 / 知识飞轮四大机制专题
    status: pending
    dependencies:
      - write-ch3-workflow
  - id: write-ch5-arch
    content: 使用 [subagent:code-explorer] 搜证后撰写第五章 `05-architecture.md`：六层体系架构逐层详解 + 产物溯源表
    status: pending
    dependencies:
      - write-ch3-workflow
  - id: write-ch6-ch7-appendix
    content: 撰写第六章占位 + 第七章路线图 + 附录参考来源总表与缺失信息清单
    status: pending
    dependencies:
      - write-ch4-mechanisms
      - write-ch5-arch
  - id: review-crossref
    content: 全册交叉审校：统一溯源标注格式、补充章节互引链接、检查 Mermaid 图渲染、输出缺失信息清单
    status: pending
    dependencies:
      - write-ch6-ch7-appendix
---

## 用户需求

将现有"AI 原生研发闭环体系"方案梳理为一本多文件结构的技术小册，讲清每一个设计点的来源、参考依据、设计动机和好处，配合架构图辅助理解。

## 产品概述

一本面向内部的标准版技术小册（15000-25000 字），以多文件目录结构组织，每章独立可读。读者首先是作者自己——在后续调整架构时有明确依据可查；其次可改编为对外分享版本。小册不依赖真实落地案例（案例章留占位），聚焦体系设计的完整性和每个决策点的溯源推理。

## 核心特性

1. **目录索引页**：全册导航，含各章摘要、阅读建议和章节依赖关系
2. **问题驱动的开篇**：从三个核心问题出发，用推理链叙事（学 cavanwan），而非直接列清单
3. **四层参考来源解析**：逐层讲清方案的知识根基，每层标注具体来源、贡献了什么、怎么吸收
4. **六阶段全流程详解**：每阶段按"解决什么问题 - 输入/约束/交付物 - 设计理由溯源"三段式展开
5. **体系支撑六层架构**：Rules / Skills / Commands / Hooks / Memory / MCP 逐层讲解，每个产物追溯写法来源和内容来源
6. **关键机制专题**：契约先行、验证回流、反合理化、知识飞轮等横切机制独立成节
7. **Mermaid 架构图**：全流程全景图、体系六层架构图、参考来源层次图、反馈闭环图等
8. **落地案例占位**：预留案例章结构，等真实需求跑完后填充
9. **缺失信息清单**：识别当前素材中不足的部分，列出供作者补充

## 技术方案

### 文件格式

纯 Markdown 文件，不依赖任何构建工具。每章一个 `.md` 文件，放在 `.codebuddy/booklet/` 目录下。图表使用 Mermaid 语法内嵌（无需额外图片文件），现有 `.codebuddy/images/harness-cli/` 的 PNG 在需要引用外部实践图示时通过相对路径引用。

### 内容来源与转化策略

小册不是方案文档的复制粘贴，而是按"读者视角"重新组织：

| 素材文件 | 在小册中的角色 | 转化方式 |
| --- | --- | --- |
| `plans/ai-native-engineering-scheme.md` | 主体内容来源 | 拆解重组为六章正文，补充推理链叙事 |
| `docs/design-provenance.md` | 溯源数据库 | 每个设计点的"来自哪里"直接引用此表 |
| `memory/external-practices.md` | 吸收判断依据 | 第三章参考来源解析的判断逻辑 |
| `memory/project-architecture.md` | 背景章节素材 | 第一章项目现状部分 |
| `memory/platform-and-framework.md` | 技术约束说明 | 第五章 Rules 层讲解中引用 |
| `references/ai-dev-practice.md` | 叙事风格参考 | 学习其"翻车案例 -> 推导 -> 解法"推理链 |
| `references/从跟AI聊到让AI按流程走...md` | 案例展示参考 | 学习其"产出目录树 + 数据对比"展示方式 |
| `Harness-CLI...md` | 机制设计参考 | 学习其"输入 -> 约束 -> 交付物"格式 |


### 写作原则

1. **推理链叙事**（学 cavanwan）：每个设计点按"遇到什么问题 -> 参考了谁 -> 为什么选这个方案 -> 好处是什么"展开
2. **输入-约束-交付物格式**（学 tobytang/zipsu）：每个阶段的核心信息用统一表格呈现
3. **溯源标注**：关键设计点标注 `[来源: xxx]`，方便后续修改时追溯
4. **图文并茂**：每章至少一张 Mermaid 图，复杂概念用图先建直觉再用文字展开

### 章节规划与字数分配

| 章节 | 文件名 | 预计字数 | 内容定位 |
| --- | --- | --- | --- |
| 目录索引 | `00-index.md` | 500 | 全册导航、阅读建议 |
| 第一章 | `01-why.md` | 2500 | 背景与问题定义（三个核心问题 + 推理链开篇） |
| 第二章 | `02-design-philosophy.md` | 2500 | 设计理念（四层来源 + 吸收策略 + 人机分工原则） |
| 第三章 | `03-workflow.md` | 5000 | 六阶段全流程详解（每阶段三段式展开） |
| 第四章 | `04-key-mechanisms.md` | 3000 | 关键机制专题（契约先行 / 验证回流 / 反合理化 / 知识飞轮） |
| 第五章 | `05-architecture.md` | 4000 | 体系支撑六层架构（每层产物溯源） |
| 第六章 | `06-case-study.md` | 500 | 落地案例（占位结构） |
| 第七章 | `07-roadmap.md` | 1500 | 实施路线、当前状态、已知局限 |
| 附录 | `appendix-sources.md` | 1000 | 参考来源总表 + 缺失信息清单 |
| **合计** |  | **~20500** |  |


### 目录结构

```
.codebuddy/booklet/
├── 00-index.md              # [NEW] 目录索引。全册导航页，含各章标题、一句话摘要、推荐阅读顺序、章节依赖关系图（Mermaid）。读者通过此页快速定位感兴趣的章节。
├── 01-why.md                # [NEW] 第一章：为什么需要这套体系。从三个核心问题出发（AI 无记忆 / 信息不沉淀 / 缺阶段约束），用推理链叙事展开，包含项目现状四项目对比表、问题与解法的映射关系。包含 Mermaid 问题-解法映射图。
├── 02-design-philosophy.md  # [NEW] 第二章：设计理念与参考来源。讲清四层参考来源（自身基础 / 同业务实践 / 业内优秀实践 / Harness 思想），每层标注具体来源和贡献，说明吸收策略和筛选四问。包含人机分工总原则和落地方式选择。包含 Mermaid 四层来源架构图。
├── 03-workflow.md           # [NEW] 第三章：六阶段全流程。全流程全景图（Mermaid），六阶段概览表，每阶段按"解决什么问题 - 输入/约束/交付物 - 场景示例 - 设计理由溯源"三段式展开。每个设计理由标注来源。这是小册最核心的章节。
├── 04-key-mechanisms.md     # [NEW] 第四章：关键机制专题。横切四大机制独立讲解：契约先行（XDC/XContract 天然匹配）、验证失败多级回流（5 种判定 + 4 级根因）、反合理化与完成前验证（Superpower + agent-skills）、知识飞轮与做完即沉淀（CE + gstack 四分类）。每个机制含来源溯源 + 在体系中的落地点。
├── 05-architecture.md       # [NEW] 第五章：体系支撑六层架构。逐层详解 Rules(5条) / Skills(10个) / Commands(2个) / Hooks(3个) / Memory+Context+Templates / MCP，每个产物追溯写法来源和内容来源（引用 design-provenance.md）。包含 Mermaid 六层架构图和各层产物清单表。
├── 06-case-study.md         # [NEW] 第六章：落地案例（占位）。预留案例结构模板（需求背景 / 产出目录树 / 阶段产出摘要 / 时间线对比 / 关键决策 / 踩坑记录），标注"等真实需求跑完全流程后填充"。
├── 07-roadmap.md            # [NEW] 第七章：实施路线与展望。四阶段实施路线（已完成 / 进行中 / 计划中），当前状态标注，已知局限诚实列出，下一步计划，关注但暂不吸收的设计点清单。
└── appendix-sources.md      # [NEW] 附录：参考来源总表与缺失信息。精简版参考来源总表（12 个来源，每个一行），外部实践吸收判断总表，以及当前识别到的缺失信息清单（需作者补充的内容）。
```

### 实施说明

- Mermaid 图表在 Markdown 中直接内嵌，使用 ` ```mermaid ` 代码块
- 章节间通过相对链接互引（如 `[详见第五章](05-architecture.md#rules-层)`）
- 溯源标注统一格式：`[来源: KM 团队四要素结构化]`、`[来源: Superpower verification-before-completion]`
- 每章开头有"本章要点"摘要框，结尾有"本章关键设计点溯源表"

## 代理扩展

### Skill

- **drawio-diagrams**
- 用途：为小册生成高质量的架构图，包括全流程全景图、六层体系架构图、四层参考来源图等
- 预期产出：`.codebuddy/booklet/` 下的 drawio 架构图文件，可与 Mermaid 互补用于复杂图示

### SubAgent

- **code-explorer**
- 用途：在编写各章节时，搜索 `.codebuddy/` 目录下的 Skills / Rules / Hooks 源文件，确保小册中描述的产物细节与实际文件一致
- 预期产出：准确的产物描述、文件路径和功能说明