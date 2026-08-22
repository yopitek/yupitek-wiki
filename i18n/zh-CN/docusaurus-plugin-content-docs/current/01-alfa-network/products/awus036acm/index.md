---
id: alfa-product-awus036acm
title: ALFA AWUS036ACM——经典全能选手（MT7612U）
sidebar_position: 8
description: ALFA AWUS036ACM——经典 MT7612U AC1200 双频网卡适配器，内核内置驱动、高功率、监听模式出色。推荐的初学者 Kali 网卡适配器。
tags: [alfa, 网卡适配器, mt7612u, ac1200, kali, 监听模式]
keywords: [AWUS036ACM, MT7612U, 推荐 Kali 网卡适配器, AC1200 USB 网卡适配器]
---

# ALFA AWUS036ACM——经典全能选手（MT7612U）

> **一句话定位（One-liner）**：**AWUS036ACM** 是社区默认推荐：一款**高功率 MT7612U AC1200** 双频网卡适配器，其驱动**内置于 Linux 内核**。无需 DKMS、无需编译——在 Kali 或 Ubuntu 上插上，监听模式就能用。它是「我该买哪款 ALFA？」的无聊答案，而无聊意味着可靠。

## 规格总览（Spec overview）

| 项目 | 规格 |
|---|---|
| 芯片组 | MediaTek MT7612U |
| Wi-Fi 等级 | AC1200（300 + 867 Mbps） |
| 接口 | USB 3.0 |
| 频段 | 2.4 + 5 GHz |
| 天线 | 2 × 外置 5 dBi，RP-SMA |
| 发射功率 | 高功率（500 mW 等级） |
| Linux 驱动 | `mt76x2u`——**自 4.19 起内核内置** |
| 监听模式 | ✅ 优秀 |
| 数据包注入 | ✅ 优秀 |

## 总览

AWUS036ACM 继承了 [AWUS036ACH](/alfa-network/products/awus036ach/) 闻名的一切——2×2 AC1200、高功率、双频、两根外置天线——并去掉了学生最烦它的那一点：**DKMS 驱动构建**。ACM 的 MT7612U 是 Linux 内核的正式公民，所以：

- 插上 → `wlan0` 出现。零命令。
- 无 DKMS → 内核更新时什么都不会坏。
- 监听模式 + 注入 → 通过原版 `mac80211` 工具工作。

正是这个组合让它成为「我是学生，我想要一款安全课程用的网卡适配器，我不想和操作系统打架」的答案——也是为什么整个 wiki 在 [Ubuntu](/alfa-network/linux-setup-ubuntu/) 和 [Kali](/alfa-network/linux-setup-kali/) 指南中把它当作参考网卡适配器。

## 安装与驱动

无需安装任何东西——完整细节见 [MT7612U 驱动页面](/alfa-network/drivers/mt7612u/)。快速验证：

```bash
lsusb | grep -i mediatek
iw dev
```

**预期输出**：

```text
Bus 001 Device 004: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac 2T2R Wireless Adapter
phy#0
	Interface wlan0
		ifindex 3
		addr 00:c0:ca:xx:xx:xx
		type managed
```

（`00:c0:ca` 前缀是 ALFA 的 MAC OUI——一个方便的实验室识别技巧。）

```mermaid
flowchart LR
    A["AWUS036ACM"] --> B["In-kernel mt76x2u (0 steps)"]
    B --> C["iw dev → wlan0"]
    C --> D["airmon-ng start wlan0"]
    D --> E["wlan0mon + injection 30/30"]
```

## 进阶用法

### 监听模式 + 注入

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**预期输出**：`Injection is working!` 和 `30/30: 100%`。

### 天线升级

两个 RP-SMA 端口意味着你可以装[面板天线](/alfa-network/products/apa-m25/)做聚焦的长距离链路，或装双高增益偶极子做全向覆盖——而且 2×2 无线电会真正用到两个流。

### Wireshark 捕获装置

结合 [Raspberry Pi 指南](/alfa-network/hardware/raspberry-pi/)构建一个无头常开捕获站。

## 兼容性

| 平台 | 支持 | 说明 |
|---|---|---|
| Kali Linux | ✅ | 内核内置，零设置 |
| Ubuntu | ✅ | 20.04+ 即插即用 |
| NetHunter / Android | ✅ | 标准 NetHunter 网卡适配器 |
| Windows | ✅ | 官方驱动 |
| Raspberry Pi / Jetson | ✅ | 内核内置，扎实的 AP + 监听支持 |

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 不在 `lsusb` 中 | 供电 / 线缆 | 换端口 / 带供电的集线器——[故障排查](/alfa-network/troubleshooting/) |
| 没有接口 | 驱动未加载（罕见） | `sudo modprobe mt76x2u`；检查 `dmesg \| grep mt76` |
| 注入 0/30 | 空信道 / 无射频信号区域 | `sudo iw wlan0mon set channel 6`；在接入点附近测试 |
| 挂起/恢复时 WLAN 失效 | 已知的笔记本 USB 怪癖 | 恢复后重新插拔 |

## 相关资源

- [MT7612U 驱动页面](/alfa-network/drivers/mt7612u/)
- [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)
- [NetHunter 设置指南](/alfa-network/linux-setup-nethunter/)
- [AWUS036AXM](/alfa-network/products/awus036axm/)——Wi-Fi 6 + 蓝牙升级款
- [网卡适配器对比](/alfa-network/wifi-adapter-comparison/)