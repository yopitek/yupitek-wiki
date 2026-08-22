---
id: alfa-product-awus036acs
title: ALFA AWUS036ACS——口袋大小雙頻 AC433
sidebar_position: 9
description: ALFA AWUS036ACS——小巧 55 mm RTL8811AU AC433 雙頻無線網卡，配兩支 5 dBi 天線與 DKMS 驅動的監聽模式。口袋 Kali 夥伴。
tags: [alfa, 無線網卡, rtl8811au, ac433, 可攜式]
keywords: [AWUS036ACS, RTL8811AU, 口袋無線網卡, 可攜式 Kali 無線網卡]
---

# ALFA AWUS036ACS——口袋大小雙頻 AC433

> **一句話定位（One-liner）**：**AWUS036ACS** 是 55 mm 口袋 ALFA——一支 **RTL8811AU AC433** 雙頻無線網卡，配兩支可摺疊的 5 dBi 天線與 DKMS 驅動的監聽模式（monitor mode）。它是你隨身攜帶的無線網卡，因為「你永遠不知道什麼時候會想看看某些 Wi-Fi」。

## 規格總覽 (Spec overview)

| 項目 | 規格 |
|---|---|
| 晶片 | Realtek RTL8811AU |
| Wi-Fi 等級 | AC433（150 + 433 Mbps） |
| 介面 | USB 2.0 |
| 頻段 | 2.4 + 5 GHz |
| 天線 | 2 × 外接 5 dBi，RP-SMA |
| 機身 | ~55 mm——口袋大小 |
| Linux 驅動程式 | `rtl8811au`（DKMS，不在核心內） |
| 監聽模式 | ✅ 良好 |
| 封包注入 | ✅ 良好 |

## 總覽

ACS 是把經典 ALFA 配方縮小而不失去精髓的結果。它保留雙頻、外接天線與可用的監聽模式，但把它們包進一個消失在筆電包裡的 **55 mm 機身**。它的 1×1 RTL8811AU 無線電是 AC433 等級——對管理訊框擷取、注入示範與輕量分析綽綽有餘，而且對吞吐量限制很誠實。

取捨與其他 Realtek ALFA 相同：驅動程式**不在核心內**，所以有一次性的 DKMS 建置（之後它會幫你處理核心更新）。如果你寧願零驅動程式工作，多花一點錢買內建於核心的 [AWUS036ACM](/alfa-network/products/awus036acm/)。

## 安裝與驅動程式

完整細節在 [RTL8811AU 驅動程式頁面](/alfa-network/drivers/rtl8811au/)。簡短版本：

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl8811au.git
cd rtl8811au && sudo make dkms_install
sudo modprobe 8811au
```

**預期輸出**：`DKMS: install completed.` 然後 `iw dev` 中出現介面。

```mermaid
flowchart LR
    A["AWUS036ACS in backpack"] --> B["DKMS driver build (once)"]
    B --> C["modprobe 8811au"]
    C --> D["airmon-ng start wlan0"]
    D --> E["wlan0mon — ready anywhere"]
```

## 進階使用

### 在路上做監聽模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**預期輸出**：`wlan0mon` + `30/30: 100%`。

### 旅行設備

把可摺疊天線（運輸時保持連接）配上 [Jetson](/alfa-network/hardware/jetson/) 或筆電，組成可攜式擷取/分析站。摺起天線、放進口袋、完成。

## 相容性

| 平台 | 支援 | 注意事項 |
|---|---|---|
| Kali Linux | ✅ | DKMS；aircrack-ng repo |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | 🔧 | Realtek，所以不保證 |
| Windows | ✅ | 官方驅動程式 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS 建置 |

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| DKMS 建置失敗 | 缺少標頭檔 / 新核心 | `sudo apt install linux-headers-$(uname -r)`；`git pull && make dkms_install` |
| 只有 managed 模式 | 核心 stub 衝突 | 把 `rtl8811au` 加入黑名單（見[驅動程式頁面](/alfa-network/drivers/rtl8811au/)） |
| 注入 0/30 | 空頻道 | `sudo iw wlan0mon set channel 6` |
| 吞吐量低 | 1×1 AC433 硬體 | 不是 bug |
| 重新開機後偵測不到 | 模組未自動載入 | 把 `8811au` 加入 `/etc/modules-load.d/alfa.conf` |

## 相關資源

- [RTL8811AU 驅動程式頁面](/alfa-network/drivers/rtl8811au/)
- [Kali 設定指南](/alfa-network/linux-setup-kali/)
- [AWUS036ACH](/alfa-network/products/awus036ach/)——全尺寸高功率兄弟
- [AWUS036ACM](/alfa-network/products/awus036acm/)——內建於核心的替代方案
- [無線網卡比較](/alfa-network/wifi-adapter-comparison/)