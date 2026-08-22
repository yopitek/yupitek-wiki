---
id: alfa-product-awus036acs
title: ALFA AWUS036ACS——口袋级双频 AC433
sidebar_position: 9
description: ALFA AWUS036ACS——55 mm 微型 RTL8811AU AC433 双频网卡适配器，带两根 5 dBi 天线和 DKMS 驱动的监听模式。口袋 Kali 伴侣。
tags: [alfa, 网卡适配器, rtl8811au, ac433, 便携]
keywords: [AWUS036ACS, RTL8811AU, 口袋网卡适配器, 便携 Kali 网卡适配器]
---

# ALFA AWUS036ACS——口袋级双频 AC433

> **一句话定位（One-liner）**：**AWUS036ACS** 是 55 mm 口袋 ALFA——一款 **RTL8811AU AC433** 双频网卡适配器，带两根可折叠的 5 dBi 天线和 DKMS 驱动的监听模式。它是你随身携带的网卡适配器，因为「你永远不知道什么时候会想看看 Wi-Fi」。

## 规格总览（Spec overview）

| 项目 | 规格 |
|---|---|
| 芯片组 | Realtek RTL8811AU |
| Wi-Fi 等级 | AC433（150 + 433 Mbps） |
| 接口 | USB 2.0 |
| 频段 | 2.4 + 5 GHz |
| 天线 | 2 × 外置 5 dBi，RP-SMA |
| 机身 | ~55 mm——口袋大小 |
| Linux 驱动 | `rtl8811au`（DKMS，非内核内置） |
| 监听模式 | ✅ 良好 |
| 数据包注入 | ✅ 良好 |

## 总览

ACS 是把经典 ALFA 配方缩小而不丢失精髓的产物。它保留双频、外置天线和可用的监听模式，但装进一个放进笔记本包就消失的 **55 mm 机身**。它的 1×1 RTL8811AU 无线电是 AC433 等级——对管理帧捕获、注入演示和轻度分析足够，对吞吐量极限也足够诚实。

取舍与其他 Realtek ALFA 如出一辙：驱动**不在内核中**，所以有一次 DKMS 构建（之后它会替你处理内核更新）。如果你宁愿零驱动工作，多花一点钱买内核内置的 [AWUS036ACM](/alfa-network/products/awus036acm/)。

## 安装与驱动

完整细节见 [RTL8811AU 驱动页面](/alfa-network/drivers/rtl8811au/)。简版：

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl8811au.git
cd rtl8811au && sudo make dkms_install
sudo modprobe 8811au
```

**预期输出**：`DKMS: install completed.`，然后 `iw dev` 中出现接口。

```mermaid
flowchart LR
    A["AWUS036ACS in backpack"] --> B["DKMS driver build (once)"]
    B --> C["modprobe 8811au"]
    C --> D["airmon-ng start wlan0"]
    D --> E["wlan0mon — ready anywhere"]
```

## 进阶用法

### 旅途中使用监听模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**预期输出**：`wlan0mon` + `30/30: 100%`。

### 旅行装备

把可折叠天线（运输途中保持连接）与 [Jetson](/alfa-network/hardware/jetson/) 或笔记本搭配，组成便携捕获/分析站。折好天线，放进口袋，完成。

## 兼容性

| 平台 | 支持 | 说明 |
|---|---|---|
| Kali Linux | ✅ | DKMS；aircrack-ng 仓库 |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | 🔧 | Realtek，所以不保证 |
| Windows | ✅ | 官方驱动 |
| Raspberry Pi / Jetson | ✅ | ARM64 上的 DKMS 构建 |

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| DKMS 构建失败 | 缺少头文件 / 新内核 | `sudo apt install linux-headers-$(uname -r)`；`git pull && make dkms_install` |
| 只能 managed 模式 | 内核桩模块冲突 | 黑名单 `rtl8811au`（见[驱动页面](/alfa-network/drivers/rtl8811au/)） |
| 注入 0/30 | 空信道 | `sudo iw wlan0mon set channel 6` |
| 吞吐量低 | 1×1 AC433 硬件 | 不是 bug |
| 重启后检测不到 | 模块未自动加载 | 把 `8811au` 加入 `/etc/modules-load.d/alfa.conf` |

## 相关资源

- [RTL8811AU 驱动页面](/alfa-network/drivers/rtl8811au/)
- [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [AWUS036ACH](/alfa-network/products/awus036ach/)——全尺寸高功率兄弟款
- [AWUS036ACM](/alfa-network/products/awus036acm/)——内核内置替代款
- [网卡适配器对比](/alfa-network/wifi-adapter-comparison/)