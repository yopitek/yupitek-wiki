---
id: alfa-product-awus036ax
title: ALFA AWUS036AX——Wi-Fi 6 雙頻 AX1800
sidebar_position: 10
description: ALFA AWUS036AX——Wi-Fi 6 RTL8832BU AX1800 雙頻網路卡，支援 WPA3、2x2 MIMO 與 DKMS 驅動程式。相較於 AC 等級網路卡的長距離升級選擇。
tags: [alfa, 網路卡, rtl8832bu, wifi-6, wpa3, ax1800]
keywords: [AWUS036AX, RTL8832BU, Wi-Fi 6 網路卡, WPA3, AX1800]
---

# ALFA AWUS036AX——Wi-Fi 6 雙頻 AX1800

> **一句話摘要**：**AWUS036AX** 是 ALFA 的 Wi-Fi 6 入門款——一款 **RTL8832BU AX1800** 雙頻網路卡，支援 **WPA3**、**2×2 MIMO**，並配備兩支外接天線。如果你的校園或實驗室路由器已改為僅支援 WPA3，這款網路卡仍能讓你連得上線。

## 規格總覽 (Spec overview)

| 項目 | 規格 |
|---|---|
| 晶片 | Realtek RTL8832BU |
| Wi-Fi 等級 | AX1800（574 + 1201 Mbps） |
| 介面 | USB 3.2 |
| 頻段 | 2.4 + 5 GHz |
| 天線 | 2 × 外接雙頻，RP-SMA |
| 安全性 | WPA3（同時支援 WPA2/WPA） |
| MIMO | 2×2 |
| Linux 驅動程式 | `rtl8852bu`（DKMS，非核心內建） |
| 監聽模式 | ❌ 社群驅動程式不支援（請參閱[驅動程式指南](/alfa-network/drivers/rtl8832bu/)） |

## 總覽

AWUS036AX 是銜接 ALFA 著名 AC 世代與 Wi-Fi 6 世界的橋樑。內部採用新一代 **RTL8832BU** 2×2 ax 無線電（AX1800），帶來學生真正有感的兩項升級：

1. **WPA3 支援**——校園與 6 GHz 時代的網路正逐步鎖定為 WPA3-SAE。舊的 AC 網路卡會被拒絕；這款則能協商新的安全性交握。
2. **Wi-Fi 6 效率**——OFDMA 與更佳的多使用者處理能力，讓 AX 在擁擠的階梯教室 RF 環境中，表現比任何 AC 網路卡都更穩定。

它保留了經典的 ALFA DNA——兩支外接天線、高功率前端，以及以用戶端為優先的 Wi-Fi 6 無線電。驅動程式**不在核心內**，因此需要進行一次性的 DKMS 建置。

## 安裝與驅動程式

完整步驟請見 [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)。簡短版本：

```bash
cd /opt && sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826 && sudo sh install-driver.sh
sudo modprobe 8852bu
```

**預期輸出**：安裝程式完成（它要求時請重新開機），之後 `iw dev` 中會出現一個介面。

```mermaid
flowchart LR
    A["AWUS036AX"] --> B["DKMS build (rtl8852bu)"]
    B --> C["modprobe 8852bu"]
    C --> D["Connect WPA3 network"]
```

## 進階用法

### 連線至僅支援 WPA3 的網路

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**預期輸出**：`Connected`，且在靠近 AP 時 5 GHz 連線速率最高達 **1201 Mb/s**（2×2 80 MHz）。

### 監聽模式

此晶片的社群驅動程式**不**支援監聽模式。若需要監聽模式與封包注入，請使用核心內建驅動的 MediaTek 網路卡，例如 [AWUS036ACM](/alfa-network/products/awus036acm/) 或 [AWUS036AXML](/alfa-network/products/awus036axml/)。

## 相容性

| 平台 | 支援 | 備註 |
|---|---|---|
| Kali Linux | ✅ | DKMS |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek；可能無法在手機核心上建置 |
| Windows | ✅ | 官方驅動程式，WPA3 正常 |
| Raspberry Pi / Jetson | ✅ | ARM64 上使用 DKMS |

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| 看不到 WPA3 網路 | 驅動程式/wpa_supplicant 太舊 | 更新驅動程式與作業系統 |
| DKMS 建置失敗 | 新核心與 repo 不相容 | `cd /opt/rtl8852bu-20250826 && git pull && sudo sh install-driver.sh` |
| 連線速率高但傳輸慢 | USB 2.0 連接埠 | 使用 USB 3.x 連接埠（本網路卡為 USB 3.2） |
| 注入 0/30 | 空頻道 | `sudo iw wlan0mon set channel 6` |

## 相關資源

- [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AXER](/alfa-network/products/awus036axer/)——nano 版 Wi-Fi 6 機種
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快的 AX3000 + 藍牙機種
- [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/) / [Kali 設定指南](/alfa-network/linux-setup-kali/)
- [網路卡比較](/alfa-network/wifi-adapter-comparison/)
