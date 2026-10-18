---
title: "Hak5 Plunder Bug 原厂技术说明书与全功能操作手册"
model: "Plunder Bug"
manufacturer: "Hak5"
category: "双向被动/主动网络嗅探分流设备 (LAN Tap)"
docs_url: "https://docs.hak5.org/plunder-bug/"
version: "1.0"
locale: "zh-cn"
---

# Hak5 Plunder Bug 原厂技术说明书与全功能操作手册

> Hak5 出品的 Plunder Bug 是一款专为信息安全专业人员、网络稽核团队与系统管理员打造的口袋型乙太网络分流嗅探设备（LAN Tap）。通过其精密的硬件架构与 USB Type-C 接口，它能在不中断现有网络通信的情况下，以被动分流或主动注入方式透明嗅探 10/100 Mbps 双向网络数据包。

---

## 目录

- [**1. 产品概述与硬件架构**](#1-产品概述与硬件架构)
  - [1.1 Plunder Bug 原厂介绍](#11-plunder-bug-原厂介绍)
  - [1.2 技术规格与硬件校准基准表](#12-技术规格与硬件校准基准表)
- [**2. 硬件连接、接线与驱动程序配置**](#2-硬件连接接线与驱动程序配置)
  - [2.1 乙太网络链路实体分流接入 (Tapping an Ethernet Link)](#21-乙太网络链路实体分流接入-tapping-an-ethernet-link)
  - [2.2 跨平台驱动程序安装与配置 (Drivers)](#22-跨平台驱动程序安装与配置-drivers)
- [**3. 主动与被动运作模式及跨平台切换**](#3-主动与被动运作模式及跨平台切换)
  - [3.1 模式切换机制原理说明 (About Mode Switching)](#31-模式切换机制原理说明-about-mode-switching)
  - [3.2 Windows 平台模式切换作业进程](#32-windows-平台模式切换作业进程)
  - [3.3 macOS 平台模式切换作业进程](#33-macos-平台模式切换作业进程)
  - [3.4 Linux 平台模式切换作业进程](#34-linux-平台模式切换作业进程)
- [**4. 高端网络应用、数据包截获与维护指引**](#4-高端网络应用数据包截获与维护指引)
  - [4.1 简易交换机模式配置 (Using as a Simple Switch)](#41-简易交换机模式配置-using-as-a-simple-switch)
  - [4.2 Wireshark 与 tcpdump 实战嗅探流程](#42-wireshark-与-tcpdump-实战嗅探流程)
  - [4.3 故障排查、物理保养与维护准则](#43-故障排查物理保养与维护准则)

---

## 1. 产品概述与硬件架构

<!-- section：overview -->
本章节详细说明 Hak5 Plunder Bug 的产品架构、运作原理与原厂硬件规格基准表。

### 1.1 Plunder Bug 原厂介绍

Plunder Bug 是 Hak5 研发的极致微型化乙太网络 Tap 嗅探设备。传统网络分流器体积庞大、需要外置电源，或需通过繁复的网管交换器镜像端口（SPAN/Mirror Port）配置；Plunder Bug 则将所有分流逻辑浓缩于随身拇指大小的机身中。

内核设计特性包括：
- **双向零延迟分流**：串接于目标主机与上游网络设备之间，维持 10/100 Mbps 链路的全双工通信。
- **USB Type-C 高速输出**：分流数据直接封装为标准乙太网络讯框，通过 USB Type-C 端口即时传输至稽核专用笔记型电脑或 Android 智能型手机。
- **超低功耗驱动**：仅需由 USB 主机端汲取极微量电力（小于 250 mA），无需额外电源供应器。
- **双模运作机制**：支持纯被动监听模式（Passive Tap，对目标完全隐形，不发出任何数据包）与主动网络接口模式（Active Mode，可主动向网络发送诊断与测试流量）。

### 1.2 技术规格与硬件校准基准表

| 硬件组件项目 | 原厂官方技术规格基准 |
|---|---|
| **设备架构** | 口袋型主动/被动双模乙太网络分流器 (Active/Passive USB LAN Tap) |
| **网络接口** | 2 组 10/100 Fast Ethernet 端口 (RJ-45 串接式分流端) |
| **Tap 输出端口** | 1 组 USB Type-C 高速端口 |
| **供电需求** | 5 V DC 通过 USB Type-C 供电 (耗电量 < 250 mA) |
| **运作模式** | 被动分流模式 (Passive Tap)、主动虚拟网卡模式 (Active NIC)、简易交换机模式 |
| **内核芯片组** | 高性能低功耗 ASIX / Realtek 乙太网络控制芯片组 |
| **操作系统兼容性** | Linux (免驱动原生支持)、macOS (免驱动/专用驱动)、Windows (ASIX 驱动)、Android |

---

## 2. 硬件连接、接线与驱动程序配置

<!-- section：configuration -->
本章节提供 Plunder Bug 实体接线拓扑说明以及各大操作系统环境下的驱动程序安装指引。

### 2.1 乙太网络链路实体分流接入 (Tapping an Ethernet Link)

正确的实体连接是确保网络信号完整传输且不引发网络中断的前提：

```text
[ 上游网络设备 (交换器/路由器) ]
           │
           ▼ (RJ-45 网络线)
┌──────────────────────────────────────┐
│       Hak5 Plunder Bug (LAN Tap)     │
│   [RJ-45 埠 A]        [RJ-45 埠 B]   │
└──────────────────┬───────────────────┘
                   │ (USB Type-C 传输线)
                   ▼
       [ 稽核分析电脑 (Wireshark) ]
                   │
           ▲ (RJ-45 网络线)
           │
[ 目标主机 / 受测服务器 ]
```

1. **断开目标连接**：将原本插入目标主机的网络线拔出，插入 Plunder Bug 的 **RJ-45 端口 A**。
2. **连接目标主机**：使用随附的短跳线，一端插入 Plunder Bug 的 **RJ-45 端口 B**，另一端接回目标主机的网络端口。确认两侧 RJ-45 连接指示灯正常亮起。
3. **连接分析工作站**：使用 USB Type-C 传输线将 Plunder Bug 连接至测试用电脑。

### 2.2 跨平台驱动程序安装与配置 (Drivers)

- **Linux**：多数现代 Linux 内核（Kernel 4.x / 5.x / 6.x）均已内置 ASIX AX88179 / Realtek USB 乙太网络驱动程序，插入后立即识别为新的网络接口（如 `eth1` 或 `enp0s20u2`），完全免安装驱动。
- **macOS**：macOS 10.15 及更高版本具备内置 USB 网络驱动。插入后于“系统配置”>“网络”中即可看到添加之 USB 乙太网络设备。
- **Windows**：Windows 10 / 11 通常会自动经由 Windows Update 下载兼容驱动。若未自动辨识，请至 ASIX 官方网站下载最新版 USB-to-LAN 驱动程序安装套件。
- **Android**：支持具备 USB-OTG 功能之 Android 设备，配合专用数据包截取 App（如 Packet Capture 或 Wireshark for Android）即可实现掌上型即时网络监听。

---

## 3. 主动与被动运作模式及跨平台切换

<!-- section：features -->
本章节详细说明 Plunder Bug 的内核运作机制，包括被动监听模式与主动注入模式的切换作业流程。

### 3.1 模式切换机制原理说明 (About Mode Switching)

Plunder Bug 具备两种根本不同的工作模式：
1. **被动监听模式 (Passive Tap Mode)**：
   - USB 网络接口处于“纯接收”状态，硬件层级彻底阻断向网络发送任何数据包（TX 禁用）。
   - 在目标网络与安全性监控系统（IDS/IPS/NAC）眼中，该 Tap 完全隐形，不具备 IP 地址与 MAC 地址，达到 100% 隐蔽嗅探。
2. **主动网络接口模式 (Active NIC Mode)**：
   - 激活完整双向通信能力，分析电脑可直接通过 Plunder Bug 发送 ARP 查找、ping、通信端口扫描或注入测试数据包。
   - 适合用于现场故障检测、DHCP 测试或渗透测试主动攻击。

### 3.2 Windows 平台模式切换作业进程

#### 使用官方 PowerShell 自动化脚本 (`plunderbug.ps1`)：
```powershell
# 以系统管理员身分执行 PowerShell
.\plunderbug.ps1 -Mode Passive
# 系统将提示切换成功，并自动调整接口配置为纯嗅探状态
```

#### 手动配置流程：
1. 打开“网络和共用中心”>“变更接口卡配置”。
2. 找到 Plunder Bug 对应的乙太网络卡，右键点击“内容”。
3. 取消勾选“Client for Microsoft Networks”、“网际网络通信协定第 4 版 (TCP/IPv4)”及“IPv6”，仅保留“Npcap Packet Driver”或数据包截取驱动，避免本机操作系统主动向目标链路广播杂讯。

### 3.3 macOS 平台模式切换作业进程

#### 使用命令行脚本 (`plunderbug.sh`)：
```bash
chmod +x plunderbug.sh
sudo ./plunderbug.sh passive
```

#### 手动配置流程：
```bash
# 查询 Plunder Bug 接口识别码 (例如 en5)
networksetup -listallhardwareports

# 关闭接口上的自动 IPv4/IPv6 配置，进入被动嗅探模式
sudo ifconfig en5 up promisc -arp
```

### 3.4 Linux 平台模式切换作业进程

在 Linux 环境中，管理员享有最高弹性：
```bash
# 激活混杂模式 (Promiscuous Mode) 并停用 ARP 解析与发送
sudo ifconfig eth1 0.0.0.0 promisc -arp up

# 或使用 ip 工具链
sudo ip link set eth1 promisc on
sudo ip link set eth1 arp off
sudo ip link set eth1 up
```

---

## 4. 高端网络应用、数据包截获与维护指引

<!-- section：maintenance -->
本章节提供交换机模式应用教学、Wireshark 集成截获流程以及设备物理保养与维护指引。

### 4.1 简易交换机模式配置 (Using as a Simple Switch)

当不需要进行分流嗅探，而是需要临时在现场扩展乙太网络连接时，Plunder Bug 亦可通过内部交换逻辑运作：
- 将端口 A 与端口 B 分别连接至不同主机或交换器。
- 设备内部转发数据包，充当超微型 2 端口无网管交换机，确保链路连通性。

### 4.2 Wireshark 与 tcpdump 实战嗅探流程

在完成实体分流与被动模式配置后，即可启动分析软件：

```bash
# 使用 tcpdump 进行背景安静嗅探并存入 pcap 档案
sudo tcpdump -i eth1 -s 0 -w /tmp/capture_$(date +%Y%m%d_%H%M%S).pcap

# 在 Wireshark 中直接选取 Plunder Bug 接口
# 点击“Start Capture”，即可在数据包清单中即时分析 DNS 查询、HTTP 流量、SMB 协商等
```

### 4.3 故障排查、物理保养与维护准则

#### 常见问题排查：
- **RJ-45 链路灯未亮**：检查网络线线芯是否完好，确认上游交换器与目标主机端口口均已通电。
- **电脑无法辨识 USB 设备**：确认使用的 USB Type-C 传输线具备高速数据传输能力（非仅充电线），更换主机端端口测试。
- **Wireshark 看不到数据包**：确认网络接口已打开混杂模式（Promiscuous Mode）。

#### 物理保养规范：
- 避免在潮湿、高静电或强磁场环境下操作。
- 拔插 RJ-45 卡榫时请勿暴力拉扯，保持针脚清洁以维持信号传输品质。
