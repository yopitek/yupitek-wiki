---
id: alfa-product-awus036axer
title: ALFA AWUS036AXER——Wi-Fi 6 Nano（內建天線）
sidebar_position: 11
description: ALFA AWUS036AXER——10.5 g Wi-Fi 6 nano 無線網卡，內建天線、RTL8832BU AX1800、WPA3 與 USB 3.2。極簡體積的日常 AX。
tags: [alfa, 無線網卡, rtl8832bu, wifi-6, nano, 內建天線]
keywords: [AWUS036AXER, RTL8832BU nano, 10.5g 無線網卡, 內建天線 Wi-Fi 6]
---

# ALFA AWUS036AXER——Wi-Fi 6 Nano（內建天線）

> **一句話定位（One-liner）**：**AWUS036AXER** 是 ALFA 的 **10.5 g nano**——與大支 AWUS036AX 相同的 **RTL8832BU AX1800** Wi-Fi 6 引擎，但改用**內建天線**與 USB 3.2，所以它平貼在連接埠上、幾乎看不見。給日常隨身攜帶族的 Wi-Fi 6 + WPA3。

## 規格總覽 (Spec overview)

| 項目 | 規格 |
|---|---|
| 晶片 | Realtek RTL8832BU |
| Wi-Fi 等級 | AX1800（574 + 1201 Mbps） |
| 介面 | USB 3.2 |
| 頻段 | 2.4 + 5 GHz |
| 天線 | **內建**（沒有外接 RP-SMA） |
| 重量 | 10.5 g |
| 安全性 | WPA3 |
| MIMO | 2×2 |
| Linux 驅動程式 | `rtl88x2bu`（DKMS） |
| 監聽模式 | ✅（內建天線——見注意事項） |

## 總覽

AXER 把 AWUS036AX 的無線電拿來並去掉體積。它不用兩支外接天線，改用摺進 **10.5 g 機身**的**整合式天線**——結果插進筆電連接埠後幾乎不突出。你保留 Wi-Fi 6 速度、WPA3 與 2×2 MIMO；你換掉的是外接天線的範圍與天線升級路徑。

這是一支**以用戶端為優先的無線網卡**：它是給演講廳裡想要快速、安全的 Wi-Fi 6、又不想隨身帶著 dongle 加天線的學生。它*不是*長距離監聽的選擇——請見進階使用中的注意事項。

## 安裝與驅動程式

與 [AWUS036AX](/alfa-network/products/awus036ax/) 相同的驅動程式故事——完整步驟在 [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)：

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu && sudo make dkms_install
sudo modprobe 88x2bu
```

**預期輸出**：`DKMS: install completed.` 然後 `iw dev` 中出現介面。

```mermaid
flowchart LR
    A["AWUS036AXER (10.5 g)"] --> B["DKMS build rtl88x2bu"]
    B --> C["modprobe 88x2bu"]
    C --> D["Connect — fast and flush"]
```

## 進階使用

### 用戶端模式的卓越表現

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**預期輸出**：已連線；靠近 AP 時 5 GHz 上最高 **1201 Mb/s** 連結速率。

### 監聽模式——有一個警告

內建天線代表範圍與靈敏度受限。監聽模式*可用*（驅動程式支援它），但對認真的擷取工作，外接天線的 [AWUS036AX](/alfa-network/products/awus036ax/) 或 [AWUS036ACM](/alfa-network/products/awus036acm/) 是更好的儀器。NetHunter 相容性對這支來說也很勉強。

## 相容性

| 平台 | 支援 | 注意事項 |
|---|---|---|
| Kali Linux | ✅ | DKMS，但內建天線限制範圍 |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek、內建天線、低優先 |
| Windows | ✅ | 官方驅動程式，WPA3 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS |

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| 範圍比外接天線 ALFA 短 | 內建天線是設計使然 | 預期行為——用於用戶端工作，不用於長距離連結 |
| WPA3 網路看不見 | 驅動程式過期 | 更新 `rtl88x2bu` + 作業系統 |
| DKMS 建置失敗 | 新核心 | `git pull && make dkms_install` |
| USB 2.0 連接埠上很慢 | 頻寬上限 | 使用 USB 3.x 連接埠 |

## 相關資源

- [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AX](/alfa-network/products/awus036ax/)——相同引擎、外接天線、更多範圍
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快 + 藍牙
- [無線網卡比較](/alfa-network/wifi-adapter-comparison/)