---
id: alfa-driver-rtl8832bu
title: RTL8832BU 驅動程式指南（AWUS036AX / AWUS036AXER）
sidebar_position: 6
description: RTL8832BU 晶片深入探討——AWUS036AX 與 AWUS036AXER 背後的 Wi-Fi 6 晶片、社群 rtl8852bu DKMS 驅動程式、WPA3。此驅動程式不支援監聽模式。
tags: [alfa, 驅動程式, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU 驅動程式, RTL8852BU, AWUS036AX, rtl8852bu, Linux Wi-Fi 6, WPA3]
---

# RTL8832BU 驅動程式指南（AWUS036AX / AWUS036AXER）

> **一句話摘要**：**Realtek RTL8832BU** 是 **AWUS036AX** 及其 nano 版兄弟機種 **AWUS036AXER** 內部的 Wi-Fi 6（802.11ax）晶片。它不在核心內，因此你只需建置一次社群的 `rtl8852bu` DKMS 驅動程式，即可享有 AX1800 速度與 **WPA3** 支援。**此驅動程式不支援監聽模式**——請參閱[監聽模式與封包注入](#monitor-mode-and-injection)。

## 概念：Wi-Fi 6，Realtek 風格

RTL8832BU 是一顆 2×2 802.11ax 無線電（AX1800：574 + 1201 Mbps）。與較舊的 AC 網路卡相比，使用者最直接感受到的優勢是 **WPA3**——只支援 WPA3 的現代路由器會拒絕你舊的 AC 網路卡，但會欣然接受 AX。

驅動程式的狀況與其他 Realtek 晶片相同：**未納入上游核心**，因此我們使用社群驅動程式。目前持續維護的 repo 是 **[`morrownr/rtl8852bu-20250826`](https://github.com/morrownr/rtl8852bu-20250826)**（「Linux Driver for USB WiFi Adapters that are based on the RTL8832BU and RTL8852BU Chipsets」）；其 README 列出 AWUS036AX 與 AWUS036AXER 為支援機種。其安裝程式會將驅動程式註冊到 DKMS，使其在核心更新後自動重新建置。

> 本指南早期版本使用 `aircrack-ng/rtl88x2bu`。該 repository 已不存在，且 88x2bu 系列（RTL8812BU / RTL8822BU）屬於另一個 802.11ac 晶片家族——請勿將其用於 AWUS036AX / AXER。

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["No in-kernel driver for RTL8832BU"]
    B --> C["Build rtl8852bu via DKMS"]
    C --> D["8852bu module loaded"]
    D --> E["Connect: WPA3-capable"]
```

## 前置需求

- [ ] Linux（Ubuntu 20.04+ / Kali / Debian）
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` 權限
- [ ] AWUS036AX 或 AWUS036AXER

## 步驟 1：建置驅動程式

```bash
cd /opt
sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo sh install-driver.sh
```

**預期輸出**：腳本會以 DKMS 建置並安裝驅動程式。請回答其提示，並在它要求時重新開機。

## 步驟 2：載入並驗證

```bash
sudo modprobe 8852bu
iw dev
```

**預期輸出**：一行介面資訊，例如 `Interface wlan0 ... type managed`。安裝程式通常會設定好重新開機後自動載入；若沒有，請執行：

```bash
echo 8852bu | sudo tee /etc/modules-load.d/alfa.conf
```

## 步驟 3：連線（WPA3 開箱即用）

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**預期輸出**：`Device 'wlan0' successfully activated with 'MySSID'.`

驗證安全性套件與連線速率：

```bash
iw dev wlan0 link
```

**預期輸出**：顯示 `SSID: MySSID` 以及協商後的速率——在 5 GHz 頻段最高約 **1201 Mb/s**，或依距離而降至較低速率（2×2 80 MHz）。

## 監聽模式與封包注入 {#monitor-mode-and-injection}

此驅動程式的 README 明確指出**不支援監聽模式**。若你需要監聽模式與封包注入，請改用搭載核心內建 MediaTek 驅動程式的網路卡（例如 [AWUS036ACM](/alfa-network/products/awus036acm/) 或 [AWUS036AXML](/alfa-network/products/awus036axml/)），或搭配社群驅動程式使用 [AWUS036ACH](/alfa-network/products/awus036ach/)。請參閱[網路卡比較](/alfa-network/wifi-adapter-comparison/)。

## 疑難排解

| 症狀 | 原因 | 修復 |
|---|---|---|
| 在非常新的核心上建置失敗 | repo 需要最新的 commit | `cd /opt/rtl8852bu-20250826 && sudo git pull && sudo sh install-driver.sh` |
| 看不到 WPA3 網路 | 驅動程式或 wpa_supplicant 太舊 | 更新驅動程式；`sudo apt update && sudo apt upgrade` |
| 核心升級後驅動程式失效 | DKMS 未重新建置 | `sudo dkms status`，然後重新執行 `sudo sh install-driver.sh` |
| 已安裝針對同一硬體的另一個核心外驅動程式 | 模組衝突 | 安裝程式能偵測大多數衝突；請檢查 `sudo dkms status` 並移除舊驅動程式 |
| 連線速率高但傳輸慢 | USB 2.0 連接埠瓶頸 | 使用 USB 3.x 連接埠（AX 為 USB 3.2） |

## 參考資料

- [AWUS036AX 產品頁面](/alfa-network/products/awus036ax/)與 [AWUS036AXER 產品頁面](/alfa-network/products/awus036axer/)
- [Kali 設定指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/)
- [疑難排解索引](/alfa-network/troubleshooting/)
- 驅動程式 repo：[morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
