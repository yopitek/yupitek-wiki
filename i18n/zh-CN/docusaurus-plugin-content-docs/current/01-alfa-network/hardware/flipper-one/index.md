---
id: alfa-hardware-flipper-one
title: Flipper One × ALFA Network 兼容性与选型指南
sidebar_label: Flipper One
sidebar_position: 5
description: Flipper One 内置 MT7921AUN Wi-Fi 6E 芯片与外置 ALFA 网卡选型指南——搞懂 Flipper Zero 与 One 架构差异，双网卡并行与监听模式设置。
tags: [flipper, flipper-one, flipper-zero, alfa, awus036axml, mt7921aun, wifi-6e]
keywords: [Flipper One, Flipper Zero, AWUS036AXML, MT7921AUN, Wi-Fi 6E, USB Host]
---

# Flipper One × ALFA Network 兼容性与选型指南

> **一句话定位**：Flipper One 本身就内置了一颗 Wi-Fi 6E 芯片，很多情况下不用外置网卡就够用。但如果你需要更远的距离、更强的信号，或想同时做「连接」加「监听」两件事，外置一支 ALFA 网卡会是更好的选择。这篇文章帮你搞懂什么时候该加装、该怎么接。

## 这篇文章适合你吗？

- **难度**：中阶（需要熟悉基本的 Linux 终端指令）
- **预估时间**：15〜25 分钟
- **你会用到的技能**：基本终端操作
- **读完你可以做到**：
  1. 搞懂 Flipper Zero 跟 Flipper One 在能不能外置网卡这件事上的根本差异
  2. 判断自己的情境该用内置芯片还是外置 ALFA 网卡
  3. 实际把 ALFA 网卡接上 Flipper One 并验证是否成功

---

## 概念说明：Flipper Zero 跟 Flipper One 差在哪？为什么一个能接网卡、一个不能？

如果你是从 Flipper Zero 一路玩过来，可能会想问：「能不能买一条 USB-C 转接线，把 ALFA 网卡接到 Flipper Zero 上？」

答案是：**在硬件层面完全不可能**，原因不是软件限制，而是两者的硬件架构根本不同：

- **Flipper Zero** 的 USB-C 端口只支持「设备模式（Device Mode）」——意思是它只能被电脑或手机当成一个周边设备来连接，它自己**没有能力去驱动、供电给另一个外置设备**，所以不管接什么转接线，都无法把一张网卡「接上去」让系统辨识到。
- **Flipper One** 则不一样：它搭载真正的 ARM Cortex-A 应用处理器，运行完整的 Linux 操作系统，并且真的具备 **USB Host（主机）模式**——这代表它可以像一台电脑一样，通过 OTG（On-The-Go）转接线去驱动并辨识外置的 USB 设备，包括 ALFA 无线网卡。

> 📘 **名词小教室**
> - **USB Host（主机）模式 vs Device（设备）模式**：USB Host 模式代表这台设备能「主动」去驱动、供电给其他 USB 设备（就像你的电脑可以接鼠标、U盘）；Device 模式则相反，代表这台设备只能「被」别人（例如电脑）当成一个周边设备接上去，自己没办法反过来驱动别的设备。这是判断一台设备能不能外置网卡的关键。
> - **OTG（On-The-Go）**：一种让行动设备的 USB 端口可以在「设备模式」和「主机模式」之间切换的技术，让手机、Flipper One 这类小型设备也能像电脑一样外置周边设备。
> - **Wi-Fi 6E**：Wi-Fi 6 的延伸版本，多了 6 GHz 这个相对空旷、干扰少的频段可以使用。

---

## 内置 MT7921AUN vs 外置 ALFA 网卡，怎么选？

Flipper One 内置的芯片其实跟 **ALFA AWUS036AXML** 用的是同一颗——**MediaTek MT7921AUN**，支持完整的 Wi-Fi 6E（2.4 / 5 / 6 GHz）。差别主要在天线和发射功率：

| 比较项目 | Flipper One 内置芯片 | 外置 AWUS036AXML | 外置 AWUS036ACM |
| ------------ | ----------------------- | --------------------------------- | -------------------------------- |
| 芯片型号     | MediaTek MT7921AUN      | MediaTek MT7921AUN                | MediaTek MT7612U                 |
| 支持频段     | 2.4 / 5 / 6 GHz | 2.4 / 5 / 6 GHz           | 2.4 / 5 GHz                  |
| 天线     | 机身内部微型天线             | 外置 RP-SMA 天线（可自行更换）               | 外置 RP-SMA 天线（可自行更换）              |
| 发射功率     | 较低（随身设备的标准限制）     | 较高（有独立功率放大器）               | 较高（有独立功率放大器）              |
| 适合情境     | 日常随身、轻量扫描                | 需要 6 GHz 全频段、想要更远距离的监听情境 | 想要稳定的 5 GHz 数据包注入，且不需要 6 GHz |

**简单判断方式**：如果你只是想随身带着做轻量扫描，内置芯片就够了；如果你需要更远的距离、更强的信号，或想让内置芯片专心负责连接（例如通过 SSH 远程操作），外置的 ALFA 网卡专心负责监听，那就该加装外置网卡。

---

## 你需要准备的东西

- [ ] **硬件**：Flipper One（确认你手上的是 Flipper One，不是 Flipper Zero——参考上一节的差异判断）
- [ ] **ALFA 无线网卡**（依需求择一）：
  - [AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)——要用 6 GHz、要远距离就选这支
  - [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)——稳定的 5 GHz 方案
- [ ] **USB Type-C OTG 转接线**：用来连接 Flipper One 跟 ALFA 网卡
- [ ] **驱动进程参考（GitHub）**：
  - MediaTek MT76 系列驱动（适用 MT7921AUN / MT7612U，两款 ALFA 网卡都用这个驱动家族）：https://github.com/morrownr/mt76

---

## Step-by-Step 设置教学

### 步骤 1：通过 OTG 转接线接上 ALFA 网卡

用 Type-C OTG 转接线，把 ALFA AWUS036AXML（或 ACM）接上 Flipper One。

---

### 步骤 2：确认网卡是否被正确辨识

在 Flipper One 的终端输入：

```bash
lsusb
```

**预期结果**：你应该会看到类似这样的一行输出，代表系统已经认出这是一张 MediaTek 网卡：

```text
Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

接着检查这张网卡实际支持哪些频段：

```bash
iw phy
```

**预期结果**：如果是 AWUS036AXML，输出里应该会列出三个频段的完整支持范围：

```text
Band 1: 2.4 GHz (20/40 MHz)
Band 2: 5 GHz (20/40/80/160 MHz)
Band 4: 6 GHz (20/40/80/160 MHz HE channels)
```

---

### 步骤 3：创建「内置连接 + 外置监听」的双网卡架构

这是外置网卡最实用的情境：让 Flipper One 内置的网卡（`wlan0`）继续保持连接（例如通过 SSH 或网页操作），外置的 ALFA 网卡（`wlan1`）则专心切到监听模式：

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

**预期结果**：指令运行没有错误消息，代表 `mon0` 这个监听接口已经成功创建在外置的 ALFA 网卡上，这时候你可以继续用 `wlan0` 保持连接操作，同时用 `mon0` 进行数据包截取，两者互不干扰。

---

## 常见问题与排除指引

### Q1：我可以把 ALFA 网卡接在 Flipper Zero 上吗？
- **原因**：Flipper Zero 的 USB-C 端口只支持设备模式（Device Mode），没有 USB Host（主机）能力。
- **解决方法**：无法通过任何转接线解决，这是硬件本身的限制。如果你需要外置网卡的功能，需要使用 Flipper One。

### Q2：6 GHz 频段可以正常连接，但某些数据包注入工具用不了？
- **原因**：目前部分开源的数据包注入（Frame Injection）工具，对 6 GHz 这个相对新的规范支持还不够成熟，这是工具本身开发进度的问题，不是你的设置错误。
- **解决方法**：6 GHz 频段目前建议优先用于一般连接与扫描；如果你的项目一定需要数据包注入，可以先改用 5 GHz 频段测试（AWUS036ACM 或把 AXML 切到 5 GHz）。

### Q3：内置芯片跟外置网卡可以同时开监听模式吗？
- **原因**：技术上可以，但因为两者都是 MediaTek 芯片、可能共用部分系统资源，同时对两个信道做监听在部分情境下可能不稳定。
- **解决方法**：建议采用步骤 3 的做法——一个负责连接、一个专心监听，而不是两个都做监听，稳定性会好很多。

---

## 参考数据与延伸阅读

- [AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)
- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [ALFA 无线网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——同样使用 MT7921AUN 芯片的另一个集成情境
- [词汇表](/getting-started/glossary)——USB Host 模式、OTG 等名词的完整解释
- MediaTek MT76 系列驱动（社群维护，含 DKMS）：https://github.com/morrownr/mt76

**标签：** `flipper` `flipper-one` `flipper-zero` `alfa` `awus036axml` `mt7921aun` `wifi-6e` `新手指南`
