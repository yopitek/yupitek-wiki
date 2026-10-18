---
id: alfa-product-awus036axer
title: ALFA AWUS036AXER——Wi-Fi 6 Nano（内置天线）
sidebar_position: 11
description: ALFA AWUS036AXER——10.5 g 的 Wi-Fi 6 nano 网卡，内置天线，RTL8832BU AX1800、WPA3 与 USB 3.2。体积极小的日常 AX 选择。
tags: [alfa, 网卡, rtl8832bu, wifi-6, nano, 内置天线]
keywords: [AWUS036AXER, RTL8832BU nano, 10.5g 网卡, 内置天线 Wi-Fi 6]
---

# ALFA AWUS036AXER——Wi-Fi 6 Nano（内置天线）

> **一句话摘要**：**AWUS036AXER** 是 ALFA 的 **10.5 g nano** 机型——与大型 AWUS036AX 采用相同的 **RTL8832BU AX1800** Wi-Fi 6 引擎，但配备**内置天线**与 USB 3.2，插入后几乎与端口齐平、毫不显眼。为日常随身携带族群提供 Wi-Fi 6 + WPA3。

## 规格总览 (Spec overview)

| 项目 | 规格 |
|---|---|
| 芯片 | Realtek RTL8832BU |
| Wi-Fi 等级 | AX1800（574 + 1201 Mbps） |
| 接口 | USB 3.2 |
| 频段 | 2.4 + 5 GHz |
| 天线 | **内置**（无外置 RP-SMA） |
| 重量 | 10.5 g |
| 安全性 | WPA3 |
| MIMO | 2×2 |
| Linux 驱动程序 | `rtl8852bu`（DKMS） |
| 监听模式 | ❌ 社区驱动程序不支持（请参阅[驱动程序指南](/alfa-network/drivers/rtl8832bu/)） |

## 总览

AXER 沿用 AWUS036AX 的无线电，并去除多余的体积。它以收进 **10.5 g 机身**的**集成式天线**取代两支外置天线——插入笔电端口后几乎不会突出。你保有 Wi-Fi 6 速度、WPA3 与 2×2 MIMO；代价是失去外置天线的距离优势与天线升级的弹性。

这是一款**以客户端为优先的网卡**：适合在阶梯教室里想要快速、安全的 Wi-Fi 6，又不想随身带着网卡加天线的学生。它*并非*长距离监听的首选——请参阅高端用法中的说明。

## 安装与驱动程序

驱动程序的情况与 [AWUS036AX](/alfa-network/products/awus036ax/) 相同——完整步骤请见 [RTL8832BU 驱动程序页面](/alfa-network/drivers/rtl8832bu/)：

```bash
cd /opt && sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826 && sudo sh install-driver.sh
sudo modprobe 8852bu
```

**预期输出**：安装程序完成（它要求时请重启），之后 `iw dev` 中会出现一个接口。

```mermaid
flowchart LR
    A["AWUS036AXER (10.5 g)"] --> B["DKMS build rtl8852bu"]
    B --> C["modprobe 8852bu"]
    C --> D["Connect — fast and flush"]
```

## 高端用法

### 卓越的客户端模式

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**预期输出**：已连接；靠近 AP 时 5 GHz 连接速率最高达 **1201 Mb/s**。

### 监听模式

此芯片的社区驱动程序**不**支持监听模式，而且内置天线本来就会限制截取距离。若需要监听模式，请使用外置天线且内核内置驱动的网卡，例如 [AWUS036ACM](/alfa-network/products/awus036acm/)。

## 兼容性

| 平台 | 支持 | 备注 |
|---|---|---|
| Kali Linux | ✅ | DKMS，但内置天线限制了距离 |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek、内置天线，优先级低 |
| Windows | ✅ | 官方驱动程序，WPA3 |
| Raspberry Pi / Jetson | ✅ | ARM64 上使用 DKMS |

## 疑难排解

| 症状 | 原因 | 修复 |
|---|---|---|
| 距离比外置天线的 ALFA 短 | 设计上采用内置天线 | 属于正常现象——请用于客户端用途，而非长距离连接 |
| 看不到 WPA3 网络 | 驱动程序过旧 | 更新 `rtl8852bu` 与操作系统 |
| DKMS 建置失败 | 新内核 | `git pull && make dkms_install` |
| 在 USB 2.0 端口上速度慢 | 带宽上限 | 使用 USB 3.x 端口 |

## 相关资源

- [RTL8832BU 驱动程序页面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AX](/alfa-network/products/awus036ax/)——相同引擎，外置天线，距离更远
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快且支持蓝牙
- [网卡比较](/alfa-network/wifi-adapter-comparison/)
