---
id: alfa-driver-rtl8832bu
title: RTL8832BU 驅動程式指南（AWUS036AX / AWUS036AXER）
sidebar_position: 6
description: RTL8832BU 晶片深入探討——AWUS036AX 與 AWUS036AXER 背後的 Wi-Fi 6 RTL88x2BU 驅動程式、DKMS 安裝、WPA3 與監聽模式。
tags: [alfa, 驅動程式, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU 驅動程式, AWUS036AX, rtl88x2bu, Linux Wi-Fi 6, WPA3]
---

# RTL8832BU 驅動程式指南（AWUS036AX / AWUS036AXER）

> **一句話定位（One-liner）**：**Realtek RTL8832BU** 是 **AWUS036AX** 與其 nano 兄弟 **AWUS036AXER** 內部的 Wi-Fi 6（802.11ax）晶片。它不在核心內，所以你建置一次 `rtl88x2bu` DKMS 驅動程式——然後享受 AX1800 速度、**WPA3** 支援與可用的監聽模式（monitor mode）。

## 概念：Wi-Fi 6，Realtek 風格

RTL8832BU 是一顆 2×2 802.11ax 無線電（AX1800：574 + 1201 Mbps）。與較舊的 AC 無線網絡卡相比，使用者看得見的最大勝利是 **WPA3**——只講 WPA3 的現代路由器會拒絕你的舊 AC dongle，但會欣然接受 AX。

驅動程式狀況與其他 Realtek 晶片如出一轍：**沒有上游**，所以我們使用社群驅動程式。首選 repo 是 **`aircrack-ng/rtl88x2bu`**，它涵蓋 88X2BU 家族（RTL8822BU 與 RTL8832BU），支援監聽模式 + VIF。DKMS 讓它在核心更新後保持重建。

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["No in-kernel driver for RTL8832BU"]
    B --> C["Build rtl88x2bu via DKMS"]
    C --> D["88x2bu module loaded"]
    D --> E["Connect: WPA3-capable"]
    E --> F["airmon-ng start wlan0 → monitor mode"]
```

## 前置需求

- [ ] Linux（Ubuntu 20.04+ / Kali / Debian）
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` 許可權
- [ ] AWUS036AX 或 AWUS036AXER

## 步驟 1：建置驅動程式

```bash
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu
sudo make dkms_install
```

**預期輸出**：

```text
DKMS: install completed.
```

## 步驟 2：載入並驗證

```bash
sudo modprobe 88x2bu
iw dev
```

**預期輸出**：一行介面，例如 `Interface wlan0 ... type managed`。跨重新開機自動載入：

```bash
echo 88x2bu | sudo tee /etc/modules-load.d/alfa.conf
```

## 步驟 3：連線（WPA3 開箱即用）

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**預期輸出**：`Device 'wlan0' successfully activated with 'MySSID'.`

驗證安全套件與連結速度：

```bash
iw dev wlan0 link
```

**預期輸出**：顯示 `SSID: MySSID` 加上協商速率——在 5 GHz 上你應該看到 **1201 Mb/s** 或依距離而定的較低迴落值（2×2 80 MHz）。

## 步驟 4：監聽模式 + 注入

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**預期輸出**：

```text
PHY	Interface	Driver		Chipset
phy0	wlan0		88x2bu		Realtek
...
12:34:56  Injection is working!
12:34:56  30/30:  100%
```

> **你可能會想問**——*「Wi-Fi 6 和監聽模式？它們能混用嗎？」* 可以——社群驅動程式保留滲透測試工具需要的經典監聽/注入行為，而 managed 模式加上 AX 速率與 WPA3。你不必二選一。

## 步驟 5：恢復正常

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| 在非常新的核心上建置失敗 | repo 需要最新 commit | `cd /opt/rtl88x2bu && sudo git pull && sudo make dkms_install` |
| WPA3 網路看不見 | 驅動程式或 wpa_supplicant 太舊 | 更新驅動程式；`sudo apt update && sudo apt upgrade` |
| 無線網絡卡只有 managed、沒有監聽 | 核心 stub 衝突（罕見） | 用 `dmesg` 確認哪個模組繫結；把 stub 加入黑名單 |
| 注入 0/30 | 空頻道 | `sudo iw wlan0mon set channel 6`；在 AP 附近測試 |
| 高速連結但傳輸慢 | USB 2.0 連線埠瓶頸 | 使用 USB 3.x 連線埠（AX 是 USB 3.2） |

## 參考資料

- [AWUS036AX 產品頁面](/alfa-network/products/awus036ax/) 與 [AWUS036AXER 產品頁面](/alfa-network/products/awus036axer/)
- [Kali 設定指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/)
- [疑難排解索引](/alfa-network/troubleshooting/)
- 驅動程式 repo：[aircrack-ng/rtl88x2bu](https://github.com/aircrack-ng/rtl88x2bu)