# 平台与框架知识

> 从 MEMORY.md 拆分 | 最后更新: 2026-04-03

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
```

### ⚠️ 关键目录约定
- **controller 必须由契约生成结构**（函数签名由工具生成），开发者只填业务逻辑
- **controller/entity/middleware/util/config 自动加载**，controller 必须有，其余可选
- **没有 service 目录**：轻量逻辑用 entity，复杂逻辑按微服务拆成独立服务
- **Entity 按分层对应不同对象**：应用层=AO，领域层=DO，领域DAO=PO

### 自动加载机制
- `src/` 下 `util|entity|controller|middleware|config` 一级目录和二级 `index.ts` 自动加载
- 装饰器直接使用（`@conf`, `@entity` 等），controller 无需 import

### 统一配置 `xdc.yml`
- 替代了 `.image.json`, `package.json`, `pb.config.js` 的合并配置
- 环境差异：`xdc.dev.yml` / `xdc.test.yml` 自动合并覆盖
- 支持 `${ENV_KEY}` 语法读取环境变量

### 动态配置（七彩石 Rainbow）
- 配置在 `infra.dynamicConf` 下
- 默认 120s 更新一次
- ⚠️ 单例模式下动态配置更新需特殊处理

### 依赖注入（DI）
- **属性注入**：`@entity('XxxEntity')`, `@conf` 等，在构造函数**之后**执行
- **构造参数注入**：`constructor(@conf private svrConf: ServerConfig)` — 构造函数内可用
- 默认**单例**，声明 `@entityProvider('Name', false)` 为非单例

### 服务调用
- `xdc.yml` 的 `infra.deps.modules` 配置依赖模块
- `npm run gen-client` 生成客户端调用代码

### 异常处理
- 业务异常推荐：`throw new BizError(errCode)` 或 `throw new BizError({ errCode, errMsg })`
- 未 catch → `500`，框架异常 → `422`，参数校验失败 → `400`

---

## 契约管理：插件 + MCP 闭环工作流

> 来源: [iwiki p/4016369074](https://iwiki.woa.com/p/4016369074) | 更新: 2026-04-03

### 契约插件工作流
```
拉取远端契约(.tmp/) → AI 编辑 → 规范校验 → 提交契约 → 创建 MR → 流水线自动 build
```

### xcontract MCP 工具能力

| 工具 | 能力 | 闭环中的角色 |
|------|------|------------|
| `getInterfaceList` | 查询模块已有接口列表 | 查现有接口 |
| `getInterfaceDetail` | 获取单个接口契约详情 | 查详情 |
| `queryInterfaceContractByDesc` | 自然语言语义搜索接口 | 智能查找 |
| `validateProtoContent` | 校验 proto 合法性 | 本地校验 |
| `createContractMr` | 创建契约 MR | 提交变更 |

### ⚠️ 当前缺口
- MCP 无"拉取契约文件到本地"能力 → 首次需插件或手动 git
- `validateProtoContent` 仅支持 proto → yaml(OpenAPI) 校验需本地工具

---

## 环境配置
- Node 要求 >= 18.18.0，当前环境默认 Node 12，每次 npm install 前必须: `export NVM_DIR="/opt/nvm" && . "$NVM_DIR/nvm.sh" && nvm use 20`
- XPage 服务器重启: `cd /data/workspace/queryopenorderlist && curl -s http://wxpay.woa.com/xdc/wxpaymenuconfig/restart.sh | bash -s pro`
- Vite 本地开发: `cd mmpayqueryopenorderlisthtml && npm run start`（端口 9001）
