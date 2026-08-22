# Yupitek Wiki

Yupitek 產品技術支援文件站。涵蓋 5 大品牌：**ALFA Network**、**Hak5**、**Flipper Zero**、**SDRLAB**、**ACS**。

由單一 monorepo 以 Docusaurus 建置，部署至三個獨立子網域（依 AD 多網域 i18n 架構）：

| 語系 | 網域 | Source of truth |
|------|------|-----------------|
| English | https://doc.yupitek.com | `docs/` |
| 简体中文 | https://doczhcn.yupitek.com | `i18n/zh-CN/` |
| 繁體中文 | https://doczhtw.yupitek.com | `i18n/zh-TW/` |

## 技術棧

- **Docusaurus 3.10.x**（classic preset，純 `.md`，不用 `.mdx`）
- **Mermaid**（`@docusaurus/theme-mermaid`，文件內流程圖）
- **搜尋**：`@easyops-cn/docusaurus-search-local`（language: `["en","zh"]`）
- **CJK 排版**：`remark-cjk-friendly`
- **Node 22**（`.nvmrc`）+ `package-lock.json`（commit 鎖版本）

## 開發

```bash
nvm use        # Node 22
npm install    # 安裝依賴
npm run start  # 本機開發（en，預設 locale）
npm run build  # 生產建置（預設 en）
```

### 建置指定語系

```bash
npm run build:en     # 英文 → doc.yupitek.com
npm run build:zh-cn  # 簡中 → doczhcn.yupitek.com
npm run build:zh-tw  # 繁中 → doczhtw.yupitek.com
```

## 目錄結構

```
.
├── docs/                  # 英文 source of truth（核心內容）
│   ├── 00-getting-started/
│   ├── 01-alfa-network/
│   ├── 02-hak5/
│   ├── 03-flipper-zero/
│   ├── 04-sdrlab/
│   ├── 05-acs/
│   └── 99-admin/
├── i18n/
│   ├── zh-CN/             # 簡中 mirror（對應飛書知識庫）
│   └── zh-TW/             # 繁中 mirror
├── src/                   # React 元件 / CSS
├── static/                # 靜態資產（圖片、圖解 SVG）
├── scripts/               # 同步腳本（飛書 / cnb.cool）
└── .github/workflows/     # 3 個 Cloudflare Pages 部署
```

## 部署

三個 Cloudflare Pages 專案，各由 GitHub Actions 觸發：

- `deploy-en.yml` → `yupitek-wiki-en` 專案 → doc.yupitek.com
- `deploy-zh-cn.yml` → `yupitek-wiki-zh-cn` 專案 → doczhcn.yupitek.com
- `deploy-zh-tw.yml` → `yupitek-wiki-zh-tw` 專案 → doczhtw.yupitek.com

需要 secrets：`CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`。

## 中國鏡像

### 飛書知識庫

簡體版（`i18n/zh-CN`）文章對應飛書知識庫架構，分組對照表見 [`scripts/feishu-node-mapping.md`](scripts/feishu-node-mapping.md)。同步腳本與 CI 設定：

- `scripts/feishu-sync.py` — 依 manifest 批次建立飛書知識庫節點（參數化帳號 / space）
- `.github/workflows/sync-feishu.yml` — 手動觸發（`workflow_dispatch`）的同步 CI

### cnb.cool 完整 mirror

- **用途**：提供中國境內可直連的完整 repo 鏡像，作為飛書知識庫之外的原始碼備援通道。鏡像含三語系 markdown 源碼（`docs/`、`i18n/zh-CN/`、`i18n/zh-TW/`）、圖解資產（`static/img/`）與全部建置設定。
- **同步方式**：`scripts/cnb-mirror.sh`（`git push --mirror` 至參數化 remote），可手動執行或由 CI 排程。
- **如何瀏覽**：於 cnb.cool 專案頁直接閱讀 markdown；英文源在 `docs/`，簡中對應飛書版在 `i18n/zh-CN/docusaurus-plugin-content-docs/current/`，繁中在 `i18n/zh-TW/docusaurus-plugin-content-docs/current/`。
- **如何下載**：
  - 單篇：頁面 Raw 按鈕取得原始 `.md`
  - 整包：Clone（`git clone <cnb.cool remote>`）或 Download ZIP
- **注意**：mirror 為唯讀備援，開發一律以 GitHub 為 source of truth；飛書上傳僅取用 `i18n/zh-CN` 內容（不含 Docusaurus 設定檔）。
