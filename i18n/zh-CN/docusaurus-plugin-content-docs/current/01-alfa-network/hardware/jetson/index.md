---
id: alfa-hardware-jetson
title: ALFA 网卡在 NVIDIA Jetson (Orin Nano / NX) 上的集成与设置指南
sidebar_label: NVIDIA Jetson
sidebar_position: 1
description: ALFA 无线网卡在 NVIDIA Jetson Orin Nano / NX 上的集成教程——6 GHz Wi-Fi 6E 流媒体、监听模式启用与 JetPack 内核驱动设置，含每一步的预期结果。
tags: [alfa, jetson, nvidia, robotics, wifi-6e, monitor-mode]
keywords: [Jetson Orin ALFA, Jetson Wi-Fi 6E, AWUS036AXML Jetson, 机器人无线传输, JetPack 驱动]
---

# ALFA 无线网卡在 NVIDIA Jetson 上（Orin Nano / NX）

> **一句话定位**：Jetson 内置的 Wi-Fi 天线很弱，做机器人或电脑视觉项目时常常撑不住。装上一支 ALFA 无线网卡，就能让 Jetson 用 6 GHz 频段（Wi-Fi 6E）低延迟串流影像，或激活监听模式做无线研究。

> ⚠️ **实测范围**：Yupitek 的 ALFA 兼容性测试仅在 ASUS GX10／Ubuntu 24.04 ARM64／kernel 6.17 上进行，**NVIDIA Jetson尚未实测**。本页关于驱动是否可用的说明，是依平台内核版本与各驱动进入 mainline 的版本（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）推断，并非在该硬件上验证。实际请以 `uname -r` 为准。请仅在您自己拥有或已获授权的网络上测试。

## 这篇文章适合你吗？

- **难度**：入门〜中阶（会下 Linux 终端指令即可，不需要写程序）
- **预估时间**：30〜60 分钟（含系统更新与驱动编译时间）
- **你会用到的技能**：基本终端操作（拷贝粘贴指令、看懂指令输出）
- **读完你可以做到**：
  1. 确认自己的 Jetson 该走哪一条驱动安装路径
  2. 让 ALFA 无线网卡在 Jetson 上被正确辨识
  3. 用 6 GHz 频段做低延迟摄影机串流，或激活监听模式做数据包截取

---

## 概念说明：为什么 Jetson 需要外置无线网卡

Jetson Orin Nano / NX 主板（含它的载板）出厂就带了一颗无线网卡，但那颗网卡的设计目标只是「能上网、能 `apt update`」，不是为了机器人或电脑视觉这种对带宽、延迟要求更高的应用设计的。如果你的项目需要下面任何一项，内置网卡通常不够用：

- **6 GHz（Wi-Fi 6E）频段**：Jetson 载板的内置网卡只有 2.4 GHz 和 5 GHz。6 GHz 是一个相对「空旷」、杂讯少的频段，很适合拿来即时传摄影机画面或光达（LiDAR）点云数据，不用跟同一间实验室里一堆人的 2.4 GHz 设备抢带宽。
- **稳定的高吞吐量连接**：目前实测确认 6 GHz 可用的 ALFA 无线网卡是 **AWUS036AXML**（芯片 MT7921AUN；AXM 的 6 GHz 未实测），而且它的驱动程序从 Linux 内核 5.18 版之后就已经内置，不用自己编译。
- **监听模式（Monitor Mode）**：如果你的项目是做无线网络研究（例如分析数据包），可以通过标准的 `mac80211` 驱动路径，在支持的芯片上直接激活监听模式。

> 📘 **名词小教室**
> - **监听模式（Monitor Mode）**：让网卡不只接收「要给自己的」数据包，而是把空气中飞过的所有无线数据包都抓下来，是做无线网络分析、Wireshark 课程作业的基础模式。一般上网用的「Managed 模式」做不到这件事。
> - **DKMS（Dynamic Kernel Module Support）**：一种让驱动程序「跟着内核版本自动重新编译」的机制。白话说：以后系统更新内核版本，DKMS 会自动帮你的网卡驱动重新编译一次，不用每次都手动重装。
> - **JetPack**：NVIDIA 官方为 Jetson 系列准备的完整系统套件（包含定制化的 Linux 内核、驱动程序、开发工具）。JetPack 的版本会直接决定你的 Jetson 用的是哪个内核版本，这对能不能用某些网卡芯片有直接影响。
> - **L4T（Linux for Tegra）**：Jetson 专用的 Linux 内核，不是一般 Ubuntu 桌机用的内核，所以内核版本命名和更新方式跟一般 Linux 教学看到的不太一样。

Jetson 能用哪种驱动路径，关键在于你的 **JetPack 版本**（决定内核版本）：

| JetPack 版本 | L4T 内核版本 | `mt7921u`（AWUS036AXM / AXML；mainline 自 5.18） | `mt76x2u` / `mt76x0u`（AWUS036ACM / ACHM；mainline 自 4.19） |
| ------------ | ------------ | ------------------------------------ | ------------------------------------ |
| JetPack 5.x  | 5.10         | ❌ 内核早于 5.18，需自行 backport／DKMS | ✅ 内核已内置                        |
| JetPack 6.x  | 5.15         | ❌ 内核早于 5.18，需自行 backport／DKMS | ✅ 内核已内置                        |

上表是**按内核版本推断，并未在 Jetson 上实测**。Realtek 机型的 mainline 起始版本为：EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17；内核低于该版本时需要 DKMS 或更新内核，实际视平台内核版本而定。

**记住这条规则**：AWUS036AXML 的驱动 `mt7921u` 需要内核 5.18 以上，请用 `uname -r` 确认；按 NVIDIA 公布的内核版本，JetPack 5（5.10）与 JetPack 6（5.15）都早于 5.18，内核不含主线 `mt7921u`，需要 backport／DKMS 驱动（推断，未实测；可用 `modinfo mt7921u` 确认）。经典款 **AWUS036ACM** 的 `mt76x2u` 自内核 4.19 起内置，JetPack 5 或 6 都可以用。

---

## 你需要准备的东西

- [ ] **硬件**：已安装好 JetPack 的 NVIDIA Jetson Orin Nano 或 Orin NX
- [ ] **网络环境**：第一次设置建议先接乙太网络线（避免因为 Wi-Fi 没设好而连不上机器调试）
- [ ] **ALFA 无线网卡**：
  - 要用 6 GHz（Wi-Fi 6E）：[AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)（JetPack 5／6 的内核均早于 5.18，需 backport／DKMS 驱动）
  - 一般用途、兼容性最广：[AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)（JetPack 5 / 6 都可以）
- [ ] **驱动程序参考（GitHub）**：
  - MediaTek MT76 系列驱动（社区维护的独立可安装版本，含 DKMS，适用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（aircrack-ng 社区维护，支持 ARM64）：https://github.com/aircrack-ng/rtl8812au
- [ ] 若使用高功率无线网卡，建议准备一个**有独立供电的 USB Hub**（Jetson 的 USB 连接端口在高负载时可能供电不足）

---

## Step-by-Step 设置教学

### 步骤 1：检查你的 JetPack 版本与内核版本

在开始之前，先确认自己属于上面表格的哪一列。打开终端，输入：

```bash
uname -r
dpkg -l | grep nvidia-l4t-core | head -1
```

**预期结果**：你会看到类似下面两种其中一种输出：

```text
5.15.x-tegra           # JetPack 6（内核 5.15）
# 或
5.10.x-tegra           # JetPack 5（内核 5.10）
```

无论是 `5.10.x` 还是 `5.15.x`，内核都早于 5.18：AWUS036ACM／ACHM（mt76，4.19 起内置）可以直接使用；AWUS036AXM／AXML（`mt7921u`）需要 backport／DKMS 驱动，请先用 `modinfo mt7921u` 确认内核是否已带有此模块。

---

### 步骤 2：MediaTek 内置于内核的路径（建议优先尝试）

这是最省事的路径：MediaTek 芯片的驱动已经写进 Linux 内核里，插入网卡通常不用额外装任何东西。

把 ALFA 无线网卡插入 Jetson 的 USB 端口，然后：

```bash
lsusb | grep -i mediatek
iw dev
```

**预期结果**：`lsusb` 那行应该会看到类似这样的输出：

```text
Bus 001 Device 002: ID 0e8d:7961 MediaTek Corp. MT7921U
```

`iw dev` 则会看到一个新的无线接口，例如：

```text
phy#0
	Interface wlan0
		ifindex 3
		type managed
```

如果你用的是 JetPack 6 + AWUS036AXML，可以再确认 6 GHz 信道有没有被系统看见：

```bash
iwlist wlan0 freq | grep -E "6 GHz|Channel 1|Channel 233" | head
```

**如果什么都没出现**：通常是法规领域（国家代码）还没设置，运行以下指令后重新激活接口即可：

```bash
sudo iw reg set TW
sudo ip link set wlan0 down && sudo ip link set wlan0 up
```

> 💡 这里的 `TW` 是台湾的国家代码，如果你人在其他国家，请换成对应的代码。

---

### 步骤 3：连接并测试串流

先确认网卡能正常连上一个 Wi-Fi 网络：

```bash
nmcli device wifi connect "你的SSID" password "你的密码"
```

**预期结果**：

```text
Device 'wlan0' successfully activated with 'MySSID'.
```

连上之后，如果你的项目是要串流摄影机画面，可以用下面这段指令测试（示例用 GStreamer，走 6 GHz 频段的低延迟串流）：

```bash
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! \
    x264enc tune=zerolatency bitrate=8000 ! rtph264pay ! \
    udpsink host=192.168.1.50 port=5000
```

**预期结果**：画面应该是连续、低延迟的串流（把指令里的 `192.168.1.50` 换成你接收端的实际 IP）。这就是 6 GHz 频段的价值所在——空旷、少人抢带宽，延迟会比挤在 2.4 GHz 上明显低。

---

### 步骤 4：Realtek 机型的安装路径（如果你的网卡不是 MediaTek 芯片）

如果 `lsusb` 抓不到 MediaTek 设备，代表你的网卡可能是 Realtek 芯片，需要额外编译安装驱动程序（也就是前面提到的 DKMS）。Realtek 机型是否需要 DKMS 取决于内核版本：EACS 自 6.2、ACH／ACS 自 6.13、AX／AXER 自 6.17 起已内置于 mainline，低于该版本才需要（视平台内核版本而定，未在 Jetson 实测）；下方 aircrack-ng 的驱动仅适用于 RTL8812AU（AWUS036ACH）。

Jetson 的 ARM64（aarch64）架构也可以编译 DKMS 驱动，只是编译时间会比一般桌机 Linux 慢一些，尤其在 Orin Nano 上请耐心等待：

```bash
sudo apt install -y build-essential dkms git
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

**预期结果**：最后一行会出现：

```text
DKMS: install completed.
```

在 Orin Nano 上这个步骤可能需要几分钟，不要中途中断。

---

### 步骤 5：激活监听模式（无线研究 / 实验室用途）

如果你的项目需要做数据包分析而不只是连网，可以激活监听模式测试：

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**预期结果**：接口会变成 `wlan0mon`，代表监听模式已启用。`aireplay-ng --test` 的注入成功率因网卡而异：在 ASUS GX10／kernel 6.17 的实测中，ACM 在 2.4 GHz 约 63–83%；**AXM／AXML 的注入测试会失败**（显示 `Found 0 APs`／`No Answer`，主因是 kernel 6.16 起 mac80211 chanctx 的退化，并非芯片限制），且监听表现偏弱。以上在 Jetson 上尚未实测。

> ⚠️ **供电提醒**：Orin Nano 的 USB 连接端口在高负载下可能供电不稳。如果你的网卡是高功率型号，建议搭配**有独立供电的 USB Hub**。另外也留意 Jetson 的电源模式（`nvpmodel`）——如果目前是降频的省电模式，也可能影响 USB 供电稳定度，可以尝试切换到较高性能的电源模式。

---

## 常见问题与排除指引

### Q1：AWUS036AXML 在 JetPack 5／6 上完全看不到？
- **原因**：JetPack 5（5.10）与 JetPack 6（5.15）的内核都早于 5.18，没有主线 `mt7921u` 驱动模块。
- **解决方法**：升级 JetPack 无法解决；请安装 backport／DKMS 版 `mt7921u` 驱动，或改用 mt76 芯片、内核 4.19 起内置的 AWUS036ACM。

### Q2：明明设置好了，却找不到 6 GHz 信道？
- **原因**：法规领域（国家代码）没有设置，系统不知道该开放哪些信道。
- **解决方法**：运行 `sudo iw reg set <你的国家代码>`，再重新激活网卡接口。

### Q3：跑摄影机串流时网卡常常断线？
- **原因**：USB 供电不足，高负载时电压不稳。
- **解决方法**：改用有独立供电的 USB Hub；或把 Jetson 的电源模式（`nvpmodel`）调到较高性能等级。

### Q4：DKMS 编译很慢，甚至失败？
- **原因**：ARM64 架构本身编译速度较慢，加上有时候缺少对应的内核标头档（headers）。
- **解决方法**：
  ```bash
  sudo apt install -y linux-headers-$(uname -r)
  ```
  装好标头档后再重新运行 `sudo make dkms_install`。

### Q5：监听模式怎么样都激活不了？
- **原因**：通常是 Realtek 网卡的 stub 驱动程序（系统默认但功能阳春的驱动）跟你要用的完整版驱动互相打架。
- **解决方法**：确认你已经按照步骤 4 安装好 aircrack-ng 版本的驱动程序，而不是系统自带的阳春版。

---

## 参考数据与延伸阅读

- [AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)——想用 6 GHz 就选这支
- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)——兼容性最广的全能款
- [ALFA 无线网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——JetPack 骨子里就是 Ubuntu，很多概念可以互通
- [ALFA 无线网卡在 Kali Linux 上——监听模式与数据包注入](/alfa-network/linux-setup-kali/)——监听模式的延伸细节
- [ALFA 无线网卡在 Raspberry Pi 上（3 / 4 / 5）](/alfa-network/hardware/raspberry-pi/)——另一款轻量嵌入式主机的集成方式
- [词汇表](/getting-started/glossary)——监听模式、DKMS 等名词的完整解释
- MediaTek MT76 系列驱动（社区维护，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动（aircrack-ng 社区维护）：https://github.com/aircrack-ng/rtl8812au
- [NVIDIA Jetson 官方文档](https://docs.nvidia.com/jetson/)

**标签：** `alfa` `jetson` `nvidia` `机器人` `wifi-6e` `监听模式` `新手指南`
