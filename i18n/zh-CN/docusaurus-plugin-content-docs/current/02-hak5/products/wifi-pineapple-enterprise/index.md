---
title: "Hak5 WiFi Pineapple Enterprise 原厂技术说明书与全功能操作手册"
model: "WiFi Pineapple Enterprise"
manufacturer: "Hak5"
category: "企业级无线安全稽核与流氓 AP 测试平台"
docs_url: "https://docs.hak5.org/wifi-pineapple-enterprise/"
version: "2.0"
locale: "zh-cn"
---

# Hak5 WiFi Pineapple Enterprise 原厂技术说明书与全功能操作手册

> Hak5 WiFi Pineapple Enterprise 是专为大型企业环境、金融机构与政府机关设计的机架式/桌面型无线安全稽核设备。配备多内核高速网络处理器、Gigabit 乙太网络与 SFP 端口、高功率双频并发射频芯片数组与 MIMO 天线系统，支持大规模即时频谱监听、自动化 Campaigns 任务与云端集中管理。

---

## 目录

- [**1. 产品概述与内核硬件架构**](#1-产品概述与内核硬件架构)
  - [1.1 WiFi Pineapple Enterprise 原厂介绍](#11-wifi-pineapple-enterprise-原厂介绍)
  - [1.2 企业级硬件技术规格与校准基准表](#12-企业级硬件技术规格与校准基准表)
- [**2. 初次配置、实体接线与网络共用**](#2-初次配置实体接线与网络共用)
  - [2.1 实体连接与机架部署指引 (Physical Connections)](#21-实体连接与机架部署指引-physical-connections)
  - [2.2 初始配置精灵与帐号初始化 (Setting up)](#22-初始配置精灵与帐号初始化-setting-up)
  - [2.3 企业网络环境连接配置 (Linux / Windows / Wi-Fi)](#23-企业网络环境连接配置-linux--windows--wi-fi)
  - [2.4 USB U 盘脱机自动部署 (Setup by USB Disk)](#2-4-usb-U 盘離線自動部署-setup-by-usb-disk)
- [**3. Web UI 图形化接口、Recon、PineAP 与 Cloud C²**](#3-web-ui-圖形化接口 reconpineap-與-cloud-c)
  - [3.1 Web UI 企业控制台架构 (Introduction to the UI)](#31-web-ui-企业控制台架构-introduction-to-the-ui)
  - [3.2 仪表板资源监控与即时状态 (Dashboard)](#32-仪表板资源监控与即时状态-dashboard)
  - [3.3 Campaigns 企业级自动化作战任务 (Campaigns)](#33-campaigns-企业级自动化作战任务-campaigns)
  - [3.4 PineAP 企业流氓 AP 攻击引擎 (PineAP)](#34-pineap-企业流氓-ap-攻击引擎-pineap)
  - [3.5 全频段频谱侦察与信号测绘 (Recon)](#35-全频段频谱侦察与信号测绘-recon)
  - [3.6 企业 WPA 握手包收集与管理 (Handshakes)](#36-企业-wpa-握手包收集与管理-handshakes)
  - [3.7 Hak5 Cloud C² 企业集权纳管 (Cloud C²)](#37-hak5-cloud-c-企业集权纳管-cloud-c)
- [**4. Wi-Fi 基础理论、射频技术与 802.11 讯框架构**](#4-wi-fi-基础理论射频技术与-80211-讯框架构)
  - [4.1 企业无线通信底层技术 (Introduction to WiFi)](#41-企业无线通信底层技术-introduction-to-wifi)
  - [4.2 射频芯片、MIMO 天线与功率规划](#4-2-射頻晶片 mimo-天線與功率規劃)
  - [4.3 802.11 讯框结构与讯框注入机制 (Frame Injection)](#43-80211-讯框结构与讯框注入机制-frame-injection)
- [**5. 常见问题排查、固件维护与出厂重置**](#5-常见问题排查固件维护与出厂重置)
  - [5.1 连网故障排查与管理端口诊断](#51-连网故障排查与管理端口诊断)
  - [5.2 密码重置与原厂出厂复原 (Factory Reset)](#52-密码重置与原厂出厂复原-factory-reset)
  - [5.3 固件在线与脱机升级标准作业进程 (Updates)](#53-固件在线与脱机升级标准作业进程-updates)

---

## 1. 产品概述与内核硬件架构

<!-- section：overview -->
### 1.1 WiFi Pineapple Enterprise 原厂介绍

WiFi Pineapple Enterprise 是 Hak5 专为大规模企业环境安全评估打造的高性能无线安全设备。

相较于便携型产品，Enterprise 版本专注于持续性的全天候监控与高负载无线渗透测试。具备企业级多内核处理器、多组 Gigabit 乙太网络与高速光纤接口、高灵敏度 MIMO 天线数组，可无死角监听园区内的所有无线频段，即时发现未经授权的个人热点、影子 Wi-Fi 以及潜在的无线网络入侵行为。

### 1.2 企业级硬件技术规格与校准基准表

| 硬件组件项目 | 原厂官方技术规格说明 |
|---|---|
| **机身规格架构** | 企业级机架式 / 桌面型金属散热机身 |
| **处理器规格 (CPU)** | 高性能多内核网络处理器 SoC |
| **系统内存 (RAM)** | 大容量高速 DDR4 内存 |
| **网络连接接口** | 多组 Gigabit 乙太网络 RJ-45 端口与高速 SFP 光纤插槽 |
| **无线射频模块** | 多组高功率双频并发（Dual-Concurrent）企业级无线收发器 |
| **天线配置** | 外置式高增益多天线 MIMO 全向天线数组 |
| **集中管理支持** | 支持 Hak5 Cloud C² 企业版全生命周期纳管 |

---

<!-- section：configuration -->
## 2. 初次配置、实体接线与网络共用

### 2.1 实体连接与机架部署指引 (Physical Connections)

1. 将高增益天线安装于机身后面板之对应 RP-SMA 接头。
2. 使用标准网络线将 Management 接口连接至管理交换器或配置电脑。
3. 连接交流电源线并打开电源开关，确认面板电源指示灯恒亮。

---

### 2.2 初始配置精灵与帐号初始化 (Setting up)

1. 于浏览器中打开 `http://172.16.42.1:1471` 进入 Setup Wizard。
2. 配置强固之 root 管理员密码与系统主机名称。
3. 依据企业网段规划配置静态 IP 或 DHCP 用户端模式。

---

### 2.3 企业网络环境连接配置 (Linux / Windows / Wi-Fi)

详细说明在企业服务器机房环境下，如何通过 VLAN Tagging、网络接口桥接或 Linux iptables 创建出站网际网络共用信道。

---

### 2.4 USB U 盘脱机自动部署 (Setup by USB Disk)

将包含配置参数的部署 U 盘插入机身 USB 端口，开机时系统将自动读取并完成初始化配置，大幅简化大量站点的快速部署难度。

---

<!-- section：features -->
## 3. Web UI 图形化接口、Recon、PineAP 与 Cloud C²

### 3.1 Web UI 企业控制台架构 (Introduction to the UI)

专为网络安全运维中心（SOC）设计的直觉式仪表板，提供多维度无线资产可视化图表与警报即时通知。

---

### 3.2 仪表板资源监控与即时状态 (Dashboard)

即时监控 CPU 温度、内存使用量、各射频模块的工作负载、空中讯框密度与关联客户端清单。

---

### 3.3 Campaigns 企业级自动化作战任务 (Campaigns)

支持调度周期性安全巡检任务，自动扫描未授权 AP、诱捕影子设备、截获握手包并自动产出合规性 PDF 稽核报告。

---

### 3.4 PineAP 企业流氓 AP 攻击引擎 (PineAP)

支持 Beacon Response 智能回应、SSID Pool 大容量热点广播、以及针对企业内部特定 SSID 的定向授权稽核测试。

---

### 3.5 全频段频谱侦察与信号测绘 (Recon)

全面扫描 2.4 GHz 与 5 GHz 频谱，绘制涵盖所有频道之无线电磁环境热图，精准标记各设备之 RSSI 信号强度。

---

### 3.6 企业 WPA 握手包收集与管理 (Handshakes)

自动拦截与分析 WPA2-Enterprise 与 WPA3 验证流程，支持将握手包集中归档并通过 API 导出至后端密码哈希集群破解。

---

### 3.7 Hak5 Cloud C² 企业集权纳管 (Cloud C²)

将园区内部署的所有 Enterprise 设备统一绑定至 Hak5 Cloud C² 云端服务器，实现跨分部、跨厂区的单一管理窗格。

---

## 4. Wi-Fi 基础理论、射频技术与 802.11 讯框架构

### 4.1 企业无线通信底层技术 (Introduction to WiFi)

深度探讨 802.11 a/b/g/n/ac/ax 标准演进、正交频分多任务（OFDM）调制技术与企业级漫游协定（802.11 k/v/r）。

---

### 4.2 射频芯片、MIMO 天线与功率规划

分析多天线空间串流（Spatial Streams）、波束成形（Beamforming）原理以及企业机房天线布建之最佳实务。

---

### 4.3 802.11 讯框结构与讯框注入机制 (Frame Injection)

解析 Management、Control 与 Data 讯框之字段定义，并说明高负载讯框注入与 Deauthentication 断线攻击之防御机制。

---

<!-- section：maintenance -->
## 5. 常见问题排查、固件维护与出厂重置

### 5.1 连网故障排查与管理端口诊断

说明管理接口无法访问、DHCP 配发失败或 SFP 光纤模块未识别之诊断排除步骤。

---

### 5.2 密码重置与原厂出厂复原 (Factory Reset)

若管理者密码遗失或系统配置毁损，可通过后面板之实体重置孔进行出厂复原重设。

---

### 5.3 固件在线与脱机升级标准作业进程 (Updates)

支持通过 Web 管理接口自动检查更新，或于隔离内网环境中通过本地上传 `.bin` 映像档完成无痛热升级。
