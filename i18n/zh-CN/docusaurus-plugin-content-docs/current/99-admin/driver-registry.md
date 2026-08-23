---
draft: true
slug: driver-registry
id: admin-driver-registry
title: 驱动注册表
sidebar_position: 2
description: 本 wiki 中记录的每个无线芯片组与其支持的 ALFA 网卡适配器、驱动类型及内核内置状态的对应关系。
---

# 驱动注册表

驱动注册表将每个**无线芯片组**映射到使用它的 ALFA 网卡适配器、**驱动类型**以及在现代 Linux 内核上的**内核内置状态**。这与 [`linux-compatibility-matrix`](/alfa-network/linux-compatibility-matrix/) 以及 [`/alfa-network/drivers/`](/alfa-network/drivers/) 下的各芯片组驱动指南相互对应。

## 芯片组表

| 芯片组 | 网卡适配器 | 驱动绑定 | 内核内置? | 驱动指南 |
|---------|----------|----------------|------------|--------------|
| MT7612U | AWUS036ACM | `mt76x2u` | ✅ 内核内置 | [指南](/alfa-network/drivers/mt7612u/) |
| MT7610U | AWUS036ACHM | `mt76x0u` | ✅ 内核内置 | [指南](/alfa-network/drivers/mt7610u/) |
| MT7921AUN | AWUS036AXM, AWUS036AXML | `mt7921u` | ✅ 内核内置 | [指南](/alfa-network/drivers/mt7921aun/) |
| RTL8812AU | AWUS036ACH | 树外 / DKMS | ❌ 非内核内置 | [指南](/alfa-network/drivers/rtl8812au/) |
| RTL8811AU | AWUS036ACS | 树外 / DKMS | ❌ 非内核内置 | [指南](/alfa-network/drivers/rtl8811au/) |
| RTL8832BU | AWUS036AX, AWUS036AXER | 树外 / DKMS | ❌ 非内核内置 | [指南](/alfa-network/drivers/rtl8832bu/) |
| RTL8821CU | AWUS036EACS | 树外 / DKMS | ❌ 非内核内置 | [指南](/alfa-network/drivers/rtl8821cu/) |

## 驱动类型

- **内核内置（mainline）** — 已包含在 Linux 内核中；网卡适配器通常在当前内核上开箱即用，无需额外安装。MediaTek（`mt76x2u` / `mt76x0u` / `mt7921u`）网卡适配器属于此类。
- **树外 / DKMS** — 驱动源码在内核之外维护。必须编译并安装，最好通过 DKMS 以便在内核更新后仍然有效。本注册表中的所有 Realtek 芯片组都属于此类。

## 内核更新

对于树外驱动，最常见的单一故障就是**内核更新**导致模块失效，因为预编译的模块不再匹配正在运行的内核。

```bash
# 为当前运行的内核重建 DKMS 模块
sudo dkms autoinstall

# 或者，在 Debian/Ubuntu 上使用 apt 管理的便捷重建方式
sudo apt install --reinstall linux-headers-$(uname -r)
```

另请参阅 [FAQ](/getting-started/faq/) 与 [`troubleshooting`](/alfa-network/troubleshooting/)。

## 驱动设置指南

- [`ubuntu`](/alfa-network/linux-setup-ubuntu/)、[`kali`](/alfa-network/linux-setup-kali/) 与 [`nethunter`](/alfa-network/linux-setup-nethunter/) 涵盖完整的系统设置。
- [`共享的 ALFA Linux 指南`](/sdrlab/shared/alfa-linux-guide/) 在 SDRLAB 中复用 ALFA 驱动知识时被引用。

## 维护

每当驱动指南、网卡适配器产品页面或兼容性矩阵被编辑时，请保持本注册表同步，以免交叉引用出现偏差。