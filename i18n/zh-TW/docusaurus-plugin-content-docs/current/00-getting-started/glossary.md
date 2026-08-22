---
slug: glossary
id: getting-started-glossary
title: 詞彙表
sidebar_position: 5
description: 以淺白語言說明 Yupitek Wiki 中所使用的技術詞彙。
---

# 詞彙表

本 Wiki 中會遇到的詞彙，以淺白語言說明。品牌與型號名稱一律保留英文。

| 詞彙 | 定義 |
|------|------------|
| **Adapter（無線網卡）** | 插入電腦以提供無線連線能力的 USB Wi-Fi 網卡。 |
| **Access Point（AP，存取點）** | 讓無線用戶端連線到網路的裝置。啟用 AP 模式可將無線網卡變成熱點。 |
| **Monitor mode（監聽模式）** | 無需連線到網路即可擷取原始 802.11 訊框的無線模式 — 這是 Wi-Fi 稽核的基礎。 |
| **Packet injection（封包注入）** | 在空中傳送自訂無線訊框，用於攻擊與測試。 |
| **Driver（驅動程式）** | 讓作業系統與硬體溝通的核心軟體。內建核心（in-kernel）驅動程式已內建於 Linux；樹外（out-of-tree）驅動程式則需另行安裝。 |
| **DKMS** | Linux 框架，當核心更新時會自動重建樹外核心模組。 |
| **Firmware（韌體）** | 儲存在裝置本身的低階軟體。 |
| **Firmware update（韌體更新）** | 更換裝置上的韌體以新增功能或修正錯誤。 |
| **Troubleshooting（疑難排解）** | 診斷並解決問題的過程。 |
| **Compatibility matrix（相容性矩陣）** | 顯示哪些無線網卡可搭配哪些作業系統、晶片組與驅動程式的表格。 |
| **Getting started / Quick start（快速入門）** | 引導您完成首次設定的簡短指南。 |
| **Antenna gain（天線增益）** | 以 dBi 為單位，衡量天線在特定方向上集中 RF 能量的程度。 |
| **Sub-GHz** | 低於 1 GHz 的無線電頻率（例如 433 MHz），Flipper Zero 使用此頻段。 |
| **Software-defined radio（SDR，軟體定義無線電）** | 部分以軟體實作的無線電，讓單一裝置可以接收與傳送多種頻率。 |
| **NFC / RFID** | 非接觸式卡片技術（13.56 MHz NFC 與 125 kHz RFID），用於讀卡機與 Flipper Zero。 |
| **PC/SC** | 在電腦上存取智慧卡讀卡機的標準軟體框架。 |

## 本 Wiki 使用的慣例

- **品牌與型號名稱**（例如 `AWUS036ACM`、`WiFi Pineapple`）一律不翻譯。
- 英文技術詞彙首次出現時，會以行內方式說明。
- 本 Wiki 的路徑使用 `/alfa-network/` 這種形式 — 完整清單請參閱 [產品登錄](/admin/product-registry/)。

如果缺少某個詞彙，或某個定義不清楚，請透過 [審查佇列](/admin/review-queue/) 回報。