---
id: alfa-product-awus036ax
title: ALFA AWUS036AX——Wi-Fi 6 双频 AX1800
sidebar_position: 10
description: ALFA AWUS036AX——Wi-Fi 6 RTL8832BU AX1800 双频网卡，支持 WPA3、2x2 MIMO 与 DKMS 驱动程序。相较于 AC 等级网卡的长距离升级选择。
tags: [alfa, 网卡, rtl8832bu, wifi-6, wpa3, ax1800]
keywords: [AWUS036AX, RTL8832BU, Wi-Fi 6 网卡, WPA3, AX1800]
---

# ALFA AWUS036AX——Wi-Fi 6 双频 AX1800

> **一句话摘要**：**AWUS036AX** 是 ALFA 的 Wi-Fi 6 入门款——一款 **RTL8832BU AX1800** 双频网卡，支持 **WPA3**、**2×2 MIMO**，并配备两支外置天线。如果你的校园或实验室路由器已改为仅支持 WPA3，这款网卡仍能让你连得上。

## 规格总览 (Spec overview)

| 项目 | 规格 |
|---|---|
| 芯片 | Realtek RTL8832BU |
| Wi-Fi 等级 | AX1800（574 + 1201 Mbps） |
| 接口 | USB 3.2 |
| 频段 | 2.4 + 5 GHz |
| 天线 | 2 × 外置双频，RP-SMA |
| 安全性 | WPA3（同时支持 WPA2/WPA） |
| MIMO | 2×2 |
| Linux 驱动程序 | `rtl8852bu`（DKMS，非内核内置） |
| 监听模式 | ❌ 社区驱动程序不支持（请参阅[驱动程序指南](/alfa-network/drivers/rtl8832bu/)） |

## 总览

AWUS036AX 是衔接 ALFA 著名 AC 世代与 Wi-Fi 6 世界的桥梁。内部采用新一代 **RTL8832BU** 2×2 ax 无线电（AX1800），带来学生真正有感的两项升级：

1. **WPA3 支持**——校园与 6 GHz 时代的网络正逐步锁定为 WPA3-SAE。旧的 AC 网卡会被拒绝；这款则能协商新的安全性交握。
2. **Wi-Fi 6 效率**——OFDMA 与更佳的多用户处理能力，让 AX 在拥挤的阶梯教室 RF 环境中，表现比任何 AC 网卡都更稳定。

它保留了经典的 ALFA DNA——两支外置天线、高功率前端，以及以客户端为优先的 Wi-Fi 6 无线电。驱动程序**不在内核内**，因此需要进行一次性的 DKMS 建置。

## 安装与驱动程序

完整步骤请见 [RTL8832BU 驱动程序页面](/alfa-network/drivers/rtl8832bu/)。简短版本：

```bash
cd /opt && sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826 && sudo sh install-driver.sh
sudo modprobe 8852bu
```

**预期输出**：安装程序完成（它要求时请重启），之后 `iw dev` 中会出现一个接口。

```mermaid
flowchart LR
    A["AWUS036AX"] --> B["DKMS build (rtl8852bu)"]
    B --> C["modprobe 8852bu"]
    C --> D["Connect WPA3 network"]
```

## 高端用法

### 连接至仅支持 WPA3 的网络

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**预期输出**：`Connected`，且在靠近 AP 时 5 GHz 连接速率最高达 **1201 Mb/s**（2×2 80 MHz）。

### 监听模式

此芯片的社区驱动程序**不**支持监听模式。若需要监听模式与封包注入，请使用内核内置驱动的 MediaTek 网卡，例如 [AWUS036ACM](/alfa-network/products/awus036acm/) 或 [AWUS036AXML](/alfa-network/products/awus036axml/)。

## 兼容性

| 平台 | 支持 | 备注 |
|---|---|---|
| Kali Linux | ✅ | DKMS |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek；可能无法在手机内核上建置 |
| Windows | ✅ | 官方驱动程序，WPA3 正常 |
| Raspberry Pi / Jetson | ✅ | ARM64 上使用 DKMS |

## 疑难排解

| 症状 | 原因 | 修复 |
|---|---|---|
| 看不到 WPA3 网络 | 驱动程序/wpa_supplicant 太旧 | 更新驱动程序与操作系统 |
| DKMS 建置失败 | 新内核与 repo 不兼容 | `cd /opt/rtl8852bu-20250826 && git pull && sudo sh install-driver.sh` |
| 连接速率高但传输慢 | USB 2.0 端口 | 使用 USB 3.x 端口（本网卡为 USB 3.2） |
| 注入 0/30 | 空频道 | `sudo iw wlan0mon set channel 6` |

## 相关资源

- [RTL8832BU 驱动程序页面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AXER](/alfa-network/products/awus036axer/)——nano 版 Wi-Fi 6 机型
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快的 AX3000 + 蓝牙机型
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/) / [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [网卡比较](/alfa-network/wifi-adapter-comparison/)
