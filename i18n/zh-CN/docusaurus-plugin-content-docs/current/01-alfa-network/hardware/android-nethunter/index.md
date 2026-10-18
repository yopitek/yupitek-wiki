---
id: alfa-hardware-android-nethunter
title: Android Kali NetHunter × ALFA Network 集成与供电指南
sidebar_label: Android NetHunter
sidebar_position: 6
description: Kali NetHunter 手机搭配 ALFA 无线网卡——OTG Y-Cable 供电设置、驱动确认与监听模式启用指南，含每一步的预期结果。
tags: [kali, nethunter, android, otg, alfa, awus036ach, rtl8812au, monitor-mode]
keywords: [Kali NetHunter, Android OTG, AWUS036ACH, AWUS036NEH, AWUS036NHA, RTL8812AU, Y-cable]
---

# Android Kali NetHunter × ALFA Network 集成与供电指南

> **一句话定位**：手机的 USB 端口供电能力有限，直接接上高功率的 ALFA 网卡常常会让手机重开机或网卡断线。这篇文章教你怎么用一条 Y-Cable 解决供电问题，并在 Kali NetHunter 上正确设置你的 ALFA 网卡。

## 这篇文章适合你吗？

- **难度**：中阶（需要熟悉基本的 Linux 终端指令，并已经在手机上安装好 Kali NetHunter）
- **预估时间**：20〜30 分钟
- **你会用到的技能**：基本终端操作
- **读完你可以做到**：
  1. 选对兼容的 ALFA 网卡型号，并判断需不需要额外供电
  2. 正确接线并在手机供电有限的情况下稳定使用高功率网卡
  3. 在 NetHunter 上验证网卡辨识、激活监听模式

---

## 概念说明：手机的供电限制是怎么一回事

Android 手机的 USB-C（或 Micro-USB）端口在 **OTG Host 模式**下，硬件上能提供的供电上限通常只有 **500mA（2.5W）左右**。但像 ALFA AWUS036ACH 这类高功率网卡，在发射数据包的瞬间，峰值功率可能达到 **3.6W（720mA @ 5V）**——远超过手机能稳定提供的供电量。

这就是为什么很多人第一次把高功率网卡接上手机时，会遇到手机突然重开机，或网卡连接一直断断续续的状况：不是网卡坏了，也不是设置错了，单纯是手机供电不够用。

解决方法是使用一条 **Y-Cable（Y 形分线器）**：它有两个输入端和一个输出端，让你可以一边通过手机传输数据给网卡，一边从外部电源（例如充电宝）额外供电，把「数据传输」和「供电」这两件事分开处理，网卡就不用只靠手机那 500mA 硬撑。

> 📘 **名词小教室**
> - **OTG（On-The-Go）**：一种让手机的 USB 端口可以切换成「主机模式」的技术，让手机可以像电脑一样外置鼠标、U盘、网卡等设备。
> - **Y-Cable（Y 形分线器）**：一条线材上有两个 USB 输入端、一个输出端，可以同时接手机（传输数据）跟外部电源（供电），是解决 OTG 供电不足最直接的做法。
> - **监听模式（Monitor Mode）**：让网卡把空气中飞过的所有无线数据包都抓下来，而不只是接收「要给自己的」数据包，是做无线网络安全分析的基础模式。

---

## 兼容的 ALFA 网卡型号怎么选

Kali NetHunter 官方文档（[kali.org/docs/nethunter/wireless-cards/](https://www.kali.org/docs/nethunter/wireless-cards/)）列出了几款官方支持的 ALFA 网卡，各自的供电需求不同：

| ALFA 型号        | 内核芯片              | 支持频段            | 供电建议                |
| -------------- | ----------------- | --------------- | ------------------- |
| **AWUS036ACH** | Realtek RTL8812AU | 2.4 GHz + 5 GHz | 功率较高，**建议搭配 Y-Cable 外置供电** |
| **AWUS036NEH** | Ralink RT3070     | 2.4 GHz         | 手机 OTG 直接供电即可，不需要额外置线 |
| **AWUS036NHA** | Atheros AR9271    | 2.4 GHz         | 手机 OTG 直接供电即可，不需要额外置线 |
| **AWUS036ACM** | MediaTek MT7612U  | 2.4 GHz + 5 GHz | 功率中等，建议准备 Y-Cable 以求稳定 |

**简单判断方式**：只要你选的是双频（2.4 + 5 GHz）且信号较强的机型（AWUS036ACH、AWUS036ACM），就准备一条 Y-Cable；如果是单纯 2.4 GHz 的入门机型（AWUS036NEH、AWUS036NHA），手机直接供电通常就够了。

---

## 你需要准备的东西

- [ ] **硬件**：已安装好 Kali NetHunter 的 Android 手机
- [ ] **ALFA 无线网卡**：依上一节选择合适型号
- [ ] **USB OTG Y-Cable**：如果你选的是高功率型号（AWUS036ACH / ACM），务必准备
- [ ] **充电宝或外部电源**：搭配 Y-Cable 使用，提供网卡额外供电
- [ ] **驱动进程参考（GitHub）**：
  - Realtek RTL8812AU 驱动（适用 AWUS036ACH）：https://github.com/aircrack-ng/rtl8812au
  - MediaTek MT76 系列驱动（适用 AWUS036ACM）：https://github.com/morrownr/mt76
- [ ] **Kali NetHunter 官方项目**：目前官方原代码已搬迁到 GitLab（不是 GitHub），如需查阅原代码或回报问题请至：https://gitlab.com/kalilinux/nethunter

---

## Step-by-Step 设置教学

### 步骤 1：用 Y-Cable 正确接线

1. 把 Y-Cable 其中一个输入端接上手机的 USB 端口。
2. 另一个输入端接上充电宝或外部电源（负责供电）。
3. 输出端接上 ALFA 网卡。

> ⚠️ **供电提醒**：如果你跳过 Y-Cable，直接把高功率网卡插在手机上，很可能会遇到手机重开机或网卡反复断线的状况——这不是设置问题，是供电不足，回到这一步接好线材即可解决。

---

### 步骤 2：验证硬件辨识

打开 NetHunter Terminal（Root 模式），输入：

```bash
lsusb
```

**预期结果**：清单里应该会出现你的 ALFA 网卡型号信息，代表手机已经正确辨识到这张网卡。

再检查无线接口是否出现：

```bash
iwconfig
# 或
ip link show
```

**预期结果**：应该会看到一个新的无线接口（通常是 `wlan1`），代表网卡已经可以被系统使用。如果 Realtek 芯片的机型（如 AWUS036ACH）没有出现，代表可能需要先确认 NetHunter 内核是否已包含对应驱动——可以参考文末的第四节「高端：自订内核注意事项」。

---

### 步骤 3：启动监听模式并进行数据包稽核

```bash
# 1. 终止可能干扰的系统服务
airmon-ng check kill

# 2. 开启监听模式（假设网卡接口为 wlan1）
airmon-ng start wlan1

# 3. 验证 monitor 接口（通常会变成 wlan1mon）
iwconfig wlan1mon
```

**预期结果**：`iwconfig wlan1mon` 应该会显示 `Mode:Monitor`，代表监听模式已经成功激活。

接着可以启动自动化的无线安全稽核工具进行测试：

```bash
wifite -i wlan1mon
```

**预期结果**：`wifite` 会开始扫描附近的无线网络，列出侦测到的基地台清单。

---

## 高端：自订内核注意事项（选读）

这一段只有在你使用的是**非官方预编译 NetHunter 内核的自订 ROM** 时才需要参考，一般直接使用官方预编译内核的读者可以跳过这一节。

如果你需要自己编译内核，记得激活以下设置项目，才能正确支持无线网卡：

```ini
CONFIG_NET_RADIO=y
CONFIG_WIRELESS_EXT=y
CONFIG_WEXT_PRIV=y
CONFIG_CFG80211=m
CONFIG_MAC80211=m
CONFIG_CFG80211_WEXT=y

# RTL8812AU 驱动模块（AWUS036ACH 适用）
CONFIG_RTL8812AU=m

# Ralink / Atheros 内建驱动（AWUS036NEH / AWUS036NHA 适用）
CONFIG_RT2800USB=m
CONFIG_ATH9K_HTC=m
```

---

## 常见问题与排除指引

### Q1：接上网卡后手机直接重开机？
- **原因**：手机 OTG 供电不足（上限约 500mA），高功率网卡瞬间需求超过这个上限。
- **解决方法**：改用 Y-Cable 搭配外部电源供电（见步骤 1），不要让手机独自负担网卡的全部供电。

### Q2：`lsusb` 看不到我的网卡？
- **原因**：接线方式错误，或是 Y-Cable 本身的数据传输端没有正确接到手机。
- **解决方法**：确认 Y-Cable 的两端没有接反——负责数据传输的一端要接手机，负责供电的一端接电源；也可以换一条 Y-Cable 测试排除线材本身的问题。

### Q3：Realtek 芯片的网卡（AWUS036ACH）辨识不到？
- **原因**：目前使用的 NetHunter 内核可能没有内置 RTL8812AU 驱动。
- **解决方法**：确认你安装的是官方支持该网卡的 NetHunter 内核版本；如果你是自行编译内核，请参考上方「高端：自订内核注意事项」章节，确认有勾选对应的驱动选项。

### Q4：监听模式激活后信号断断续续？
- **原因**：通常还是供电不稳，或者是天线位置不佳。
- **解决方法**：优先确认供电是否稳定（Y-Cable 接线、电源容量足够）；也可以尝试调整网卡天线的角度与位置。

---

## 参考数据与延伸阅读

- [AWUS036ACH 产品页面](/alfa-network/products/awus036ach/)
- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [ALFA 无线网卡在 NetHunter（Android）上——OTG 设置指南](/alfa-network/linux-setup-nethunter)
- [ALFA 无线网卡在 Kali Linux 上——监听模式与数据包注入](/alfa-network/linux-setup-kali/)
- [词汇表](/getting-started/glossary)——OTG、监听模式等名词的完整解释
- Realtek RTL8812AU 驱动（aircrack-ng 社群维护）：https://github.com/aircrack-ng/rtl8812au
- MediaTek MT76 系列驱动（社群维护，含 DKMS）：https://github.com/morrownr/mt76
- [Kali NetHunter 官方无线网卡兼容清单](https://www.kali.org/docs/nethunter/wireless-cards/)
- Kali NetHunter 官方项目（已搬迁至 GitLab）：https://gitlab.com/kalilinux/nethunter

**标签：** `kali` `nethunter` `android` `otg` `alfa` `awus036ach` `rtl8812au` `monitor-mode` `新手指南`
