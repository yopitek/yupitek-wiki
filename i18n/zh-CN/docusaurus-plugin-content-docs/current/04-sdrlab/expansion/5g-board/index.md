---
title: Flipper Zero 5G 扩展板 — 完整指南
source_url: https://doc.yupitek.com/sdrlab/expansion/5g-board/ （zh-cn 版）
revision: 2026-10-03
status: 待上架确认稿（审核纪录另存 audit_wiki.md，不含在此档）
translated_from: flipper_board_wiki_manual_zhtw.md
---

# Flipper Zero 5G 扩展板 — 完整指南

> **一句话**：5G 扩展板把双频 **2.4GHz + 5GHz Wi-Fi** 工具装到你的 Flipper Zero 上 — 一颗 ESP32-C5 跑 Marauder 固件，加上 GPS 接收器、2.8 寸屏幕与内置电池，全部整合在一个小模块里。

---

## 规格概览

| 项目 | 规格 |
|---|---|
| **Wi-Fi 模块** | **ESP32-C5**（2.4GHz + 5GHz），出厂预烧 Marauder 5G 固件 |
| **Sub-GHz** | **433MHz** A07 射频模块，**10 dBm** 输出（需在 Flipper 设为 External） |
| **GPS** | 内置 GPS 模块，可由 Flipper 或板上电池供电 |
| **屏幕** | **2.8 寸彩色 TFT**，内置 Marauder UI |
| **电池** | **800 mAh** 电池；充满电后充电指示灯熄灭 |
| **天线** | SMA 接口；随附双频 Wi-Fi 天线（3 dBi）、GPS 天线（20 dBi）、433MHz 天线（3 dBi） |
| **microSD** | **FAT32 格式** — 抓包存 `.pcap`，wardrive 存 `wardrive_*.csv` |
| **保护** | 所有脚位镀金，每个信号脚内置 **TVS** 保护元件 |
| **烧录** | USB-C 口（前左侧）；按住背面按键再插入 USB 进入烧录模式 |
| **操作** | Flipper Zero 应用程序：`[ESP32] WiFiMarauder`、`GPS` |
| **连接** | Flipper Zero GPIO 排针 |
| **蓝牙** | **BLE（Bluetooth LE）** ⚠️ 不支持 Bluetooth Classic |

### 天线

本板使用 SMA 天线接口。厂商列出的随附天线共三支：双频 Wi-Fi 天线（3 dBi，无需区分频段）、GPS 天线（20 dBi）与 433MHz 天线（3 dBi）。请依板上标示将天线接到对应接口。

---

## 这块板子能用来做什么

ESP32-C5 是 Wi-Fi 的主力：搭配 **Marauder 固件**可以扫描 AP 与客户端、嗅探 beacon 与 probe request、执行 deauth 与 PMKID 抓取测试，并记录 Wi-Fi 活动 — **现在包含 5GHz 网络，这是旧 ESP32 板看不到的**。

GPS 模块把你的 wardrive 记录变成带坐标的数据。内置电池让 Wi-Fi 侧不必一直吃 Flipper 的电，也可以脱离 Flipper 单机运行。

433MHz Sub-GHz 模块让你可以从 Flipper Zero 的 Sub-GHz 菜单操作 433MHz 信号研究 — 对 Flipper 内置收讯不良的环境特别有用。

> **请只在你自己的网络与设备上使用。** Deauth 与 probe 嗅探会干扰他人，且在大多数国家受管制。这是实验／教学工具。

---

## 开始之前

- Flipper 需要**含 WiFi Marauder 与 GPS 应用的定制固件** — 例如 **Momentum**。（固件基础见 [Flipper Zero 章节](/flipper-zero/)。）
- **本板已内置** 433MHz Sub-GHz 模块、2.8 寸 Marauder 屏幕、800mAh 电池。
- 准备一张 **FAT32** 格式的 microSD。

---

## 设置：GPIO 引脚（Momentum 固件）

在 **Momentum** 上：

1. 打开 `Protocol Settings → GPIO Pin Settings`
2. 将 **GPS Pin** 设为 **13** 或 **14**（UART 引脚）
3. 将 **ESP32 Pin** 设为 **15、16**（与 ESP32-C5 通信的 UART）
4. 退出设置并重启 Flipper

> ⚠️ **GPS 与 ESP32 是两组不同的 UART 引脚。**
> 本板出厂配置为：GPS = 13／14，ESP32 = 15／16。
> **不可把两者设成同一组引脚**，否则 GPS 与 Wi-Fi 都会没有响应。
> 若使用其他固件，设置路径可能略有差异，请参照各固件自身的 GPIO 设置菜单。

---

## 使用本板

### WiFi Marauder

1. 装好本板后，打开 `Apps → GPIO → [ESP32] WiFiMarauder`
2. 执行 **Scan AP**：附近的 AP 会显示 SSID、信道、RSSI、加密方式
3. 执行 **Packet Monitor** 或 **Beacon Sniff** 观察 beacon／probe 流量
4. **Wardrive**（搭配 GPS）会把记录输出为 CSV，之后可导出分析

扫描结果示例（**仅为示意格式，非实际抓取数据**）：

```
SSID              CH  RSSI  ENC     AUTH
yupitek-lab       6   -55   WPA2    PSK
Campus_Guest      11  -72   OPEN
```

### GPS

1. 接上 GPS 天线，朝向开阔天空方向放置（靠近窗户可以，户外更好）
2. 打开 `Apps → GPIO → GPS`，等待 — **首次定位需数分钟（冷启动）**
3. 卫星定位后位置数据就会进来。搭配 Marauder 即可取得带坐标的 Wi-Fi 记录

> ℹ️ GPS 时间固定回报 **UTC+0**。北京时间（UTC+8）请自行加 8 小时。固件菜单没有时区设置选项。

### 433MHz Sub-GHz

1. `Flipper Zero → Sub-GHz → Advanced Settings → Module`
2. 改为 **External**
3. 从 Sub-GHz 菜单使用 433MHz 频段

> 不做这一步，Flipper 会继续使用内置的 CC1101，本板的 433MHz 模块不会被启用。

### microSD 记录

1. 将 microSD 格式化为 **FAT32**（**不支持 exFAT／NTFS**）
2. 插入机身记忆卡槽
3. 在模块内 `Device → Settings` 确认 **PCAP saving 已开启**
4. 抓取结果存为 `.pcap`（用 [Wireshark](https://www.wireshark.org) 打开）；wardrive 另存 `wardrive_*.csv`

---

## 更新 ESP32-C5 固件

本板出厂**已预烧 Marauder 5G**，正常情况下不需要重新烧录。

若确实需要更新，请先向原厂或经销商索取**本板专用**的固件文件与版本号后再进行 — 开源 Marauder 发布页的通用 ESP32-C5 版本是否完全兼容本板的屏幕、SD 卡、GPS 与引脚配置，目前尚待原厂确认，请勿直接套用未经确认的版本，以免造成设备无法开机。

### 进入烧录模式（USB-C）

1. 按住背面按键
2. 保持按住的同时插入 USB-C 线（前左侧烧录口）
3. 使用确认支持 **ESP32-C5** 的烧录工具烧入固件
4. 拔线、重启 Flipper Zero

> ⚠️ 烧录前请确认所用工具支持 ESP32-C5 芯片；不确定时请以原厂／经销商提供的说明为准。

---

## 疑难排解

| 问题 | 原因 | 解法 |
|---|---|---|
| 应用程序显示「no module」 | GPIO 引脚未设置 | 重新检查 `GPIO Pin Settings`；重启 Flipper |
| 扫不到任何网络 | ESP32 UART 引脚设错 | 设置 ESP32 Pin 为 **15、16**；重启 |
| 5GHz 网络看不到或扫描不稳定 | 可能为固件版本相关限制 | 以扫描／监测为主；建议到 [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) 查询当前版本状态 |
| 5GHz deauth 没反应 | 已知固件限制 | 2.4GHz 较成熟稳定，建议优先使用 |
| GPS 一直无法定位 | 天线未接／室内／未满足定位时间 | 接上 GPS 天线、朝向开阔天空、走到户外或窗边，等待数分钟完成冷启动 |
| 模块有电但 Flipper 没反应 | Flipper 固件没有对应应用程序 | 安装含 WiFi Marauder／GPS 应用的定制固件（例如 Momentum） |
| SD 卡无法识别 | 格式不符 | 必须 FAT32；重新格式化 |
| 没有 PCAP 文件 | PCAP 存储未开启 | `Device → Settings` 开启 PCAP saving |
| 开机时模块没反应 | GPIO 连接器未完全密合 | 轻压至 flush；确认电池有电或已接 USB-C |

更多帮助：见 [SDRLAB 疑难排解中心](/sdrlab/troubleshooting/)。

---

## 已知限制

- **5GHz Deauth 的稳定度取决于固件版本。** 开源 Marauder 固件在 ESP32-C5 上的 5GHz deauth 支持仍在持续改进，建议以 2.4GHz 进行 deauth 测试为主；5GHz 建议以扫描、信号监测、wardrive 记录为主要用途。使用前建议到 [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) 确认当前版本状态。
- **5GHz PMKID／EAPOL 可用性尚无定论。** 建议自行实测后再据以宣称支持与否。
- **microSD 仅 FAT32**，不支持 exFAT、NTFS。
- **蓝牙仅 BLE**，ESP32-C5 无 Bluetooth Classic（BR/EDR）。
- **两个 USB-C 口功能不同** — 上缘前面为充电口；前左侧为 ESP32-C5 烧录口。

---

## 相关页面

- [WiFi multiboard（ESP32-S2）](/sdrlab/expansion/wifi-multiboard/) — 仅 2.4GHz 的小弟弟
- [NRF24 模块](/sdrlab/expansion/nrf24/) — 2.4GHz 包无线电嗅探
- [Flipper Zero 章节](/flipper-zero/) — 基础固件与设备说明

**标签**：`sdrlab` · `flipper-zero` · `5g-board` · `esp32-c5` · `marauder` · `gps`
