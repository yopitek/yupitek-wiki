---
id: alfa-hardware-openwrt-router
title: OpenWrt 路由器 × ALFA Network 网卡配置与已知限制
sidebar_label: OpenWrt 路由器
sidebar_position: 7
description: OpenWrt 路由器（含 GL.iNet）搭配 ALFA 无线网卡——软件包安装、无线设置与上游已知 Bug 应对策略，含每一步的预期结果。
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt 路由器 × ALFA Network 配置与限制指南

> **一句话定位**：OpenWrt 路由器（包括 GL.iNet 系列、x86 软路由等）可以透过 USB 外接 ALFA 无线网卡，多出一组独立的无线频段，拿来当第二组无线中继、广播热点，或是无线安全监听节点。这篇文章教你怎么装、也老实告诉你目前有哪些已知的限制。

## 这篇文章适合你吗？

- **难度**：中阶（需要会用 SSH 操作路由器）
- **预估时间**：15〜25 分钟
- **你会用到的技能**：基本终端操作
- **读完你可以做到**：
  1. 判断自己的 ALFA 网卡型号在 OpenWrt 上该装哪个驱动软件包
  2. 完成软件包安装与无线接口设置
  3. 知道目前有哪些已知的驱动限制，避免踩坑

---

## 概念说明：为什么要在路由器上外接无线网卡

OpenWrt 路由器（尤其是小型的 GL.iNet 系列）内建的无线模块数量有限，如果你的需求是下面任何一种，内建模块通常不够用：

- **多一组独立的无线中继（WISP）**：让路由器一边连上既有的 Wi-Fi 当「用户端」取得网络，一边自己再广播出一个新的 Wi-Fi 给你的装置用。
- **多一组广播热点**：内建无线模块已经在用了，还想再开一个独立的 SSID。
- **无线安全监听节点**：把路由器变成一个长期摆著的数据包撷取点。

外接 ALFA 网卡就是在原本的无线模块之外，多插一张独立的网卡来做这些事。

> 📘 **名词小教室**
> - **kmod（Kernel Module，内核模块）**：OpenWrt 上驱动程序的安装单位，`kmod-mt7921u` 就是「MT7921U 这颗芯片的内核模块」，装上之后系统才认得这张网卡。
> - **opkg**：OpenWrt 专用的软件包管理工具，跟一般 Linux 上的 `apt` 是类似的东西，用来安装/更新软件包。
> - **WISP（Wireless ISP，无线网络服务供应）模式**：一种让路由器「先连上别人的 Wi-Fi，再把网络分享出去」的运作方式，常用于延伸网络信号。

---

## ALFA 网卡型号在 OpenWrt 上的支援情况

| ALFA 型号 | 芯片 | OpenWrt 24.10 | OpenWrt 25.12 | 驱动软件包 |
|---|---|---|---|---|
| **AWUS036ACM** | MediaTek MT7612U | ✅ 官方软件包库有提供 | ✅ 官方软件包库有提供 | `kmod-mt76x2u` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ 官方软件包库有提供（有已知限制，见下方） | ✅ 官方软件包库有提供（有已知限制，见下方） | `kmod-mt7921u` |
| **AWUS036ACHM** | MediaTek MT7610U | ✅ 官方软件包库有提供 | ✅ 官方软件包库有提供 | `kmod-mt76x0u` |
| **AWUS036ACH** | Realtek RTL8812AU | ✅ 官方软件包库有提供（社群维护的驱动） | ✅ 官方软件包库有提供（社群维护的驱动） | `kmod-rtl8812au-ct` |

上表只标示驱动软件包是否存在于 OpenWrt 官方软件包库（已对照 downloads.openwrt.org 确认）。实际在特定路由器上的运作情形、监听与注入支援度，取决于硬件平台与内核版本，请参阅 [openwrt.org](https://openwrt.org/) 与 [Table of Hardware](https://openwrt.org/toh/start)。

**简单判断方式**：如果你是第一次尝试，建议优先选 **AWUS036ACM**（MT7612U）——不受下面提到的已知限制影响。想要更新的 Wi-Fi 6/6E（AWUS036AXML）也可以用，但要先看过下面的已知限制章节。

---

## 你需要准备的东西

- [ ] **硬件**：一台已刷好 OpenWrt 的路由器（含 GL.iNet 系列），且可透过 SSH 连接管理
- [ ] **ALFA 无线网卡**：依上表选择
- [ ] **驱动程序参考（GitHub）**：
  - MediaTek MT76 系列驱动原始码（OpenWrt 官方维护，`kmod-mt7921u`、`kmod-mt76x2u` 等软件包的来源）：https://github.com/openwrt/mt76

---

## Step-by-Step 设置教学

透过 SSH 登入路由器终端，依序执行（以下命令使用 `opkg`；25.12 等较新版本可能改用 `apk`，请至 openwrt.org 确认）：

### 步骤 1：更新软件包库索引

```bash
opkg update
```

**预期结果**：终端会列出一连串软件包库更新的讯息，没有出现红色错误讯息即代表成功。

---

### 步骤 2：安装对应的驱动软件包

依照你使用的网卡型号，选择对应的指令：

```bash
# 若使用 AWUS036AXML（Wi-Fi 6/6E）：
opkg install kmod-mt7921u kmod-mt76-core wireless-tools usbutils

# 若使用 AWUS036ACM（802.11ac）：
opkg install kmod-mt76x2u kmod-mt76-core wireless-tools usbutils
```

**预期结果**：画面显示软件包下载与安装完成的讯息，最后没有出现错误。

---

### 步骤 3：重新侦测无线硬件并套用设置

```bash
wifi config
/etc/init.d/network restart
```

**预期结果**：网络服务重新启动后，可以到 LuCI 网页管理接口（路由器的网页后台）的「网络 → 无线」页面，应该会看到多出一组新的无线接口，代表 ALFA 网卡已经被系统正确辨识并可以设置使用。

---

## 已知限制（老实跟你说，不隐瞒）

### 限制 1：AWUS036AXML 在主动监听模式下会让驱动停止运作

- **现象**：依上游 `openwrt/mt76` 的 [Issue #839](https://github.com/openwrt/mt76/issues/839)，在 AWUS036AXML（`mt7921u`）启用「主动监听（active monitor）」后，驱动程序会停止运作；同一份回报中，一般（被动）监听模式则可正常撷取数据包。
- **状态**：该 Issue 在上游已标示为关闭；实际行为可能随内核版本而异，请至 Issue 页面确认最新情况。
- **实务建议**：
  - 如果你只需要**单纯撷取数据包**（被动监听，例如用 Kismet 或 tcpdump），请使用一般监听模式。
  - Issue 中指出主动监听在 `mt76x0u` 与 `mt76x2u` 上可运作；需要主动监听时，建议改用 **AWUS036ACM**（`mt76x2u`）或 **AWUS036ACHM**（`mt76x0u`）。

### 限制 2：6GHz 频段的支援情形

6GHz 在 OpenWrt 上能否使用，取决于驱动程序、地区法规设置与 LuCI 版本，请以 [openwrt.org](https://openwrt.org/) 的最新说明为准。

---

## 常见问题与排除指引

### Q1：装完软件包后，LuCI 接口还是看不到新的无线接口？
- **原因**：可能是软件包安装过程中有错误被忽略了，或是网络服务没有正确重启。
- **解决方法**：重新执行 `opkg update` 确认软件包库索引是最新的，再重新执行步骤 2、3；也可以用 `dmesg | grep -i mt76` 或 `dmesg | grep -i mt7921` 检查内核有没有正确加载驱动。

### Q2：AWUS036ACH（Realtek 芯片）可以用吗？
- **说明**：OpenWrt 官方软件包库有提供 `kmod-rtl8812au-ct`（社群维护的 RTL8812AU 驱动）。监听与注入等功能是否可用，请参阅 [openwrt.org](https://openwrt.org/)；若你需要已知稳定的方案，优先考虑 AWUS036ACM。

---

## 参考数据与延伸阅读

- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)
- [ALFA 无线网卡在 Orange Pi / RK3588 上](/alfa-network/hardware/orange-pi/)——另一个使用 MT76 系列驱动的整合情境
- [词汇表](/getting-started/glossary)——kmod、opkg 等名词的完整解释
- MediaTek MT76 系列驱动原始码（OpenWrt 官方维护）：https://github.com/openwrt/mt76
- 已知 Bug 追踪：https://github.com/openwrt/mt76/issues/839

**标签：** `openwrt` `glinet` `router` `alfa` `awus036axml` `mt7921u` `mt7612u` `kmod` `新手指南`
