# 工作区长期记忆（索引）

> 最后更新: 2026-04-07
>
> 本文件是索引，详情按需读取对应主题文件。

## 项目概况

微信支付存款组 MIS 系统，4 个项目：

| 项目 | 角色 | 技术栈 | 详情 |
|------|------|--------|------|
| `queryopenorderlist` | **新前端（目标架构）** | Vue 3 + TDesign + XPage | → `memory/project-architecture.md` |
| `xdc_wxpay` | **新后端（目标架构）** | Node.js + XDC SDK + OpenAPI | → `memory/project-architecture.md` |
| `payclient-oa-depositmisview` | 旧前端（迁移参考） | Vue 2 + Element UI | → `memory/project-architecture.md` |
| `lqp` | 旧后端（迁移参考） | Egg.js / Koa / Kite | → `memory/project-architecture.md` |

## 主题文件索引

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `memory/project-architecture.md` | 四项目详细架构 + 对比表 + 迁移关系 | 需要了解项目结构、技术栈差异、迁移方向时 |
| `memory/platform-and-framework.md` | wxpay 平台 API + XDC Kite 框架 + 契约管理 + 环境配置 | 开发前端页面（平台 API）或后端接口（框架约定）时 |
| `memory/scheme-summary.md` | AI 研发闭环体系方案摘要 + 体系支撑表 + 实施路线 | 需要了解方案全貌、当前进展、体系产物时 |
| `memory/2026-04-02.md` | 2026-04-02 工作日志 | 回顾历史决策时 |
| `memory/2026-04-03.md` | 2026-04-03 工作日志 | 回顾历史决策时 |

## 核心约束速记

- **契约驱动**：接口定义先行，编码前锁定
- **原生能力先行**：优先用 CodeBuddy Rules/Skills/Hooks/MCP，不过早引入框架
- **三层分离（前端）**：Pages ↔ Models ↔ Services
- **无 Service 层（后端）**：轻量逻辑用 entity，复杂逻辑拆微服务
- **验证有证据**：禁止"应该""大概"，必须运行命令+读输出+确认通过

## 环境速记

- Node >= 18.18.0，切换命令：`export NVM_DIR="/opt/nvm" && . "$NVM_DIR/nvm.sh" && nvm use 20`
- XPage 重启：`cd /data/workspace/queryopenorderlist && curl -s http://wxpay.woa.com/xdc/wxpaymenuconfig/restart.sh | bash -s pro`

## 当前状态

方案 v0.2 + 全部执行指令就绪（5 Rules + 7 Skills + 2 Commands + 3 Hooks），下一步是拿真实需求验证 6 阶段全流程。详见 `memory/scheme-summary.md`。
