---
title：“Hak5 WiFi Pineapple Mark VII 原厂技术说明书与全功能操作手册”
model：“WiFi Pineapple Mark VII”
manufacturer：“Hak5”
category：“无线网络安全审计与流氓 AP 测试平台”
docs_url：“https://docs.hak5.org/wifi-pineapple/”
version：“2.0”
locale：“zh-cn”
---

# Hak5 WiFi Pineapple Mark VII 原厂技术说明书与全功能操作手册

> Hak5 出品的 WiFi Pineapple Mark VII 是全球无线网络安全审计、红队渗透测试与流氓 AP（Rogue AP）攻击演练的行业黄金标准。配备 3 组专属特化 2.4 GHz 射频芯片、单核心 MIPS 580 MHz 网络处理器、256 MB 内存与 2 GB eMMC 高速存储，结合专属 PineAP 攻击套件与 Campaigns 自动化作战引擎。

---

## 目录

- [**1. 产品概述与核心硬件架构**](#1-产品概述与核心硬件架构)
  - [1.1 WiFi Pineapple Mark VII 原厂介绍](#1-1-wifi-pineapple-mark-vii-原厂介绍)
  - [1.2 硬件技术规格与原厂校准基准表](#1-2-硬件技术规格与原厂校准基准表)
- [**2. 初次配置、系统连接与互联网共享**](#2-初次配置系统连接与互联网共享)
  - [2.1 物理连接与通电指示 (Connecting)](#2-1-物理连接与通电指示-connecting)
  - [2.2 配置向导与初始化 (Setting up)](#2-2-配置向导与初始化-setting-up)
  - [2.3 Linux 系统连接配置指南](#2-3-linux-系统连接配置指南)
  - [2.4 Windows 系统连接配置指南](#2-4-windows-系统连接配置指南)
  - [2.5 通过无线 Wi-Fi 进行无网线配置](#2-5-通过无线-wi-fi-进行无网线配置)
  - [2.6 USB U 盘离线自动部署 (Setup by USB Disk)](#2-6-usb-u 盘离线自动部署-setup-by-usb-disk)
- [**3. Web UI 图形化界面、Recon、PineAP 与 Cloud C²**](#3-web-ui-图形化界面 reconpineap-与-cloud-c)
  - [3.1 Web UI 界面架构导览 (Introduction to the UI)](#3-1-web-ui-界面架构导览-introduction-to-the-ui)
  - [3.2 仪表盘监控与实时状态 (Dashboard)](#3-2-仪表盘监控与实时状态-dashboard)
  - [3.3 Campaigns 自动化作战任务 (Campaigns)](#3-3-campaigns-自动化作战任务-campaigns)
  - [3.4 PineAP 流氓 AP 攻击引擎核心 (PineAP)](#3-4-pineap-流氓-ap-攻击引擎核心-pineap)
  - [3.5 Recon 全频段无线频谱侦查 (Recon)](#3-5-recon-全频段无线频谱侦查-recon)
  - [3.6 Handshake 握手包收集与管理 (Handshakes)](#3-6-handshake-握手包收集与管理-handshakes)
  - [3.7 Modules 扩展模块管理系统 (Modules)](#3-7-modules-扩展模块管理系统-modules)
  - [3.8 系统配置、更新与偏好设置 (Settings)](#3-8-系统配置更新与偏好设置-settings)
  - [3.9 Hak5 Cloud C² 云端集中纳管 (Cloud C²)](#3-9-hak5-cloud-c-云端集中纳管-cloud-c)
- [**4. Wi-Fi 基础理论、射频技术与 802.11 帧架构**](#4-wi-fi-基础理论射频技术与-80211-帧架构)
  - [4.1 无线网络通信原理 (Introduction to WiFi)](#4-1-无线网络通信原理-introduction-to-wifi)
  - [4.2 射频芯片与角色分工 (Radios and Chipsets)](#4-2-射频芯片与角色分工-radios-and-chipsets)
  - [4.3 Station 与 AP 运行模式剖析](#4-3-station-与-ap-运行模式剖析)
  - [4.4 发射功率与高增益天线原理 (Power & Antennas)](#4-4-发射功率与高增益天线原理-power--antennas)
  - [4.5 信道划分与全球区域法规限制](#4-5-信道划分与全球区域法规限制)
  - [4.6 802.11 帧结构与管理帧解析](#4-6-80211-帧结构与管理帧解析)
  - [4.7 帧注入与客户端状态机 (Frame Injection)](#4-7-帧注入与客户端状态机-frame-injection)
- [**5. 开发者资源与自定义模块开发**](#5-开发者资源与自定义模块开发)
  - [5.1 官方开发者资源库 (Developer Resources)](#5-1-官方开发者资源库-developer-resources)
  - [5.2 模块架构与社区软件包库贡献指南](#5-2-模块架构与社区软件包库贡献指南)
- [**6. 常见问答、故障排除、固件升级与硬件改动**](#6-常见问答故障排除固件升级与硬件改动)
  - [6.1 macOS 平台连接支持 (macOS Support)](#6-1-macos-平台连接支持-macos-support)
  - [6.2 互联网共享连接建立与排查](#6-2-互联网共享连接建立与排查)
  - [6.3 忘记密码还原与原厂出厂重置 (Factory Reset)](#6-3-忘记密码还原与原厂出厂重置-factory-reset)
  - [6.4 固件升级与救援恢复模式 (Firmware Recovery)](#6-4-固件升级与救援恢复模式-firmware-recovery)
  - [6.5 兼容 802.11 ac 5 GHz 网卡清单 (Compatible Adapters)](#6-5-兼容-80211 ac-5-ghz-网卡清单-compatible-adapters)
  - [6.6 MK7 LED 改装与 Kismet 保护外壳安装](#6-6-mk7-led-改装与-kismet-保护外壳安装)

---

## 1. 产品概述与核心硬件架构

<!-- section：overview -->
### 1.1 WiFi Pineapple Mark VII 原厂介绍

Hak5 WiFi Pineapple Mark VII 是专为网络安全从业人员、红队演练专家以及合规性审计人员量身打造的第七代旗舰级无线渗透测试硬件。

相较于前代产品，Mark VII 进行了彻底的架构重构，内置 3 组独立且各司其职的 2.4 GHz 802.11 b/g/n 射频芯片，实现了同频段下“一组专职被动频谱侦察、一组专职流氓 AP 广播与凭据诱捕、一组专职连接注入与干扰”的三工并行能力，彻底消除了以往单一射频在切换模式时所造成的频谱监听盲区。

配合直观流畅的 Web UI 与 Hak5 Cloud C² 云端纳管平台，安全团队可将 Mark VII 隐蔽部署于目标建筑物内，并由千里之外的远程指挥中心进行实时的无线资产测绘与凭据侧录。

### 1.2 硬件技术规格与原厂校准基准表

| 硬件组件项目 | 官方技术规格基准说明 |
|---|---|
| **核心处理器 (SoC / CPU)** | Single Core MIPS 24 KEc 580 MHz |
| **系统内存 (RAM)** | 256 MB DDR2 |
| **内部存储空间 (Storage)** | 2 GB eMMC 高速闪存 |
| **无线射频模块** | 3 组独立特化之 2.4 GHz 802.11 b/g/n 芯片组（硬件滤波防干扰）|
| **扩展连接接口** | USB-C 供电/以太网接口、USB 2.0 Host（支持 5 GHz 双频扩展）|
| **天线配置** | 3 支高增益全向式 RP-SMA 旋钮式天线 |
| **状态指示模块** | 多色可编程 RGB LED 系统状态指示灯 |
| **默认管理 IP / 子网掩码** | 172.16.42.1 / 255.255.255.0 |

---

<!-- section：configuration -->
## 2. 初次配置、系统连接与互联网共享

### 2.1 物理连接与通电指示 (Connecting)

1. 将随附的 3 支天线拧紧安装至 Mark VII 机身上的 RP-SMA 接口。
2. 使用 USB Type-C 连接线将设备连接至测试电脑或合格之 5 V 2 A 电源适配器。
3. 机身 LED 将亮起蓝灯闪烁，代表嵌入式 Linux 操作系统正在启动（约耗时 30 至 60 秒）。
4. 当 LED 呈现常亮状态时，代表系统已开机完成并进入就绪模式。

---

### 2.2 配置向导与初始化 (Setting up)

1. 打开浏览器，输入管理地址：`http://172.16.42.1:1471`。
2. 系统将自动重定向至“Setup Wizard”初次配置向导。
3. 依序配置 root 管理员密码、时区以及管理用 Wi-Fi AP 之 SSID 与连接密钥。
4. 保存配置后重新加载，即可使用新密码登录正式管理控制台。

---

### 2.3 Linux 系统连接配置指南

在 Linux 环境下，可使用原厂提供的 `wp7.sh` 配置脚本，一键配置 iptables 转发与网络共享：
```bash
sudo ./wp7.sh
```
选择对应外网网卡与 USB 网卡接口，脚本将自动建立 NAT 规则，使 Mark VII 具备访问外网能力。

---

### 2.4 Windows 系统连接配置指南

在 Windows 10 / 11 中：
1. 进入“网络和共享中心”$
ightarrow$“更改适配器设置”。
2. 在连接互联网的网卡（Wi-Fi 或以太网）上右键选择“属性”。
3. 切换至“共享”标签页，勾选“允许其他网络用户通过此计算机的 Internet 连接来连接”，并在下拉菜单中选择 WiFi Pineapple 的虚拟以太网网卡。

---

### 2.5 通过无线 Wi-Fi 进行无网线配置

在无 USB 连接线的环境下，Mark VII 开机后会自动广播名为 `Pineapple_xxxx` 的开放式配置 AP。管理员可直接以笔记本或手机 Wi-Fi 连入该热点完成配置。

---

### 2.6 USB U 盘离线自动部署 (Setup by USB Disk)

将配置好的 `pineapple.tar.gz` 镜像文件放置于 FAT32 格式 U 盘根目录，插入 Mark VII 开机，系统将全自动完成静默配置，无需任何人机交互。

---

<!-- section：features -->
## 3. Web UI 图形化界面、Recon、PineAP 与 Cloud C²

### 3.1 Web UI 界面架构导览 (Introduction to the UI)

Mark VII 拥有经过彻底美化与响应式设计的现代化管理界面，左侧导航栏分为：
- **Dashboard（仪表盘）**
- **Campaigns（作战任务）**
- **PineAP（流氓 AP 核心）**
- **Recon（全频段侦查）**
- **Modules（扩展模块）**
- **Settings（系统配置）**

---

### 3.2 仪表盘监控与实时状态 (Dashboard)

仪表盘实时汇总当前系统资源负载、CPU 使用率、内存消耗、网络传输量、已关联客户端以及当前正在进行的作战模式。

---

### 3.3 Campaigns 自动化作战任务 (Campaigns)

Campaigns 功能允许安全专家预先定义复合式作战场景：
- 定时自动启动 Recon 扫描周围 5 分钟。
- 自动将发现的所有未加密热点加入 SSID Pool。
- 启动 PineAP 开放热点诱捕与凭据钓鱼。
- 任务结束后全自动产出专业 PDF / HTML 审计报告。

---

### 3.4 PineAP 流氓 AP 攻击引擎核心 (PineAP)

PineAP 是 WiFi Pineapple 系列闻名全球的核心引擎：
- **Beacon Response**：监听客户端发送的 Probe Request 广播，并伪造为该 SSID 予以响应。
- **SSID Pool**：维护动态热点名称数据库，支持以千计之热点轮播。
- **Karma 攻击现代演进版**：完美适配现代智能手机之随机 MAC 与加密保护机制。

---

### 3.5 Recon 全频段无线频谱侦查 (Recon)

利用独立的监听芯片进行全信道扫描，实时分析各 AP 的信道占用度、加密标准（WEP、WPA、WPA2、WPA3-SAE、OWE），并精确捕获每一个空中数据包的信号强度变化。

---

### 3.6 Handshake 握手包收集与管理 (Handshakes)

支持自动监听并截获 WPA/WPA2 4-way Handshake 与 PMKID。捕获之握手包可在 Web UI 中直接一键下载为兼容 hashcat 与 John the Ripper 之标准格式。

---

### 3.7 Modules 扩展模块管理系统 (Modules)

通过丰富的社区模块中心，可一键安装 Nmap 网络扫描、Evil Portal 自定义强制门户、DNS 劫持转向等第三方高阶攻击工具。

---

### 3.8 系统配置、更新与偏好设置 (Settings)

管理 root 密码、修改主机名、配置时区、调整 LED 灯号颜色以及一键备份所有作战配置。

---

### 3.9 Hak5 Cloud C² 云端集中纳管 (Cloud C²)

将 Mark VII 注册绑定至企业私有 Cloud C² 服务器，可在任何具备互联网的地方，穿越 NAT 与防火墙，实现远程云端操作与实时警报接收。

---

## 4. Wi-Fi 基础理论、射频技术与 802.11 帧架构

### 4.1 无线网络通信原理 (Introduction to WiFi)

深入解析 IEEE 802.11 射频传播特性、2.4 GHz 与 5 GHz 频段衰减差异以及半双工（Half-Duplex）CSMA/CA 冲突避免机制。

---

### 4.2 射频芯片与角色分工 (Radios and Chipsets)

详细剖析 Mark VII 内部 3 组无线网卡的微架构分工：
- **Radio 0 (wlan0)**：默认负责 AP 广播与客户端连接。
- **Radio 1 (wlan1)**：默认作为客户端外网连接（Client Mode）或二次注入。
- **Radio 2 (wlan2)**：专职被动监听与 Recon 频谱侦测。

---

### 4.3 Station 与 AP 运行模式剖析

对比 Station（STA 终端客户端）与 Access Point（AP 基站）在空中协调机制中的角色差异。

---

### 4.4 发射功率与高增益天线原理 (Power & Antennas)

说明 dBm 与毫瓦（mW）之转换公式，以及全向性天线（Omni-directional）在垂直与水平方向之辐射方向图特性。

---

### 4.5 信道划分与全球区域法规限制

比较全球各国（FCC、ETSI、MKK）在 2.4 GHz 信道（1-11 vs 1-13 vs 14）与发射功率上限（EIRP）的法规差异。

---

### 4.6 802.11 帧结构与管理帧解析

详细拆解 802.11 帧的三大分类：
1. **管理帧（Management Frames）**：Beacon、Probe Request/Response、Authentication、Association、Deauthentication。
2. **控制帧（Control Frames）**：RTS、CTS、ACK。
3. **数据帧（Data Frames）**：封装上层 IP 数据包之实际载荷。

---

### 4.7 帧注入与客户端状态机 (Frame Injection)

说明原始帧注入（Raw Frame Injection）的实现机制，以及如何通过发送伪造的 Deauth 管理帧打断连接，迫使客户端重新执行四次握手。

---

## 5. 开发者资源与自定义模块开发

### 5.1 官方开发者资源库 (Developer Resources)

Hak5 官方提供模块开发 SDK 与前端 API 规范，支持 HTML5、JavaScript 与后端 PHP / Python / Go 编写自定义扩展插件。

---

### 5.2 模块架构与社区软件包库贡献指南

介绍模块目录结构、`module.info` 配置文件编写规范，以及如何通过 GitHub 提交 PR 将自制模块发布至全球官方软件包库。

---

<!-- section：maintenance -->
## 6. 常见问答、故障排除、固件升级与硬件改动

### 6.1 macOS 平台连接支持 (macOS Support)

针对 macOS 系统缺少原生 RNDIS 驱动程序之情况，建议通过 Wi-Fi 连接或使用 HoRNDIS 内核扩展模块进行连接。

---

### 6.2 互联网共享连接建立与排查

排查无法连接外网之常见原因：DNS 配置缺失、默认网关冲突或本地防火墙拦截。

---

### 6.3 忘记密码还原与原厂出厂重置 (Factory Reset)

若忘记 root 密码：
1. 长按机身底部针孔内之重置按钮 10 秒以上。
2. LED 呈现快速红灯闪烁后放开。
3. 设备将自动格式化并恢复出厂默认值。

---

### 6.4 固件升级与救援恢复模式 (Firmware Recovery)

在 Web UI 检查更新，或在无法正常开机时，长按 Reset 键同时上电进入 Web Recovery 模式（默认 IP `192.168.1.1`）手动刷入官方救援镜像。

---

### 6.5 兼容 802.11 ac 5 GHz 网卡清单 (Compatible Adapters)

支持通过 USB 2.0 Host 接口外接原厂 **MK7 AC** 双频无线网卡（采用 MediaTek MT7610 U 芯片），立即为 Mark VII 赋予 5 GHz 802.11 ac 频段的侦查与注入能力。

---

### 6.6 MK7 LED 改装与 Kismet 保护外壳安装

详细图解官方 Kismet 外壳安装步骤，优化内部被动散热并支持额外外接散热风扇模块。
