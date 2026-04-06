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

## AI 辅助开发体系建设方案（2026-04-03 定稿）

> 正式方案文档：`.codebuddy/plans/ai-native-engineering-scheme.md`
>
> **一句话目标**：通过 Rules 沉淀项目知识 + 契约驱动自动生成代码骨架 + MCP 打通外部工作流，让 AI 在真实需求中能以"较少人工干预"完成前后端开发闭环。

### 核心思路

参考业界「开发机 + System Prompt + Skills」方案，去掉不必要的 Web 平台层，直接利用 CodeBuddy IDE 原生能力（Rules / Skills / Plan / MCP）建立 AI 辅助开发体系。核心价值在于**知识沉淀**——让 AI 理解项目架构、开发工作流、UI 规范和契约管理。

### 设计原则

在实践中逐步沉淀的原则，指导 AI 辅助开发的决策和流程设计。

1. **契约驱动，接口定义先行（Contract-First）**
   - 后端开发的第一步不是写代码，是定义契约（proto/yaml）
   - 契约是前后端的唯一真相源：AI 先查现有接口 → 草拟/修改契约 → 校验 → 提交 MR → 合并后自动生成代码骨架 → 最后才填充业务逻辑
   - 好处：接口定义结构化、可校验、可自动生成代码，AI 最擅长处理这类有明确规范的任务

2. **代码第一性，Rules 只补盲区**
   - 能通过代码和 MCP 实时获取的信息不写进 Rules（避免过期）
   - Rules 只写"代码看不出来的东西"：平台约束、路由禁忌、框架潜规则、历史坑点
   - 流程逻辑通过 xcontract MCP 实时读取，保证代码第一准确性

3. **反馈闭环，做完即提炼**
   - 每次需求做完后，更新 Rules 中不准确或遗漏的部分
   - AI 犯的错写进 `pitfalls.md`，确保不再犯同样的错

### 能力映射

| 业界做法 | CodeBuddy 对应方案 |
|---------|-------------------|
| System Prompt（项目架构、技术栈、目录结构） | **Rules**（`.codebuddy/rules/`） |
| System Prompt（全栈开发工作流、判断逻辑） | **Rules 中的开发流程规范** |
| ui-guide skill（布局模式、组件选择、样式约束） | **UI Guide Rule/Skill** 适配 TDesign |
| proto-inspector skill（查询+对比接口） | **MCP 工具**（xcontract 已有现成的） |
| feature-planner skill（需求→方案模板） | **Plan 模板 + 标准化方案流程** |

### 执行路线图（四步，边做边验证）

```
第一步：选一个真实小需求 + 同步建立核心 Rules
  ↓
第二步：补 UI Guide（TDesign 组件规范 + 布局模式）
  ↓
第三步：再来一个需求，验证闭环
  ↓
第四步：迭代优化 + 批量复用
```

> **关键调整**：原来"先写 Rules → 再验证"改为"边写 Rules 边用真实需求验证"。
> 没有具体范例参照，Rules 容易停留在"正确但无用的废话"。

### 每步产物清单

#### 第一步：核心 Rules + 黄金路径

| 产物 | 说明 |
|------|------|
| `rules/project-architecture.md` | 技术栈版本、目录结构约定、四项目关系、路由定义方式 |
| `rules/frontend-workflow.md` | 前端新页面开发步骤：Page → Model → Service，路由注册 |
| `rules/backend-workflow.md` | 后端新接口开发步骤：Controller → 契约，中间件配置 |
| `rules/migration-guide.md` | 旧页面迁移改造步骤（Vue2→Vue3、Element→TDesign、Vuex→Composition API） |
| `rules/pitfalls.md` | 常见坑与禁忌（Node 版本切换、XPage 路由刷新问题等） |
| **黄金路径示例** | 一个从需求到前后端闭环的完整范例（选真实小需求） |

#### 第二步：UI Guide

| 产物 | 说明 |
|------|------|
| `rules/ui-guide.md` 或 Skill | TDesign 组件选择指南、布局模式（表单页/列表页/详情页）、Tailwind CSS 用法 |

#### 第三步：验证闭环

| 产物 | 说明 |
|------|------|
| 第二个真实需求的实现 | 验证 Rules 是否足够让 AI 较少干预下完成开发 |
| Rules 修订记录 | 根据实战反馈修正 Rules 中不准确或遗漏的部分 |

#### 第四步：迭代 + 复用

| 产物 | 说明 |
|------|------|
| 优化后的 Rules 体系 | 经过多轮验证的稳定版本 |
| 迁移实践 | 开始将旧业务模块逐步迁移到新架构 |

### 边界说明（先不做的事）

- **不先覆盖历史全部业务迁移** — 先跑通新页面开发闭环
- **不先做复杂审批流** — 审批/FSM 等复杂业务逻辑后续再说
- **不先把 Skill 做得很重** — Rules 够用就不做 Skill，保持轻量
- **不搞量化验收指标** — 验收标准就一条：拿真实需求，AI 能否在较少人工干预下跑通前后端闭环

### 验收标准

**一句话**：拿一个真实新需求，AI 能否在较少人工干预下，完成从"需求描述 → 前端 Page/Model/Service + 后端 Controller/契约 → 页面可运行"的闭环。能就过，不能就迭代 Rules。

### Handoff 背景知识清单

> 给其他 AI / 同事评估本方案时，至少需要提供以下 5 类背景：

1. **项目结构背景**：四个项目分别干什么（旧前端 depositmisview、旧后端 lqp、新前端模板 queryopenorderlist、新后端模板 xdc_wxpay），哪个是旧、哪个是新，迁移方向是什么
2. **架构差异背景**：旧前端 `Vue2 + Element + Webpack` → 新前端 `Vue3 + TDesign + Vite + XPage`；旧后端 `Egg/Koa + Protobuf RPC` → 新后端 `XDC Node SDK + OpenAPI`
3. **开发约束背景**：`src/index.ts` 是新前端路由真相源、XPage 提供壳（布局由平台管理）、前后端通过 OpenAPI 契约对齐、`code !== 0` 视为失败
4. **目标背景**：不是做通用 AI 产品，是做面向**当前项目迁移/新增需求**的 AI 辅助开发体系
5. **黄金路径范例**：一个从需求到前后端闭环的具体示例（第一步中产出）

### Harness Engineering 思想参考

> 来源: OpenAI 博文 + OpenHarness 仓库 (github.com/HKUDS/OpenHarness) | 更新: 2026-04-03

#### 核心概念

Harness Engineering 是 2025-2026 年兴起的 AI 工程新范式。核心范式转移：工程师从"写代码"转向"设计让 AI 可靠运行的环境"。**Harness = 约束(Constraints) + 反馈(Feedback) + 控制系统(Control Systems)**——模型提供智能，Harness 提供手、眼、记忆和安全边界。OpenAI 内部实验：7 人团队用 Codex 从空仓库生成 100 万行代码、合并 1500 个 PR，约 10 倍效率提升。

#### OpenHarness 子系统概览（11733 行 Python，44 倍轻于 Claude Code）

| 子系统 | 核心作用 |
|--------|---------|
| **Engine** | Agent 循环（stream → tool-call → loop），支持并发工具执行 |
| **Tools** | 43 个工具（文件/Shell/搜索/Web/MCP） |
| **Skills** | 按需技能加载（.md 文件即 Prompt，三层栈：内置→用户→插件） |
| **Prompts** | System Prompt 分段组装管线（环境+技能+项目指令+记忆） |
| **Memory** | 持久化跨会话记忆（文件即数据库，项目隔离，查询感知注入） |
| **Permissions** | 三级权限模式（PLAN→DEFAULT→FULL_AUTO），路径/命令级过滤 |
| **Hooks** | Pre/Post 生命周期钩子，4 种执行器（命令/HTTP/LLM-Prompt/Agent） |
| **Config** | 四层配置优先级（CLI > 环境变量 > 配置文件 > 默认值） |
| **Coordinator** | 多 Agent 协调（团队注册 + 消息传递 + 角色分化） |
| **Plugins** | 扩展生态（命令/钩子/Agent，兼容 claude-code/plugins） |

#### 与我们现有体系的对比分析

| OpenHarness 设计 | 我们可以迁移/已有的 | 优先级 |
|------------------|-------------------|--------|
| CLAUDE.md 项目指令（向上遍历发现） | ≈ 我们的 `rules/` 目录（CodeBuddy 自动注入） | ✅ 已在规划中 |
| Prompt 分段组装管线 | CodeBuddy 原生支持（Rules 自动注入 system prompt） | ✅ 已具备 |
| 截断防护（每段有字符/行数上限） | Rules 写精简版，详情留 MEMORY.md 按需读取 | ✅ 验证了方向 |
| 技能按需加载（列表进 prompt，内容运行时注入） | 暂不需要（项目体量小，Rules 够用） | ⏸️ 后续可引入 |
| Hook 拦截链（PreToolUse → 权限 → 执行 → PostToolUse） | CodeBuddy 已支持原生 Hooks，兼容 Claude Code Hooks，支持 `PreToolUse`/`PostToolUse` 等 7 类事件、运行时拦截、参数改写、项目/用户级配置 | ✅ 已具备，可优先落地验证 |
| 查询感知记忆（根据用户输入搜索匹配记忆再注入） | MEMORY 手动读取，Rules 自动注入，策略已对 | ✅ 策略正确 |
| 渐进式信任（PLAN→DEFAULT→FULL_AUTO） | 使用姿势层面，初期多确认，验证后逐步放手 | ✅ 自然演进 |

#### 核心结论

我们当前建设的是一套面向业务项目的 **AI 原生研发闭环体系**。它借鉴了 `Harness Engineering` 关于约束、反馈与控制系统的思想，但正式定位不是构建一个通用 `Harness`，而是优先利用 `CodeBuddy` 原生能力，把这些思想映射到业务研发执行闭环中。当前更合理的路径仍是**优先用 CodeBuddy 原生能力落地和验证**，而不是过早引入额外框架。

#### 后续待办

- [ ] 评估是否需要引入 OpenHarness 或类似轻量 Agent 框架来增强自动化能力（重点看原生 Hooks 无法覆盖的复杂场景，如多阶段治理链路、Agent 审查器、插件生态）
- [x] 建立 CodeBuddy 原生能力最小可用原型（项目 Rules + SessionStart / PreToolUse Hooks + handoff / memory 模板）
- [ ] 用真实需求验证该原型是否已足够满足现阶段需求，并据此继续收敛规则与治理链

### 状态

- [x] 方案制定 + GPT 评估 + 调整定稿（2026-04-03）
- [x] 补充平台/框架文档认知 + 契约 MCP 闭环分析 + 业界实践借鉴（2026-04-03）
- [x] Harness Engineering 概念学习 + OpenHarness 仓库分析 + 对比结论沉淀（2026-04-03）
- [x] 建立第一版 CodeBuddy 原生研发闭环骨架（2026-04-03）
  - [x] 创建项目 Rules：`workspace-architecture` / `xpage-frontend-guardrails` / `xdc-backend-contract-guardrails` / `delivery-workflow`
  - [x] 创建项目级 Hooks 配置：`.codebuddy/settings.json`
  - [x] 落地 Hooks 脚本：`.codebuddy/hooks/session_start_context.py` / `.codebuddy/hooks/pretool_guard.py`
  - [x] 创建临时上下文与交接模板：`.codebuddy/context/current-task.md` / `.codebuddy/templates/handoff-template.md` / `.codebuddy/templates/memory-capture-template.md`
- [ ] **第二步：用真实需求验证黄金路径**
  - [ ] 用一个真实前端或后端需求验证 Rules + Hooks 是否有效
  - [ ] 根据真实使用反馈精简 MEMORY.md，把稳定规则保留在 Rules，MEMORY 只保留索引与长期参考
  - [ ] 评估是否还需要更复杂的治理链（多阶段 Hook、Agent 审查器、插件生态）
- [ ] 第二步：UI Guide
- [ ] 第三步：第二个需求验证闭环
- [ ] 第四步：迭代优化 + 批量复用
- [x] 已检查本轮新增文件，无多余临时文件需要清理（未发现 `.pyc` / `.tmp` / `.bak`；`rules/`、`hooks/`、`context/`、`templates/`、`settings.json` 均为预期产物）

> **当前状态**：第一版 CodeBuddy 原生研发闭环骨架已完成，下一步是拿一个真实前端或后端需求验证 `Rules + Hooks + handoff/memory` 的黄金路径。

### 与优先级清单对照（2026-04-03）

#### 第一优先
- [x] **Hooks 最小原型**：已完成。已落地 `SessionStart` + `PreToolUse`，覆盖项目上下文注入、高危命令拦截、敏感路径保护。
- [x] **Rules 分层**：已完成第一版。已创建 4 条基础 Rules，但仍需在真实需求中继续收敛和精简。
- [~] **常用 SOP 渐进沉淀**：调整为“基于真实需求逐步形成”，而不是预先一次性补齐 `plan` / `review` / `debug` / `test` / `commit` 模板。当前暂不作为先做事项。

#### 第二优先
- [ ] **MEMORY.md 拆成索引 + 主题文件**：未完成。当前仍以单个 `MEMORY.md` 为主，后续需拆成索引页 + 主题文件。
- [x] **当前任务上下文文件化**：已完成。已创建 `.codebuddy/context/current-task.md`。
- [x] **统一 handoff 模板**：已完成。已创建 `.codebuddy/templates/handoff-template.md`。

#### 第三优先
- [~] **模式化工作流**：部分完成。`delivery-workflow` 已写入默认工作流原则，但还没有正式落成 `Review-only` / `Implement` / `Fast-fix` 三种可执行模式。
- [ ] **自动同步 issue/PR 摘要**：未完成。
- [ ] **工蜂 / Git 自动化交付链路**：未完成。后续可接入工蜂 / Git 能力，覆盖分支推送、MR 创建 / 更新、评审状态查询。
- [ ] **更强的多 agent 协作**：未完成。

#### 结论
- **已完成**：Hooks 最小原型、Rules 第一版分层、当前任务上下文化、统一 handoff 模板。
- **部分完成**：模式化工作流（只有原则，还没有正式模式）、常用 SOP 的沉淀方向已明确但暂不预制模板。
- **未完成**：MEMORY 拆分、issue/PR 自动摘要同步、工蜂 / Git 自动化交付链路、更强多 agent 协作。
