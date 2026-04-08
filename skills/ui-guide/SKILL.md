---
name: ui-guide
description: XPage + TDesign 前端 UI 开发指南。当需要新建前端页面、选择布局模板、复用公共组件时自动触发。
allowed-tools: Read, Grep, Glob
---

# XPage + TDesign UI 开发指南

为前端项目 `queryopenorderlist` 提供 UI 开发规范和正向模板参考。

## 1. XPage 低代码模板速查

XPage 平台提供 6 种低代码 UI 模板，新建页面时优先从这些模板出发：

| 模板类型 | 参考文件 | 布局特征 | 适用场景 |
|---------|---------|---------|---------|
| **API 调试型** | `src/pages/api.vue` | 左右分栏：左侧 schema-form + 右侧请求/响应 JSON 预览 | 接口调试、API 联调工具 |
| **Tab 表单型** | `src/pages/bind-merchant.vue` | t-tabs 切换多组表单 | 正反操作（绑定/解绑）、多场景切换 |
| **单卡片表单型** | `src/pages/form.vue` | 单个 t-card 内完整表单 + 校验规则 | 标准数据录入 |
| **多卡片表单型** | `src/pages/card-form.vue` | 多个 t-card 各含一组表单，底部统一提交 | 复杂数据录入（分组） |
| **分组编辑型** | `src/pages/form-group.vue` | 多个分组区块（绿色左边框标题），支持草稿/编辑/创建 | 商品管理、详情配置 |
| **步骤表单型** | `src/pages/step-form.vue` | t-steps 引导 + 分步表单 + 最终确认页 | 多步骤流程、开通/审批 |

> **注**：`src/pages/query-open-order.vue` 是手工编写的查询页面（非低代码模板），也可作为查询表格型参考。

## 2. XPage 标准代码模式

### 2.1 Model 单例模式（必须遵循）

```typescript
// 页面组件中
import XxxModel from '@/models/page-models/xxx-model';

const model = XxxModel.getInstance();
const { formDataRef, savingRef, ... } = model;

onUnmounted(() => {
  XxxModel.destroyInstance();
});
```

### 2.2 表单布局规范

| 属性 | 推荐值 |
|------|--------|
| 表单容器宽度 | `max-w-[650px]`（标准）或 `max-w-[800px]`（宽） |
| 标签宽度 | `labelWidth="100px"`（标准）或 `180px`（长标签） |
| 操作按钮位置 | `ml-[125px]`（与 label 右对齐）+ `t-space` |
| 卡片阴影 | `shadow="never"`（XPage 环境默认无阴影）或 `shadow-md` |
| 页面高度 | `h-[calc(100vh-60px)] overflow-auto` |

### 2.3 分组区块标题样式

```html
<h2 class="border-l-[4px] border-[#07c160] pl-4 h-[20px] leading-[20px] text-lg font-semibold text-[#07c160] mb-4">
  区块标题
</h2>
```

### 2.4 校验与提交标准写法

```typescript
const onSubmit = async () => {
  const validateResult = await formRef.value.validate();
  if (validateResult === true) {
    try {
      await model.submitForm(formDataRef.value);
      MessagePlugin.success('提交成功');
    } catch (error) {
      MessagePlugin.error('提交失败');
    }
  } else {
    const errors = Object.values(validateResult);
    const firstErrorDetails = errors[0] as Array<{ message: string }>;
    MessagePlugin.warning(firstErrorDetails[0]?.message || '表单校验失败');
  }
};
```

## 3. TDesign 组件速查

| 场景 | 组件 | 要点 |
|------|------|------|
| 表单 | `t-form` + `t-form-item` | 必须绑定 `:data` 和 `:rules` |
| 输入 | `t-input` / `t-textarea` / `t-input-number` | 金额用 `t-input-adornment` 加前缀 |
| 选择 | `t-select` + `t-option` | 支持 `filterable` `multiple` |
| 单选 | `t-radio-group` + `t-radio` | |
| 多选 | `t-checkbox-group` | 可用 `:options` 简写 |
| 日期 | `t-date-picker` | |
| 上传 | `t-upload` | `theme="image"` 用于图片上传 |
| 步骤 | `t-steps` + `t-step-item` | 配合 `v-show` 控制显隐 |
| 标签页 | `t-tabs` + `t-tab-panel` | |
| 描述列表 | `t-descriptions` + `t-descriptions-item` | 用于信息展示确认 |
| 卡片 | `t-card` | `shadow="never"` |
| 提示 | `t-alert` | `theme="info/warning/success"` |
| 颜色选择 | `t-color-picker` | |

## 4. 公共组件

查看 `{FE_ROOT}/src/components/` 目录了解项目已有的公共组件，优先复用。

## 5. 新建页面 Checklist

- [ ] 选择最匹配的低代码模板类型（上表 6 选 1）
- [ ] 在 `{FE_PAGES_DIR}` 下创建页面 `.vue` 文件
- [ ] 在 `{FE_MODELS_DIR}` 下创建对应的 Model 文件
- [ ] 在 `{FE_ROUTER_ENTRY}`（`src/index.ts`）中注册路由
- [ ] 使用 Model 单例模式 + `onUnmounted` 销毁
- [ ] 遵循 Pages↔Models↔Services 三层分离
