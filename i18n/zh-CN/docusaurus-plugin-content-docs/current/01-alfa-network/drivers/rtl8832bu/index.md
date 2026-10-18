---
id: alfa-driver-rtl8832bu
title: RTL8832BU 驱动程序指南（AWUS036AX / AWUS036AXER）
sidebar_position: 6
description: RTL8832BU 芯片深入探讨——AWUS036AX 与 AWUS036AXER 背后的 Wi-Fi 6 芯片、社区 rtl8852bu DKMS 驱动程序、WPA3。此驱动程序不支持监听模式。
tags: [alfa, 驱动程序, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU 驱动程序, RTL8852BU, AWUS036AX, rtl8852bu, Linux Wi-Fi 6, WPA3]
---

# RTL8832BU 驱动程序指南（AWUS036AX / AWUS036AXER）

> **一句话摘要**：**Realtek RTL8832BU** 是 **AWUS036AX** 及其 nano 版兄弟机型 **AWUS036AXER** 内部的 Wi-Fi 6（802.11ax）芯片。它不在内核内，因此你只需建置一次社区的 `rtl8852bu` DKMS 驱动程序，即可享有 AX1800 速度与 **WPA3** 支持。**此驱动程序不支持监听模式**——请参阅[监听模式与封包注入](#monitor-mode-and-injection)。

## 概念：Wi-Fi 6，Realtek 风格

RTL8832BU 是一颗 2×2 802.11ax 无线电（AX1800：574 + 1201 Mbps）。与较旧的 AC 网卡相比，用户最直接感受到的优势是 **WPA3**——只支持 WPA3 的现代路由器会拒绝你旧的 AC 网卡，但会欣然接受 AX。

驱动程序的状况与其他 Realtek 芯片相同：**未纳入上游内核**，因此我们使用社区驱动程序。目前持续维护的 repo 是 **[`morrownr/rtl8852bu-20250826`](https://github.com/morrownr/rtl8852bu-20250826)**（「Linux Driver for USB WiFi Adapters that are based on the RTL8832BU and RTL8852BU Chipsets」）；其 README 列出 AWUS036AX 与 AWUS036AXER 为支持机型。其安装程序会将驱动程序注册到 DKMS，使其在内核更新后自动重新建置。

> 本指南早期版本使用 `aircrack-ng/rtl88x2bu`。该 repository 已不存在，且 88x2bu 系列（RTL8812BU / RTL8822BU）属于另一个 802.11ac 芯片家族——请勿将其用于 AWUS036AX / AXER。

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
- [ ] `sudo` 权限
- [ ] AWUS036AX 或 AWUS036AXER

## 步骤 1：建置驱动程序

```bash
cd /opt
sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo sh install-driver.sh
```

**预期输出**：脚本会以 DKMS 建置并安装驱动程序。请回答其提示，并在它要求时重启。

## 步骤 2：加载并验证

```bash
sudo modprobe 8852bu
iw dev
```

**预期输出**：一行接口信息，例如 `Interface wlan0 ... type managed`。安装程序通常会设置好重启后自动加载；若没有，请运行：

```bash
echo 8852bu | sudo tee /etc/modules-load.d/alfa.conf
```

## 步骤 3：连接（WPA3 开箱即用）

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**预期输出**：`Device 'wlan0' successfully activated with 'MySSID'.`

验证安全性套件与连接速率：

```bash
iw dev wlan0 link
```

**预期输出**：显示 `SSID: MySSID` 以及协商后的速率——在 5 GHz 频段最高约 **1201 Mb/s**，或依距离而降至较低速率（2×2 80 MHz）。

## 监听模式与封包注入 {#monitor-mode-and-injection}

此驱动程序的 README 明确指出**不支持监听模式**。若你需要监听模式与封包注入，请改用搭载内核内置 MediaTek 驱动程序的网卡（例如 [AWUS036ACM](/alfa-network/products/awus036acm/) 或 [AWUS036AXML](/alfa-network/products/awus036axml/)），或搭配社区驱动程序使用 [AWUS036ACH](/alfa-network/products/awus036ach/)。请参阅[网卡比较](/alfa-network/wifi-adapter-comparison/)。

## 疑难排解

| 症状 | 原因 | 修复 |
|---|---|---|
| 在非常新的内核上建置失败 | repo 需要最新的 commit | `cd /opt/rtl8852bu-20250826 && sudo git pull && sudo sh install-driver.sh` |
| 看不到 WPA3 网络 | 驱动程序或 wpa_supplicant 太旧 | 更新驱动程序；`sudo apt update && sudo apt upgrade` |
| 内核升级后驱动程序失效 | DKMS 未重新建置 | `sudo dkms status`，然后重新运行 `sudo sh install-driver.sh` |
| 已安装针对同一硬件的另一个内核外驱动程序 | 模块冲突 | 安装程序能侦测大多数冲突；请检查 `sudo dkms status` 并移除旧驱动程序 |
| 连接速率高但传输慢 | USB 2.0 端口瓶颈 | 使用 USB 3.x 端口（AX 为 USB 3.2） |

## 参考数据

- [AWUS036AX 产品页面](/alfa-network/products/awus036ax/)与 [AWUS036AXER 产品页面](/alfa-network/products/awus036axer/)
- [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)
- [疑难排解索引](/alfa-network/troubleshooting/)
- 驱动程序 repo：[morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
