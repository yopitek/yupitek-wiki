---
id: alfa-product-awus036ax
title: ALFA AWUS036AX——Wi-Fi 6 雙頻 AX1800
sidebar_position: 10
description: ALFA AWUS036AX——Wi-Fi 6 RTL8832BU AX1800 雙頻無線網絡卡，支援 WPA3、2x2 MIMO 與 DKMS 驅動程式。比 AC 等級無線網絡卡更長距離的升級款。
tags: [alfa, 無線網絡卡, rtl8832bu, wifi-6, wpa3, ax1800]
keywords: [AWUS036AX, RTL8832BU, Wi-Fi 6 無線網絡卡, WPA3, AX1800]
---

# ALFA AWUS036AX——Wi-Fi 6 雙頻 AX1800

> **一句話定位（One-liner）**：**AWUS036AX** 是 ALFA 的 Wi-Fi 6 入門款——一支 **RTL8832BU AX1800** 雙頻無線網絡卡，支援 **WPA3**、**2×2 MIMO** 與兩支外接天線。如果你的校園或實驗室路由器已經只支援 WPA3，這支無線網絡卡仍然能讓你連進去。

## 規格總覽 (Spec overview)

| 專案 | 規格 |
|---|---|
| 晶片 | Realtek RTL8832BU |
| Wi-Fi 等級 | AX1800（574 + 1201 Mbps） |
| 介面 | USB 3.2 |
| 頻段 | 2.4 + 5 GHz |
| 天線 | 2 × 外接 6 dBi，RP-SMA |
| 安全性 | WPA3（與 WPA2/WPA 並存） |
| MIMO | 2×2 |
| Linux 驅動程式 | `rtl88x2bu`（DKMS，不在核心內） |
| 監聽模式 | ✅ 良好 |

## 總覽

AWUS036AX 是 ALFA 著名的 AC 世代與 Wi-Fi 6 世界之間的橋樑。引擎蓋下是現代的 **RTL8832BU** 2×2 ax 無線電（AX1800），帶來兩項學生真正有感升級：

1. **WPA3 支援**——校園與 6 GHz 世代的網路正在鎖定 WPA3-SAE。舊 AC 無線網絡卡會被拒絕；這支會協商新的安全握手。
2. **Wi-Fi 6 效率**——OFDMA 與更好的多使用者處理代表 AX 在擁擠的演講廳 RF 中比任何 AC 無線網絡卡都撐得住。

它保留經典的 ALFA DNA——兩支 6 dBi 外接天線、高功率前端，以及你想要時的 DKMS 驅動監聽模式（monitor mode）。驅動程式**不在核心內**，所以有一次性的 DKMS 建置。

## 安裝與驅動程式

完整步驟在 [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)。簡短版本：

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu && sudo make dkms_install
sudo modprobe 88x2bu
```

**預期輸出**：`DKMS: install completed.` 然後 `iw dev` 中出現介面。

```mermaid
flowchart LR
    A["AWUS036AX"] --> B["DKMS build (rtl88x2bu)"]
    B --> C["modprobe 88x2bu"]
    C --> D["Connect WPA3 network"]
    D --> E["airmon-ng start wlan0 (optional)"]
```

## 進階使用

### 連到只支援 WPA3 的網路

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**預期輸出**：`Connected` 與靠近 AP 時最高 **1201 Mb/s** 的 5 GHz 連結速率（2×2 80 MHz）。

### 監聽模式（需要時）

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**預期輸出**：`wlan0mon` + 注入 `30/30: 100%`。

## 相容性

| 平臺 | 支援 | 注意事項 |
|---|---|---|
| Kali Linux | ✅ | DKMS |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek；可能無法在手機核心上建置 |
| Windows | ✅ | 官方驅動程式，WPA3 沒問題 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS |

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| WPA3 網路看不見 | 驅動程式/wpa_supplicant 太舊 | 更新驅動程式 + 作業系統 |
| DKMS 建置失敗 | 新核心 vs repo | `cd /opt/rtl88x2bu && git pull && make dkms_install` |
| 高連結速率但傳輸慢 | USB 2.0 連線埠 | 使用 USB 3.x 連線埠（無線網絡卡是 USB 3.2） |
| 注入 0/30 | 空頻道 | `sudo iw wlan0mon set channel 6` |

## 相關資源

- [RTL8832BU 驅動程式頁面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AXER](/alfa-network/products/awus036axer/)——nano Wi-Fi 6 變體
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快的 AX3000 + 藍芽機型
- [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/) / [Kali 設定指南](/alfa-network/linux-setup-kali/)
- [無線網絡卡比較](/alfa-network/wifi-adapter-comparison/)