---
title：“Hak5 Packet Squirrel Mark II 原厂技术说明书与全功能操作手册”
model：“Packet Squirrel Mark II”
manufacturer：“Hak5”
category：“以太网中间人串联旁路监听与远程访问设备”
docs_url：“https://docs.hak5.org/packet-squirrel/”
version：“4.0”
locale：“zh-cn”
---

# Hak5 Packet Squirrel Mark II 原厂技术说明书与全功能操作手册

> Hak5 出品的 Packet Squirrel Mark II 是口袋型以太网中间人（Device-in-the-Middle，DitM）多功能渗透测试工具的最新演进版本。专为隐蔽远程访问、无痛数据包捕获、安全 VPN 加密隧道建立以及响应式网络攻击载荷所设计，轻拨物理开关即可瞬间切换作战模式。

---

## 目录

- [**1. 产品概述与核心硬件架构**](#1-产品概述与核心硬件架构)
  - [1.1 Packet Squirrel Mark II 原厂介绍](#1-1-packet-squirrel-mark-ii-原厂介绍)
  - [1.2 物理连接与接线指南 (Connecting the Packet Squirrel)](#1-2-物理连接与接线指南-connecting-the-packet-squirrel)
  - [1.3 初次开机配置步骤 (Setting up the Packet Squirrel)](#1-3-初次开机配置步骤-setting-up-the-packet-squirrel)
  - [1.4 Mark II 世代全新特性 (Changes & New features)](#1-4-mark-ii-世代全新特性-changes-new-features)
- [**2. 入门指南与核心操作**](#2-入门指南与核心操作)
  - [2.1 Packet Squirrel 运行原理 (Packet Squirrel Basics)](#2-1-packet-squirrel-运行原理-packet-squirrel-basics)
  - [2.2 访问与登录控制台 (Accessing the Packet Squirrel)](#2-2-访问与登录控制台-accessing-the-packet-squirrel)
  - [2.3 Web UI 网页图形化界面 (Web UI)](#2-3-web-ui-网页图形化界面-web-ui)
  - [2.4 让设备连接上网 (Getting the Packet Squirrel online)](#2-4-让设备连接上网-getting-the-packet-squirrel-online)
  - [2.5 LED 状态指示灯定义 (Status LED)](#2-5-led-状态指示灯定义-status-led)
  - [2.6 Hak5 Cloud C² 云端纳管 (Cloud C²)](#2-6-hak5-cloud-c-云端纳管-cloud-c)
  - [2.7 USB 存储设备支持 (USB storage support)](#2-7-usb-存储设备支持-usb-storage-support)
  - [2.8 选择与编辑载荷 (Selecting and editing payloads)](#2-8-选择与编辑载荷-selecting-and-editing-payloads)
  - [2.9 配置载荷参数 (Configuring payloads)](#2-9-配置载荷参数-configuring-payloads)
  - [2.10 运行载荷 (Running payloads)](#2-10-运行载荷-running-payloads)
  - [2.11 网络拓扑与运行模式 (Networking and modes)](#2-11-网络拓扑与运行模式-networking-and-modes)
- [**3. 网络基础理论与数据包操纵教程**](#3-网络基础理论与数据包操纵教程)
  - [3.1 网络技术词汇表 (Networking Glossary)](#3-1-网络技术词汇表-networking-glossary)
  - [3.2 OSI 七层模型实务解析 (OSI layers)](#3-2-osi-七层模型实务解析-osi-layers)
  - [3.3 私有 IP 网段划分 (Private IP ranges)](#3-3-私有-ip-网段划分-private-ip-ranges)
  - [3.4 子网掩码运算 (Network masks)](#3-4-子网掩码运算-network-masks)
  - [3.5 数据包注入技术 (Packet injection)](#3-5-数据包注入技术-packet-injection)
  - [3.6 网络地址转换与重定向 (Translation and redirection)](#3-6-网络地址转换与重定向-translation-and-redirection)
  - [3.7 数据包捕获实战 (Packet capture)](#3-7-数据包捕获实战-packet-capture)
- [**4. 载荷开发与 DuckyScript 指令集**](#4-载荷开发与-duckyscript-指令集)
  - [4.1 载荷开发基础 (Payload development basics)](#4-1-载荷开发基础-payload-development-basics)
  - [4.2 DuckyScript for Packet Squirrel 语法体系](#4-2-duckyscript-for-packet-squirrel-语法体系)
  - [4.3 BUTTON 微动按钮监听指令](#4-3-button-微动按钮监听指令)
  - [4.4 C2EXFIL 云端数据外发指令](#4-4-c2exfil-云端数据外发指令)
  - [4.5 C2NOTIFY 云端告警通知指令](#4-5-c2notify-云端告警通知指令)
  - [4.6 C2WATCHDIR 目录自动同步指令](#4-6-c2watchdir-目录自动同步指令)
  - [4.7 DYNAMICPROXY 动态代理通道指令](#4-7-dynamicproxy-动态代理通道指令)
  - [4.8 KILLPORT 端口强制中断指令](#4-8-killport-端口强制中断指令)
  - [4.9 KILLSTREAM 数据流中断指令](#4-9-killstream-数据流中断指令)
  - [4.10 LED 状态指示灯控制指令](#4-10-led-状态指示灯控制指令)
  - [4.11 MATCHPORT 端口流量比对指令](#4-11-matchport-端口流量比对指令)
  - [4.12 MATCHSTREAM 流特征匹配指令](#4-12-matchstream-流特征匹配指令)
  - [4.13 NETMODE 网络交换拓扑切换指令](#4-13-netmode-网络交换拓扑切换指令)
  - [4.14 SELFDESTRUCT 紧急数据销毁指令](#4-14-selfdestruct-紧急数据销毁指令)
  - [4.15 SSH_START 与 SSH_STOP 服务控制指令](#4-15-ssh_start-与-ssh_stop-服务控制指令)
  - [4.16 SPOOFDNS 域名伪冒欺骗指令](#4-16-spoofdns-域名伪冒欺骗指令)
  - [4.17 SWITCH 开关档位查询指令](#4-17-switch-开关档位查询指令)
  - [4.18 UI_START 与 UI_STOP 网页界面控制指令](#4-18-ui_start-与-ui_stop-网页界面控制指令)
  - [4.19 USB_FREE、USB_STORAGE 与 USB_WAIT 存储控制指令](#4-19-usb_freeusb_storage-与-usb_wait-存储控制指令)
- [**5. 高阶载荷工程与自动化脚本技术**](#5-高阶载荷工程与自动化脚本技术)
  - [5.1 高阶载荷架构 (Advanced payloads)](#5-1-高阶载荷架构-advanced-payloads)
  - [5.2 变量扩展与引号转义 (Quotes and expansions)](#5-2-变量扩展与引号转义-quotes-and-expansions)
  - [5.3 条件分支与流程控制 (Flow control)](#5-3-条件分支与流程控制-flow-control)
  - [5.4 标准输出与重定向技巧 (Redirecting output)](#5-4-标准输出与重定向技巧-redirecting-output)
  - [5.5 载荷自定义参数文件 (Payload configuration)](#5-5-载荷自定义参数文件-payload-configuration)
  - [5.6 返回码验证与成功判定 (Return codes & success)](#5-6-返回码验证与成功判定-return-codes--success)
  - [5.7 后台常驻任务管理 (Background commands)](#5-7-后台常驻任务管理-background-commands)
  - [5.8 指令分组执行 (Command groups)](#5-8-指令分组执行-command-groups)
  - [5.9 JSON 格式数据解析 (Processing JSON)](#5-9-json-格式数据解析-processing-json)
  - [5.10 USB 存储设备硬件加密 (USB encryption)](#5-10-usb-存储设备硬件加密-usb-encryption)
  - [5.11 VPN 服务端与客户端配置 (VPN configuration)](#5-11-vpn-服务端与客户端配置-vpn-configuration)
  - [5.12 网络数据包深度操弄 (Network manipulation)](#5-12-网络数据包深度操弄-network-manipulation)
  - [5.13 实战避坑与排错指南 (Tips，tricks，& pitfalls)](#5-13-实战避坑与排错指南-tips-tricks--pitfalls)
  - [5.14 Python 3 集成自动化开发 (Python on Packet Squirrel)](#5-14-python-3-集成自动化开发-python-on-packet-squirrel)
  - [5.15 官方载荷仓库 (Payload repository)](#5-15-官方载荷仓库-payload-repository)
- [**6. 故障排除、设备维护与固件升级**](#6-故障排除设备维护与固件升级)
  - [6.1 网络通信排错指引 (Troubleshooting networking)](#6-1-网络通信排错指引-troubleshooting-networking)
  - [6.2 载荷脚本调试指引 (Troubleshooting payloads)](#6-2-载荷脚本调试指引-troubleshooting-payloads)
  - [6.3 原厂出厂还原重置 (Factory reset)](#6-3-原厂出厂还原重置-factory-reset)
  - [6.4 固件升级标准作业程序 (Upgrading firmware)](#6-4-固件升级标准作业程序-upgrading-firmware)

---

## 1. 产品概述与核心硬件架构

<!-- section：overview -->
### 硬件技术规格与原厂校准基准表

| 硬件组件名称 | 原厂技术规格说明 |
|---|---|
| **核心处理器 (CPU)** | Multi-Core Network Processor @ 580 MHz |
| **以太网端口 (Ethernet)** | 双 Gigabit (10/100/1000) RJ-45 端口（具备硬件 Bypass 与透明串联能力）|
| **存储扩展接口 (Storage)** | MicroSD 卡插槽 + USB-A 2.0 Host U 盘接口 |
| **供电接口 (Power)** | USB-C 总线供电（5 V DC，1 A）|
| **硬件控制开关** | 4 档位物理切换开关（Switch 1，Switch 2，Switch 3，Arming Mode）与微动按钮 |
| **VPN 加密协议支持** | 原生支持 OpenVPN 与 WireGuard 通道协议 |
| **状态指示灯** | 多色可编程 RGB LED 诊断灯 |

---

<!-- section：overview -->
### 1.1 Packet Squirrel Mark II 原厂介绍

Packet Squirrel Mark II 是由 Hak5 打造的最新一代微型硬件中间人（DitM）以太网渗透测试平台。具备手掌大小的轻巧体积，能够隐蔽串联于任何网络线路中，提供隐蔽的远程外联通道、无延迟流量数据包捕获、端到端 VPN 加密通信以及基于网络事件动态触发的响应式载荷。

![Packet Squirrel Mark II](https://932701053-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F520JUF2JxB2RMXztRVAV%2Fuploads%2FhYoepPPoy8Pj5K8LI3E8%2Fsquirrelmk2_flat_halfres.png?alt=media&token=306f2cf9-1510-4238-9 ead-853396a45b4 d)

> [!WARNING]
> 本文档专门适用于搭载固件版本 **4.0.0 或更新版本** 之 Packet Squirrel Mark II。如需第一代旧款硬件说明，请查阅 Hak5 旧版文档中心。

---

### 1.2 物理连接与接线指南 (Connecting the Packet Squirrel)

Packet Squirrel 具备两个 RJ-45 以太网端口：
1. **Network 侧端口 (标示为 Network 或互联网符号)**：连接上游交换机（Switch）、路由器或墙面网络插口。
2. **Target 侧端口 (标示为 Target 或计算机符号)**：连接受测目标主机、工作站或网络打印机。
3. **USB-C 供电端口**：连接 5 V 1 A 的 USB 电源适配器、移动电源或受测主机后方的 USB 接口。

串联完成后，网络流量将无缝穿透 Packet Squirrel，目标主机与上游服务器均无法察觉中间存在额外物理节点。

---

### 1.3 初次开机配置步骤 (Setting up the Packet Squirrel)

1. 将切换开关拨至最右侧的 **维护模式 (Arming Mode)**。
2. 通过网线将计算机连接至 Packet Squirrel 的 Target 端口，并插上 USB-C 电源开机。
3. 设备开机约需 30 秒，LED 将呈现蓝灯慢速闪烁。
4. 计算机将自动获取 `172.16.32.x` 网段的 IP 地址。
5. 打开浏览器访问 `http://172.16.32.1:1471`，进入 Web UI 引导式安装向导，设置 root 管理员密码。

---

<!-- section：features -->
### 1.4 Mark II 世代全新特性 (Changes & New features)

相较于第一代 Packet Squirrel，Mark II 迎来全面革新：
* **双 Gigabit 网络芯片**：支持 1000 BASE-T 极速线速转发，告别百兆瓶颈。
* **全新 DuckyScript 语言核心**：引入高阶数据包比对指令（`MATCHPORT`，`MATCHSTREAM`）与云端指令（`C2EXFIL`，`C2NOTIFY`）。
* **内置 Web UI 图形化管理后台**：开机即提供可视化仪表板，支持实时抓包下载与载荷拖曳上传。
* **WireGuard 协议原生集成**：连接握手速度更快、损耗更低的高效加密 VPN。
* **USB-C 现代化供电规格**：全面升级 USB-C 接口。

---

## 2. 入门指南与核心操作

### 2.1 Packet Squirrel 运行原理 (Packet Squirrel Basics)

数据包自 Network 端流入，由 Target 端流出；在此双向转发过程中，底层 Linux 内核可选择：
* **纯透传模式 (Transparent Bridge)**：不分配 IP，完全隐匿无踪，静默截获流量。
* **NAT 路由模式 (NAT Router)**：目标计算机经由 Packet Squirrel 转发上网，支持端口转发与流量劫持。
* **孤立阻断模式 (Isolate / Drop)**：选择性阻断特定流量或切断目标对外连接。

---

### 2.2 访问与登录控制台 (Accessing the Packet Squirrel)

在维护模式下，渗透人员可通过以下途径登录系统：
* **SSH 终端连接**：
  ```bash
  ssh root@172.16.32.1
  ```
* **Web UI 浏览器**：访问 `http://172.16.32.1:1471`。

---

### 2.3 Web UI 网页图形化界面 (Web UI)

Web UI 提供功能齐备的网页仪表板：
* **系统状态监控**：实时 CPU、内存使用率、网络流量速率曲线。
* **开关档位载荷指派**：点击 Switch 1、2、3 直接在线下载或替换载荷。
* **外发日志检索**：一键打包下载 `loot/` 目录中的 pcap 数据包捕获文件与登录凭证。
* **终端 Web Terminal**：无需第三方客户端，直接在浏览器窗口中操作 Linux Bash Shell。

---

### 2.4 让设备连接上网 (Getting the Packet Squirrel online)

当 Network 端口连接至具备 DHCP 服务器的企业局域网时，Packet Squirrel 会自动在后台获取 IP 并连接互联网，以便执行软件包更新或与 Cloud C² 连接。

---

### 2.5 LED 状态指示灯定义 (Status LED)

| 指示灯表现 | 系统运行状态说明 |
|---|---|
| 绿灯闪烁 (Green blinking) | 系统初始化开机中 |
| 蓝灯闪烁 (Blue blinking) | 维护模式就绪 (Arming Mode) |
| 紫灯/洋红 (Magenta) | 载荷正在初始化配置中 (SETUP) |
| 黄灯 (Yellow) | 载荷运行中 (ATTACK) |
| 常亮绿灯 (Solid Green) | 载荷运行圆满成功 (SUCCESS) |
| 常亮红灯 (Solid Red) | 运行失败或网络连接超时 (FAIL) |
| 红蓝交替闪烁 | 固件烧录更新中，**切勿拔除电源** |

---

### 2.6 Hak5 Cloud C² 云端纳管 (Cloud C²)

通过 Cloud C²，渗透测试团队可远程集中管理散布于各地的 Packet Squirrel：
1. 于 Cloud C² 服务器新增 Packet Squirrel 设备并下载 `device.config`。
2. 通过 Web UI 或 U 盘将该文件放入设备根目录。
3. 只要设备接入任何可连外网络，即自动反弹建立 WebSocket 加密通道，实现跨防火墙远程 Shell 与实时外发。

---

### 2.7 USB 存储设备支持 (USB storage support)

插入 USB U 盘时，系统会自动将其挂载至 `/mnt/loot/`。若检测到 U 盘，数据包捕获与海量外发日志将优先写入外部 U 盘，以保护内部闪存寿命。

---

<!-- section：configuration -->
### 2.8 选择与编辑载荷 (Selecting and editing payloads)

物理开关具备 4 个档位：
* **Switch 1**：运行 `/root/payloads/switch1/payload.sh`
* **Switch 2**：运行 `/root/payloads/switch2/payload.sh`
* **Switch 3**：运行 `/root/payloads/switch3/payload.sh`
* **Arming Mode**：进入维护模式，不运行任何攻击载荷

---

### 2.9 配置载荷参数 (Configuring payloads)

标准载荷多支持独立的配置文件 `config.txt`，便于快速自定义目标 IP、监听端口或外联服务器地址，无需修改核心 shell 脚本。

---

### 2.10 运行载荷 (Running payloads)

拨动切换开关至所需档位（例如 Switch 1），将设备串联于目标网络线路并通电。系统开机后将依序执行初始化、环境检查、网络架构配置，并以 LED 指示灯实时汇报执行进度。

---

### 2.11 网络拓扑与运行模式 (Networking and modes)

通过核心指令 `NETMODE`，可在载荷中随意切换底层网络行为：
* `NETMODE BRIDGE`：硬件网桥模式，两端直通，完全透明。
* `NETMODE NAT`：NAT 路由模式，设备充当目标的默认网关。
* `NETMODE ISOLATE`：切断 Target 端网络，完全隔离。

---

## 3. 网络基础理论与数据包操纵教程

### 3.1 网络技术词汇表 (Networking Glossary)
* **MAC 地址**：网卡物理硬件识别码。
* **ARP 协议**：将 IP 地址解析为物理 MAC 地址之协议。
* **DHCP**：动态主机配置协议，自动分配 IP、子网掩码与默认网关。
* **DNS**：域名系统，将域名解析为 IP 地址。

---

### 3.2 OSI 七层模型实务解析 (OSI layers)
* **物理层 (L1)**：双绞线信号传输。
* **数据链路层 (L2)**：以太网数据帧 (Ethernet Frame) 与 MAC 路由。
* **网络层 (L3)**：IP 数据包路由与 ICMP 控制。
* **传输层 (L4)**：TCP 连接与 UDP 数据报。
* **应用层 (L7)**：HTTP、SSH、DNS 等高层应用服务。

---

### 3.3 私有 IP 网段划分 (Private IP ranges)
RFC 1918 规范之三大保留网段：
* `10.0.0.0/8`
* `172.16.0.0/12`（Packet Squirrel 本机默认使用 `172.16.32.0/24`）
* `192.168.0.0/16`

---

### 3.4 子网掩码运算 (Network masks)
掩码决定了网络地址与主机地址的边界。CIDR 标记法（如 `/24` 对应 `255.255.255.0`，可用主机数为 254 台）。

---

### 3.5 数据包注入技术 (Packet injection)
数据包注入允许未经请求直接向目标发送伪造数据包。通过原始套接字（Raw Socket）或 Scapy 工具，Packet Squirrel 能注入伪造的 TCP Reset 数据包强制中断特定连接，或注入恶意 DNS 应答。

---

### 3.6 网络地址转换与重定向 (Translation and redirection)
利用 Linux `iptables` 内核能力，Packet Squirrel 能执行 DNAT（目的地址转换）与 SNAT（源地址转换），将目标用户的 HTTP 80 流量静默重定向至本机搭建的钓鱼服务器。

---

### 3.7 数据包捕获实战 (Packet capture)
利用内置的 `tcpdump` 工具，可依条件精准截获特定协议流量：
```bash
# 截获目标所有 DNS 查询数据包并保存为 pcap 格式
tcpdump -i br-lan -nn port 53 -w /mnt/loot/dns_traffic.pcap
```

---

## 4. 载荷开发与 DuckyScript 指令集

### 4.1 载荷开发基础 (Payload development basics)
每个档位的载荷均包含 `payload.sh` 执行文件。系统运行时以标准 POSIX Shell 环境加载，并预先注入 Packet Squirrel 专用指令集函数库。

---

### 4.2 DuckyScript for Packet Squirrel 语法体系
相较于 Rubber Ducky 的单纯击键注入，Packet Squirrel 的 DuckyScript 聚焦于**网络自动化操弄**、**后台进程监控**与**云端联动**。

---

### 4.3 BUTTON 微动按钮监听指令
* `BUTTON`：暂停载荷运行，等待用户按下机身物理微动按钮后方可继续。适用于由现场渗透人员手动控制攻击发起时机。

---

### 4.4 C2EXFIL 云端数据外发指令
* `C2EXFIL <文件路径>`：通过已连接的 Cloud C² 加密通道，将截获之日志或数据包文件自动上传至云端服务器。

---

### 4.5 C2NOTIFY 云端告警通知指令
* `C2NOTIFY <消息内容>`：向 Cloud C² 控制台发送高优先级告警事件通知。

---

### 4.6 C2WATCHDIR 目录自动同步指令
* `C2WATCHDIR <目录路径>`：监控指定目录，一旦目录内产生新的文件（如 pcap 或 txt），实时在后台自动排程上传至 Cloud C²。

---

### 4.7 DYNAMICPROXY 动态代理通道指令
* `DYNAMICPROXY`：启用本机 SOCKS5 动态代理通道，方便渗透测试人员通过远程穿透进目标局域网内网。

---

### 4.8 KILLPORT 端口强制中断指令
* `KILLPORT <端口号>`：强制终止正在该端口上传输的 TCP 连接。

---

### 4.9 KILLSTREAM 数据流中断指令
* `KILLSTREAM <连接特征>`：针对特定源与目的 IP 的连接数据流发送 RST 数据包予以切断。

---

### 4.10 LED 状态指示灯控制指令
* `LED SETUP`（配置中，洋红）、`LED ATTACK`（攻击中，黄灯）、`LED SUCCESS`（成功，常亮绿灯）、`LED FAIL`（失败，常亮红灯）、`LED OFF`（熄灭）。

---

### 4.11 MATCHPORT 端口流量比对指令
* `MATCHPORT <端口号>`：在后台持续监听，当受测主机发起针对该端口的网络请求时触发特定回调函数。

---

### 4.12 MATCHSTREAM 流特征匹配指令
* `MATCHSTREAM <正则表达式>`：深度数据包检测（DPI），匹配 TCP/UDP 负载中的明文字符串（如用户名或密钥）。

---

### 4.13 NETMODE 网络交换拓扑切换指令
* `NETMODE BRIDGE`：网桥透传。
* `NETMODE NAT`：路由转发。
* `NETMODE ISOLATE`：完全隔离。

---

### 4.14 SELFDESTRUCT 紧急数据销毁指令
* `SELFDESTRUCT`：在遭遇现场查缉等极端状况下，自动擦除本机存储之密钥、日志与敏感配置，确保作战安全。

---

### 4.15 SSH_START 与 SSH_STOP 服务控制指令
* `SSH_START`：动态开启本机 Dropbear SSH 服务。
* `SSH_STOP`：动态关闭 SSH 服务以收敛系统暴露面。

---

### 4.16 SPOOFDNS 域名伪冒欺骗指令
* `SPOOFDNS <域名> <目标 IP>`：启动本机 DNS 投毒引擎，将受测主机针对特定网址的查询请求劫持导向至指定服务器。

---

### 4.17 SWITCH 开关档位查询指令
* `SWITCH`：返回当前硬件开关所在的位置代码（1，2，3 或 arming）。

---

### 4.18 UI_START 与 UI_STOP 网页界面控制指令
* `UI_START`：启动 Web UI 网页服务器。
* `UI_STOP`：在实战攻击期间关闭 Web UI 以节省系统资源并避免被目标发现。

---

### 4.19 USB_FREE、USB_STORAGE 与 USB_WAIT 存储控制指令
* `USB_WAIT`：暂停运行，等待外部 USB U 盘插入。
* `USB_STORAGE`：获取当前挂载 U 盘之路径。
* `USB_FREE`：查询 U 盘剩余可用存储容量。

---

## 5. 高阶载荷工程与自动化脚本技术

### 5.1 高阶载荷架构 (Advanced payloads)
高阶载荷能结合条件判断、动态网络环境探测以及多协议联动，具备自适应（Adaptive）作战能力。

---

### 5.2 变量扩展与引号转义 (Quotes and expansions)
在编写包含 awk 或 sed 的复杂 shell 指令时，应精确使用单引号 `'`（防止变量提前展开）与双引号 `"`（允许变量替换）。

---

### 5.3 条件分支与流程控制 (Flow control)
通过标准 `if [ ... ]；then ... fi` 与 `case ... esac` 控制攻击逻辑分支。

---

### 5.4 标准输出与重定向技巧 (Redirecting output)
* `> /dev/null 2>&1`：静默执行指令，避免日志输出干扰终端。
* `>> /mnt/loot/results.txt`：附加写入日志文件。

---

### 5.5 载荷自定义参数文件 (Payload configuration)
在载荷文件夹建立 `config.env`，并于 `payload.sh` 开头以 `source config.env` 加载，实现逻辑与配置参数解耦。

---

### 5.6 返回码验证与成功判定 (Return codes & success)
每条关键指令执行完毕后，检查 `$?` 返回值，若不等于 0 则调用 `LED FAIL` 并记录错误日志。

---

### 5.7 后台常驻任务管理 (Background commands)
使用 `&` 将耗时的监听进程放入后台运行，并利用 `$!` 记录其进程 ID（PID），以便在收尾阶段通过 `kill` 正确释放资源。

---

### 5.8 指令分组执行 (Command groups)
利用大括号 `{ cmd1；cmd2；}` 将多个指令绑定为单一执行块，方便统一重定向或实施超时控制。

---

### 5.9 JSON 格式数据解析 (Processing JSON)
内置 `jq` 工具，可高效率提取 RESTful API 返回之 JSON 节点数据：
```bash
TOKEN=$(curl -s http://api.internal/auth | jq -r .access_token)
```

---

### 5.10 USB 存储设备硬件加密 (USB encryption)
支持 LUKS 加密分区。只有在输入正确密钥后方可解密挂载外发分区，即使设备于现场遗失亦能确保情报数据绝对保密。

---

### 5.11 VPN 服务端与客户端配置 (VPN configuration)
* **WireGuard**：通过 `wg-quick up /etc/wireguard/wg0.conf` 建立毫秒级 VPN 隧道。
* **OpenVPN**：支持 TCP 443 伪装流量，绕过严格的企业防火墙出站审查。

---

### 5.12 网络数据包深度操弄 (Network manipulation)
结合 `iptables`、`ebtables` 与 `tc`（流量控制）工具，模拟网络延迟、数据包丢失或进行中间人透明 SSL 降级。

---

### 5.13 实战避坑与排错指南 (Tips，tricks，& pitfalls)
* **避免在只读分区大量写入**：确保临时文件写入内存虚拟磁盘 `/tmp`。
* **妥善处理 DHCP 租约冲突**：切换 NETMODE 时务必重新启动本机 dnsmasq 服务。

---

### 5.14 Python 3 集成自动化开发 (Python on Packet Squirrel)
Packet Squirrel 完整内置 Python 3 解释器，可直接运行复杂的多线程扫描器、协议模拟服务器及自定义数据包解析脚本。

---

### 5.15 官方载荷仓库 (Payload repository)
Hak5 官方维护了庞大的开源载荷库，涵盖 TCP 劫持、DNS 伪冒、NTLMv2 凭证截获等数十种战术范本。

---

## 6. 故障排除、设备维护与固件升级

### 6.1 网络通信排错指引 (Troubleshooting networking)
若目标主机无法获取 IP，请检查物理网线是否插反（Network vs Target），或使用 `ifconfig` 与 `brctl show` 检查网桥状态。

---

### 6.2 载荷脚本调试指引 (Troubleshooting payloads)
于维护模式下以手动方式运行脚本：
```bash
bash -x /root/payloads/switch1/payload.sh
```
观察每行指令展开后的详细执行过程，迅速定位语法错误。

---

### 6.3 原厂出厂还原重置 (Factory reset)
若系统密码遗失或配置损坏：
1. 拔除电源，将开关拨至维护模式。
2. 长按微动按钮不放，同时插入 USB-C 电源开机。
3. 持续按住按钮 10 秒以上，直到 LED 呈现红灯快速闪烁后放开。
4. 设备将自动执行重置并恢复至原厂初始镜像。

---

<!-- section：maintenance -->
### 6.4 固件升级标准作业程序 (Upgrading firmware)

Hak5 团队持续推出新固件以提升系统性能与防护力：
1. 进入维护模式，由浏览器打开 Web UI。
2. 进入“Settings”$ightarrow$“Firmware Update”标签页。
3. 点击“Check for Updates”进行在线自动升级，或上传本地下载之固件更新包（`.bin`）。
4. 升级期间 LED 将红蓝交替闪烁，约耗时 3 至 5 分钟。
5. 升级完成后系统将自动重启回到维护模式。

> [!CAUTION]
> 固件升级进行中，**绝对不可中断电源**，否则将造成系统引导区损坏变砖。
