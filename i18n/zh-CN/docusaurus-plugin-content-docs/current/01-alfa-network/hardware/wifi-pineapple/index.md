---
id: alfa-hardware-wifi-pineapple
title: Hak5 WiFi Pineapple × ALFA Network 集成指南
sidebar_label: Hak5 WiFi Pineapple
sidebar_position: 4
description: Hak5 WiFi Pineapple Mark VII 搭配 ALFA AWUS036ACM 网卡——5GHz 频段扩展设置、Web 后台配置与天线搭配建议，含每一步的预期结果。
tags: [hak5, wifi-pineapple, mk7, alfa, awus036acm, mt7612u, 5ghz]
keywords: [WiFi Pineapple, Hak5, AWUS036ACM, MT7612U, 5GHz 监听模式, PineAP, MK7AC]
---

# Hak5 WiFi Pineapple × ALFA Network 集成指南

> **一句话定位**：Hak5 WiFi Pineapple Mark VII 出厂只涵盖 2.4 GHz 频段，要涵盖 5 GHz 频段（现在大部分设备都会用到）就需要外置网卡。ALFA AWUS036ACM 用的芯片跟 Hak5 原厂扩充卡完全同款，但天线增益更高、散热更好，是目前最推荐的搭配选择。

## 这篇文章适合你吗？

- **难度**：中阶（需要熟悉基本的 SSH 操作跟网页后台设置）
- **预估时间**：20〜30 分钟
- **你会用到的技能**：基本终端操作、浏览器操作
- **读完你可以做到**：
  1. 帮 WiFi Pineapple 正确接上并辨识 ALFA 无线网卡
  2. 在 Web 后台设置同时涵盖 2.4 GHz 和 5 GHz 的扫描与广播
  3. 依照你的使用情境挑选合适的天线

---

## 概念说明：为什么 WiFi Pineapple 需要外置网卡

WiFi Pineapple Mark VII 这台设备本身内置了两组 2.4 GHz 无线电模块（一组用来当管理连接，另外一到两组负责扫描附近的 Wi-Fi 信号并广播）。但如果你的实验或课程需要涵盖 **5 GHz 频段**（802.11a/n/ac），内置的无线电就不够用了，必须通过机身上的 USB 端口外置一张支持 5 GHz 的网卡。

Hak5 官方文档明确指出，**MediaTek MT7612U** 芯片是唯一保证能在 WiFi Pineapple 上稳定运作的 5 GHz 网卡芯片。原因跟软件架构有关：WiFi Pineapple 使用的是 OpenWrt 这套嵌入式系统，Realtek 系列芯片（例如 RTL8812AU）在这个环境下需要额外的驱动进程，在高负载（大量数据包同时处理）时容易让系统当机或无预警重开机；而 MediaTek 的 `mt76x2u` 驱动则是直接写进 OpenWrt 内核里，稳定性好很多。

**ALFA AWUS036ACM** 使用的正是同一颗 MT7612U 芯片，跟 Hak5 官方扩充卡 MK7AC 系统辨识起来完全一样，差别在于 ALFA 网卡用的是标准 RP-SMA 天线接头（可以自己换天线），而且散热设计更好，长时间使用比较不容易过热降速。

> 📘 **名词小教室**
> - **Recon（侦察扫描）**：WiFi Pineapple 里的一个功能模块，用来扫描附近有哪些 Wi-Fi 基地台（AP）和连接中的设备。
> - **PineAP**：WiFi Pineapple 的内核功能之一，可以仿真广播 Wi-Fi 信号，常用于无线网络安全教学与研究情境。
> - **USB VID:PID**：每个 USB 设备出厂时都有一组「厂商代码:产品代码」，系统可以靠这组代码辨识设备是什么型号，等一下验证网卡有没有被正确辨识时会用到。

---

## 你需要准备的东西

- [ ] **硬件**：Hak5 WiFi Pineapple Mark VII 主机
- [ ] **ALFA 无线网卡**：[AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [ ] **供电设备**：一个能稳定输出 **5V/3A（15W）以上**、支持 QC 或 PD 快充协定的电源供应器或充电宝（原因见下方「供电注意事项」）
- [ ] **天线（依使用情境挑选，详见第四节）**：全向天线或指向性平板天线
- [ ] **驱动进程参考（GitHub）**：
  - MediaTek MT76 系列驱动原代码（WiFi Pineapple 的固件与此驱动家族同源）：https://github.com/openwrt/mt76
- [ ] **官方兼容性文档**：[Hak5 官方兼容 802.11ac 网卡清单](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)

---

## Step-by-Step 设置教学

### 步骤 1：硬件连接与供电确认

> ⚠️ **供电注意事项（请先看这段再动手）**：WiFi Pineapple Mark VII 主机本身耗电约 3〜5W，加上 AWUS036ACM 在 5GHz 满载发射时瞬间电流可达 900mA（约 4.5W），整机总功耗最高可能到 9.5W。
> - ❌ **不要用**：笔记本电脑的 USB 供电端口（通常只有 500mA）或便宜的 5V/1A 豆腐头充电器，功率不够会导致设备不稳定甚至自动重开机。
> - ✅ **请用**：能稳定输出 5V/3A（15W）以上、支持 QC 或 PD 快充协定的专用电源供应器或充电宝。

1. 将 ALFA AWUS036ACM 接上 WiFi Pineapple Mark VII 主机侧边或顶部的 **USB Host** 端口。
2. 建议先接上网卡，**再**接通 Pineapple 主机电源，这样可以避免开机瞬间供电不足的问题。

---

### 步骤 2：通过 SSH 确认网卡是否被正确辨识

用 SSH 连接进入 WiFi Pineapple 控制台（默认 IP 是 `172.16.42.1`）：

```bash
ssh root@172.16.42.1
```

连上之后，依序运行以下指令确认网卡状态：

```bash
# 1. 检视 USB 汇流排装置清单
lsusb
```

**预期结果**：

```text
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

```bash
# 2. 检视内核加载日志，确认驱动有没有正确加载
dmesg | grep -E "mt76|wlan"
```

**预期结果**：应该会看到类似这样的几行消息，代表驱动进程和固件都加载成功：

```text
mt76x2u 1-1:1.0: ASIC revision: 76120011 mac 00110000
mt76x2u 1-1:1.0: firmware: mt7662u.bin loaded
ieee80211phy3: mt76x2u registered as wlan3
```

```bash
# 3. 检查目前所有无线接口
iw dev
```

**预期结果**：清单里会多出一个新的接口（通常是 `wlan3`），代表 ALFA 网卡已经成功被系统辨识为一张独立的无线网卡。

---

### 步骤 3：在 Web 后台设置 5GHz 扫描与广播

1. 打开浏览器，前往 `http://172.16.42.1:1471` 登录 Pineapple 的 Web 管理接口。
2. 进入 **Recon（侦察扫描）** 模块：
   - 接口选择下拉列表里应该会自动出现 `wlan3 (5GHz)`。
   - 勾选同时扫描 **2.4 GHz + 5 GHz**，扫描周期可以设置为 `Continuous`（持续）或 `1 min`（每分钟）。
   - 点击 **Start Scan**，系统就会开始同时扫描 5GHz 信道（36〜165）上的基地台与连接设备。
3. 进入 **PineAP** 模块：
   - 在 **PineAP Settings** 里，可以把 5GHz 的广播指派给 `wlan3`，这样就能让 2.4GHz（`wlan1`）和 5GHz（`wlan3`）两个频段同时广播。

**预期结果**：Recon 页面上开始出现侦测到的设备与基地台清单，代表 5GHz 频段已经成功纳入扫描范围。

---

## 天线搭配建议（依使用情境挑选）

- **想要大范围、四面八方都能收到信号**（例如一般走动测试、涵盖整个会议室）：
  搭配两支 **ALFA ARS-NT5B7** 双频全向天线（2.4GHz 5dBi / 5GHz 7dBi），信号在水平 360 度范围内收发均匀，适合会议室或走廊这类需要环绕覆盖的场景。
- **想要对准特定方向、拉长距离**（例如定点观测特定楼层或区域）：
  搭配两片 **ALFA APA-M25** 双频指向性平板天线（2.4GHz 8dBi / 5GHz 10dBi，指向角约 60 度），可以有效过滤掉背后方向的杂讯，适合对准特定楼层或办公区域进行精准测试。

---

## 常见问题与排除指引

### Q1：插入 AWUS036ACM 之后，Pineapple 灯号突然熄灭、自动重开机？
- **原因**：USB 瞬间电压下降。插入高功率网卡的瞬间，电容充电加上射频模块初始化，需要的电流超过供电端能负荷的范围。
- **解决方法**：
  1. 先把 AWUS036ACM 插入 Pineapple，再接通 Pineapple 主机电源开机（不要开机状态下插拔）。
  2. 更换输出能力达 5V/3A 以上的电源供应器。

### Q2：接口卡在 `wlan2`，Web 后台看不到 5GHz 选项？
- **原因**：如果之前曾经插过其他 USB 网卡，系统里 `/etc/config/wireless` 这个设置档可能残留了旧的冲突设置。
- **解决方法**：通过 SSH 运行以下指令重置无线设置：
  ```bash
  rm -f /etc/config/wireless
  wifi config
  /etc/init.d/network restart
  ```

---

## 参考数据与延伸阅读

- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [Hak5 官方兼容 802.11ac 网卡清单](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)
- [ALFA 无线网卡在 Unitree 机器人上（Go2 / B2 / A1）](/alfa-network/hardware/unitree/)——另一个 5GHz 频段应用情境的集成方式
- [词汇表](/getting-started/glossary)——Recon、PineAP 等名词的完整解释
- MediaTek MT76 系列驱动原代码：https://github.com/openwrt/mt76

**标签：** `hak5` `wifi-pineapple` `mk7` `alfa` `awus036acm` `mt7612u` `5ghz` `新手指南`
