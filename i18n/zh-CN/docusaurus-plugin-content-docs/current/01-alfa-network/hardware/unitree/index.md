---
id: alfa-hardware-unitree
title: ALFA 网卡适配器在 Unitree 机器人上（Go2 / B2 / A1）
sidebar_position: 3
description: 为 Unitree 机器狗构建远距离无线控制链路——机载 Jetson 上的 ALFA 网卡适配器设置、5 GHz 链路调优与遥测技巧。
tags: [alfa, unitree, 机器人, 机器狗, 无线控制]
keywords: [Unitree Go2 Wi-Fi, 机器狗控制链路, ALFA 机器人遥测, 远距离 5 GHz]
---

# ALFA 网卡适配器在 Unitree 机器人上（Go2 / B2 / A1）

> **一句话定位（One-liner）**：Unitree 的机器狗（Go2、B2、A1）搭载 NVIDIA Jetson，出厂配的是**弱小的内置 Wi-Fi 天线**。带外置天线的 ALFA 网卡适配器把机器人的无线控制链路从「跟着你在房间里走」变成「在场地另一端指挥它」。

## 概念：无线控制链路问题

机器狗是长着腿的神经系统：机载 Jetson 向你的控制器流传输视频、LiDAR 和 IMU 遥测数据，并接收步态/任务指令。这条链路需要**低延迟、高可靠性、远距离**。机器人计算模块上的原厂天线正是你对消费级笔记本的预期——30 米就勉强，而且 2.4 GHz 会被实验室的 Wi-Fi、蓝牙和机器人自己的电机 EMI 吃得干干净净。

解决办法与 [Jetson](/alfa-network/hardware/jetson/) 相同：用 ALFA 网卡适配器替换无线电路径。实践中有效的配方：

1. **频段**：优先 **5 GHz**——机器人上的 2.4 GHz 是电机和其他设备干扰的苦海。
2. **天线**：网卡适配器的外置天线胜过机器人机身上的任何内置天线，而且你可以把它们放在金属面板上方，避免被遮挡。
3. **网卡适配器**：内核内置芯片组零麻烦、高可靠（便宜的 [AWUS036ACM](/alfa-network/products/awus036acm/)，要 Wi-Fi 6 + 蓝牙选 [AWUS036AXM](/alfa-network/products/awus036axm/)，想要 6 GHz 频段选 [AWUS036AXML](/alfa-network/products/awus036axml/)）。

```mermaid
flowchart LR
    A["Robot onboard Jetson"] --> B["ALFA adapter (5 GHz)"]
    B <-->|"dedicated control SSID"| C["Ground station laptop"]
    C --> D["ros2 / SDK commands"]
    A --> E["Camera + LiDAR + IMU telemetry"]
    E --> B
```

## 前置需求

- [ ] Unitree 机器人（Go2 / B2 / A1），机载电脑可通过 SSH 访问（出厂通常是 `192.168.123.161`）
- [ ] 运行 Ubuntu 的地面站笔记本（参见 [Ubuntu 指南](/alfa-network/linux-setup-ubuntu/)）
- [ ] ALFA 网卡适配器 + 如果机器人 USB 供电弱，准备**带供电的 USB 集线器**

## 第 1 步：访问机器人并检查内核

```bash
ssh unitree@<robot-ip>
uname -r
```

**预期输出**：一个 L4T/NVIDIA 内核（例如 `5.10.65-tegra` 或 `6.6.0-tegra`）。与 [Jetson 指南](/alfa-network/hardware/jetson/)一样，MT7921AUN 网卡适配器需要内核 5.18+（JetPack 6）；MT7612U 在任何较新内核上都能用。

## 第 2 步：插入 ALFA 网卡适配器

在机器人的机载电脑上：

```bash
lsusb | grep -iE "mediatek|realtek"
iw dev
```

**预期输出**：你的网卡适配器在 `lsusb` 中可见，外加一个新接口（通常是 `wlan1`）。对于 Realtek 芯片组，按 [Ubuntu 指南](/alfa-network/linux-setup-ubuntu/)所述安装 DKMS 驱动——或者干脆选一款内核内置型号，跳过整个步骤。

## 第 3 步：设置专用的 5 GHz 控制 SSID

专用接入点（放在地面站或路由器上）让控制链路与实验室流量隔离。让机器人连接它：

```bash
sudo nmcli device wifi connect "robot-link" password "your-passphrase"
iw dev wlan1 link
```

**预期输出**：`Connected to robot-link`，以及显示 5 GHz 信道和速率的链路行。验证信道是 5 GHz：

```bash
iw dev wlan1 info | grep channel
```

**预期输出**：`channel 36 (5180 MHz)`（或其他 5 GHz 信道）——如果显示 2.4 GHz，把接入点切换到 5 GHz。

## 第 4 步：锁定频段并最大化链路

在机器人侧强制仅 5 GHz，让它永远不会回落到嘈杂的频段：

```bash
sudo nmcli connection modify robot-link 802-11-wireless.band bg
```

> ⚠️ 等等——那条命令强制的是 **2.4 GHz**。要仅 5 GHz，请用 `802-11-wireless.band a`：

```bash
sudo nmcli connection modify robot-link 802-11-wireless.band a
sudo nmcli connection up robot-link
```

**预期输出**：在 5 GHz 频段上重新连接。再用 `iw dev wlan1 info | grep channel` 命令检查。

把发射功率提高到你所在地区允许的法定最大值：

```bash
sudo iw reg set TW   # your country code
sudo iwconfig wlan1 txpower 30
```

**预期输出**：无错误——`iwconfig` 显示 `Tx-Power=30 dBm`（受法规上限约束）。

## 第 5 步：用遥测 ping 测试验证

通过链路推送数据并测量远距离往返（ICMP 不是好的延迟代理；用 UDP 突发）：

```bash
# On the robot:
iperf3 -s &
# On the ground station:
iperf3 -c <robot-ip> -u -b 100M -t 10
```

**预期输出**：一个吞吐量数字（Mbits/sec）和 0–1% 丢包。在你的工作距离上丢包超过 ~1%，说明天线位置或信道需要调整——尝试另一个 5 GHz 信道（重新配置后 `sudo iw dev wlan1 set channel 149`），或把网卡适配器移到机身上方。

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 电机启动时链路中断 | 电机 EMI + 弱天线 | 把网卡适配器移到金属上方；切换到 5 GHz；检查信道拥塞 |
| 网卡适配器在机器人上不可见 | 机器人 USB 端口供电受限 | 带供电的 USB 集线器；尝试不同端口 |
| MT7921AUN 网卡适配器检测不到 | 旧 JetPack 上内核 < 5.18 | 升级机器人上的 JetPack，或使用 MT7612U 等级网卡适配器 |
| 远距离回落到 2.4 GHz | 频段引导 / 接入点配置 | 在机器人上强制 `802-11-wireless.band a`（第 4 步） |
| 高延迟尖峰 | 信道拥塞 | 选一个干净的 5 GHz 信道；如果你的接入点支持，考虑 6 GHz（AXML） |

## 参考

- [Jetson 指南](/alfa-network/hardware/jetson/)——相同的内核考量，更深入的细节
- [AWUS036AXM 产品页面](/alfa-network/products/awus036axm/)——机器人链路的 Wi-Fi 6 + 蓝牙
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)——驱动安装
- [Unitree 官方文档](https://support.unitree.com/)——机器人 SDK 与网络参考