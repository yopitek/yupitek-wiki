# 飛書知識庫分組對照表（Feishu Wiki ↔ yupitek-wiki repo）

> 用途：workbuddy / feishu_batch_import.py 批次上傳時，將 `i18n/zh-CN/docusaurus-plugin-content-docs/current/` 下的文件歸位到飛書知識空間的正確節點。
>
> - 知識空間：**Yupitek 榆閤科技｜產品知識庫**（`SPACE_ID` 見 `feishu_batch_import.py` / `.env`）
> - 架構原則：第一層＝品牌，第二層＝文件類型（比照 docs.alfa.com.tw 心智模型，詳見 Obsidian `yupitek_wiki/Feisu_doc_files/feisu_scheme.md`）
> - `node_token` 欄位：先用 `list_wiki_nodes.py` 列出實際節點樹後回填；上傳前不得為空。
> - 對照基準：zh-CN 版本（飛書知識庫以中文為主，en/zh-TW 全量內容以官網為準）。

## 第一層：品牌節點 ↔ repo 目錄

| 飛書節點 | repo 路徑（相對 `i18n/zh-CN/docusaurus-plugin-content-docs/current/`） | 檔案數 | node_token（待回填） |
|---|---|---|---|
| 📌 使用指南 | `index.md`、`00-getting-started/intro.md`、`00-getting-started/support-policy.md` | 3 | _待填_ |
| 📁 ALFA Network | `01-alfa-network/**` | 32 | _待填_ |
| 📁 HAK5 | `02-hak5/**` | 22 | _待填_ |
| 📁 Flipper Zero | `03-flipper-zero/**` | 10 | _待填_ |
| 📁 SDRLab | `04-sdrlab/**` | 13 | _待填_ |
| 📁 ACS 智慧卡讀卡機 | `05-acs/**` | 4 | _待填_ |
| 📁 名詞索引／技術詞彙表 | `00-getting-started/glossary.md` | 1 | _待填_ |
| 📁 常見問題 FAQ（總覽） | `00-getting-started/faq.md` | 1 | _待填_ |
| 📁 公告與版本紀錄 | `99-admin/change-log.md` | 1 | _待填_ |
| 🔒 內部管理（不上傳） | `99-admin/driver-registry.md`、`99-admin/product-registry.md`、`99-admin/review-queue.md`、`99-admin/templates.md`、`99-admin/translation-glossary.md` | 5 | — |

合計：92 檔（86 可上傳 + 5 內部管理 + 1 change-log）。

## 第二層：文件類型子節點規則（各品牌通用）

| 文件類型節點 | 歸位規則（檔名模式） | 範例 |
|---|---|---|
| 技術文件 | `wifi-adapter-comparison.md`、`linux-compatibility-matrix.md`、`hardware/**`、`expansion/**`、`firmware*.md`、`sdr-software.md`、`mobile-app.md`、`official-resources.md` | ALFA Wi-Fi Adapter Comparison、SDR 軟體指南 |
| 使用手冊 | `products/*/index.md` | AWUS036AX 產品頁 |
| 快速安裝指南（QSG） | `quickstart*.md`、`linux-setup-*.md` | HAK5 quickstart、ALFA linux-setup-ubuntu |
| 驅動與下載 | `drivers/**`、`driver-registry`（內部除外） | MT7921AUN 驅動頁 |
| FAQ／疑難排解 | `faq.md`、`troubleshooting*.md` | ALFA troubleshooting |

### 各品牌明細

#### ALFA Network（32 檔）
- 品牌首頁：`01-alfa-network/index.md`
- 技術文件：`wifi-adapter-comparison.md`、`linux-compatibility-matrix.md`、`hardware/jetson/index.md`、`hardware/raspberry-pi/index.md`、`hardware/unitree/index.md`
- QSG：`linux-setup-ubuntu.md`、`linux-setup-kali.md`、`linux-setup-nethunter.md`
- FAQ／疑難排解：`troubleshooting.md`
- 驅動與下載：`drivers/index.md` ＋ `drivers/{mt7610u,mt7612u,mt7921aun,rtl8811au,rtl8812au,rtl8821cu,rtl8832bu}/index.md`（8 檔）
- 使用手冊：`products/*/index.md`（14 檔：apa-m04、apa-m25、apa-m25-6e、ars-25-57a、ars-nt5b7、awus036ach、awus036achm、awus036acm、awus036acs、awus036ax、awus036axer、awus036axm、awus036axml、awus036eacs）

#### HAK5（22 檔）
- 品牌首頁：`02-hak5/index.md`
- 技術文件：`firmware-downloads.md`
- QSG：`quickstart.md`
- FAQ／疑難排解：`faq.md`、`troubleshooting-index.md`
- 使用手冊：`products/*/index.md`（17 檔：bash-bunny-mark-ii、key-croc、malicious-cable-detector、omg-adapter、omg-cable、omg-plug、omg-programmer、omg-unblocker、packet-squirrel-mark-ii、plunder-bug-lan-tap、screen-crab、shark-jack、shark-jack-cable、usb-rubber-ducky、wifi-pineapple-enterprise、wifi-pineapple-mark-vii、wifi-pineapple-pager）

#### Flipper Zero（10 檔）
- 品牌首頁：`03-flipper-zero/index.md`
- 技術文件：`firmware-qflipper.md`、`mobile-app.md`、`official-resources.md`
- QSG：`quickstart.md`
- FAQ／疑難排解：`troubleshooting.md`
- 使用手冊：`products/*/index.md`（4 檔：flipper-zero、silicone-case、video-game-module、wifi-devboard）

#### SDRLab（13 檔）
- 品牌首頁：`04-sdrlab/index.md`
- 技術文件：`firmware.md`、`sdr-software.md`、`hardware/{h4m,rtl-sdr-v4,trx-duo}/index.md`、`expansion/{5g-board,ethernet-test-module,nrf24,wifi-multiboard}/index.md`、`shared/alfa-linux-guide.md`
- QSG：`quickstart.md`
- FAQ／疑難排解：`troubleshooting.md`

#### ACS 智慧卡讀卡機（4 檔）
- 品牌首頁：`05-acs/index.md`
- 使用手冊：`products/{acr122u,acr1252u,acr1552u}/index.md`

## 上傳注意事項

1. **圖片路徑**：md 內 `/img/...` 引用需改為飛書雲端圖片（API 上傳後替換），SVG 圖檔不直接上傳，先轉 PNG（≤2MB）再插入。
2. **Mermaid 區塊**：飛書 docx 不支援 mermaid 原始碼，上傳前轉為圖片（PNG/SVG→PNG）或刪除改用文字步驟。
3. **Sierra Wireless**：目前 repo 無此品牌目錄；未來新增時須置頂免責聲明文件（見 feisu_scheme.md §2.4）。
4. **frontmatter**：Docusaurus frontmatter（sidebar_position 等）上傳前剝離，標題取 `title` 欄位，命名格式「品牌 型號｜主題」。
5. **捷徑（Shortcut）**：跨品牌共用文件（如 `04-sdrlab/shared/alfa-linux-guide.md` 同時關聯 ALFA）用 Shortcut 節點，不複製內容。
