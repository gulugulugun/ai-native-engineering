# 附录

---

## A. 外部实践对照精要

> 完整分析见 `memory/external-practices.md`。本附录只列稳定结论。

### A.1 已分析来源总览

| 来源 | 核心方向 | 当前结论 |
|------|----------|----------|
| **KM** (tobytang) | 流程编排 + 固定交付物 | 已吸收：四要素规则、测试左移、契约先行 |
| **voucher** (cavanwan) | 知识体系 + 人机分工 | 已吸收：代码第一性、反馈飞轮、人机分工模型、知识排除原则 |
| **voucher/mkt OpenSpec** (cavanwan) | 内容治理（Spec 活文档 + DAG + 知识精选） | 已吸收：Spec 主线机制、任务依赖关系图、知识排除原则（不引入 CLI） |
| **信贷 MIS** | 配置表 + UI Guide | 已吸收：子系统配置表、契约校验、Git 规范 |
| **Harness CLI** (zipsu) | 流程自动化 + 可回溯 | 已吸收：验证回流、代码库搜证、DoD+回退、需求就绪度 |
| **specmate** | 执行层流程治理 | 可吸收/条件吸收：SubAgent 隔离、澄清分级、批次执行 |
| **开发知识库** | 复杂存量系统知识底座 | 可吸收：基准文档增量更新 + 只评审 diff |

### A.2 筛选时默认问的 4 个问题

1. 它解决的是我们**哪个真实问题**？
2. 它属于**哪一层**参考来源？
3. 它是否适配当前 `CodeBuddy + Rules / Hooks / Memory / MCP + 契约驱动` 路线？
4. 它应该进入**正式方案、Rules、Memory**，还是仅保留参考？

### A.3 引用注意事项

- `specmate` 应拆成两部分看：执行层流程治理 vs 知识底座能力
- 效率提升、可用率提升等量化数据标注为"材料提供数据"，不能写成已验证结论
- 仓库内存在少量文档/实现不一致，引用时优先以"源码已验证机制"表述

---

## B. 参考来源索引

### B.1 同业务实践

| 来源 | 作者 | 位置 |
|------|------|------|
| 《从"跟AI聊"到"让AI按流程走"》 | tobytang | [`references/从跟AI聊到让AI按流程走-团队研发工作流实践.md`](../references/从跟AI聊到让AI按流程走-团队研发工作流实践.md) |
| 《以 Code 为核心的开发模式实践》 | cavanwan | [`references/ai-dev-practice.md`](../references/ai-dev-practice.md) |
| Harness CLI | zipsu | [`Harness-CLI-AI驱动的需求开发自动化流水线.md`](../Harness-CLI-AI驱动的需求开发自动化流水线.md) |
| 信贷 MIS | credit_mis | [CLAUDE.md](https://iwiki.woa.com/p/4018105585) · [UI Guide](https://iwiki.woa.com/p/4018105655) · [Proto Inspector](https://iwiki.woa.com/p/4018105662) · [Feature Planner](https://iwiki.woa.com/p/4018105617) · [LiveCoding 技术文档](https://iwiki.woa.com/p/4019637501) · [LiveCoding 路线图](https://iwiki.woa.com/p/4019636475) |
| specmate | specmate 团队 | 源码搜证，结论见 `memory/external-practices.md` |

### B.2 业内优秀实践

| 来源 | 作者 | 链接/位置 |
|------|------|----------|
| agent-skills | Addy Osmani | [github.com/nicepkg/agent-skills](https://github.com/nicepkg/agent-skills) |
| Superpower | Jesse Vincent (obra) | [github.com/obra/superpowers](https://github.com/obra/superpowers) / 本地 `.superpowers/` |
| CE (Compound Engineering) | Dan Shipper (EveryInc) | [every.to/p/compound-engineering](https://every.to/p/compound-engineering) |
| gstack | Garry Tan (YC) | [github.com/garrytan/gstack](https://github.com/garrytan/gstack) |
| Claude Code system prompt | 通过 `system_prompts_leaks` 仓库提取 | — |

### B.3 底层思想

| 来源 | 链接 |
|------|------|
| Harness Engineering (OpenAI) | [openai.com/zh-Hans-CN/index/harness-engineering](https://openai.com/zh-Hans-CN/index/harness-engineering/) |
| OpenHarness | [github.com/openai/openharness](https://github.com/openai/openharness) |
| The Anatomy of an Agent Harness (LangChain) | [blog.langchain.com/the-anatomy-of-an-agent-harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) |
| Harness Engineering (Martin Fowler) | [martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) |

---

## C. 术语表

| 术语 | 说明 |
|------|------|
| **Harness** | 模型外面包裹的"控制层"——约束、反馈和控制系统 |
| **Harness Engineering** | 设计 Harness 的工程学科，2026 年 AI 工程圈热门话题 |
| **Rules** | CodeBuddy 的规则文件，AI 每次会话自动加载的约束 |
| **Skills** | CodeBuddy 的技能文件，按阶段/场景按需加载的执行指令 |
| **Hooks** | CodeBuddy 的钩子机制，在 AI 操作的关键时刻自动触发 |
| **Memory** | 长期知识存储，跨会话持久化 |
| **MCP** | Model Context Protocol，外部工具接入协议 |
| **SubAgent** | 子代理，专注于特定任务、有明确写入边界的独立执行体 |
| **Spec** | 规范定义文档，回答"做什么"，是后续所有阶段的唯一锚点 |
| **DoD** | Definition of Done，完成定义——做到什么程度算完 |
| **四要素** | 业务规则的结构化格式：规则描述 / 满足时行为 / 违反时行为 / 边界条件 |
| **四分类** | Memory 条目的分类模型：Pattern / Pitfall / Preference / Architecture |
| **delta-first** | 先生成变化点草稿，人确认后才写入基线的归档策略 |
| **契约先行** | 先定义 OpenAPI 契约，再生成/编写实现代码 |
| **测试左移** | 测试用例在编码前就基于需求规则生成 |
| **反合理化** | AI 为跳过步骤找"合理理由"的倾向，需要通过约束阻止 |
| **飞轮效应** | 每次需求完成后的沉淀让下一次需求起点更高，循环递增 |
| **XPage** | 微信支付低代码前端平台 |
| **XDC** | 微信支付后端开发平台 |
| **XContract** | 微信支付契约管理平台 |
| **Svrkit** | 微信支付内部 RPC 框架 |
| **BizError** | XDC 框架中的业务异常类 |

---

## D. 缺失信息清单

以下信息在编写小册过程中发现缺失或不够明确，需要你后续补充：

| # | 缺失内容 | 影响章节 | 建议补充方式 |
|---|---------|---------|------------|
| 1 | **真实落地案例** | 第 7 章 | 跑完第一个真实需求全流程后填充 |
| ~~2~~ | ~~信贷 MIS 实践的完整参考文档~~ | ~~第 2 章、第 6 章~~ | ✅ 已补充（4 篇 iWiki 文档） |
| ~~3~~ | ~~空 Skill 目录的规划~~ | ~~第 5 章~~ | ✅ 已删除（原为精简版预留，决定先跑完整流程） |
| 4 | **实际的翻车案例截图/记录** | 第 1 章 | 当前用的是参考文章中的案例，如果有自己项目的翻车案例更有说服力 |
| 5 | **时间线量化数据** | 第 7 章 | 需要真实需求的计时数据，目前无法填写 |
| ~~6~~ | ~~MCP iWiki 接入计划~~ | ~~第 5 章~~ | ✅ iWiki MCP 已接入可用 |

---

> **回到目录**：[README.md](README.md)
