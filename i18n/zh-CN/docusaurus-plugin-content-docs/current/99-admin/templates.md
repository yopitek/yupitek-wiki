---
slug: templates
id: admin-templates
title: 模板
sidebar_position: 4
description: 编写与翻译 wiki 内容时推荐的页面模板，与文章方案一致。
---

# 模板

这些模板描述了每种页面类型的推荐结构。它们在项目的 `article_scheme.md` 中有完整定义，此处为快速参考摘要。

## Frontmatter

每个页面都以 YAML frontmatter 开头：

```yaml
---
id: <unique-id>
title: <Page Title>
sidebar_position: <number>
description: <one-line summary shown in search and listings>
---
```

## 页面类型模板

### 产品页面（`products/{model}/index.md`）

用于任何单个产品。

1. 一句话定位陈述（「这是什么，面向谁」）。
2. **规格**表。
3. **概述**段落。
4. **驱动 / 固件安装**（步骤较复杂时添加 Mermaid 流程图）。
5. **进阶用法**。
6. **兼容性**表。
7. **故障排查**。
8. 相关资源链接（绝对路径）。

### 设置 / 指南页面

1. 学习目标。
2. 概念讲解。
3. 前置条件检查清单。
4. 逐步的 `Step 1..N` 区块，每个区块包含一条 ```bash 命令及其**预期输出**。
5. 验证步骤。
6. 常见错误表。
7. 参考资料。

### 对比页面

1. 先给结论。
2. 快速对比表。
3. 深入分析。
4. 基于场景的推荐。
5. 测试数据（如有）。

### 故障排查页面

1. **诊断优先的决策树**（Mermaid 流程图）。
2. 问题索引表。
3. 针对每个问题：症状 / 诊断 / 根本原因 / 修复。
4. 「仍然卡住？」→ 审核队列。

## 图表规则

- 内联流程/时序图：**Mermaid**。
- 主视觉 / 重点图表：独立 SVG，存放在 `static/img/{article-id}/` 下。

## DoD（完成定义）

- Frontmatter 存在且 `id` 唯一。
- 结构与对应的模板一致。
- 设置/指南/故障排查页面至少包含一个图表。
- 每条 ```bash 命令均已实际测试；包含预期输出。
- 内部链接使用绝对路由路径（无 `../`）。
- 无 `TODO` / `TBD` 占位符。
- `npm run build:en` 通过且零失效链接。

## 相关

- [`审核队列`](/admin/review-queue/) — 新内容发布前的检查地点。
- [`变更日志`](/admin/change-log/) — 记录何时发生了什么更改。