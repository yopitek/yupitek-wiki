---
title：“Hak5 Shark Jack 原厂技术说明书与全功能操作手册”
model：“Shark Jack”
manufacturer：“Hak5”
category：“便携式网络渗透测试植入设备”
docs_url：“https://docs.hak5.org/shark-jack/”
version：“2.0”
locale：“zh-cn”
---

# Hak5 Shark Jack 原厂技术说明书与全功能操作手册

> Hak5 Shark Jack 是一款专为网络侦察与隐蔽渗透设计的口袋型网络攻击硬件。外观为精巧的 RJ-45 接头外形，内置 Linux 系统、专属锂电池、580 MHz 处理器与快速以太网芯片，插入目标网络插孔即可于数秒内全自动执行网络资产扫描与凭据外发。

---

## 目录

- [**1. 产品概述与核心硬件架构**](#1-产品概述与核心硬件架构)
  - [1.1 Shark Jack 原厂介绍](#1-1-shark-jack-原厂介绍)
  - [1.2 核心运行原理与功能特性 (Shark Jack Basics)](#1-2-核心运行原理与功能特性-shark-jack-basics)
  - [1.3 原厂出厂默认值与连接参数 (Default Settings)](#1-3-原厂出厂默认值与连接参数-default-settings)
- [**2. 开箱入门、连接与 sharkjack.sh 核心实用程序**](#2-开箱入门连接与-sharkjacksh-核心实用程序)
  - [2.1 开箱与初始配置指引 (Unboxing and Setup)](#2-1-开箱与初始配置指引-unboxing-and-setup)
  - [2.2 sharkjack.sh 官方工具库解析 (Using sharkjack.sh)](#2-2-sharkjacksh-官方工具库解析-using-sharkjacksh)
  - [2.3 两大核心维护指令 (Two Key Commands)](#2-3-两大核心维护指令-two-key-commands)
  - [2.4 第一支网络载荷编写实战 (Writing a Simple Payload)](#2-4-第一支网络载荷编写实战-writing-a-simple-payload)
- [**3. 固件更新与出厂维护程序**](#3-固件更新与出厂维护程序)
  - [3.1 手动固件升级程序 (Manual Upgrade)](#3-1-手动固件升级程序-manual-upgrade)
  - [3.2 通过网络空中线上升级 (Over-the-Air Upgrade)](#3-2-通过网络空中线上升级-over-the-air-upgrade)
- [**4. 载荷开发与 DuckyScript 指令集参考**](#4-载荷开发与-duckyscript-指令集参考)
  - [4.1 载荷开发核心架构 (Payload Development Basics)](#4-1-载荷开发核心架构-payload-development-basics)
  - [4.2 NETMODE 网络模式配置指令 (The NETMODE Command)](#4-2-netmode-网络模式配置指令-the-netmode-command)
  - [4.3 LED 状态指示灯指令 (The LED Command)](#4-3-led-状态指示灯指令-the-led-command)
  - [4.4 SWITCH 硬件切换开关指令 (The SWITCH Command)](#4-4-switch-硬件切换开关指令-the-switch-command)
  - [4.5 BATTERY 电池状态指令 (The BATTERY Command)](#4-5-battery-电池状态指令-the-battery-command)
  - [4.6 SERIAL_WRITE 串口输出指令 (The SERIAL_WRITE Command)](#4-6-serial_write-串口输出指令-the-serial_write-command)
  - [4.7 Hak5 Cloud C² 集成指令 (The Cloud C2 Commands)](#4-7-hak5-cloud-c-集成指令-the-cloud-c2-commands)
  - [4.8 系统预先安装之工具库 (Included Tools)](#4-8-系统预先安装之工具库-included-tools)
- [**5. 载荷管理与 Cloud C² 集成**](#5-载荷管理与-cloud-c-集成)
  - [5.1 载荷存储与管理架构 (Payload Management)](#5-1-载荷存储与管理架构-payload-management)
  - [5.2 LIST 载荷清单查询指令 (The LIST Command)](#5-2-list-载荷清单查询指令-the-list-command)
  - [5.3 ACTIVATE 载荷动态启用指令 (The ACTIVATE Command)](#5-3-activate-载荷动态启用指令-the-activate-command)
- [**6. 故障排除、硬件改动技巧与规格安全**](#6-故障排除硬件改动技巧与规格安全)
  - [6.1 固件救援与修复模式 (Firmware Recovery)](#6-1-固件救援与修复模式-firmware-recovery)
  - [6.2 利用手机进行反向充电与供电技巧 (Charge from your Phone)](#6-2-利用手机进行反向充电与供电技巧-charge-from-your-phone)
  - [6.3 结合 Plunder Bug 物理接线技巧 (Using with Plunder Bug)](#6-3-结合-plunder-bug-物理接线技巧-using-with-plunder-bug)
  - [6.4 Android 串口连接线配置 (Android Serial Setup)](#6-4-android-串口连接线配置-android-serial-setup)
  - [6.5 官方技术规格基准表 (Hardware Specifications)](#6-5-官方技术规格基准表-hardware-specifications)
  - [6.6 重要安全指引与法规声明 (Safety and Warnings)](#6-6-重要安全指引与法规声明-safety-and-warnings)

---

## 1. 产品概述与核心硬件架构

<!-- section：overview -->
### 1.1 Shark Jack 原厂介绍

Hak5 Shark Jack 是一款精巧型便携式网络渗透测试植入设备。外观集成了标准 RJ-45 公头，体积极其小巧，可随身放入口袋或钥匙扣。

与需要漫长开机配置的笔记本电脑不同，Shark Jack 专为极速实战所打造：机身内置独立充电式锂电池，只要将其推入目标企业的任何局域网（LAN）插座，Shark Jack 便会在数秒内完成开机、自动通过 DHCP 获取 IP、以静默方式进行周边主机扫描、监听敏感数据包、或通过 Cloud C² 建立反向加密远程连接，并在任务完成后借由多色 LED 闪烁绿灯向操作员汇报成功。

### 硬件技术规格与原厂校准基准表

| 硬件组件名称 | 官方技术规格说明 |
|---|---|
| **核心处理器 (SoC / CPU)** | Single Core MIPS @ 580 MHz |
| **系统内存 (RAM)** | 64 MB DDR2 |
| **内部存储空间 (Storage)** | 128 MB High-Speed Flash 高速闪存 |
| **以太网接口 (Network)** | 10/100 Fast Ethernet RJ-45 接口 |
| **内部自主电源 (Battery)** | 内置充电式锂电池（支持独立免插电作业）|
| **硬件模式切换开关** | 3 段式实体切换滑动开关（Arming 维护、Off 关闭/充电、Attack 攻击）|
| **状态指示模块** | 多色可编程 RGB LED 指示灯 |
| **默认网络 IP / 子网掩码** | 172.16.24.1 / 255.255.255.0 |

---

<!-- section：features -->
### 1.2 核心运行原理与功能特性 (Shark Jack Basics)

Shark Jack 的核心作战哲学在于“即插即跑、快速撤离”（Plug and Pwn）：
1. **独立供电运行**：内置锂电池可提供约 10 至 15 分钟的独立高负载作战时间，完全无需外接电源线即可完成一次完整的内部网络勘察。
2. **三段物理模式开关**：
   - **Arming 模式（靠近 USB 口侧）**：维护模式，启动内部 DHCP 服务器与 SSH 服务，供工程师连接电脑调试与管理载荷。
   - **Off / Charge 模式（中间位置）**：关闭系统，连接 USB-C 时对内置电池进行充电。
   - **Attack 模式（靠近 RJ-45 口侧）**：实战攻击模式，插入网络孔后自动执行当前启用的载荷脚本。
3. **实时视觉反馈**：内置可自定义 RGB LED，让操作人员在不携带屏幕的情况下对扫描进度与状态一目了然。

---

### 1.3 原厂出厂默认值与连接参数 (Default Settings)

当处于 Arming 维护模式下时，Shark Jack 提供下列标准管理参数：
- **以太网接口 IP**：`172.16.24.1`
- **子网掩码**：`255.255.255.0`
- **DHCP 分配范围**：`172.16.24.10` 至 `172.16.24.250`
- **SSH 登录端口**：`22`
- **默认管理员账号**：`root`
- **默认原厂密码**：`armshark`

---

<!-- section：configuration -->
## 2. 开箱入门、连接与 sharkjack.sh 核心实用程序

### 2.1 开箱与初始配置指引 (Unboxing and Setup)

1. 将 Shark Jack 实体开关切换至中间“Off”位置，通过 USB-C 数据线连接电源充电 1 小时。
2. 切换开关至“Arming”模式，将 RJ-45 网线一端接至 Shark Jack，另一端接至管理用计算机。
3. 管理计算机的网卡将自动取得 `172.16.24.x` 的 IP 地址。
4. 打开终端，执行 SSH 连接：
   ```bash
   ssh root@172.16.24.1
   # 提示输入密码时键入：armshark
   ```
5. 连接成功后，系统将显示 ASCII 鲨鱼图腾与终端提示符。

---

### 2.2 sharkjack.sh 官方工具库解析 (Using sharkjack.sh)

`sharkjack.sh` 是 Shark Jack 系统的核心 API 指令库，封装了网络切换、LED 指示灯控制与电源管理等底层操作：
- `LED R FAST`：红色快速闪烁。
- `LED G SOLID`：绿色常亮。
- `NETMODE DHCP_CLIENT`：要求网络芯片向环境 DHCP 服务器申请 IP。
- `NETMODE STATIC 192.168.1.50 255.255.255.0 192.168.1.1`：设置静态 IP。

---

### 2.3 两大核心维护指令 (Two Key Commands)

原厂提供两支极度便利的专用指令：
1. `sharkjack.sh`：直接在终端打印完整的指令说明手册。
2. `cloudc2_connect`：快速验证与测试 Hak5 Cloud C² 云端通道状态。

---

### 2.4 第一支网络载荷编写实战 (Writing a Simple Payload)

所有载荷均为标准 Bash 脚本，存储于 `/root/payload/payload.sh`。以下为经典的内网资产探索载荷示例：

```bash
#!/bin/bash
# 标题：简易 Nmap 内网资产探索载荷
# 说明：自动获取 IP，扫描同网段存活主机并存盘

# 1. 设置 LED 为品红色慢闪，提示正在获取 IP
LED M SLOW
NETMODE DHCP_CLIENT

# 2. 等待网络接口获取有效默认网关
while [ -z“$GATEWAY”]；do
    GATEWAY=$(route -n | grep 'UG[ 	]' | awk '{print $2}')
    sleep 1
done

# 3. 变更 LED 为黄色快闪，代表正在进行 Nmap 扫描
LED Y FAST
SUBNET=$(ip -o -f inet addr show eth0 | awk '{print $4}')
nmap -sn $SUBNET -oN /root/loot/hosts.txt

# 4. 扫描完成，绿色常亮 5 秒后安全关机
LED G SOLID
sleep 5
LED OFF
poweroff
```

---

<!-- section：maintenance -->
## 3. 固件更新与出厂维护程序

### 3.1 手动固件升级程序 (Manual Upgrade)

1. 由 Hak5 官方下载中心下载最新固件文件（`upgrade-x.x.bin`）。
2. 在 Arming 模式下通过 SCP 将固件传送至设备：
   ```bash
   scp upgrade-x.x.bin root@172.16.24.1:/tmp/
   ```
3. 在 SSH 终端执行升级指令：
   ```bash
   sysupgrade -n /tmp/upgrade-x.x.bin
   ```
4. 升级期间 LED 将呈现蓝红交替闪烁，切勿断电或拨动模式开关。

---

### 3.2 通过网络空中线上升级 (Over-the-Air Upgrade)

若 Shark Jack 已配置可连上外部互联网，可直接执行：
```bash
upgrade
```
系统将自动检测官方服务器之最新固件版本并完成一键升级。

---

## 4. 载荷开发与 DuckyScript 指令集参考

### 4.1 载荷开发核心架构 (Payload Development Basics)

Shark Jack 的载荷采用结合 Bash 与 Hak5 扩展语法架构。脚本需赋予可执行权限（`chmod +x payload.sh`），且通常划分为四个标准作战阶段：
1. **初始化阶段**：设置 LED 与网络模式。
2. **获取网络阶段**：等待 DHCP 分配或配置静态 IP。
3. **作战执行阶段**：执行 nmap、tcpdump、responder 或自定义 Python 探索脚本。
4. **汇报与安全收尾**：将战果（Loot）同步至 Cloud C² 或本机，并执行 `poweroff` 关机保护硬件。

---

### 4.2 NETMODE 网络模式配置指令 (The NETMODE Command)

- `NETMODE DHCP_CLIENT`：默认攻击模式，充当一般终端设备向目标网段请求 IP。
- `NETMODE DHCP_SERVER`：启用内置 dnsmasq 服务，向连接的对象发送 IP（用于 Arming 模式或隔离测试）。
- `NETMODE STATIC <IP> <NETMASK> <GATEWAY>`：手动指定静态 IP，适合针对无 DHCP 服务器之封闭工控或服务器网段。

---

### 4.3 LED 状态指示灯指令 (The LED Command)

语法为：`LED <颜色> <模式>`
- **颜色**：`R`（红）、`G`（绿）、`B`（蓝）、`Y`（黄）、`C`（青）、`M`（品红）、`W`（白）、`OFF`（熄灭）。
- **模式**：`SOLID`（常亮）、`SLOW`（慢闪）、`FAST`（快闪）、`VERYFAST`（极速闪烁）。

---

### 4.4 SWITCH 硬件切换开关指令 (The SWITCH Command)

通过 `SWITCH` 指令可在脚本执行过程中即时判断实体拨键是否被操作员拨动，以实现即时安全中断。

---

### 4.5 BATTERY 电池状态指令 (The BATTERY Command)

```bash
# 获取当前电池电量百分比
BATTERY_LEVEL=$(sharkjack.sh battery)
echo“Current Battery：$BATTERY_LEVEL%”
```

---

### 4.6 SERIAL_WRITE 串口输出指令 (The SERIAL_WRITE Command)

当搭配专用调试线时，可使用 `SERIAL_WRITE` 将调试日志同步输出至物理串口终端。

---

### 4.7 Hak5 Cloud C² 集成指令 (The Cloud C2 Commands)

Shark Jack 深度集成 Hak5 Cloud C²，支持下列核心 C2 指令：
- `C2CONNECT`：后台启动 Cloud C² 代理程序并连接。
- `C2EXFIL <文件路径>`：自动将扫描结果或外发文件上传至指定 Cloud C² 服务器。

---

### 4.8 系统预先安装之工具库 (Included Tools)

系统内部集成众多开源安全瑞士军刀工具：
- **网络探测**：`nmap`、`arp-scan`、`netcat` (nc)
- **传输工具**：`curl`、`wget`、`scp`、`ssh`
- **解释环境**：完整支持 Bash 与轻量化 Python 运行环境

---

## 5. 载荷管理与 Cloud C² 集成

### 5.1 载荷存储与管理架构 (Payload Management)

Shark Jack 的载荷目录位于 `/root/payload/`。实战中可存放多组载荷脚本（如 `payload1.sh`、`payload2.sh`）。

---

### 5.2 LIST 载荷清单查询指令 (The LIST Command)

通过 `sharkjack.sh list` 可列出当前存储于设备内的所有可用攻击载荷名称与描述。

---

### 5.3 ACTIVATE 载荷动态启用指令 (The ACTIVATE Command)

通过 `sharkjack.sh activate <名称>`，可即时将指定载荷软链接至当前攻击模式启动目标。

---

## 6. 故障排除、硬件改动技巧与规格安全

### 6.1 固件救援与修复模式 (Firmware Recovery)

若升级中断导致设备无法正常开机：
1. 将开关拨至 Arming 模式。
2. 按住机身内部恢复按钮（若有配备），连接电源开机。
3. 通过默认恢复 IP `192.168.1.1` 进入 Web 恢复界面重新烧录原厂固件。

---

### 6.2 利用手机进行反向充电与供电技巧 (Charge from your Phone)

Shark Jack 的 USB Type-C 接口支持标准 5 V 输入。在户外移动测试中，只需一条 USB-C 双头 OTG 数据线，即可直接利用 Android 智能手机对 Shark Jack 进行应急充电或长时间供电。

---

### 6.3 结合 Plunder Bug 物理接线技巧 (Using with Plunder Bug)

将 Shark Jack 插入 Hak5 Plunder Bug 以太网分流器（Tap），即可将 Shark Jack 转换为便携式隐蔽数据包侧录站，实现对目标线路的透明 Sniffing。

---

### 6.4 Android 串口连接线配置 (Android Serial Setup)

通过专用 Serial-to-USB 线缆搭配 Android 终端模拟器 App，可直接在手机屏幕上查看 Shark Jack 开机日志与交互式 Shell。

---

### 6.5 官方技术规格基准表 (Hardware Specifications)

- **处理器规格**：580 MHz MIPS 架构 Single Core
- **内存规格**：64 MB DDR2
- **存储规格**：128 MB 闪存
- **尺寸与重量**：62 mm × 21 mm × 12 mm，重约 15 克
- **通信标准**：IEEE 802.3 10/100 Base-T

---

### 6.6 重要安全指引与法规声明 (Safety and Warnings)

1. **锂电池维护**：切勿在高于 60°C 的极端高温环境或车内暴晒存放 Shark Jack。
2. **网络安全授权**：严禁将本设备未经授权连接至未获测试许可之第三方网络设施。
