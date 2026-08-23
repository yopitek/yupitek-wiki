---
id: hak5-product-omg-programmer
title: O.MG Programmer
sidebar_position: 13
description: 所有 O.MG 裝置的通用程式設計器 — 啟用、升級韌體、從自我銷毀中復原，並製作鑑識備份。
tags: [hak5, omg, omg-programmer, firmware, setup, activation]
keywords: [O.MG Programmer, WebFlasher, 啟用 O.MG, 韌體升級, 鑑識備份, 自我銷毀復原]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-programmer
category: product
difficulty: intermediate
toc: true
---

# O.MG Programmer — 完整指南

> **一句話定位**：O.MG Programmer 是啟用與維護所有 O.MG 裝置（Cable、Plug、Adapter、UnBlocker）的唯一入口——一支程式設計器就能完成啟用、免費韌體升級、自我銷毀救援，以及鑑識備份。

每一臺 O.MG 裝置基於法律原因出廠時**停用**。在它能做任何事之前，必須先啟用 — 這就是 **O.MG Programmer** 的用途。它是一個小型 USB 轉接器，插在你的電腦與任何 O.MG 裝置之間，搭配一個瀏覽器為基礎的 **WebFlasher** 工具。一支 Programmer 服務*整個* O.MG 產品線，所以你永遠不需要為每臺裝置買硬體。

除了首次啟用，它還是你的管理工具：韌體升級、意外自我銷毀後的復原，以及在把裝置交給別人之前做鑑識備份。

> **為什麼要「停用」？** O.MG 植入晶片能力太強，法規要求它們以失效狀態出貨。Programmer 既是法律閘門，也是你日常的控制面板。

---

## 規格一覽

| 專案 | 規格 |
|---|---|
| 外型 | USB 轉接器（電腦 ↔ O.MG 裝置） |
| 相容性 | O.MG Cable、O.MG Plug、O.MG Adapter、O.MG UnBlocker |
| 介面 | USB-A 到你的電腦；承載所連線的 O.MG 裝置 |
| 控制工具 | WebSerial 瀏覽器中的 WebFlasher（Chrome / Edge）；Python flasher 替代方案 |
| 操作 | 啟用、韌體升級、自我銷毀復原、鑑識備份/傾印、批次安裝 |
| 官方檔案 | https://o.mg.lol/setup/ |

## 它能做什麼

| 操作 | 發生什麼 |
|---|---|
| **啟用** | 初始 3 步驟設定，讓休眠的 O.MG 裝置可以運作 |
| **韌體升級** | 免費更新；Elite 裝置無需新硬體即可獲得未來能力 |
| **自我銷毀復原** | 還原你遠端清除的裝置（例如意外觸發的地理圍欄） |
| **鑑識傾印/備份** | 拉取任何相容 O.MG 裝置記憶體的映像 |
| **批次安裝** | 一次刷寫多臺裝置，用於大量部署 |

---

## 啟用流程

```mermaid
%% name: hak5-product-omg-programmer-activation
flowchart TD
    A[Connect O.MG device to Programmer] --> B[Connect Programmer to a Chrome/Edge computer]
    B --> C[Open WebFlasher at o.mg.lol/setup]
    C --> D[Select your O.MG model]
    D --> E[Step 1: detect device (WebSerial prompt)]
    E --> F[Step 2: optionally forensic backup]
    F --> G[Step 3: flash firmware & activate]
    G --> H[Boot device — WebUI now available over WiFi]
```

### 步驟 1 — 實體設定
1. 把 O.MG 裝置插進 Programmer。
2. 把 Programmer 插進一臺執行 **Chrome 或 Edge** 的電腦（這些支援 WebSerial；Firefox/Safari 不支援）。
3. **在精靈要求之前，保持 O.MG 裝置未插上 Programmer。** Bootloader 偵測預期的是乾淨的連線。

### 步驟 2 — 開啟 WebFlasher
瀏覽到 **https://o.mg.lol/setup/** 並選擇你的裝置型號（Cable、Plug、Adapter 或 UnBlocker）。

### 步驟 3 — 依照精靈操作
- 瀏覽器會提示你**選擇序列埠** — 選擇 Programmer。
- （建議）先做可選的**鑑識備份** — 一個安全網。
- 開始刷寫。它會安裝最新韌體並啟用裝置。

預期結果：

```text
[+] Device detected
[+] Backup complete (optional)
[+] Firmware flashed successfully
[+] Device activated — connecting to WiFi...
```

### 步驟 4 — 驗證
連上 O.MG 裝置的 WiFi，開啟它的 WebUI，確認韌體版本。它現在可以運作了。

> **Python flasher 替代方案：** O.MG 韌體倉庫附帶一個 Python flasher，給沒有 WebSerial 瀏覽器的使用者。查 O.MG 韌體檔案。

---

## 進階

| 能力 | 怎麼做 |
|---|---|
| 自我銷毀復原 | 重新連線裝置 → WebFlasher → 重新刷寫以從清除中還原 |
| 鑑識取證 | 備份任何 O.MG 裝置；用傾印做惡意軟體/訓練分析 |
| 大量佈建 | 為紅隊實驗室或訓練班批次刷寫一整批 O.MG 裝置 |
| Beta 韌體存取 | Elite 擁有者安裝 Beta 韌體以取得即將推出的功能 |

> **你可能會問：** *「如果我只有一條 O.MG 線材，還需要 Programmer 嗎？」* 需要 — 它是啟用任何 O.MG 裝置唯一受支援的方式，而且一支 Programmer 涵蓋全部。它不是可選的。

---

## 疑難排解

| 症狀 | 原因 | 修正 |
|---|---|---|
| WebFlasher 顯示「No device found」 | 裝置沒接好，或瀏覽器錯誤 | 使用 Chrome/Edge；只在提示時連線裝置 |
| 瀏覽器選錯序列埠 | 多個 USB-序列裝置 | 斷開其他裝置；選擇精靈標示的序列埠 |
| 啟用卡在「detecting」 | 裝置不在 bootloader 模式 | 重新開機；在提示時乾淨地重新連線 |
| 裝置顯示舊版本 | 韌體步驟被跳過 | 重新執行 WebFlasher 並完成韌體步驟 |
| Python flasher 錯誤 | 驅動程式 / 許可權 | 以適當許可權執行；OS 注意事項見 O.MG 韌體檔案 |

---

## 相關資源

- [O.MG Cable](/hak5/products/omg-cable/) — 這支 Programmer 服務的旗艦植入裝置
- [O.MG Plug](/hak5/products/omg-plug/) / [O.MG Adapter](/hak5/products/omg-adapter/) / [O.MG UnBlocker](/hak5/products/omg-unblocker/)
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — 防禦對應工具
- [韌體與下載](/hak5/firmware-downloads/) — O.MG 韌體與 WebFlasher 連結
- [疑難排解索引](/hak5/troubleshooting-index/)
- [Hak5 總覽](/hak5/)