---
id: alfa-hardware-steam-deck
title: Steam Deck & UP Squared Pro × ALFA Network 集成指南
sidebar_label: Steam Deck / UP Squared
sidebar_position: 9
description: "参考架构（Yupitek 未实测）：UP Squared Pro 机载边缘计算与 Steam Deck 地面站搭配 ALFA AWUS036ACH 建立 5.745GHz wfb-ng 长距离图传遥测链路的设置教程。"
tags: [steam-deck, steamos, up-squared, alfa, awus036ach, rtl8812au, wfb-ng, uav]
keywords: [Steam Deck, UP Squared Pro, AWUS036ACH, RTL8812AU, wfb-ng, 无人机, SteamOS 只读]
---

# Steam Deck & UP Squared Pro × ALFA Network 集成指南

> **一句话定位**：这是一个比较高端、专门的应用情境——用 UP Squared Pro 当机载边缘运算主机、Steam Deck 当掌上型地面控制站，中间通过 ALFA AWUS036ACH 创建一条长距离、低延迟的单向影像与遥测传输链路，常见于无人载具系统（UAS，例如自制空拍机、地面机器人）的研究与社区项目。

> ⚠️ **实测范围**：Yupitek 的 ALFA 兼容性测试仅在 ASUS GX10／Ubuntu 24.04 ARM64／kernel 6.17 上进行，**Steam Deck、UP Squared Pro 与 wfb-ng尚未实测**。本页关于驱动是否可用的说明，是依平台内核版本与各驱动进入 mainline 的版本（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）推断，并非在该硬件上验证。AWUS036ACH 的内核内置驱动（`rtw88_8812au`，kernel 6.13 起）在 GX10 上只验证过监听与数据包注入（2.4／5 GHz 均为 100%），并未验证 wfb-ng；下方是否需要 DKMS 驱动，取决于 SteamOS 的内核版本。请仅在您自己拥有或已获授权的网络上测试。

## 这篇文章适合你吗？

- **难度**：高端（需要熟悉 Linux 终端操作，并对无线通信的基本概念有一定了解）
- **预估时间**：45〜60 分钟
- **你会用到的技能**：终端操作、基本的无线网络概念（信道、频段）
- **读完你可以做到**：
  1. 理解为什么这类长距离遥测链路要用「单向广播」而不是一般的双向连接
  2. 在 SteamOS 这种只读系统上正确安装驱动程序，且不破坏系统的安全性设计
  3. 知道系统更新后驱动程序为什么会消失、该怎么快速恢复

> ⚠️ **适用范围提醒**：这篇文章整理的是一个特定研究与社区情境的参考配置（Yupitek 并未实测），跟前面几篇「新手入门」性质的文章不太一样，会用到比较多高端概念。如果你是第一次接触 ALFA 网卡，建议先从 [Raspberry Pi 集成指南](/alfa-network/hardware/raspberry-pi/) 开始熟悉基本操作。

---

## 概念说明：这套链路架构在做什么、为什么这样设计

一般空拍机或机器人的控制链路，通常需要「双向」沟通——地面站送出控制指令，机载端回传影像和传感器数据，两边要互相确认数据包有没有收到（也就是一般网络连接常见的 ACK 应答机制）。但这套机制在长距离、信号不稳定的环境下有个缺点：每次应答都要花时间，距离一拉远、信号一变差，整体延迟就会明显上升，画面容易卡顿。

这里采用的做法是 **`wfb-ng`（Wi-Fi Broadcast Next Generation）**，内核概念是把影像和遥测数据「单向广播」出去，不等待对方确认收到与否：

- **机载端（UP Squared Pro）**：负责跑边缘运算、截取影像与传感器数据，通过 ALFA 网卡把数据广播出去。
- **地面站（Steam Deck）**：带着另一支 ALFA 网卡，接收机载端广播出来的画面与遥测信息，让操作者可以掌上型即时查看。

拿掉「等待确认」这个步骤，换来的是更低、更稳定的延迟——这对即时操控来说比「每个数据包都保证送达」更重要，就算偶尔漏掉一两帧画面，也比整体延迟飙高来得好。

> 📘 **名词小教室**
> - **wfb-ng（Wi-Fi Broadcast Next Generation）**：一套开源的无线影像/遥测广播框架，专门为长距离、低延迟的单向数据传输设计，常见于自制空拍机、机器人的第一人称视角（FPV）链路。
> - **ACK 应答机制**：一般网络连接中，接收方收到数据包后会回传一个「我收到了」的确认信号给发送方；`wfb-ng` 这类单向广播应用会刻意关闭这个机制，用牺牲一点可靠度换取更低的延迟。
> - **不可变（Immutable）只读文件系统**：SteamOS 为了系统稳定性与安全性，默认把系统内核文件设成「只读」，一般情况下不允许任意写入或修改，这也是为什么安装驱动程序前需要先手动解除保护。

---

## 为什么这个研究情境指定使用 AWUS036ACH？

在 `wfb-ng` 这类长距离单向广播链路中，需要驱动程序能做到几件比较特殊的事：把数据包长度设到接近极限、关闭前面提到的 ACK 应答机制，并且能在非标准或特定的 5GHz 信道（例如 5.745 GHz，信道 149）上进行无连接的单向广播。

**ALFA AWUS036ACH** 使用的 Realtek RTL8812AU 芯片，搭配独立的功率放大器（PA）与信号放大器（LNA），加上双外置天线接口，因此是社区的 `wfb-ng` 设置中最常被提到的型号。

> **老实说明**：Yupitek 并未实测 `wfb-ng`、Steam Deck 或 UP Squared Pro。其他型号（如 AWUS036AXML、AWUS036ACM）在 `wfb-ng` 框架下没有任何实测数据，这篇文章不对它们做推断；尤其 AXML 在 GX10 的实测中数据包注入失败，不适合用于依赖注入的链路。如果你想尝试其他型号，建议先自行做小规模测试验证。

---

## 你需要准备的东西

- [ ] **机载端硬件**：UP Squared Pro（或类似的边缘运算主机）
- [ ] **地面站硬件**：Valve Steam Deck（SteamOS）
- [ ] **两支 ALFA AWUS036ACH**：机载端和地面站各一支
- [ ] **驱动程序（GitHub）**：Realtek RTL8812AU 支持数据包注入版本（aircrack-ng 社区维护）：https://github.com/aircrack-ng/rtl8812au

---

## Step-by-Step 设置教学（以 Steam Deck 端为例）

> UP Squared Pro 端通常运行一般的 Linux 发行版，驱动安装方式可以参考 [ALFA 无线网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)。以下步骤示范难度较高的 Steam Deck（SteamOS）端安装流程。

### 步骤 1：切换到桌面模式，并设置管理员密码

从 Steam Deck 的电源菜单切换到「桌面模式（Desktop Mode）」，打开内置的终端程序 Konsole。如果你还没设置过管理员密码，先运行：

```bash
passwd
```

**预期结果**：系统要求你输入并确认一组新密码，设置完成后没有错误消息。

---

### 步骤 2：暂时解除只读保护

```bash
sudo steamos-readonly disable
```

**预期结果**：指令运行后没有错误消息，代表系统的根目录文件系统暂时切换成可写入状态，接下来才能安装驱动程序。

---

### 步骤 3：安装编译工具并下载驱动原代码

```bash
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman -Sy --needed base-devel linux-neptune-headers git dkms

git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**预期结果**：最后会看到 DKMS 安装完成的消息，代表驱动程序已经成功编译并加载系统。这个步骤在 Steam Deck 上可能需要几分钟，请耐心等待，不要中途中断。

---

### 步骤 4：重新激活只读保护

```bash
sudo steamos-readonly enable
```

**预期结果**：指令运行后没有错误消息。**这一步不要跳过**——重新激活只读保护是维护系统稳定性与安全性的重要步骤，跳过的话系统之后可能会出现不可预期的问题。

---

### 步骤 5：验证网卡是否正确辨识

```bash
lsusb | grep -i realtek
iw dev
```

**预期结果**：`lsusb` 应该会看到 Realtek RTL8812AU 的设备信息，`iw dev` 则会列出一个新的无线接口，代表 ALFA 网卡已经可以被 `wfb-ng` 使用。

---

## SteamOS 系统更新防护提醒（重要踩坑点）

SteamOS 有一个容易让人踩坑的机制：**A/B 分区覆盖**。每次进行重大系统更新时，SteamOS 会把系统写入一个全新的分区，这代表你先前手动编译安装在 `/usr/lib/modules/` 底下的 DKMS 驱动程序，会在更新后被还原成原本没装驱动的状态——也就是说，**系统更新之后，你的 ALFA 网卡很可能又抓不到了**，这不是设置跑掉，是 SteamOS 更新机制本身的设计。

**建议做法**：把步骤 1〜4 的指令整理成一支脚本，存在 `/home/deck/scripts/rebuild_alfa.sh`，之后每次系统更新完，只需要重新运行这支脚本一次，就能快速恢复外置网卡的功能，不用每次都手动重打一遍指令。

---

## 常见问题与排除指引

### Q1：系统更新后网卡突然又抓不到了？
- **原因**：SteamOS 的 A/B 分区覆盖机制，重大更新会清空先前手动安装的 DKMS 驱动。
- **解决方法**：重新运行步骤 1〜4（建议先准备好前述的自动化脚本），驱动程序会重新编译安装一次。

### Q2：`sudo ./dkms-install.sh` 编译失败？
- **原因**：可能是 `linux-neptune-headers`（Steam Deck 专用的内核标头档）版本跟目前系统内核版本不匹配，尤其是刚更新完系统的情况下。
- **解决方法**：先运行 `sudo pacman -Syu` 确认软件包库是最新的，再重新运行 `sudo pacman -Sy --needed base-devel linux-neptune-headers git dkms`，确保标头档版本跟目前内核一致。

### Q3：忘记重新激活只读保护会怎样？
- **原因**：只读保护是 SteamOS 设计上的一部分，用来确保系统文件不会被意外修改或损坏。
- **解决方法**：只要想起来，随时运行 `sudo steamos-readonly enable` 补回来即可，不会有无法复原的问题，但建议养成安装完立刻重新激活的习惯，避免忘记。

### Q4：能不能用其他型号的 ALFA 网卡（AXML / ACM）试试看？
- **原因**：Yupitek 并未实测 `wfb-ng`，本页只以 AWUS036ACH 为参考配置；AXML 在 GX10 的实测中数据包注入失败（`Found 0 APs`／`No Answer`），ACM 的注入成功率为 2.4 GHz 63–83%、5 GHz 76%。
- **解决方法**：技术上可以尝试 ACM，但 AXML 不建议；请先自己做小规模、短距离的测试，确认延迟与可靠度符合你的需求后，再应用到正式场景。

---

## 参考数据与延伸阅读

- [AWUS036ACH 产品页面](/alfa-network/products/awus036ach/)
- [ALFA 无线网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——UP Squared Pro 端的驱动安装可参考此篇
- [词汇表](/getting-started/glossary)——wfb-ng、ACK 应答机制等名词的完整解释
- Realtek RTL8812AU 驱动（aircrack-ng 社区维护，含数据包注入支持）：https://github.com/aircrack-ng/rtl8812au
- [wfb-ng 官方项目](https://github.com/svpcom/wfb-ng)——开源的无线影像/遥测广播框架

**标签：** `steam-deck` `steamos` `up-squared` `alfa` `awus036ach` `rtl8812au` `wfb-ng` `无人机系统` `进阶`
