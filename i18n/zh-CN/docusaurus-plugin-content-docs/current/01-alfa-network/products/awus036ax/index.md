---
id: alfa-product-awus036ax
title: ALFA AWUS036AX——Wi-Fi 6 双频 AX1800
sidebar_position: 10
description: ALFA AWUS036AX——Wi-Fi 6 RTL8832BU AX1800 双频网卡适配器，支持 WPA3、2x2 MIMO 和 DKMS 驱动。AC 等级网卡适配器的远距离升级款。
tags: [alfa, 网卡适配器, rtl8832bu, wifi-6, wpa3, ax1800]
keywords: [AWUS036AX, RTL8832BU, Wi-Fi 6 网卡适配器, WPA3, AX1800]
---

# ALFA AWUS036AX——Wi-Fi 6 双频 AX1800

> **一句话定位（One-liner）**：**AWUS036AX** 是 ALFA 的 Wi-Fi 6 入门款——一款 **RTL8832BU AX1800** 双频网卡适配器，支持 **WPA3**、**2×2 MIMO** 和两根外置天线。如果你的校园或实验室路由器已经只支持 WPA3，这款网卡适配器仍能让你连上。

## 规格总览（Spec overview）

| 项目 | 规格 |
|---|---|
| 芯片组 | Realtek RTL8832BU |
| Wi-Fi 等级 | AX1800（574 + 1201 Mbps） |
| 接口 | USB 3.2 |
| 频段 | 2.4 + 5 GHz |
| 天线 | 2 × 外置 6 dBi，RP-SMA |
| 安全 | WPA3（同时支持 WPA2/WPA） |
| MIMO | 2×2 |
| Linux 驱动 | `rtl8852bu`（DKMS，非内核内置） |
| 监听模式 | ❌ 社区驱动不支持（参见[驱动指南](/alfa-network/drivers/rtl8832bu/)） |

## 总览

AWUS036AX 是 ALFA 著名的 AC 世代与 Wi-Fi 6 世界之间的桥梁。引擎盖下是现代 **RTL8832BU** 2×2 ax 无线电（AX1800），带来两项学生真正能感受到的升级：

1. **WPA3 支持**——校园和 6 GHz 时代的网络正在收紧到 WPA3-SAE。旧 AC 网卡适配器会被拒绝；这款能协商新的安全握手。
2. **Wi-Fi 6 效率**——OFDMA 和更好的多用户处理意味着 AX 在拥挤的阶梯教室射频环境中比任何 AC 网卡适配器都更稳。

它保留经典 ALFA 基因——两根 6 dBi 外置天线、高功率前端，以及需要时的 DKMS 驱动监听模式。驱动**不在内核中**，所以有一次 DKMS 构建。

## 安装与驱动

完整步骤见 [RTL8832BU 驱动页面](/alfa-network/drivers/rtl8832bu/)。简版：
cd /opt && sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826 && sudo sh install-driver.sh
sudo modprobe 8852bu
```

**预期输出**：安装程序完成（提示时重启），然后 `iw dev` 中出现接口。

```mermaid
flowchart LR
    A["AWUS036AX"] --> B["DKMS build (rtl8852bu)"]
    B --> C["modprobe 8852bu"]
    C --> D["Connect WPA3 network"]
## 进阶用法

### 连接仅 WPA3 的网络

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**预期输出**：`Connected`，靠近接入点时 5 GHz 链路速率最高 **1201 Mb/s**（2×2 80 MHz）。
### 监听模式

该芯片组的社区驱动**不**支持监听模式。如需使用监听模式和注入功能，请使用内核内置的 MediaTek 适配器，例如 [AWUS036ACM](/alfa-network/products/awus036acm/) 或 [AWUS036AXML](/alfa-network/products/awus036axml/)。
| 平台 | 支持 | 说明 |
|---|---|---|
| Kali Linux | ✅ | DKMS |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek；可能在手机内核上无法构建 |
| Windows | ✅ | 官方驱动，WPA3 正常 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS |

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| WPA3 网络不可见 | 驱动/wpa_supplicant 太旧 | 更新驱动 + 操作系统 |
| DKMS 构建失败 | 新内核 vs 仓库 | `cd /opt/rtl8852bu-20250826 && git pull && sudo sh install-driver.sh` |
| 链路高速但传输慢 | USB 2.0 端口 | 使用 USB 3.x 端口（网卡适配器是 USB 3.2） |
| 注入 0/30 | 空信道 | `sudo iw wlan0mon set channel 6` |

## 相关资源

- [RTL8832BU 驱动页面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AXER](/alfa-network/products/awus036axer/)——纳米 Wi-Fi 6 变体
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快的 AX3000 + 蓝牙型号
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/) / [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [网卡适配器对比](/alfa-network/wifi-adapter-comparison/)