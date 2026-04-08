---
name: archiving
description: 新需求的归档与沉淀阶段。当测试验证完成、需要提炼经验并更新 Rules 和 Memory 时自动触发。这是 Implement 流程的第 6 阶段。
allowed-tools: Read, Write, Edit
---

# 归档与沉淀阶段

你正在执行 Implement 流程的**第 6 阶段：归档与沉淀**。

## 前置条件

测试阶段已完成且人已验收。

## 执行步骤

1. 回顾本次需求的全部过程产物。
2. 按四分类整理沉淀内容：
   - **Pattern**：可复用的模式和做法（如"分页查询参数校验逻辑"）
   - **Pitfall**：踩过的坑和需避免的做法（如"下游 Svrkit 超时需降级"）
   - **Preference**：命名偏好、约定（如"查询接口统一用 GET /api/{resource-name}"）
   - **Architecture**：架构决策和技术选型（如"轻量逻辑放 entity/，不加 service 层"）
3. 该进 Rules 的更新 Rules，该进 Memory 的更新 Memory。
4. 检查是否有可复用的任务模式可以提炼为模板。

## 注意

- 只沉淀长期有效、可复用的经验。
- 临时讨论、一次性聊天不写入 Memory。
- 人必须确认沉淀内容的准确性，避免把特殊处理误记为通用规则。

## 完成

归档完成后，本次 Implement 流程结束。反馈闭环生效——本次沉淀的 Rules / Memory / 模板将在下一个需求中自动生效。
