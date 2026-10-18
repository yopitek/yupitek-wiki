---
id: alfa-product-awus036axer
title: ALFA AWUS036AXER——Wi-Fi 6 Nano（內建天線）
sidebar_position: 11
description: ALFA AWUS036AXER——10.5 g 的 Wi-Fi 6 nano 網路卡，內建天線，RTL8832BU AX1800、WPA3 與 USB 3.2。體積極小的日常 AX 選擇。
tags: [alfa, 網路卡, rtl8832bu, wifi-6, nano, 內建天線]
keywords: [AWUS036AXER, RTL8832BU nano, 10.5g 網路卡, 內建天線 Wi-Fi 6]
---

# ALFA AWUS036AXER——Wi-Fi 6 Nano（內建天線）

> **一句話摘要**：**AWUS036AXER** 是 ALFA 的 **10.5 g nano** 機種——與大型 AWUS036AX 採用相同的 **RTL8832BU AX1800** Wi-Fi 6 引擎，但配備**內建天線**與 USB 3.2，插入後幾乎與連接埠齊平、毫不顯眼。為日常隨身攜帶族群提供 Wi-Fi 6 + WPA3。

## 規格總覽 (Spec overview)

| 項目 | 規格 |
|---|---|
| 晶片 | Realtek RTL8832BU |
| Wi-Fi 等級 | AX1800（574 + 1201 Mbps） |
| 介面 | USB 3.2 |
| 頻段 | 2.4 + 5 GHz |
| 天線 | **內建**（無外接 RP-SMA） |
| 重量 | 10.5 g |
| 安全性 | WPA3 |
| MIMO | 2×2 |
| Linux 驅動程式 | `rtl8852bu`（DKMS） |
| 監聽模式 | ❌ 社群驅動程式不支援（請參閱[驅動程式指南](/alfa-network/drivers/rtl8832bu/)） |

## 總覽

AXER 沿用 AWUS036AX 的無線電，並去除多餘的體積。它以收進 **10.5 g 機身**的**整合式天線**取代兩支外接天線——插入筆電連接埠後幾乎不會突出。你保有 Wi-Fi 6 速度、WPA3 與 2×2 MIMO；代價是失去外接天線的距離優勢與天線升級的彈性。

這是一款**以用戶端為優先的網路卡**：適合在階梯教室裡想要快速、安全的 Wi-Fi 6，又不想隨身帶著網路卡加天線的學生。它*並非*長距離監聽的首選——請參閱進階用法中的說明。

## 安裝與驅動程式

驅動程式的情況與 [AWUS036AX](/alfa-network/products/awus036ax/) 相同——完整步驟請見 [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)：

```bash
cd /opt && sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826 && sudo sh install-driver.sh
sudo modprobe 8852bu
```

**預期輸出**：安裝程式完成（它要求時請重新開機），之後 `iw dev` 中會出現一個介面。

```mermaid
flowchart LR
    A["AWUS036AXER (10.5 g)"] --> B["DKMS build rtl8852bu"]
    B --> C["modprobe 8852bu"]
    C --> D["Connect — fast and flush"]
```

## 進階用法

### 卓越的用戶端模式

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**預期輸出**：已連線；靠近 AP 時 5 GHz 連線速率最高達 **1201 Mb/s**。

### 監聽模式

此晶片的社群驅動程式**不**支援監聽模式，而且內建天線本來就會限制擷取距離。若需要監聽模式，請使用外接天線且核心內建驅動的網路卡，例如 [AWUS036ACM](/alfa-network/products/awus036acm/)。

## 相容性

| 平台 | 支援 | 備註 |
|---|---|---|
| Kali Linux | ✅ | DKMS，但內建天線限制了距離 |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek、內建天線，優先順序低 |
| Windows | ✅ | 官方驅動程式，WPA3 |
| Raspberry Pi / Jetson | ✅ | ARM64 上使用 DKMS |

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| 距離比外接天線的 ALFA 短 | 設計上採用內建天線 | 屬於正常現象——請用於用戶端用途，而非長距離連線 |
| 看不到 WPA3 網路 | 驅動程式過舊 | 更新 `rtl8852bu` 與作業系統 |
| DKMS 建置失敗 | 新核心 | `git pull && make dkms_install` |
| 在 USB 2.0 連接埠上速度慢 | 頻寬上限 | 使用 USB 3.x 連接埠 |

## 相關資源

- [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AX](/alfa-network/products/awus036ax/)——相同引擎，外接天線，距離更遠
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快且支援藍牙
- [網路卡比較](/alfa-network/wifi-adapter-comparison/)
