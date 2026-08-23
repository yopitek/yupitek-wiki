---
draft: true
slug: templates
id: admin-templates
title: 範本
sidebar_position: 4
description: 撰寫與翻譯 wiki 內容的建議頁面範本，符合文章架構。
---

# 範本

這些範本描述每種頁面型別的建議結構。它們在專案的 `article_scheme.md` 中有完整定義，這裡摘要供快速參考。

## Frontmatter（前置資料）

每個頁面都以 YAML frontmatter 開頭：

```yaml
---
id: <unique-id>
title: <Page Title>
sidebar_position: <number>
description: <one-line summary shown in search and listings>
---
```

## 頁面型別範本

### 產品頁面（`products/{model}/index.md`）

用於任何單一產品。

1. 一句話定位陳述（「這是什麼、給誰用」）。
2. **規格**表格。
3. **總覽**段落。
4. **驅動程式／韌體安裝**（步驟不平凡時加上 Mermaid 流程圖）。
5. **進階用法**。
6. **相容性**表格。
7. **疑難排解**。
8. 相關資源連結（絕對路徑）。

### 設定／指南頁面

1. 學習目標。
2. 概念說明。
3. 前置需求核對清單。
4. 逐步的 `Step 1..N` 區塊，每個都附 ```bash 指令與其**預期輸出**。
5. 驗證步驟。
6. 常見錯誤表格。
7. 參考資料。

### 比較頁面

1. 結論優先。
2. 快速比較表格。
3. 深入分析。
4. 依情境的建議。
5. 測試資料（如果有的話）。

### 疑難排解頁面

1. **診斷優先的決策樹**（Mermaid 流程圖）。
2. 問題索引表格。
3. 每個問題：症狀／診斷／根本原因／修正。
4. 「還是卡住？」→ 審查佇列。

## 圖表規則

- 行內流程／序列圖：**Mermaid**。
- 主視覺／重點圖表：存放在 `static/img/{article-id}/` 下的獨立 SVG。

## DoD（完成定義）

- 有 frontmatter 且 `id` 唯一。
- 結構符合對應的範本。
- 設定／指南／疑難排解頁面至少有一張圖表。
- 每個 ```bash 指令都實際測試過；附上預期輸出。
- 內部連結使用絕對路由路徑（不用 `../`）。
- 沒有 `TODO` / `TBD` 佔位符。
- `npm run build:en` 透過且零壞連結。

## 相關

- `Review Queue` — 新內容上線前在此檢查。
- [`Change Log`](/admin/change-log/) — 記錄何時變更了什麼。