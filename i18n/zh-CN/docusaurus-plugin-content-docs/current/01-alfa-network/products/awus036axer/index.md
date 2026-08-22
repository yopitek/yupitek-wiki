---
id: alfa-product-awus036axer
title: ALFA AWUS036AXER——Wi-Fi 6 纳米款（内置天线）
sidebar_position: 11
description: ALFA AWUS036AXER——10.5 g Wi-Fi 6 纳米网卡适配器，内置天线、RTL8832BU AX1800、WPA3 和 USB 3.2。极简体积的日常 AX。
tags: [alfa, 网卡适配器, rtl8832bu, wifi-6, 纳米, 内置天线]
keywords: [AWUS036AXER, RTL8832BU 纳米, 10.5g 网卡适配器, 内置天线 Wi-Fi 6]
---

# ALFA AWUS036AXER——Wi-Fi 6 纳米款（内置天线）

> **一句话定位（One-liner）**：**AWUS036AXER** 是 ALFA 的 **10.5 g 纳米款**——与大型 AWUS036AX 相同的 **RTL8832BU AX1800** Wi-Fi 6 引擎，但采用**内置天线**和 USB 3.2，所以它平贴端口、几乎隐形。为日常携带人群准备的 Wi-Fi 6 + WPA3。

## 规格总览（Spec overview）

| 项目 | 规格 |
|---|---|
| 芯片组 | Realtek RTL8832BU |
| Wi-Fi 等级 | AX1800（574 + 1201 Mbps） |
| 接口 | USB 3.2 |
| 频段 | 2.4 + 5 GHz |
| 天线 | **内置**（无外置 RP-SMA） |
| 重量 | 10.5 g |
| 安全 | WPA3 |
| MIMO | 2×2 |
| Linux 驱动 | `rtl88x2bu`（DKMS） |
| 监听模式 | ✅（内置天线——见说明） |

## 总览

AXER 拿走 AWUS036AX 的无线电，剥掉体积。它不用两根外置天线，而是用一根**集成天线**折叠进 **10.5 g 机身**——结果插进笔记本端口后几乎不突出。你保留 Wi-Fi 6 速度、WPA3 和 2×2 MIMO；你放弃的是外置天线的覆盖范围和天线升级路径。

这是一款**客户端优先的网卡适配器**：它面向阶梯教室里想要快速、安全 Wi-Fi 6、又不想随身带着适配器加天线到处跑的学生。它*不是*远距离监听的选择——见进阶用法中的说明。

## 安装与驱动

与 [AWUS036AX](/alfa-network/products/awus036ax/) 完全相同的驱动故事——完整步骤见 [RTL8832BU 驱动页面](/alfa-network/drivers/rtl8832bu/)：

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu && sudo make dkms_install
sudo modprobe 88x2bu
```

**预期输出**：`DKMS: install completed.`，然后 `iw dev` 中出现接口。

```mermaid
flowchart LR
    A["AWUS036AXER (10.5 g)"] --> B["DKMS build rtl88x2bu"]
    B --> C["modprobe 88x2bu"]
    C --> D["Connect — fast and flush"]
```

## 进阶用法

### 客户端模式出色

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**预期输出**：已连接；靠近接入点时 5 GHz 链路速率最高 **1201 Mb/s**。

### 监听模式——有一个注意事项

内置天线意味着覆盖范围和灵敏度有限。监听模式*能用*（驱动支持），但严肃的捕获工作，外置天线的 [AWUS036AX](/alfa-network/products/awus036ax/) 或 [AWUS036ACM](/alfa-network/products/awus036acm/) 是更好的工具。NetHunter 兼容性在这款上也很勉强。

## 兼容性

| 平台 | 支持 | 说明 |
|---|---|---|
| Kali Linux | ✅ | DKMS，但内置天线限制覆盖范围 |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek、内置天线、优先级低 |
| Windows | ✅ | 官方驱动，WPA3 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS |

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 覆盖范围比外置天线 ALFA 短 | 内置天线是设计使然 | 预期行为——用于客户端工作，不做长距离链路 |
| WPA3 网络不可见 | 驱动过旧 | 更新 `rtl88x2bu` + 操作系统 |
| DKMS 构建失败 | 新内核 | `git pull && make dkms_install` |
| USB 2.0 端口上慢 | 带宽上限 | 使用 USB 3.x 端口 |

## 相关资源

- [RTL8832BU 驱动页面](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AX](/alfa-network/products/awus036ax/)——相同引擎，外置天线，覆盖更远
- [AWUS036AXM](/alfa-network/products/awus036axm/)——更快 + 蓝牙
- [网卡适配器对比](/alfa-network/wifi-adapter-comparison/)