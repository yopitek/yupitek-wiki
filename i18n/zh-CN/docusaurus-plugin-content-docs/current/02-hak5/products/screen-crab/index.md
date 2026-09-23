---
title：“Hak5 Screen Crab 原厂技术说明书与全功能操作手册”
model：“Screen Crab”
manufacturer：“Hak5”
category：“HDMI 视频中间人侧录植入设备”
docs_url：“https://docs.hak5.org/screen-crab/”
version：“2.0”
locale：“zh-cn”
---

# Hak5 Screen Crab 原厂技术说明书与全功能操作手册

> Hak5 Screen Crab 是一款极度隐蔽的 HDMI 视频中间人（Video Man-in-the-Middle）侧录与流媒体植入硬件。串联于主机与显示器之间，安静捕获高分辨率屏幕截图，并支持 2.4 GHz Wi-Fi 与 Hak5 Cloud C² 云端带外回传。

---

## 目录

- [**1. 产品概述与硬件架构**](#1-产品概述与硬件架构)
  - [1.1 Screen Crab 原厂介绍](#1-1-screen-crab-原厂介绍)
  - [1.2 运行架构与核心原理 (Screen Crab Basics)](#1-2-运行架构与核心原理-screen-crab-basics)
- [**2. 组态配置、Cloud C² 与操作模式**](#2-组态配置-cloud-c-与操作模式)
  - [2.1 组态配置文件解析 (Configuring the Screen Crab)](#2-1-组态配置文件解析-configuring-the-screen-crab)
  - [2.2 LED 状态指示灯诊断 (LED Status Indications)](#2-2-led-状态指示灯诊断-led-status-indications)
  - [2.3 Hak5 Cloud C² 云端连接配置 (Configuring Cloud C²)](#2-3-hak5-cloud-c-云端连接配置-configuring-cloud-c)
  - [2.4 2024 SSL 证书安全更新 (2024 SSL Update)](#2-4-2024-ssl-证书安全更新-2024-ssl-update)
- [**3. 硬件规格、安全性指南与故障排除**](#3-硬件规格安全性指南与故障排除)
  - [3.1 重要安全指引与法规声明 (Safety and Warnings)](#3-1-重要安全指引与法规声明-safety-and-warnings)
  - [3.2 官方技术规格基准表 (Hardware Specifications)](#3-2-官方技术规格基准表-hardware-specifications)
  - [3.3 常见故障排查指引 (Troubleshooting Guide)](#3-3-常见故障排查指引-troubleshooting-guide)

---

## 1. 产品概述与硬件架构

<!-- section：overview -->
### 1.1 Screen Crab 原厂介绍

Hak5 Screen Crab 是一款专为红队渗透测试、硬件安全审计与系统管理员设计的隐蔽型 HDMI 视频中间人植入设备。

设备本体串联于任何标准 HDMI 输出源（例如工作站计算机、服务器、KVM 切换器、视频游戏主机）与显示设备（例如液晶显示器、投影仪、电视）之间。在运行期间，Screen Crab 完全保持直通（Passthrough），目标端用户与受测主机完全无法察觉任何延迟或画质降阶。

设备在内部并联捕获视频画面信号，根据预设的时间间隔自动截取高画质屏幕截图，并可存储于本机 MicroSD 存储卡，或通过内置 Wi-Fi 天线即时将图片加密传输至 Hak5 Cloud C² 云端服务器。

### 硬件技术规格与原厂校准基准表

| 硬件组件项目 | 官方技术规格说明 |
|---|---|
| **视频直通接口 (Video Interface)** | HDMI 输入 / 输出（支持分辨率最高达 1080 p @ 60 fps）|
| **无线传输模块 (Wireless)** | 2.4 GHz 802.11 b/g/n，提供带外（Out-of-Band）隐蔽回传 |
| **本机存储接口 (Storage)** | MicroSD 存储卡插槽（兼容 FAT32 与 exFAT，容量最高支持 128 GB）|
| **供电接口 (Power)** | USB Type-C 5 V DC 供电 |
| **音频侧录功能 (Audio Capture)** | 支持 HDMI PCM 内嵌音频旁路侧录分析 |
| **状态指示模块** | 多色 RGB 状态诊断 LED 指示灯 |

---

<!-- section：features -->
### 1.2 运行架构与核心原理 (Screen Crab Basics)

Screen Crab 采用物理层直通信号分流架构，其核心特点包含：
1. **无驱动程序需求**：在目标操作系统内完全不产生任何 USB 或 PCI 设备标识，对目标主机而言完全透明。
2. **EDID 智能模拟与复制**：自动转发显示器原生 EDID 参数，确保目标系统输出最佳分辨率，无分辨率突变或闪烁。
3. **灵活触发机制**：支持定时截图、动态检测画面变更、或远程 C2 指令即时手动截图。
4. **图像压缩引擎**：内置硬件 JPEG 编码器，可在毫秒级别完成高分辨率图像压缩并写入存储设备。

---

<!-- section：configuration -->
## 2. 组态配置、Cloud C² 与操作模式

### 2.1 组态配置文件解析 (Configuring the Screen Crab)

Screen Crab 的所有运行参数均记录于 MicroSD 卡根目录下的 `config.txt` 文本文件中。使用文本编辑器即可完成全功能组态配置：

```ini
# Screen Crab 主要配置文件示例
# 截图模式：INTERVAL（定时）或 MANUAL（手动）
CAPTURE_MODE=INTERVAL

# 截图间隔时间（单位：秒）
INTERVAL=30

# 图像画质配置（1-100）
QUALITY=85

# Wi-Fi 连接配置（选填，供 Cloud C2 云端回传使用）
WIFI_SSID=MyCorporateWiFi
WIFI_PASS=SecurePassword123

# Cloud C2 注册连接文件存放于 MicroSD 根目录：device.config
```

---

### 2.2 LED 状态指示灯诊断 (LED Status Indications)

Screen Crab 具备多色 RGB 状态指示灯，开机后将依序呈现系统各阶段状态：

| 灯号状态 | 意义说明 | 操作建议 |
|---|---|---|
| **绿灯常亮** | 正常运行中，截图正常执行 | 设备处于就绪状态 |
| **绿灯闪烁** | 正在捕获当前画面并写入存储介质 | 正在进行 I/O 操作 |
| **蓝灯闪烁** | Wi-Fi 正在尝试连接中 | 确认 AP 信号强度与密码 |
| **蓝灯常亮** | 已成功连接至 Wi-Fi 与 Cloud C² | 云端通道已建立 |
| **红灯常亮** | 错误状态：未检测到 MicroSD 卡或文件系统损坏 | 检查 MicroSD 是否格式化为 FAT32/exFAT |
| **黄灯闪烁** | 未检测到有效 HDMI 输入视频源 | 检查信号线接线顺序 |

---

### 2.3 Hak5 Cloud C² 云端连接配置 (Configuring Cloud C²)

通过集成 Hak5 Cloud C²，安全人员无需回收设备即可进行即时监视：
1. 登录您的 Cloud C² 服务器网页管理界面。
2. 在“Devices”列表中点击“Add Device”，选择 **Screen Crab**。
3. 下载生成的注册配置文件 `device.config`。
4. 将 `device.config` 文件放置于 MicroSD 存储卡之根目录。
5. 确保 `config.txt` 中已正确填写可访问外网之 Wi-Fi 账号密码。
6. 将 Screen Crab 重新上电，设备将自动连接并在 Cloud C² 仪表盘上显示“Online”，提供即时画面流媒体浏览。

---

<!-- section：maintenance -->
### 2.4 2024 SSL 证书安全更新 (2024 SSL Update)

> [!IMPORTANT]
> 针对 2024 年之后的 Cloud C² 云端通信，官方实施了全新的 TLS/SSL 证书链路验证标准。若设备出厂年份较早，请务必依原厂指南将更新的 root CA 证书复制至 MicroSD 卡，以确保 HTTPS/WSS 加密通道不因证书过期而中断。

---

## 3. 硬件规格、安全性指南与故障排除

### 3.1 重要安全指引与法规声明 (Safety and Warnings)

1. **合法授权原则**：Screen Crab 仅供具备完整书面授权之红队渗透测试、安全演练或企业自建网络环境安全检验之用。
2. **散热与通风**：视频处理芯片在 1080 p 60 fps 连续编码时会产生正常运行热量，请确保设备周围保留通风空间，切勿紧贴密闭高温管线。
3. **电压保护**：仅限使用合格之 5 V USB-C 供电源，避免使用具备非标准高压快充协议之适配器。

---

### 3.2 官方技术规格基准表 (Hardware Specifications)

- **处理架构**：专属高频视频处理芯片
- **分辨率兼容性**：1080 p (1920x1080)、720 p (1280x720)、480 p 等标准数字视频模式
- **存储规格**：MicroSD 扩展槽，最高支持 128 GB
- **外壳设计**：哑光黑隐蔽式小巧铝合金外壳
- **耗电量**：约 5 V @ 500 mA - 800 mA

---

### 3.3 常见故障排查指引 (Troubleshooting Guide)

1. **显示器无画面输出（黑屏）**：
   - 确认 HDMI IN 与 HDMI OUT 方向是否接反（主机应接 IN，显示器接 OUT）。
   - 检查 USB-C 供电线是否有足够 5 V 电流。
2. **截图皆为全黑或噪点**：
   - 目标设备可能启用了 HDCP 数字内容保护机制。Screen Crab 遵循标准消费级规范，若信号受 HDCP 保护将无法截图。
3. **MicroSD 卡无法读取**：
   - 使用 SD Card Formatter 工具重新将存储卡格式化为 FAT32 或 exFAT。
