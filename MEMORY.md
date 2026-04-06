# 工作区长期记忆

> 最后更新: 2026-04-03

## 项目背景

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
     - 17 个业务域的 Controller（lqt/lqp/activityBanner/common/erlei-cards/mcp/msgSend/tools/xjg/rlj/zlj/yht/dataBoard/processMonitor/protocolManage/lqtNoticeManage/brandInfoTools）
     - 定时任务: 10 个 schedule（监控、过期处理等）
     - 权限: `@APIDescriptionDecorator` + `@AuthDecorator` 装饰器
     - 审批: PASS 系统 + 有限状态机（FSM）
  2. **`app/mmpayxdcwebankcardweb`**（银行卡 Web 服务）
     - 技术栈: Koa 2 + TypeScript 4 + 手动中间件组装（非 Egg）
     - 路由: 同样使用 `better-controller` 装饰器扫描
     - 中间件: extendLoader → cubeReporter → requestLog → errorHandler → csrf → responseFormater → sessionAuth → templateRender → exportKeyAuth
     - Protobuf RPC 通信
  3. **`app/mmpayxdclqp4kfbroker`**（客服 Broker 服务）
     - 技术栈: XDC Kite 框架 + TypeScript 4
     - 定位: 零钱加系统对客服的 broker
     - 描述: "零钱加系统对客服的broker"
- **公共层**: `domain/mmpayxdcdepositlqpmisdao`（DAO 微服务）

### 🟢 新模板一：queryopenorderlist（XPage 前端模板）
- **路径**: `/data/workspace/queryopenorderlist/mmpayqueryopenorderlisthtml/`
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

### 🟢 新模板二：xdc_wxpay（XDC Node 后端模板）
- **路径**: `/data/workspace/xdc_wxpay/`
- **定位**: XDC 平台 Node.js 后端服务模板（重构目标架构）
- **技术栈**: Node.js 20 + TypeScript + XDC Node SDK（`@xdc/node-sdk`）
- **架构**: Controller 模式，`src/entry.ts` 注册 Controller + 中间件
- **契约驱动**: `.xdc/contract/` 包含 OpenAPI 规范（`openapi.yaml`）和数据模型，前后端通过契约对齐
- **示例 API**: KV 增删改查（`kv-controller.ts`）
- **测试**: Mocha + Chai

---

## 四项目架构对比

| 维度 | 旧前端 (depositmisview) | 旧后端 (lqp) | 新前端模板 (queryopenorderlist) | 新后端模板 (xdc_wxpay) |
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
| **布局** | 自建 Layout (Header+Aside+Main) | — | XPage 平台提供壳 | — |
| **权限** | 前端 authKey + 路由 meta | @AuthDecorator + @APIDescriptionDecorator | XPage 平台管理 | XDC 中间件 |
| **代码规模** | 442 文件 (220ts+153vue) | 主服务 547 文件 (291ts) | ~100 文件 | ~52 文件 |

## 迁移关系

```
旧前端 (depositmisview, Vue2+ElementUI+Webpack)
  ──迁移→ 新前端模板 (queryopenorderlist, Vue3+TDesign+Vite+XPage)

旧后端 (lqp/mmpayxdcdepositlqpmis, Egg.js)
  ──迁移→ 新后端模板 (xdc_wxpay, XDC Node SDK)
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

---

## wxpay 运营系统平台（宿主平台）

> 来源: [iwiki p/4012548245](https://iwiki.woa.com/p/4012548245) | 更新: 2026-04-03

### 平台概况
- 面向微信支付系统的**业务运营门户**，用户为产品运营人员、审批者、业务架构师
- 正式环境: `https://wxpay.woa.com/xdc/wxpaysite#/`
- 测试环境: `https://wxpay-test.woa.com/xdc/wxpaysite#/`
- 内置能力（自动集成）：身份鉴权、审计、xmonitor、服务流水上报、本地开发调试、数据仪表盘、审批流、xpage 低代码编辑

### 开发全流程
1. **新增菜单**（菜单管理页面）→ 菜单英文名即为后续开发模块名
2. **新增菜单模版特性** → 审批通过后编辑菜单树（拖拽排列）
3. **创建开发模块** → 两种方式：从站点模板创建（首次）/ 绑定已有模块（多菜单共用）
4. **连接 AnyDev 云研发环境** → 选 `minimal_2025xxxx` 模板，clone 前后端代码到 `/data/workspace`
5. **代码编辑** → 低代码 XPage 编辑器 或 AnyDev 上直接源码开发
6. **体验测试** → 菜单模版编辑页面设白名单，测试环境预览
7. **发布** → XDC 模块发布流程 → 菜单模版提交审批 → 灰度 → 全量

### 前端 API（⚠️ 重要约束）

#### `window.wxpay.router` — 路由跳转必须用这个，禁止直接用 vue-router
- `.push({ path: '/xxx' })` — 本菜单内跳转（同 vue-router push）
- `.replace()` — 本菜单内替换（同 vue-router replace）
- `.go()` — 本菜单内前进后退（同 vue-router go）
- `.goto({ path: '/biz/xxx/yyy' })` — 跳转到其他菜单，需传完整 hash 路径
- `.open(url)` — 新窗口打开（同 window.open）
- `.currentRoute` — 当前路由参数，**非 Ref**

#### `window.wxpay.request` — API 请求
- API 同 axios，自动封装敏感权限（无权限时自动跳申请页）
- 非契约调用直接用此方法

#### `window.wxpay.util`
- `.hideSideMenu()` — 隐藏侧边栏（需要全屏的页面调用）
- `.collapseSideMenu()` — 折叠侧边栏

### 路由规则
- **单菜单 ↔ 单模块**：路由 path 以 `/` 开头，首页为 `/` 路由对应的页面
- **多菜单共用一个模块**：创建菜单正常写路由；其他菜单路由需加 `/菜单英文名/` 前缀

### 前端接口调用两种方式
1. **契约调用**：`xdc.yml` 配置依赖后端模块 → `npm run gen` 生成客户端代码 → 直接 import 调用
2. **非契约调用**：`window.wxpay.request`（axios 风格）

### 发布注意事项
- 提交菜单审批前，确保对应开发模块已发布到 XDC 正式环境
- 审批通过后先灰度再全量

---

## XDC Kite 框架详解（后端框架）

> 来源: [iwiki p/1595683571](https://iwiki.woa.com/p/1595683571) | 更新: 2026-04-03

### 契约开发流程（四步闭环）
1. **初始化选择契约框架** — XDC 研发平台新增模块时选择（koa/kite/wxpay 等框架模板）
2. **在契约平台编辑接口契约** — 支持 PB / 模板 / yaml 三种格式，定义请求/响应结构
3. **生成服务端和客户端代码** — `npm run gen`（调用 `kite gen all`），自动生成函数签名和客户端调用代码
4. **填充业务逻辑** — 服务端：`@operation('xxx')` 装饰器下只需写业务实现；客户端：`import module → module.api()` 一行调用

> 核心：**契约驱动 = 接口定义先行 → 工具自动生成代码骨架 → 开发者只关注业务逻辑**

### 架构设计（Clean Architecture 映射）

基于 The Clean Architecture（洋葱圈模型），架构到目录的映射：

| 整洁架构层 | XDC Kite 目录 | 说明 |
|-----------|-------------|------|
| Enterprise Business Rules (Entities) | `entity/` | 业务实体，聚焦业务规则 |
| Application Business Rules (Use Cases) | `controller/` | 业务流程控制器，串流程 + 用例实现 |
| Interface Adapters (Presenters/Gateways) | `middleware/` | 洋葱模式中间件，大部分由 XDC 主导 |
| Frameworks & Drivers | XDC 框架本身 | 外部接口、DB、Web 等 |

### 目录结构
```
.xdc/              # 工具生成代码目录（契约生成的客户端代码）
src/
├── config/         # 业务配置类型
├── controller/     # 控制器 ⚠️ 必须由契约生成结构（函数签名）
├── entity/         # 业务实体（按分层：AO/DO/PO）
├── middleware/      # 洋葱模式中间件
├── util/           # 工具方法，依赖注入
├── view/           # 视图直出（仅应用层有）
├── entry.ts        # 服务入口
test/               # 测试
.env                # 本地环境变量（不提交）
xdc.yml             # 统一配置
bin/script/         # 脚本、二进制（可选）
```

### ⚠️ 关键目录约定
- **controller 必须由契约生成结构**（函数签名由工具生成），开发者只填业务逻辑
- **controller/entity/middleware/util/config 自动加载**，controller 必须有，其余可选
- **没有 service 目录**：轻量逻辑用 entity，复杂逻辑按微服务拆成独立服务
- **Entity 按分层对应不同对象**：应用层=AO，领域层=DO，领域DAO=PO；一个服务理论上只有一类对象

### 自动加载机制
- `src/` 下 `util|entity|controller|middleware|config` 一级目录和二级 `index.ts` 自动加载
- 自动加载 glob: `src/@(util|entity|controller|middleware|config)/*.ts` 和 `src/@(util|entity|controller|middleware|config)/*/*.ts`
- 装饰器直接使用（`@conf`, `@entity` 等），controller 无需 import
- 自定义加载：直接 `import` 或配置 `frame.autoImportGlobPaths`

### 统一配置 `xdc.yml`
- 替代了 `.image.json`, `package.json`, `pb.config.js` 的合并配置
- 环境差异：`xdc.dev.yml` / `xdc.test.yml` 自动合并覆盖正式环境配置（lodash.mergeWith + 数组 concat）
- 可配 `infra.arrayConfMergeMode: replace` 切换为数组替换
- 支持 `${ENV_KEY}` 语法读取环境变量

### 动态配置（七彩石 Rainbow）
- 配置在 `infra.dynamicConf` 下
- 默认 120s 更新一次
- `serverConfKey`：与 `xdc.yml` 格式完全一致的远程配置，合并时七彩石优先
- `bizConfKeyTypeMap`：业务自定义配置 key，支持 string/number/json/yaml 类型
- ⚠️ 单例模式下动态配置更新需特殊处理（构造时只读一次的场景）

### 依赖注入（DI）
- **属性注入**：`@entity('XxxEntity')`, `@conf` 等，在构造函数**之后**执行
- **构造参数注入**：`constructor(@conf private svrConf: ServerConfig)` — 构造函数内可用
- 默认**单例**，声明 `@entityProvider('Name', false)` 为非单例
- 非单例实例可通过 `this.getEntity()` / `this.getUtil()` 获取

### 服务调用
- `xdc.yml` 的 `infra.deps.modules` 配置依赖模块（兼容 svrkit 和 XDC 契约模块）
- `npm run gen-client` 生成客户端调用代码
- 支持 `@branchName` 指定分支
- `infra.deps.protoTypes` 只生成类型不下发路由（结构依赖用）
- `infra.deps.dalsetRoles` 配置 dalset 角色

### 模块鉴权
- 在 `contract.svrAuthConf.svrAuth` 下配置 appid + secret
- 契约生成的代码自动带签名

### 异常处理
- 未 catch 业务异常 → `500 Internal Server Error`
- 框架内部异常 → `422 Unprocessable Entity`
- 契约参数校验失败 → `400 Bad Request`
- 业务异常推荐：`throw new BizError(errCode)` 或 `throw new BizError({ errCode, errMsg })`
- 自定义 HTTP 状态码：`res.setStatus(403)`

### 构建与部署
- 非 ts 文件需配置 `infra.build.copyFiles` 到 dist 目录
- 本地敏感信息放 `.env`（不提交），线上托管在 XDC 环境变量
- 敏感信息获取 API：`this.getSensitiveKey(key)`

### 静态托管
- `xdc.yml` 配置 `infra.static: {}` 即可开启
- 默认托管 `src/view` 到根路径
- 支持 `alias` 别名映射

### 单步调试
- VSCode 按 F5 直接调试
- 或 `package.json` scripts 加 `"debug": "cross-env RUN_ENV=dev kite dev -r '--inspect'"`

---

## 契约管理：插件 + MCP 闭环工作流

> 来源: [iwiki p/4016369074](https://iwiki.woa.com/p/4016369074) + xcontract MCP 工具分析 | 更新: 2026-04-03

### 契约插件工作流
```
拉取远端契约(.tmp/) → AI 编辑 → 规范校验 → 提交契约 → 创建 MR → 流水线自动 build
```
- 拉取的契约默认存到项目根目录 `.tmp/` 文件夹
- 智能识别仓库类型（OpenAPI / Proto），默认选中含模块名的文件
- 变更后的文件自动进入"待提交契约"目录
- 提交入口：编辑器顶部按钮 / 右键菜单 / 契约目录树
- MR 合并后流水线自动校验 proto 规范、生成 build 文件

### xcontract MCP 工具能力

| 工具 | 能力 | 闭环中的角色 |
|------|------|------------|
| `getInterfaceList` | 查询模块已有接口列表 | 查现有接口 |
| `getInterfaceDetail` | 获取单个接口契约详情（请求/响应结构） | 查详情 |
| `queryInterfaceContractByDesc` | 自然语言语义搜索接口 | 智能查找 |
| `getProtoInfo` | 查 proto 路径/模块/Git 信息 | 定位文件 |
| `validateProtoContent` | 校验 proto 合法性 | 本地校验 |
| `createContractMr` | 创建契约 MR（proto/yaml） | 提交变更 |
| `getLogicModule` | 获取逻辑模块信息 | 辅助 |
| `searchBaseComponent` | 语义搜索基础组件 | 辅助 |

### AI 辅助契约开发流程（本地闭环）

```
1. [一次性] 拉取契约文件 → 插件右键或 git clone → .tmp/ 目录
2. [AI] 查现有接口 → MCP getInterfaceList / getInterfaceDetail
3. [AI] 编写/修改契约文件 → 本地编辑 .tmp/ 下 proto/yaml
4. [AI] 校验契约 → MCP validateProtoContent（proto）
5. [AI] 提交+创建MR → MCP createContractMr
6. [自动] 流水线校验 + 生成 build 文件
7. [本地] npm run gen → 生成 controller 骨架 + 客户端调用代码
8. [AI] 在生成的骨架中填充业务逻辑
```

### ⚠️ 当前缺口
- MCP 无"拉取契约文件到本地"能力 → 首次需插件或手动 git
- `validateProtoContent` 仅支持 proto → yaml(OpenAPI) 校验需本地工具
- MR 合并是异步的 → Step 6→7 之间需等待

## 环境配置
- Node 要求 >= 18.18.0，当前环境默认 Node 12，每次 npm install 前必须: `export NVM_DIR="/opt/nvm" && . "$NVM_DIR/nvm.sh" && nvm use 20`
- XPage 服务器重启: `cd /data/workspace/queryopenorderlist && curl -s http://wxpay.woa.com/xdc/wxpaymenuconfig/restart.sh | bash -s pro`
- Vite 本地开发: `cd mmpayqueryopenorderlisthtml && npm run start`（端口 9001）

---

## AI 原生研发闭环体系方案（v0.2，2026-04-06 重构）

> 正式方案文档：`.codebuddy/plans/ai-native-engineering-scheme.md`
>
> **一句话目标**：通过 Rules + Hooks + Memory + MCP + 阶段化工作流，把 AI 从"代码补全工具"提升为"可治理的研发执行体"——每个阶段有固定输入、明确约束和标准交付物，过程可追溯、结果可验证、经验可沉淀。

### 全流程设计（5 个阶段）

```
需求与分析 → 方案设计 → 编码实现 → 测试与验证 → 归档与沉淀 → 反馈闭环（反哺下一轮）
```

| 阶段 | 人的角色 | AI 的角色 | 核心交付物 |
|------|---------|----------|-----------|
| 需求与分析 | **主导** | 辅助：结构化需求、提取规则 | `requirement-analysis.md` |
| 方案设计 | **主导** | 辅助：梳理现状、生成契约草案 | `contract-proposal.md` + `tasks.md` |
| 编码实现 | 辅助 | **主导**：按任务逐步生成代码 | 符合契约的前后端代码 |
| 测试与验证 | 辅助 | **主导**：生成用例、执行测试 | `test-cases.md` + lint/契约校验结果 |
| 归档与沉淀 | **主导** | 辅助：提炼规则和记忆更新 | Rules / Memory / 模板更新 |

### 核心设计原则

- **契约驱动**：接口定义先行，编码前锁定字段和行为
- **代码第一性**：能从代码和 MCP 获取的不重复堆进 Rules
- **反馈闭环**：每次需求做完即更新 Rules / Memory / 测试资产
- **原生能力先行**：优先用 CodeBuddy 原生能力，不过早引入框架

### 参考来源分层与筛选原则

后续吸收外部经验时，按三层看材料：
- **业务内实践层**：优先判断是否贴合真实业务研发场景
- **通用工程方法层**：借鉴 Skill 结构、验证门禁、流程表达方式
- **底层思想层**：统一认知坐标，不直接作为方案命名

筛选四问：解决什么真实问题？属于哪一层？适配当前路线吗？该沉淀到哪里？

### 体系支撑能力（已落地）

| 层 | 已落地产物 | 作用 |
|----|-----------|------|
| Rules | 4 条：workspace-architecture / xpage-frontend-guardrails / xdc-backend-contract-guardrails / delivery-workflow | 项目约束与开发规范 |
| Hooks | 2 个：session_start_context / pretool_guard | 上下文注入 + 运行时风险控制 |
| Memory | MEMORY.md + context/current-task.md + handoff 模板 + memory-capture 模板 | 长期知识 + 任务上下文 + 交接 |
| MCP | XContract（可用）/ 工蜂 Git（部分可用）/ iWiki（待接入） | 外部系统能力接入 |

### 实施路线与当前状态

- [x] **第一阶段：最小可用原型**（已完成 2026-04-03）— Rules 4 条 + Hooks 2 个 + 模板 3 个
- [x] **方案调研与外部实践对照**（已完成 2026-04-06）— Harness 思想 + KM/voucher 业务实践 + agent-skills 通用方法
- [ ] **第二阶段：真实需求验证**（下一步）— 选一个真实需求走完整全流程，验证阶段化交付物
- [ ] **第三阶段：持续沉淀** — 基于真实需求沉淀常用模板和轻量 SOP，Memory 拆分
- [ ] **第四阶段：扩展增强** — 工蜂 Git 自动化、iWiki MCP、多 Agent 协作

> **当前状态**：方案 v0.2 已完成全流程设计改写，下一步是拿一个真实需求验证全流程的 5 个阶段。

### Harness Engineering 思想参考

> 来源: OpenAI 博文 + OpenHarness 仓库 | 更新: 2026-04-03

`Harness Engineering` 是本方案的**底层思想参考**，不是正式命名。核心思想：模型提供智能，Harness 提供约束、反馈和控制系统。我们把这些思想映射到 `CodeBuddy` 原生能力（Rules = 约束、Hooks = 控制、Memory = 反馈）上，而不是复制一个通用 Harness 框架。
