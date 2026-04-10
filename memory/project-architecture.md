# 项目架构

> 从 MEMORY.md 拆分 | 最后更新: 2026-04-03

工作区包含 **4 个项目**：2 个旧项目（需要迁移重构）+ 2 个新模板（重构目标架构）。
所有项目属于**微信支付存款组**的内部运营管理系统（MIS）。

---

## 四个项目总览

### ⬛ 旧项目一：payclient-oa-depositmisview（前端 Web）
- **路径**: `/data/workspace/payclient-oa-depositmisview/`
- **定位**: 存款组运营管理后台——**前端**（完整 SPA）
- **技术栈**: Vue 2.7 + TypeScript 4 + Webpack 4 (Vue CLI 4) + Element UI 2.13 + Vuex 3 + Vue Router 3 (hash 模式)
- **UI 库**: `element-ui` + `@tencent/wxpay-mis-ui`
- **构建产物**: 完整 SPA，输出到 `build/` 目录
- **架构**:
  - 布局: 自建 Layout（Element Container: Header + Aside + Main）
  - API 层: Axios 封装 BaseAPI 类（RESTful CRUD），21 个 API 模块统一导出，自动 CSRF + 错误拦截
  - 状态管理: Vuex + `vuex-module-decorators`（装饰器风格），5 个动态模块（Metadata/MsgSend/ActivityBanner/AbTestTool/Count）
  - 类型: 187 个类型文件，含大量 Protobuf 生成的 TS 类型
  - 组件: Schema 驱动表单、通用表格、审批流组件、员工搜索等
- **7 大业务模块**:
  - LQT（零钱通）: 4 路由 11 导航 — 转入转出、额度、ABTest、域名配置等
  - ECARD（二类卡/零钱升级）: 14 路由 13 导航（最大模块） — 开卡监控、公安惩戒、升级链接
  - XJG（小金罐）: 3 路由 3 导航 — 钱包入口、协议上传、公告
  - BK（绑卡）: 1 路由 — 协议上传
  - YHT（银行通）: 1 路由 — 开通入口
  - RLJ/ZLJ（日利金/转利金）: 仅公告管理导航
- **路径别名**: `@src`, `@components`, `@pages`, `@apis`, `@stores`, `@mytypes`, `@constant` 等
- **开发代理**: `/api` → `http://localhost:7001`（指向旧后端 Node 服务）

### ⬛ 旧项目二：lqp（后端 Node.js 集合）
- **路径**: `/data/workspace/lqp/`
- **定位**: 存款组后端服务集合，包含 3 个子项目
- **子项目**:
  1. **`app/mmpayxdcdepositlqpmis`**（主后端 MIS 服务）
     - 技术栈: Egg.js 2 + TypeScript 4 + Node 12
     - 架构: Controller(53文件) → Service(82文件) → Svrkit RPC(30+服务实例, Protobuf)
     - 路由: 装饰器自动扫描（`@Control` + `@Post`/`@Get`，类 NestJS 风格）
     - 中间件: cubeReporter → errorHandler → setApiDescription → smartProxy → checkAuth → checkFrequency → requestLog → xssCheck → xdcAudit → svrAuth → responseFormater
     - 数据库: 不直连，通过 HTTP 调用 `depositlqpmisdao` 微服务
     - 配置中心: 七彩石（Rainbow），每分钟自动刷新
     - 部署: Docker + PM2，端口 3000，4 worker
     - 17 个业务域的 Controller
     - 定时任务: 10 个 schedule（监控、过期处理等）
     - 权限: `@APIDescriptionDecorator` + `@AuthDecorator` 装饰器
     - 审批: PASS 系统 + 有限状态机（FSM）
  2. **`app/mmpayxdcwebankcardweb`**（银行卡 Web 服务）
     - 技术栈: Koa 2 + TypeScript 4 + 手动中间件组装（非 Egg）
     - 路由: 同样使用 `better-controller` 装饰器扫描
     - Protobuf RPC 通信
  3. **`app/mmpayxdclqp4kfbroker`**（客服 Broker 服务）
     - 技术栈: XDC Kite 框架 + TypeScript 4
     - 定位: 零钱加系统对客服的 broker
- **公共层**: `domain/mmpayxdcdepositlqpmisdao`（DAO 微服务）

### 🟢 新模板一：mmpayproductpermissionhtml（XPage 前端模板）
- **路径**: `/data/workspace/mmpayproductpermissionhtml/`
- **定位**: XPage 低代码平台前端项目模板（重构目标架构）
- **技术栈**: Vue 3.4 + TypeScript 5.4 + Vite 5.2 + TDesign Vue Next 1.9 + Tailwind CSS 4.1
- **构建模式**: UMD 库（`script.umd.js` + `style.css`），供 XPage 平台加载
- **架构**: MVVM 三层分离 — Pages（Vue 组件）↔ Models（单例 class + ref 响应式）↔ Services（API 请求）
- **路由**: `src/index.ts` 是路由唯一真相源
- **布局**: 线上由 XPage 平台提供壳（顶部/侧边栏/页脚），`dev/` 目录仅用于本地开发预览
- **特色**:
  - WebMCP 协议（AI 工具注册）
  - JSON Schema 驱动的动态表单组件（`schema-form.vue`）
  - 双重 Vite 配置（生产 UMD + 本地 dev 预览）
  - 自动导入（unplugin-auto-import + unplugin-vue-components）
  - 外部依赖 externalize（vue/vue-router/tdesign/xpage-sdk 等由平台提供）
- **示例页面**: 8 个页面（form-base, form-group, bind-merchant, query-open-order, card-form, form, step-form, api）

### 🟢 新模板二：mmpayxdcproductpermissionweb（XDC Node 后端模板）
- **路径**: `/data/workspace/product_usage_permission_operations/app/mmpayxdcproductpermissionweb/`
- **定位**: XDC 平台 Node.js 后端服务模板（重构目标架构）
- **技术栈**: Node.js 20 + TypeScript + XDC Node SDK（`@xdc/node-sdk`）
- **架构**: Controller 模式，`src/entry.ts` 注册 Controller + 中间件
- **契约驱动**: `.xdc/contract/` 包含 OpenAPI 规范（`openapi.yaml`）和数据模型，前后端通过契约对齐
- **示例 API**: KV 增删改查（`kv-controller.ts`）
- **测试**: Mocha + Chai

---

## 四项目架构对比

| 维度 | 旧前端 (depositmisview) | 旧后端 (lqp) | 新前端模板 (mmpayproductpermissionhtml) | 新后端模板 (mmpayxdcproductpermissionweb) |
|---|---|---|---|---|
| **Vue 版本** | Vue 2.7 | — | Vue 3.4 | — |
| **Node 版本** | — | Node 12 (Egg), Node 10+ (Koa/Kite) | Node 18+ | Node 20 |
| **TS 版本** | 4.0 | 4.9 | 5.4 | 5.x |
| **构建工具** | Webpack 4 (Vue CLI 4) | tsc + Egg Scripts | Vite 5.2 | XDC Node SDK |
| **UI 框架** | Element UI 2.13 | — | TDesign Vue Next 1.9 | — |
| **CSS 方案** | Less | — | Tailwind CSS 4.1 + Less | — |
| **状态管理** | Vuex 3 + 装饰器 | — | Composition API (ref) | — |
| **路由** | Vue Router 3 (hash) 手动配置 | 装饰器自动扫描 | Vue Router 4, src/index.ts 导出 | Controller 注册 |
| **HTTP 框架** | — | Egg.js 2 / Koa 2 / Kite | — | XDC Node SDK |
| **API 调用** | Axios (BaseAPI 封装) | — | xpage-web-sdk request | — |
| **RPC 通信** | — | Protobuf + XDC Svrkit (30+ 实例) | — | OpenAPI 契约 |
| **构建产物** | 完整 SPA (build/) | Docker 镜像 + PM2 | UMD 库 (dist/script.umd.js) | Docker 镜像 |
| **部署平台** | 独立 OA 站点 | XDC 私有容器 | XPage 低代码平台 | XDC 平台 |
| **代码规模** | 442 文件 (220ts+153vue) | 主服务 547 文件 (291ts) | ~100 文件 | ~52 文件 |

## 迁移关系

```
旧前端 (depositmisview, Vue2+ElementUI+Webpack)
  ──迁移→ 新前端模板 (mmpayproductpermissionhtml, Vue3+TDesign+Vite+XPage)

旧后端 (lqp/mmpayxdcdepositlqpmis, Egg.js)
  ──迁移→ 新后端模板 (mmpayxdcproductpermissionweb, XDC Node SDK)
```

核心变化：
1. 前端从**完整 SPA** 变为 **XPage 平台 UMD 模块**（布局由平台管理）
2. 后端从 **Egg.js** 迁移到 **XDC Node SDK**（更轻量的 Controller 模式）
3. 前后端通过 **OpenAPI 契约**对齐（替代旧的 Protobuf 类型共享）
4. UI 从 Element UI 升级为 TDesign
5. 状态管理从 Vuex 装饰器风格转为 Composition API
6. 构建从 Webpack 升级为 Vite

### 前后端关系
- 前端通过 `@tencent/xpage-web-sdk` 的 `request` 调用后端 API
- 后端通过 OpenAPI 契约定义接口规范
- 统一错误处理：`code !== 0` 为失败
