---
title：“Hak5 Key Croc 原厂技术说明书与全功能操作手册”
model：“Key Croc”
manufacturer：“Hak5”
category：“硬件渗透测试 / HitM 植入设备”
docs_url：“https://docs.hak5.org/key-croc/”
version：“1.3”
locale：“zh-cn”
---

# Hak5 Key Croc 原厂技术说明书与全功能操作手册

> Hak5 Key Croc 是一款伪装为标准 USB 串联转接头的高阶硬件击键记录与注入植入设备。内部搭载嵌入式 Linux 操作系统，支持实时关键字模式匹配、带外无线数据回传与多向量攻击途径。

---

## 目录

- [**1. 产品概述与核心硬件架构**](#1-产品概述与核心硬件架构)
  - [1.1 Key Croc 原厂介绍 (The Key Croc by Hak5)](#1-1-key-croc-原厂介绍-the-key-croc-by-hak5)
- [**2. 操作模式与初始配置**](#2-操作模式与初始配置)
  - [2.1 Key Croc 基础架构 (Key Croc Basics)](#2-1-key-croc-基础架构-key-croc-basics)
  - [2.2 串口控制台访问 (Serial Console Access)](#2-2-串口控制台访问-serial-console-access)
  - [2.3 固件升级指引 (Updating the Firmware)](#2-3-固件升级指引-updating-the-firmware)
  - [2.4 原厂出厂重置 (Factory Reset)](#2-4-原厂出厂重置-factory-reset)
- [**3. 设备配置与键盘语言映射**](#3-设备配置与键盘语言映射)
  - [3.1 核心组态配置 (Configuration)](#3-1-核心组态配置-configuration)
  - [3.2 原厂默认值 (Default Settings)](#3-2-原厂默认值-default-settings)
  - [3.3 键盘语言与扫描码解析 (Understanding Languages)](#3-3-键盘语言与扫描码解析-understanding-languages)
- [**4. 文件系统架构与目录结构**](#4-文件系统架构与目录结构)
  - [4.1 文件与目录结构 (Files and Directory Structure)](#4-1-文件与目录结构-files-and-directory-structure)
  - [4.2 文件系统深入剖析 (Understanding the File System)](#4-2-文件系统深入剖析-understanding-the-file-system)
- [**5. 网络连接与远程 Cloud C² 运作**](#5-网络连接与远程-cloud-c-运作)
  - [5.1 让 Key Croc 连接上网 (Getting the Key Croc Online)](#5-1-让-key-croc-连接上网-getting-the-key-croc-online)
  - [5.2 配置 Hak5 Cloud C² (Configuring Cloud C²)](#5-2-配置-hak5-cloud-c-configuring-cloud-c)
- [**6. 载荷开发与 Ducky Script 指令集**](#6-载荷开发与-ducky-script-指令集)
  - [6.1 载荷开发基础 (Payload Development)](#6-1-载荷开发基础-payload-development)
  - [6.2 Ducky Script 语法架构 (Ducky Script Commands)](#6-2-ducky-script-语法架构-ducky-script-commands)
  - [6.3 常用指令快速速查表 (Command Quick Reference)](#6-3-常用指令快速速查表-command-quick-reference)
  - [6.4 MATCH 触发匹配指令 (The MATCH Command)](#6-4-match-触发匹配指令-the-match-command)
  - [6.5 SAVEKEYS 日志存储指令 (The SAVEKEYS Command)](#6-5-savekeys-日志存储指令-the-savekeys-command)
  - [6.6 ATTACKMODE 攻击模式指令 (The ATTACKMODE Command)](#6-6-attackmode-攻击模式指令-the-attackmode-command)
  - [6.7 USB 标识符与硬件克隆 (USB Identifiers & Hardware ID Cloning)](#6-7-usb-标识符与硬件克隆-usb-identifiers--hardware-id-cloning)
  - [6.8 QUACK 击键序列注入指令 (The QUACK Command)](#6-8-quack-击键序列注入指令-the-quack-command)
  - [6.9 进阶 QUACK 扩充语法 (Advanced QUACK Commands)](#6-9-进阶-quack-扩充语法-advanced-quack-commands)
  - [6.10 LED 状态指示灯语法 (The LED Command)](#6-10-led-状态指示灯语法-the-led-command)
- [**7. 高阶实战指南、技巧与实用示例**](#7-高阶实战指南技巧与实用示例)
  - [7.1 Key Croc 密码嗅探实战 (Password Sniffing with the Key Croc)](#7-1-key-croc-密码嗅探实战-password-sniffing-with-the-key-croc)
  - [7.2 Key Croc 1.3 新增功能深度解析 (New Features in Key Croc 1.3)](#7-2-key-croc-1-3-新增功能深度解析-new-features-in-key-croc-1-3)
  - [7.3 交互式载荷开发与调试 (Interactive Payload Development)](#7-3-交互式载荷开发与调试-interactive-payload-development)
  - [7.4 安装额外工具（如 Metasploit）(Installing Extras like Metasploit)](#7-4-安装额外工具如-metasploit-installing-extras-like-metasploit)
  - [7.5 高频实用载荷代码片段 (Helpful Payload Snippets)](#7-5-高频实用载荷代码片段-helpful-payload-snippets)

---

## 1. 产品概述与核心硬件架构

<!-- section：overview -->
### 硬件技术规格与原厂校准基准表

| 硬件组件名称 | 原厂技术规格说明 |
|---|---|
| **核心处理器 (SoC)** | Quad-core ARM Cortex processor @ 1.2 GHz |
| **系统内存 (RAM)** | 512 MB DDR3 RAM |
| **内部存储空间** | 8 GB SSD 高速闪存 |
| **无线通信接口** | 2.4 GHz 802.11 b/g/n，内置高感度陶瓷天线 |
| **物理接口 (USB)** | USB-A 公头（上游连接主机）/ USB-A 母口（下游连接键盘）|
| **机身外观尺寸** | 74 mm × 27 mm × 14 mm |
| **工作电源需求** | USB 总线供电（5 V DC，最大约 1 A）|
| **状态指示灯** | 多色可编程 RGB LED（攻击模式下默认完全熄灭）|
| **硬件控制开关** | 机身底部针孔内隐藏式维护模式按钮（需取卡针触发）|
| **默认串口波特率** | 115200 |
| **默认 SSH 登录凭证** | 用户名：root / 密码：hak5 croc |
| **默认网络 IP 地址** | 172.16.32.1 |

---

<!-- section：overview -->
### 1.1 Key Croc 原厂介绍 (The Key Croc by Hak5)

Key Croc 是一款具备模式匹配载荷系统与远程云端管理能力的智能键盘记录与渗透测试植入设备。本文档涵盖硬件运作与部署基础、通过 Linux Shell 控制台进行高阶渗透测试、Wi-Fi 网络连接配置、固件升级维护以及 DuckyScript 载荷开发工程。

![Key Croc](https://212197980-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2 F-MhLOzjhonMdC6SLKqRt%2Fuploads%2F5ZxTlaKQGYZ03j3E4 bah%2Fkeycroc%400.5 x.png?alt=media&token=e7d21d21-bfcd-41c4-b1b6-99f8b6cb8295)

> [!WARNING]
> 本文档生成的电子书 PDF 在某些查看设备上可能无法正确排版。如需获取最新版本技术说明，请参阅官方文档站点：<https://docs.hak5.org>。

#### 原厂基础规格指标
* 传输接口：标准 USB
* 支持协议：USB 2.0
* 频率范围：2.412 GHz ～ 2.4835 GHz
* 尺寸规格：74 mm × 27 mm × 14 mm
* 额定功率：5 W（USB 5 V 1 A）
* 运行温度：35ºC ～ 45ºC
* 存储温度：-20ºC ～ 50ºC
* 相对湿度：0% 至 90%（非冷凝状态）

#### 重要安全须知与法规警告
Key Croc 为专为经过授权的安全审计人员、渗透测试专家及学术研究人员设计的专业硬件工具。在未经系统所有权人明确书面授权的情况下，在任何主机或网络上部署监控设备均属非法行为。用户必须遵循当地相关法律法规。

---

## 2. 操作模式与初始配置

<!-- section：modes -->
### 2.1 Key Croc 基础架构 (Key Croc Basics)

Key Croc 具备两种完全独立、互斥的运行状态：**Attack Mode（攻击模式）** 与 **Arming Mode（维护模式）**。

| 功能与行为指标 | Attack Mode（默认攻击模式）| Arming Mode（维护模式）|
|---|---|---|
| **启用条件** | 插入 USB 端口并在下游连接键盘开机 | 开机时按压机身底部隐藏式按钮，或通过指令触发 |
| **LED 指示灯** | **完全熄灭**（极度隐蔽）| **蓝灯慢速闪烁**（呼吸模式）|
| **键盘透传转发** | 启用（零延迟即时透传）| 暂停 |
| **按键记录存储** | 启用（写入 `croc_char.log` 等）| 暂停 |
| **模式匹配引擎** | 启用（实时比对 `/payloads/`）| 暂停 |
| **主机端识别** | 复制自原键盘之 USB 设备 | 大容量 U 盘分区（“KeyCroc”）与串口 |
| **主要核心任务** | 隐蔽监听、记录与触发攻击载荷 | 参数配置、编辑载荷与导出外发数据 |

#### 进入维护模式 (Arming Mode) 步骤
1. 将 Key Croc 插入计算机 USB 端口，暂不连接下游键盘。
2. 使用智能手机的取卡针或回形针，轻按机身底部针孔内的隐藏式微动按钮。
3. 观察多色 LED 转变为**蓝灯闪烁**。
4. 目标操作系统将自动挂载标签为 **`KeyCroc`** 的 FAT32 U 盘大容量存储分区。

---

### 2.2 串口控制台访问 (Serial Console Access)

在维护模式下，Key Croc 会向目标主机提供 USB 串口 ACM 设备端点：

1. **Windows 平台**：使用 PuTTY 连接，连接类型选择 **Serial**，通信端口填入相应的 COM 端口（如 COM3），设置波特率为 **115200**。
2. **macOS / Linux 平台**：打开终端，执行连接指令：
   ```bash
   screen /dev/tty.usbmodem* 115200
   ```
3. 按下 Enter 键即可出现 Linux 登录提示，输入默认账号 `root` 与默认密码 `hak5 croc` 进入完整 Linux Shell。

---

<!-- section：recovery -->
### 2.3 固件升级指引 (Updating the Firmware)

Hak5 团队定期发布固件修补更新以强化系统稳定性并扩展功能模块：

1. 通过针孔按钮将 Key Croc 启动进入维护模式。
2. 访问挂载的 U 盘分区，将由 Hak5 官网下载之升级包（`upgrade-x.x.tar.gz`）直接放置于 U 盘根目录。
3. 安全弹出 U 盘分区，并重新插拔 Key Croc。
4. 升级程序自动展开：LED 将显示红蓝交替闪烁（约耗时数分钟）。
5. 升级完成后系统自动重启，LED 转为蓝灯闪烁，表示系统已升级完成。

> [!CAUTION]
> 固件更新进行期间，**绝对不可拔除电源**，否则将导致芯片固件损坏变砖。

---

### 2.4 原厂出厂重置 (Factory Reset)

当配置文件损坏或系统运行异常时，可执行出厂还原：
1. 进入维护模式，在 U 盘分区根目录下建立名为 `factoryreset` 的空白文本文件。
2. 安全弹出 U 盘并重新插拔 Key Croc。
3. 系统将检测到还原标记，自动重构 FAT32 分区并将系统文件恢复至出厂镜像状态。

---

## 3. 设备配置与键盘语言映射

### 3.1 核心组态配置 (Configuration)

Key Croc 的所有持久化全局配置均存放于 U 盘根目录的 `config.txt` 中。此文件采用直观的键值对（Key-Value）配置格式：

```ini
# Key Croc 全局组态配置文件示例
DUCKY_LANG us
WIFI_SSID“Target_Office_WiFi”
WIFI_PASS“SecurePassword123”
```

---

### 3.2 原厂默认值 (Default Settings)

* **默认语言**：`us`（美式英语）
* **默认 Wi-Fi 状态**：关闭（需于 `config.txt` 设置 SSID 与密码后自动启动）
* **默认本地 IP**：`172.16.32.1`（当启用 RNDIS/ECM 网络模拟时）
* **默认 SSH 账号**：`root`
* **默认 SSH 密码**：`hak5 croc`

---

### 3.3 键盘语言与扫描码解析 (Understanding Languages)

键盘传送至主机的原始数据为硬件扫描码（Scancodes），而非 ASCII 字符。不同国家与地区的键盘布局对同一个扫描码的符号映射截然不同：

* Key Croc 的 `languages/` 文件夹内置了全球数十种键盘布局映射文件（如 `us.json`，`de.json`，`uk.json`，`fr.json`）。
* 在 `config.txt` 中声明 `DUCKY_LANG <代码>`，系统在执行击键记录解码与 `QUACK` 击键序列注入时，即可完美还原正确字符，避免特殊符号错位。

---

## 4. 文件系统架构与目录结构

<!-- section：filesystem -->
### 4.1 文件与目录结构 (Files and Directory Structure)

挂载于维护模式下的 `KeyCroc` 大容量存储设备包含以下标准目录层级：

```
KeyCroc/
├── config.txt          # 全局设备与 Wi-Fi 联网配置文件
├── payloads/           # 启用中的攻击载荷目录（开机自动加载）
├── library/            # 载荷存储库与备用脚本
├── loot/               # 击键记录与外发机密存储目录
│   ├── croc_char.log   # 解码后的可读字符文本日志
│   ├── croc_raw.log    # 底层十六进制原始扫描码日志
│   └── matches.log     # MATCH 触发事件与执行历史日志
├── languages/          # 各国键盘语言映射数据表
├── tools/              # 自定义渗透脚本、第三方可执行文件与工具包
└── version.txt         # 当前安装之固件版本号标记
```

---

### 4.2 文件系统深入剖析 (Understanding the File System)

Key Croc 采用嵌入式 Linux 双分区设计：
1. **内部 ext4 根分区 (`/`)**：只读与系统保护分区，承载完整的 Debian Linux 系统内核与后台守护进程。
2. **udisk 大容量存储分区 (`/root/udisk`)**：FAT32 分区，供 USB Mass Storage 模式对外挂载。

> [!NOTE]
> 在攻击模式下，Key Croc 核心守护进程负责将记录按键写入缓存。为避免闪存损耗并确保数据完整落盘，请于载荷中调用 `sync` 指令。

---

## 5. 网络连接与远程 Cloud C² 运作

### 5.1 让 Key Croc 连接上网 (Getting the Key Croc Online)

Key Croc 内置 2.4 GHz 802.11 b/g/n Wi-Fi 芯片。在 `config.txt` 中填好无线网络连接信息后，Key Croc 开机时将在后台自动尝试连接指定无线接入点（AP）。

连接成功后，渗透测试人员可在同一局域网内直接通过 SSH 登录：
```bash
ssh root@<KeyCroc_IP>
```

---

### 5.2 配置 Hak5 Cloud C² (Configuring Cloud C²)

搭配 Hak5 Cloud C² 服务器，Key Croc 能化身为跨越全球互联网的带外控制节点：

1. 由 Cloud C² 网页控制台添加设备并下载专属设备证书包 `device.config`。
2. 将 `device.config` 复制放置于 Key Croc U 盘分区根目录。
3. 重启后，Key Croc 将自动与 Cloud C² 建立加密反向连接隧道。渗透测试人员无论身在何处，均可通过浏览器直接监控实时按键流、下发攻击指令或提取外发日志。

---

## 6. 载荷开发与 Ducky Script 指令集

<!-- section：payloads -->
### 6.1 载荷开发基础 (Payload Development)

Key Croc 载荷是一组扩展名为 `.txt` 的 Bash 与 DuckyScript 混编脚本，放置于 `/payloads/` 目录中。Key Croc 开机进入攻击模式时，后台核心将自动解析并实时加载该目录下的所有载荷。

一个标准的 Key Croc 载荷通常包含：
1. **触发器 (Trigger)**：通过 `MATCH` 指定启动载荷的关键字或正则表达式。
2. **前置配置 (Setup)**：调用 `ATTACKMODE` 准备攻击设备，设置 `LED` 状态。
3. **注入执行 (Execution)**：利用 `QUACK` 注入指令序列，或执行 Bash 脚本将数据外发。

---

### 6.2 Ducky Script 语法架构 (Ducky Script Commands)

Key Croc 原生兼容 DuckyScript 2.0 指令集，包括条件控制、变量存储以及专属于 HitM 架构的键盘隔离与日志提取语法。

---

### 6.3 常用指令快速速查表 (Command Quick Reference)

| 指令关键字 | 语法示例 | 核心功能说明 |
|---|---|---|
| `MATCH` | `MATCH password` | 监听键盘输入，一旦匹配指定关键字立即执行后续脚本 |
| `SAVEKEYS` | `SAVEKEYS /root/udisk/loot/keys.txt 20` | 将触发前最后 N 个按键存储至指定外发路径 |
| `ATTACKMODE` | `ATTACKMODE HID ETHERNET` | 声明模拟之复合 USB 设备端点（HID / 网卡 / 串口）|
| `CLONE` | `CLONE_VID` / `CLONE_PID` | 实时复制下游插入之物理键盘的硬件描述符 |
| `QUACK` | `QUACK GUI r` | 向上游目标计算机模拟击键注入 |
| `QUACK LOCK` | `QUACK LOCK` | 暂时阻断物理键盘转发，防止用户击键打乱脚本注入 |
| `LED` | `LED ATTACK` | 控制机身 RGB LED 指示灯颜色与闪烁行为 |

---

### 6.4 MATCH 触发匹配指令 (The MATCH Command)

`MATCH` 指令是 Key Croc 的灵魂核心。它支持三种匹配策略：

#### 1. 精准字符串匹配 (Exact Strings)
```bash
MATCH hello
QUACK STRING Target said hello!
```

#### 2. 多重关键字或条件分支 (Multiple Strings)
```bash
MATCH (root|admin|administrator)
# 当目标输入以上任一用户名时触发
```

#### 3. 正则表达式模式匹配 (Regular Expressions)
```bash
# 匹配特定格式的数据格式
MATCH [0-9]{5}(?:-[0-9]{4})?
```

---

### 6.5 SAVEKEYS 日志存储指令 (The SAVEKEYS Command)

当 `MATCH` 成功拦截到目标输入的关键字（如登录入口网址或账号）时，密码往往紧随其后。`SAVEKEYS` 能截取触发点前后特定长度的击键日志并存储至独立文件中：

```bash
MATCH login.example.com
SAVEKEYS /root/udisk/loot/example_login.txt 50
```

---

### 6.6 ATTACKMODE 攻击模式指令 (The ATTACKMODE Command)

Key Croc 支持动态切换 USB 身份：
* `ATTACKMODE HID`：仅模拟键盘注入。
* `ATTACKMODE HID ETHERNET`：同时模拟键盘与虚拟以太网网卡（建立本地 TCP/IP 渗透通道）。
* `ATTACKMODE HID SERIAL`：同时模拟键盘与串口控制台。

---

### 6.7 USB 标识符与硬件克隆 (USB Identifiers & Hardware ID Cloning)

为达成完美隐身，Key Croc 默认支持自动硬件描述符克隆（Hardware Cloning）。当真实键盘插入下游母口时，Key Croc 会读取该键盘的 VID（厂商 ID）、PID（产品 ID）、制造商字符串及序列号，并以此完全相同的硬件特征向上游目标计算机注册，彻底规避企业端点白名单防护！

---

### 6.8 QUACK 击键序列注入指令 (The QUACK Command)

`QUACK` 语法负责合成虚拟击键：
```bash
QUACK GUI r
QUACK DELAY 200
QUACK STRING powershell -ep bypass -w hidden
QUACK ENTER
```

---

### 6.9 进阶 QUACK 扩充语法 (Advanced QUACK Commands)

* `QUACK LOCK`：启动物理键盘隔离机制，此时目标用户敲击键盘的信号会被暂存阻断，直到注入结束后释放，避免字符交错导致攻击脚本崩溃。
* `QUACK UNLOCK`：解除键盘隔离。
* `QUACK CLEAR`：清除当前未处理完毕的按键缓冲区。

---

### 6.10 LED 状态指示灯语法 (The LED Command)

在维护模式或调试状态下，可自由调用灯号反馈：
* `LED ATTACK`：黄灯闪烁
* `LED SUCCESS`：常亮绿灯
* `LED FAIL`：常亮红灯
* `LED OFF`：完全熄灭（实战隐蔽模式）

---

## 7. 高阶实战指南、技巧与实用示例

### 7.1 Key Croc 密码嗅探实战 (Password Sniffing with the Key Croc)

展示如何针对热门网站或企业内部 SSO 登录页面编写 `MATCH` 规则。通过比对网址关键字后自动抓取接续输入的账号密码字符串，将凭证精确提取至外发文件中。

---

### 7.2 Key Croc 1.3 新增功能深度解析 (New Features in Key Croc 1.3)

Key Croc 1.3 固件带来多项重磅突破：
* 大幅强化按键缓冲区正则表达式匹配性能。
* 扩充对复合式 USB 设备（如包含轨迹球或音量旋钮的特殊键盘）的兼容性。
* 优化 Wi-Fi 自动重连与 Cloud C² 断线重试机制。

---

### 7.3 交互式载荷开发与调试 (Interactive Payload Development)

通过串口连接直接登录 Key Croc，使用 `tail -f /root/udisk/loot/croc_char.log` 实时观测当前打字流，并实时调试自定义的 `MATCH` 语法，大幅缩短载荷开发验证周期。

---

### 7.4 安装额外工具（如 Metasploit）(Installing Extras like Metasploit)

因为 Key Croc 搭载标准 ARM Linux 系统，在连上互联网后可直接利用 `apt-get` 安装 Python3、Nmap、Responder 或甚至精简版 Metasploit Framework，将 Key Croc 化身为插在键盘线上的自律型物理渗透主机！

---

### 7.5 高频实用载荷代码片段 (Helpful Payload Snippets)

收录官方社区精选的高频实用范本：
* Windows 一键反弹 Meterpreter Shell 范本
* 敏感文件背景隐蔽外发至 Cloud C² 脚本
* 目标用户离开座位锁定检测器
