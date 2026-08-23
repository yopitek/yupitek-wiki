---
id: hak5-product-omg-cable
title: O.MG Cable
sidebar_position: 10
description: 內藏隱形 Wi-Fi 植入晶片的惡意 USB 線材 — 隱蔽按鍵注入、透過 Wi-Fi 執行 DuckyScript、自我銷毀與地理圍欄。
tags: [hak5, omg, omg-cable, malicious-cable, remote-access, duckyscript]
keywords: [O.MG Cable, 惡意 USB 線材, 透過 Wi-Fi 按鍵注入, DuckyScript, 自我銷毀, 地理圍欄, ESP32]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-cable
category: product
difficulty: advanced
toc: true
---

# O.MG Cable — 完整指南

> **一句話定位**：O.MG Cable 是一條「外觀正常、內部藏了一顆無線植入晶片」的 USB 充電/傳輸線——你以為只是條線，它卻能透過 Wi-Fi 被遠端操控，隨時注入鍵盤敲擊、執行 Payload，甚至自我銷毀。紅隊的終極社交工程武器。

如果你在研討會上隨手拿起的充電線，其實是一臺帶 Wi-Fi 無線電的電腦呢？這就是 O.MG Cable。在這種工具出現之前，這個等級的植入裝置（想想 NSA 的 COTTONMOUTH）要價數萬美金。O.MG 把它放進了一條量產、手工製作的 USB 線材裡。

這條線看起來、用起來都像一條普通的 USB 2.0 線 — 5V 充電、480 Mbps 資料 — 但內部藏著一顆植入晶片，在你透過 Wi-Fi 觸發它之前，它一直保持**休眠**（在資料線上隱形）。然後它部署 DuckyScript payload、注入按鍵，或轉向進入目標的網路，全部都能從瀏覽器控制。

> **⚠️ 僅限授權測試 — 而且這支特別。** O.MG 裝置因為太強大，法律上*必須以停用狀態出貨*。只把它們用於授權的紅隊工作、教學，以及測試你自己的偵測能力 — 防禦對應工具見 [Malicious Cable Detector](/hak5/products/malicious-cable-detector/)。

---

## 規格一覽

| 專案 | 規格 |
|---|---|
| 外型 | 手工製作 USB 2.0 線材（標準 1 m；可訂製 2 m） |
| 植入晶片 | 支援 WiFi 的無線 HID 晶片（內建 WebUI + 802.11 無線電） |
| Payload 語言 | DuckyScript 3.0（Elite）/ DuckyScript 2.0（Basic） |
| 遠端控制 | 透過 WiFi 的任何網頁瀏覽器 |
| 啟用 | 需要 [O.MG Programmer](/hak5/products/omg-programmer/)（出廠停用） |
| 特色功能 | 自我銷毀、地理圍欄、WiFi 觸發、偽造 VID/PID/MAC |
| Elite 額外功能 | 加密 C²、HIDX StealthLink、硬體鍵盤側錄器、延伸 WiFi 範圍 |
| 資料穿透 | 休眠期間正常 USB 2.0 充電 + 資料 |
| 官方檔案 | https://docs.hak5.org/omg-cable |

## Basic vs Elite（硬體等級）

| 功能 | Basic（Gen 1） | Elite（Gen 3） |
|---|---|---|
| 按鍵注入 | DuckyScript 2 | DuckyScript 3 |
| Payload 槽位 | 8 | 50–300 |
| 最大 payload 大小 | 約 4,000 次按鍵 | 約 1,500,000 次按鍵 |
| 最大速度 | 120 鍵/秒 | 890 鍵/秒 |
| 自我銷毀 / 地理圍欄 / WiFi 觸發 | ✅ | ✅ |
| FullSpeed 硬體鍵盤側錄器 | — | ✅ |
| HIDX StealthLink / 加密 C² / 延伸範圍 | — | ✅ |

---

## 攻擊如何運作

```mermaid
%% name: hak5-product-omg-cable-attack
sequenceDiagram
    participant A as Attacker (browser)
    participant C as O.MG Cable (dormant)
    participant T as Target computer
    A->>C: joins cable's WiFi, opens WebUI
    A->>C: deploys payload / triggers
    C->>T: re-enumerates as HID "keyboard"
    C->>T: injects keystrokes / exfiltrates
    T-->>C: (USB 2.0 data passthrough still works)
    A->>C: commands; optional self-destruct
```

關鍵洞察：*休眠*時，這條線就只是一條線。只有當你叫它時它才會變成鍵盤 — 這正是為什麼沒有正確工具就很難偵測它。

---

## 快速入門 — 啟用與第一個 payload

O.MG 裝置出廠時**停用**（法律要求）。你必須用 Programmer 啟用：

### 步驟 1 — 用 O.MG Programmer 啟用
1. 把 O.MG Cable 的 micro USB 端插進 [O.MG Programmer](/hak5/products/omg-programmer/)。
2. 把 Programmer 插進一臺執行 **Chrome 或 Edge**（WebSerial）的電腦。
3. 開啟 WebFlasher（https://o.mg.lol/setup/），選擇型號，依照 3 步驟精靈操作。精靈可選擇先做一次鑑識備份。

### 步驟 2 — 連上線材的 WiFi
啟用後，線材會廣播自己的 WiFi。從你的瀏覽器連上它。

### 步驟 3 — 部署 DuckyScript payload
開啟線材的 WebUI 並貼上/啟動一個 payload — 不需要為特定裝置重新編譯；DuckyScript 直接執行。

```text
REM Example: open notepad and type a proof-of-concept
DELAY 1000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 800
STRING Hello from an O.MG Cable!
ENTER
```

在 WebUI 中點 **Run**。片刻之後目標機器就會顯示打出的文字。

---

## 隱蔽功能

| 功能 | 作用 |
|---|---|
| Port Stealthing | 植入晶片在 payload 部署前保持休眠（不列舉 USB） |
| 可偽造身分 | 複製任何 VID/PID、延伸 USB ID 與 MAC 位址 |
| 無日誌 / 無偵測 | 休眠期間資料線上什麼都沒有 |
| 自我銷毀 | 遠端指令清除 payload + loot，讓線材失效（可透過 Programmer 復原） |
| 地理圍欄 | 依位置自動觸發/自我銷毀 — 讓工具保持在授權範圍內 |
| WiFi 觸發 | 用單一 beacon 遠距離觸發 payload |
| 加密 C²（Elite） | 加密控制通道；需要時可停用內建 WebUI |

> **你可能會問：** *「有什麼東西能抓到這條線嗎？」* [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) 的存在正是因為這些線材用肉眼或資料線嗅探都很難抓 — 它使用**側通道電力分析**來看到植入晶片。防禦存在，但它必須是有意為之。

---

## 進階

| 能力 | 怎麼做 |
|---|---|
| 滑鼠注入 | 注入遊標移動/點選（Elite+） |
| 硬體鍵盤側錄器（Elite） | FullSpeed USB 鍵盤側錄器附加元件（附額外儲存） |
| 加密網路 C² | 透過加密隧道從任何地方觸及線材，連到你的伺服器 |
| HIDX StealthLink（Elite） | 雙向隧道：Target ↔ O.MG ↔ 控制機器 |
| 復原自我銷毀 | 重新接上 Programmer 即可還原 |
| 批次韌體 | Programmer 支援大量韌體安裝 |

---

## 疑難排解

| 症狀 | 原因 | 修正 |
|---|---|---|
| 沒有出現 WebUI | 裝置未啟用 | 先用 Programmer 啟用 |
| WebFlasher 找不到東西 | 瀏覽器不支援 WebSerial / 裝置不在 bootloader | 使用 Chrome/Edge；在精靈要求前保持線材未插上 |
| 按鍵慢 / 亂碼 | 鍵盤配置或 DuckyScript 版本錯誤 | 用正確配置編譯/重新載入；檢查 Basic vs Elite 版本 |
| 找不到線材的 WiFi | 休眠 / 不在設定模式 | 用 Programmer 重新觸發，或按下內建按鈕序列 |
| 意外自我銷毀 | Payload/地理圍欄規則觸發 | 用 Programmer 復原（完整重置）。檢討地理圍欄範圍 |

---

## 相關資源

- [O.MG Plug](/hak5/products/omg-plug/) — 同款植入晶片，鑰匙圈 USB 插頭
- [O.MG Adapter](/hak5/products/omg-adapter/) — 植入晶片藏在 USB-A 轉 C 轉接頭
- [O.MG UnBlocker](/hak5/products/omg-unblocker/) — 植入晶片藏在「安全」資料阻斷器內
- [O.MG Programmer](/hak5/products/omg-programmer/) — 啟用/更新 O.MG 裝置所必需
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — 防禦偵測工具
- [USB Rubber Ducky](/hak5/products/usb-rubber-ducky/) — DuckyScript 語言參考
- [韌體與下載](/hak5/firmware-downloads/) — O.MG 韌體與 WebFlasher
- [疑難排解索引](/hak5/troubleshooting-index/)
- [Hak5 總覽](/hak5/)