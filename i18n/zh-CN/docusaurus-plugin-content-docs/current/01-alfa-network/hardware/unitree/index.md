---
id: alfa-hardware-unitree
title: ALFA 网卡在 Unitree 机器狗上的集成与远距遥测指南
sidebar_label: Unitree 机器狗
sidebar_position: 3
description: ALFA 无线网卡在宇树 Unitree（Go2 / B2）机器狗上的集成教程——解决内置天线信号弱与电机电磁干扰，实现低延迟图传与远距遥测控制。
tags: [alfa, unitree, robotics, quadruped, wifi-6e, telemetry]
keywords: [Unitree ALFA, 宇树 机器狗 无线网卡, Go2 遥测, AWUS036AXML Unitree, 机器人 5GHz 图传]
---

# ALFA 无线网卡在 Unitree 机器人上（Go2 / B2 / A1）

> **一句话定位**：Unitree 机器狗（Go2、B2、A1）机载的是 NVIDIA Jetson，但随附的内置 Wi-Fi 天线很弱。装上一支搭配外置天线的 ALFA 无线网卡，能把机器人的无线控制链接范围，从「只能跟着你在房间里走」变成「在场地另一端也能稳定指挥它」。

## 这篇文章适合你吗？

- **难度**：中阶（需要会用 SSH 连接操作机载电脑）
- **预估时间**：30〜45 分钟
- **你会用到的技能**：基本 Linux 终端操作、SSH 远程连接
- **读完你可以做到**：
  1. 让 ALFA 无线网卡在机器人的机载电脑上被正确辨识
  2. 创建一个专用的 5 GHz 控制连接，避开 2.4 GHz 的干扰
  3. 用实际的延迟/遗失率数据验证连接品质好不好

---

## 概念说明：机器狗的无线控制链接问题

机器狗其实是一套「长了腿的神经系统」：机载的 Jetson 电脑要把影像、光达（LiDAR）与惯性传感器（IMU）的遥测数据即时传给你，同时接收你下达的步态、任务指令。这条链接需要**低延迟、高可靠性，而且要有一定的范围**。

问题是，机器人运算模块上出厂内置的天线，表现跟你手机、笔记本电脑内置的天线差不多——大概 30 公尺就已经很勉强，而且 2.4 GHz 频段在实验室环境里常常被其他 Wi-Fi 设备、蓝牙设备，甚至机器人自己的马达电磁干扰（EMI）吃得乱七八糟。

解决方式跟 [Jetson 集成指南](/alfa-network/hardware/jetson/)是同一套逻辑——用外置的 ALFA 无线网卡取代原本的无线链接路径，实际上有效的做法是：

1. **优先用 5 GHz 频段**：机器人上的 2.4 GHz 频段很容易被马达与其他设备干扰，能避开就避开。
2. **外置天线位置很重要**：无线网卡的外置天线效果比机器人机壳上任何内置天线都好，而且你可以把它摆在金属机壳上方、信号不会被屏蔽的位置。
3. **依需求选网卡**：入门选 [AWUS036ACM](/alfa-network/products/awus036acm/)（兼容性最广）；想要 Wi-Fi 6 加蓝牙选 [AWUS036AXM](/alfa-network/products/awus036axm/)；想要 6 GHz 频段选 [AWUS036AXML](/alfa-network/products/awus036axml/)。

> 📘 **名词小教室**
> - **遥测（Telemetry）**：机器人把自己身上的传感器数据（影像、位置、姿态等）即时回传给你的过程，方便你在远程掌握机器人的状态。
> - **EMI（电磁干扰）**：机器人身上的马达运转时会产生电磁波，这些电磁波可能会干扰附近的无线信号，这也是为什么机器人上的 Wi-Fi 常常比想像中不稳定。
> - **iperf3**：一个专门用来测试网络吞吐量和延迟品质的工具，这篇文章会用它来确认连接设好之后品质到底好不好，而不是只凭感觉判断。

---

## 你需要准备的东西

- [ ] **硬件**：Unitree 机器人（Go2 / B2 / A1），机载电脑可通过 SSH 访问（出厂默认 IP 通常是 `192.168.123.161`）
- [ ] **地面站笔记本电脑**：运行 Ubuntu 系统（可参考 [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)）
- [ ] **ALFA 无线网卡**：依需求从上一节挑选型号
- [ ] **独立供电的 USB Hub**：如果机器人的 USB 供电不足以驱动高功率网卡时使用
- [ ] **驱动进程参考（GitHub）**：
  - MediaTek MT76 系列驱动（适用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Unitree 官方 SDK（如果你后续要做更高端的程序化控制）：https://github.com/unitreerobotics/unitree_sdk2
  - 社群维护的 ROS2 / Wi-Fi 集成项目（想串接 ROS2 生态系可以参考）：https://github.com/abizovnuralem/go2_ros2_sdk

---

## Step-by-Step 设置教学

### 步骤 1：连上机器人并确认内核版本

```bash
ssh unitree@<机器人IP>
uname -r
```

**预期结果**：你会看到一个 L4T（NVIDIA Jetson 专用）内核版本，例如 `5.10.65-tegra` 或 `6.6.0-tegra`。

跟 [Jetson 集成指南](/alfa-network/hardware/jetson/)里提到的规则一样：MT7921AUN 芯片的网卡（AWUS036AXM / AXML）需要内核版本 5.18 以上；MT7612U 芯片（AWUS036ACM）则在任何近期内核版本上都能用。

---

### 步骤 2：插入 ALFA 无线网卡

在机器人的机载电脑上运行：

```bash
lsusb | grep -iE "mediatek|realtek"
iw dev
```

**预期结果**：你的网卡出现在 `lsusb` 清单里，同时多出一个新的无线接口（通常是 `wlan1`）。

如果是 Realtek 芯片，请依照 [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/) 安装 DKMS 驱动进程；如果是 MediaTek 内置于内核的芯片，这一步做完就直接可以用，不用额外安装任何东西。

---

### 步骤 3：创建专用的 5 GHz 控制连接

用一个独立的无线基地台（可以是你的地面站笔记本电脑开热点，或另一台路由器）创建专用连接，让机器人的控制链接跟实验室里其他 Wi-Fi 流量分开，互不干扰：

```bash
sudo nmcli device wifi connect "robot-link" password "你的密码"
iw dev wlan1 link
```

**预期结果**：画面显示 `Connected to robot-link`，并附带一行显示目前信道与连接速率的信息。

接着确认这条连接走的真的是 5 GHz 频段：

```bash
iw dev wlan1 info | grep channel
```

**预期结果**：显示类似 `channel 36 (5180 MHz)` 这样的 5 GHz 信道信息。如果显示的是 2.4 GHz 的信道，代表你的基地台目前设置成 2.4 GHz，需要回去基地台端切换成 5 GHz。

---

### 步骤 4：锁定 5 GHz 频段，避免自动切回吵杂的 2.4 GHz

有些系统在信号不稳时会自动切回 2.4 GHz 频段，这样一来前面选 5 GHz 的努力就白费了。用下面这行指令，直接把机器人端的连接锁定在 5 GHz 频段：

```bash
sudo nmcli connection modify robot-link 802-11-wireless.band a
sudo nmcli connection up robot-link
```

> 💡 **设置小提醒**：这里的参数是 `802-11-wireless.band a`，代表锁定 5 GHz 频段（`a` 对应 802.11a/5GHz）。如果你之后查其他数据看到 `band bg`，那个参数指的是锁定 2.4 GHz（`b`/`g` 对应 2.4GHz），跟这里的目的正好相反，记得不要混用。

**预期结果**：连接会在 5 GHz 频段重新创建。可以再跑一次步骤 3 的检查指令 `iw dev wlan1 info | grep channel` 确认信道确实停留在 5 GHz。

接着，把发射功率调到你所在地区的法规上限，让信号更稳：

```bash
sudo iw reg set TW   # 换成你所在地的国家代码
sudo iwconfig wlan1 txpower 30
```

**预期结果**：指令运行没有出现错误消息，且 `iwconfig` 显示 `Tx-Power=30 dBm`（实际数值会受你所在地区的法规上限约束，不一定every次都是 30）。

---

### 步骤 5：用遥测连接测试验证连接品质

单纯的 ICMP（也就是一般的 `ping`）没办法准确反映真实的连接延迟，这一步改用 UDP 数据包测试工具 `iperf3`，量测实际吞吐量与数据包遗失率：

在机器人端运行：

```bash
iperf3 -s &
```

在地面站笔记本电脑上运行：

```bash
iperf3 -c <机器人IP> -u -b 100M -t 10
```

**预期结果**：画面会显示一个吞吐量数字（Mbits/sec）以及数据包遗失率（通常应该落在 0〜1%）。如果你在实际工作距离上量到的遗失率超过大约 1%，代表天线位置或信道需要调整——可以试试切换到另一个 5 GHz 信道（重新设置连接后运行 `sudo iw dev wlan1 set channel 149`），或者把网卡移到机壳上方更不容易被屏蔽的位置。

---

## 常见问题与排除指引

### Q1：马达启动运转时，连接就会断断续续？
- **原因**：马达产生的电磁干扰（EMI），加上天线位置不够好。
- **解决方法**：把无线网卡的天线移到金属机壳上方；改用 5 GHz 频段；并检查目前信道是否壅塞。

### Q2：无线网卡插入机器人后完全看不到？
- **原因**：机器人的 USB 连接端口供电受限。
- **解决方法**：改用独立供电的 USB Hub；或尝试插到机器人上不同的 USB 连接端口。

### Q3：MT7921AUN 网卡（AXM / AXML）侦测不到？
- **原因**：机器人上的 JetPack 版本太旧，内核版本低于 5.18。
- **解决方法**：升级机器人机载电脑的 JetPack 版本；或改用 MT7612U 芯片等级的网卡（如 AWUS036ACM）。

### Q4：距离拉远之后连接又自动回落到 2.4 GHz？
- **原因**：基地台或连接设置没有真正锁定 5 GHz 频段。
- **解决方法**：重新确认步骤 4 的指令有正确运行（`802-11-wireless.band a`），并用步骤 3 的检查指令再次确认信道。

### Q5：连接量测时出现高延迟的尖峰值？
- **原因**：目前使用的信道壅塞，附近有其他设备在抢同一个信道。
- **解决方法**：挑一个比较干净的 5 GHz 信道测试；如果你的基地台支持，也可以考虑改用 6 GHz 频段（需搭配 AWUS036AXML）。

---

## 参考数据与延伸阅读

- [ALFA 无线网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——同样的内核版本判断逻辑，内容更深入
- [AWUS036AXM 产品页面](/alfa-network/products/awus036axm/)——适合机器人控制链接的 Wi-Fi 6 + 蓝牙机型
- [ALFA 无线网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——驱动安装细节
- [词汇表](/getting-started/glossary)——遥测、EMI 等名词的完整解释
- MediaTek MT76 系列驱动（社群维护，含 DKMS）：https://github.com/morrownr/mt76
- Unitree 官方 SDK：https://github.com/unitreerobotics/unitree_sdk2
- 社群维护的 ROS2 / Wi-Fi 集成项目：https://github.com/abizovnuralem/go2_ros2_sdk
- [Unitree 官方文档](https://support.unitree.com/)——机器人 SDK 与网络设置参考

**标签：** `alfa` `unitree` `机器人` `机器狗` `無線控制` `新手指南`
