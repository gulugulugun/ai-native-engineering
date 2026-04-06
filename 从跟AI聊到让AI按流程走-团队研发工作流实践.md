---
title: 从"跟 AI 聊"到"让 AI 按流程走"：团队研发工作流实践
author: tobytang
source: https://km.woa.com/articles/show/656028
date: 2026-03-28
tags:
  - AI开发
  - Harness-Engineering
  - 研发工作流
fetched: 2026-04-06
---

# 从"跟 AI 聊"到"让 AI 按流程走"：团队研发工作流实践

> ⭐ 导语：让共识被明确冻结下来，让过程和结果能被持续约束和验证。

## 一、背景：为什么不能只靠"跟 AI 聊"

团队现状（2026 H1）：

| 指标 | 数据 | 说明 |
| --- | --- | --- |
| 开发人力 | 18 人 | — |
| H1 需求总量 | 288 个 | 平均每迭代 20 个 |
| 需求迁入率 | 41.46% | 每迭代 8-9 个中途插入 |
| 突发 | 64 条 | 客诉排查、临时跑数、治理项等 |
| 交付率 | 94% | 靠时间和经验撑住，团队人员压力较大 |

AI 编码工具（Cursor、Copilot 等）已经在用，但多数人的用法是"点对点"——把需求丢给 AI，聊几轮，拿到代码，提交。这种方式的问题：

- **信息不沉淀**：每次对话从零开始，上一轮的需求分析、风险判断、设计决策不会自动传递给下一个人或下一次需求
- **质量靠个人**：同一个需求不同人跟 AI 聊，产出质量差异大，取决于"会不会提问"
- **过程不可追溯**：需求做完后没有结构化产物，只有代码和零散的聊天记录，没法审查也没法复用

我们需要的不是"个人用 AI 更快"，而是"团队用 AI 质量可控、经验可积累"。

核心思路：**给每个研发步骤套上约束——固定输入 → 约束规则 → 明确交付物**。每个步骤封装为一个 Skill，AI 在约束下工作，输出确定性大幅提升。

---

## 二、研发工作流全景

从产品需求进来到上线归档，拆成 ⓪~⑧ 九个步骤，每步对应一个 Skill：

**14 个 Skill 覆盖全流程**：

| 阶段 | Skill | 交付物 | 视角 |
| --- | --- | --- | --- |
| ⓪ 探索 | openspec-explore | 思考记录（无固定格式） | 方案清晰度 |
| ① 需求评审 | tapd-review | review_report.md | 需求完备性 |
| ② 需求分析 | requirement-analysis | requirement-analysis.md | 功能点 + 业务规则 |
| ③-a 方案提案 | openspec-propose | proposal / design / contract / tasks / risk | 变更范围 + 技术决策 + 接口契约 |
| ③-a 安全 | stride-assessment | stride_assessment.md | 安全威胁 |
| ③-a 资金 | fund-risk-assessment | fund_risk_assessment.md | 资金安全 |
| ③-a 资产 | resource-checklist-gen | resource_checklist.md | 编码前需申请什么 |
| ③-b 详细设计 | detailed-design-agent | proto/ + sequence/ | 接口定义 + 调用序列 |
| ④ 测试设计 | test-case-generation | test-cases.md | AT / IT / E2E 三层 |
| ⑤ 验收 Case | acceptance-case-gen | acceptance-cases.md | 产品验收 |
| ⑥ 编码实现 | openspec-apply-change | 代码 MR | 逐 task、契约先行 |
| ⑦ 测试生成 | api/integration-test | ut.json + xautotest | 自动化验证 |
| ⑧ 归档 | openspec-archive | archive/ | 知识沉淀 |

每步定义了固定输入 → 约束规则 → 标准交付物，团队任何人走同样流程，产出一致、不依赖个人经验。

---

## 三、关键实践

### 3.1 工作流可自定义组装

标准流程 ⓪~⑧ 提供骨架，具体跑哪些步骤、每步出什么交付物，按团队和业务情况定制。我们做了三项定制：

- **契约先行**：方案阶段先出 contract_proposal + proto 定义，编码前接口字段和行为变更已锁定。tasks.md 中契约任务排第 0 章，AI 不用脑补接口形态。
- **安全+资金评估嵌入流程**：把 STRIDE 安全评估、资金风险评估、项目风险、资产注册清单做成独立 Skill，插在 ③ 方案提案里每个需求自动过。四份各管一个维度（安全威胁 / 资金安全 / 项目风险 / 编码前资产），不混在 design.md 的某个段落里，每份有独立的状态追踪（✅已闭环 / ⚠️待跟进）。以前靠口头讨论编码时没人记得，现在嵌在流程里跳不过去。
- **详细设计按需启用**：复杂需求（如商客连接 IM）启用 ③-b 详细设计（存储 → 技术决策 → DDD 三层契约 → 序列图），简单改造（如 SMS）用 ③-a 的 contract_proposal 就够。

### 3.2 团队知识预装入 project.md

团队约定一直有，但散在各人脑子里和零散文档中，换个人就得重新交代。做了两件事：

- `project.md` 把技术栈、分层、复用优先级、编译流程、方案质量红线等统一写下来，分"通用"和"业务"两层，Skill 启动时自动读。
- iWiki 上攒了几年的套路攻略和踩坑文章（40+ 篇），按技术点建了索引表（限频、错误码、安全、登录态等 13 篇），写方案时 AI 碰到对应技术点自动通过 MCP 把原文拉过来参考。

**iWiki 知识库索引（AI 按需自动读取）**：

| 技术点 | iWiki 文章 |
| --- | --- |
| 频率限制 | 切换北极星频率限制组件 |
| 错误码设计 | 服务返回值收敛原则 |
| XSS 防御 | XCGI防御XSS方法总结 |
| 登录态 | XCGI拦截器实现登录态校验 |
| KV 加密 | kvsvr敏感信息加密切换国密 |
| 单元测试 | 已有服务接入单元测试 |
| 重试策略 | 业务系统请求重试策略总结 |
| XWI 框架 | 七天精通微信支付 XWI 开发 |
| ... | 共 13 篇 |

> **例子**：SMS 案例中写限频方案，AI 自动找到并读了《切换北极星频率限制组件》，不用人说"我们团队用北极星"。以前这些文章是写了没人看，现在变成 AI 写方案的参考材料。

### 3.3 测试左移 — 编码前生成用例

传统做法是代码写完再补测试。我们的工作流中，④ test-case-generation Skill 在编码前就基于 ② 需求分析的功能点和业务规则自动生成 AT（接口测试）/ IT（集成测试）/ E2E（端到端测试）三层用例。

**关键方法**：② 需求分析阶段对每条业务规则要求四要素结构化——规则描述、满足时行为、违反时行为、边界条件。有了这四个要素，测试用例可以机械推导：

| 规则要素 | 推导出的测试 |
| --- | --- |
| 满足时 | 正向测试用例 |
| 违反时 | 反向测试用例 + 错误码验证 |
| 边界条件 | 边界值测试（阈值 ±1） |

再按规则类型（data_validation / business_constraint / state_transition 等）自动匹配测试设计技术，"这条规则应该写几条用例"变成确定性问题而非经验判断。

---

## 四、落地案例

### 案例一：SMS 验证码（小型改造，1 天完成，0 人工编码）

**需求背景**：商家名片手机号无所有权验证，每日 1-2 例客诉。需增加短信验证码校验。

**变更范围**：新增 2 个 CGI + 改造 2 个 CGI + 北极星限频 + SmsBizAo 短信网关。

跑完工作流后 openspec 仓库的实际产出（17 个交付物）：

```
add-profile-sms-verify/
├── review_report.md            ① 需求评审（21/27 通过，6 项缺失驱动补全）
├── requirement-analysis.md     ② 需求分析（7 FP + 11 BR + 5 RISK）
├── proposal.md                 ③ 方案提案
├── design.md                   ③ 技术设计（含 v1→v2 方案迭代记录）
├── contract_proposal.md        ③ 接口契约（4 CGI 完整字段定义）
├── tasks.md                    ③ 任务清单（8 章 30+ 子任务）
├── risk_analysis.md            ③ 风险追踪（10 项，9 已闭环）
├── stride_assessment.md        ③ STRIDE 安全评估（18 威胁，0 高风险）
├── fund_risk_assessment.md     ③ 资金风险评估（6 维度确认不涉及）
├── resource_checklist.md       ③ 资产注册清单（11 项）
├── test-cases.md               ④ 测试用例（30 AT + 6 IT + 6 E2E = 42 条）
├── acceptance-cases.md         ⑤ 产品验收 Case（18 组）
├── proto/                      ⑥ 接口 Proto 定义
├── sequence/                   3 个 CGI 序列图
└── specs/                      规格说明
```

> 设计文档已同步到 iWiki，结构与仓库一致。

**全程 0 人工编码**——AI 按 tasks.md 中的执行计划逐任务实现：

```
tasks.md 执行计划（摘要）
§1 基础设施准备        确认短信服务接入 / 北极星限频 / token 加解密工具函数
§2 新增 sendsmscode    Handler 实现 + CmdId 注册 + 错误码 + 监控上报
§3 新增 verifysmscode  Handler 实现 + CmdId 注册
§4 改造 savemchinfo    解析 verify_token + 版本判断 + token 校验
§5 改造 updatemchinfo  同 §4 逻辑
§6 编译检查            BUILD 依赖 + 废弃函数清理
§7 测试验证            按 test-cases.md 的 42 条用例验证
§8 上线监控            MR → 灰度 → 全量 → 归档
```

**STRIDE 的实际价值**：评估发现短信轰炸（D 维度）和绕过验证码直接调用保存接口（E 维度）两个威胁，三级限频 + 版本号校验直接写进 §2 和 §4 成为编码任务——不是事后补的，是方案阶段就锁定的。

**测试用例在编码前就绪**：

| 维度 | 用例数 | 覆盖 |
| --- | --- | --- |
| AT 接口测试 | 30 条 | 全部 7 FP + 11 BR，含限频边界（59s/60s/61s）、token 时效（299s/300s/301s） |
| IT 集成测试 | 6 条 | sendsmscode → verifysmscode → savemchinfo 全链路 |
| E2E 端到端 | 6 条 | 商家编辑名片完整流程，含老版本兼容、弱网 |
| 产品验收 Case | 18 组 | 直接给产品验收用，按 BR 边界值生成 |

### 案例二：商客连接 MVP（中大型新建，目标 7 天 0→1，进行中）

**需求背景**：商家端新增顾客留言能力，涉及 IM 消息、会话管理、通知等，需要新建 3 个独立服务。

需求更复杂，拆成需求级 + 2 个子需求，各自独立产出（21+ 个交付物）：

```
look_for_merchant/
├── requirement-analysis.md     ② 需求分析（25 FP + 18 BR + 11 RISK）
├── stride_assessment.md        ③ STRIDE（26 威胁，1 高风险 blocker）
├── resource_checklist.md       ③ 资产清单（29 项）
├── technical-decisions.md      ③-b 技术决策（消息同步 / 通知通道 / 存储选型）
├── storage-design.md           ③-b 存储设计（2 张 KV 表 + 索引 + 通知判定）
├── state-machine.md            ③-b 状态机
├── enter-chat-window/          子需求①：进入聊天窗
│   ├── proposal.md / design.md / contract_proposal.md / tasks.md
│   ├── sequence/               2 个 CGI 序列图
│   └── specs/                  2 份规格说明
└── conversation-list/          子需求②：留言列表
    ├── proposal.md / design.md / contract_proposal.md / tasks.md
    ├── sequence/               2 个 CGI 序列图
    └── specs/                  2 份规格说明
```

**与 SMS 案例的关键差异**：

| 维度 | SMS（小型） | 商客连接（中大型） |
| --- | --- | --- |
| 需求规模 | 7 FP + 11 BR | 25 FP + 18 BR |
| 协作方式 | 单人 | 多人，子需求级目录 |
| 详细设计 | 不需要 ③-b | 启用 ③-b（存储+决策+DDD契约+序列图） |
| STRIDE | 18 威胁，0 高风险 | 26 威胁，1 高风险 blocker |
| 工期 | 1 天 | 7 天 0→1 |

**STRIDE 的实际价值**：识别风控降级策略缺失为 P0 blocker，标记"编码前必须明确降级策略"，写入安全校验清单。如果没有 STRIDE 这一步，这个问题大概率要到联调甚至灰度阶段才暴露。

**多人协作的做法**：需求拆成子需求（enter-chat-window / conversation-list），每个子需求独立一套 proposal → tasks，可并行分配给不同人。需求级的 requirement-analysis、stride、resource_checklist 在上层共享，避免重复分析。

---

## 五、每步 Harness 详解

> 本节是技术细节，面向想复用这套工作流的团队。每步只讲"输入→约束→交付物"和一个关键要点，完整的 SMS 案例数据见上文「四、落地案例」。

### ⓪ 探索思考 — openspec-explore

唯一没有固定交付物的步骤。只读不写码，用于方案前的调研和比较。产出可沉淀为 proposal / design，或纯粹获得清晰度。

### ① 需求评审 — tapd-review

```
TAPD 需求链接 + 7 维度评审标准 → review_report.md
```

7 维度：业务（WHY/WHO/HOW）、需求（TAPD 落地/异常流程/兼容）、生命线（合规/资金/信息安全）、详细检查、项目管理、性能、用户体验。前四项必检，后三项建议。

SMS 案例：27 必检项中 21 通过，发现 6 项缺失（设计稿未定稿、老版本兼容未说明、灰度计划未提及等），缺失项直接传递给 ② 需求分析重点补全。

### ② 需求分析 — requirement-analysis-agent

```
TAPD 需求 + review_report.md → requirement-analysis.md
产出：功能点清单 + 业务规则（四要素） + 覆盖矩阵 + 风险评估
```

**关键方法：以用例视角审查规则，穷举找全，结构化表达。**

三步走：

1. **覆盖矩阵**——功能点-规则覆盖表，一眼看出哪个功能点缺规则
2. **穷举式提取**——五种策略（CRUD 补全 / 正反面 / 边界值 / 异常流 / 交叉影响）主动探查隐藏规则
3. **四要素结构化**——每条规则必须有：规则描述、满足时行为、违反时行为、边界条件

SMS 案例：11 条规则中 PRD 明确写出 6 条，AI 穷举策略补全 5 条（45%）。覆盖矩阵发现 FP-005 "0 规则"，分析后确认由 FP-002 的 BR-005 间接覆盖。

### ③ 方案提案 — openspec-propose + detailed-design-agent

```
requirement-analysis.md + project.md → 8 交付物
proposal / design / contract / tasks / risk / stride / fund / resource
```

**六个实践要点**：

1. **以用例视角组织设计**：同一个功能点贯穿需求→设计→契约→任务→测试，任何环节遗漏都能通过标签缺失发现
2. **契约先行**：contract_proposal 在编码前锁定接口字段和行为，tasks.md 契约任务排第 0 章
3. **风险独立交付**：risk_analysis.md 整合全部风险，统一编号、状态追踪、Follow-up 项
4. **STRIDE 安全评估**：对每个接口按六维度（仿冒/篡改/抵赖/泄露/拒绝服务/提权）分析，逼出具体缓解措施写入 tasks
5. **资金风险评估**：六维度（资金流向/一致性/幂等性/异常回滚/对账/并发安全），不涉及资金也需显式声明
6. **资产注册清单**：从已有交付物中自动盘点 CmdId / 错误码 / idkey / XConfig 等，编码前全部就绪

**③-b 详细设计**（复杂需求启用）：4 Phase 严格顺序——存储设计 → 技术决策 → DDD 三层契约 → 序列图。商客连接启用了全部 4 Phase，SMS 不需要。

### ④ 测试设计 — test-case-generation-agent

```
requirement-analysis.md → test-cases.md（AT + IT + E2E 三层）
```

规则四要素直接推导用例，规则类型（6 种）自动匹配测试设计技术。三层保障：追踪矩阵（广度）+ 设计技术（深度）+ 质量评审（5 维自检）。

### ⑤ 产品验收 — acceptance-case-gen

从 ② 的功能点和规则推导，用产品语言（非技术语言）输出，直接给产品经理验收用。

### ⑥ 编码实现 — openspec-apply-change

按 tasks.md 逐任务执行，三大约束：复用优先（4 级搜索范围）、编译检查门禁（BUILD / -Werror / API 签名）、错误码管理（禁止 hardcode，走 MCP 注册）。

### ⑦ 测试生成 — api-test + integration-test

基于已实现代码生成测试代码。⑦-a 接口测试输出 ut.json + mock.json（XWI 框架），⑦-b 集成测试输出 xautotest 脚本。

### ⑧ 归档 — openspec-archive

检查产出物和任务完成度，全部移入 archive/，增量 spec 同步主规范，留存供后续需求参考。

---

## 六、实践中踩过的坑

### 6.1 设计文档拆细，不搞大而全

早期尝试把方案、契约、风险、测试写在一份文档里，结果几千行没人看得动，评审也抓不住重点。后来拆成独立交付物，每个文件职责单一，评审时按需打开对应文件。SMS 案例 14 个文件看着多，但每个都可以独立审查和修改，比翻一份巨型文档效率高得多。

### 6.2 多人协作：子需求级目录

单人做 SMS 够用，但商客连接涉及多人协作，一个 openspec 目录装不下。做法是把需求拆成子需求（enter-chat-window / conversation-list），每个子需求独立一套 proposal → tasks，各自可并行推进、独立评审。需求级的 requirement-analysis、stride、resource_checklist 仍在上层共享，避免重复分析。

### 6.3 质量红线量化，约束 AI 生成代码

最初 AI 生成的代码提交 MR 后被工蜂 hook 拦住——圈复杂度超标、函数体过长、嵌套层级过深。问题在于 AI 对"代码要简洁"这类审美判断理解飘忽不定，同样的提示词有时生成 20 行有时生成 200 行。

后来把质量要求全部降维成硬阈值写进 project.md：单文件 ≤ 800 行、单函数 ≤ 30 行、嵌套 ≤ 3 层、分支 ≤ 3 个。AI 对这类可判定谓词执行得非常稳定，后续生成的代码基本不再触发规范拦截。

### 6.4 反馈驱动：代码和 Spec 保持一致

一把生成方案和代码后，后续开发、联调、测试中一定会有修改。当前做法是：小改动修完代码后反向更新对应的 spec 文件（如 contract_proposal 里的字段变更、tasks 里的状态标记），保障代码和设计文档始终一致。上线后的迭代也一样——改代码的同时更新 spec，而不是让文档和代码各走各的。这样下次再做相关需求时，spec 是可信的，不用重新对一遍代码。

---

## 七、效果数据

### SMS 验证码全流程时间线

| 步骤 | 传统方式（预估） | 本工作流（实际） |
| --- | --- | --- |
| 需求评审 | 0.5 天（会议+纪要） | ~30 min（AI 自动 27 项检查） |
| 需求分析 | 1 天（人脑提取+文档化） | ~1 h（7 FP + 11 BR + 矩阵） |
| 方案设计 | 1-2 天（设计+评审+修改） | ~3 h（8 交付物含评估+清单） |
| 测试用例 | 1-2 天（人工编写+review） | ~1 h（42 条 + 18 组验收） |
| 编码实现 | 2-3 天（手写+联调） | ~2 h（AI 全量编码，0 行手写） |
| 测试代码 | 1 天（写桩+mock） | ~1 h（ut.json + xautotest） |
| **合计** | **6-9.5 天** | **~1 天** |

### 两个案例的产出对比

| 指标 | SMS（小型） | 商客连接（中大型） |
| --- | --- | --- |
| 功能点 / 业务规则 | 7 FP + 11 BR | 25 FP + 18 BR |
| 交付物数量 | 17 个 | 21+ 个 |
| STRIDE 威胁 | 18 项，0 高风险 | 26 项，1 高风险 blocker |
| 资产注册 | 11 项 | 29 项 |
| 测试用例 | 42 条 + 18 组验收 | 编码阶段进行中 |
| 详细设计 | 不需要 ③-b | 存储 + 3 决策 + DDD 契约 + 5 序列图 |
| 工期 | 1 天 | 目标 7 天 0→1 |

---

## 八、局限与下一步

**当前局限**：

- **Skill 维护成本**：14 个流程 Skill + 30 个工具 Skill，随框架升级和业务变化需持续更新，目前主要靠个人维护
- **上下文窗口限制**：复杂需求（如商客连接 IM）的上下文超过 AI 单次处理范围，需要人工分段喂入，体验下降
- **团队接受度差异**：不同人对 AI 工具的熟悉程度不同，从"个人能用"到"团队都用"还有一段路
- **效果数据样本少**：目前只有两个案例验证，传统方式的时间是预估值而非实测

**下一步**：

- 工作流在更多需求上验证，沉淀团队可复用的 Skill 和 project.md
- 探索客诉诊断 Agent 和数据分析助手，降低突发（客诉排查、临时跑数等）对开发的打断

---

## 附录

### 标签编号体系

| 编号前缀 | 含义 | 定义位置 |
| --- | --- | --- |
| FP-xxx | 功能点 | requirement-analysis.md |
| BR-xxx | 业务规则 | requirement-analysis.md |
| RISK-xxx | 风险项 | risk_analysis.md |
| D1~Dn | 设计决策 | design.md |
| AT-xxx | 接口测试用例 | test-cases.md |
| IT-xxx | 集成测试用例 | test-cases.md |
| E2E-xxx | 端到端用例 | test-cases.md |
