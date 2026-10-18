---
id: alfa-hardware-raspberry-pi
title: ALFA 网卡在 Raspberry Pi 上的集成与设置指南
sidebar_label: Raspberry Pi
sidebar_position: 2
description: ALFA 无线网卡在 Raspberry Pi（3B+ / 4B / 5）上的集成教程——外置供电判断、驱动安装与双网卡并行设置，含每一步的预期结果。
tags: [alfa, raspberry-pi, rpi, raspbian, wifi, monitor-mode]
keywords: [Raspberry Pi ALFA, 树莓派 无线网卡, AWUS036ACH 树莓派, AWUS036ACM 树莓派, Raspberry Pi 监听模式]
---

# ALFA 无线网卡在 Raspberry Pi 上（3 / 4 / 5）

> **一句话定位**：Raspberry Pi 内置的 Wi-Fi 只有单天线，信号弱、范围小。装上一支 ALFA 无线网卡，就能把 Pi 变成一台平价的 Wi-Fi 实验室工作站——拿来截取数据包做课堂作业，或当成一个真正有信号范围的无线基地台。

## 这篇文章适合你吗？

- **难度**：入门（会下 Linux 终端指令即可，不需要写程序）
- **预估时间**：20〜40 分钟
- **你会用到的技能**：基本终端操作（拷贝粘贴指令、看懂指令输出）
- **读完你可以做到**：
  1. 让 ALFA 无线网卡在 Pi 上被正确辨识
  2. 用它做监听模式数据包截取，并在 Wireshark 上分析
  3. 把 Pi 变成一台真正的 Wi-Fi 基地台（Access Point）

---

## 概念说明：为什么 Pi 是很适合搭配 ALFA 网卡的主机

Raspberry Pi 内置的无线网卡是单天线设计，信号本来就不强——拿来 SSH 远程连接没问题，但要做数据包分析（嗅探）或帮整个房间提供 Wi-Fi，内置网卡完全不够力。外置一支 ALFA 无线网卡可以解决这两个问题：

- **监听模式（Monitor Mode）实验室工作站**：搭配内置于 Linux 内核的芯片，插入就能直接开始截取数据包，很适合做 Wireshark 课堂作业——插入、`airmon-ng start`、开始截取。
- **访问点（hostapd Access Point）**：搭配外置天线的高功率网卡（如 AWUS036ACM/ACH），可以把 Pi 变成一台真正有效范围的 Wi-Fi 基地台，信号范围比内置网卡好很多。
- **双无线电技巧**：让 Pi 内置的网卡负责「连上网络」，外置的 ALFA 网卡负责「当基地台广播」——一台 Pi，同时服务两个网络。

> 📘 **名词小教室**
> - **监听模式（Monitor Mode）**：让网卡把空气中飞过的所有无线数据包都抓下来，而不只是接收「要给自己的」数据包，是做无线网络分析的基础模式。
> - **hostapd**：一套可以让 Linux 设备变成 Wi-Fi 基地台（Access Point）的软件，装好后你的 Pi 就能像家用路由器一样广播出一个 Wi-Fi 网络让别人连。
> - **DHCP / NAT**：DHCP 是自动配发 IP 地址给连上你 Pi 的设备的机制；NAT 则是让这些设备能通过 Pi 分享到的网络连上网际网络。这两个没设好，别人连得上你的 Wi-Fi 但上不了网。

各主板的硬件差异，会直接影响你能不能顺畅使用高功率网卡：

| 主板  | USB 规格          | 使用注意事项                          |
| ---- | -------------- | ----------------------------- |
| Pi 3 | USB 2.0        | 支持机型中最旧的一款；AC433 等级或内置于内核的网卡没问题 |
| Pi 4 | USB 2.0（共享总线） | 最受欢迎的选择——用高功率网卡请务必加一个独立供电的 USB Hub |
| Pi 5 | USB 3.0 + PCIe | 目前最快的 USB 规格；搭配 AC1200/AX1800 等级网卡吞吐量最佳 |

> ⚠️ **电源是 Pi 上最常见的故障原因**。Pi 3/4 的 USB 端口共用同一条 USB 2.0 总线；一支 500 mW 的 ALFA 网卡加上键盘，很容易让整条总线电压不足。只要你用的网卡功率高于 AWUS036ACS，就建议准备一个**独立供电的 USB Hub**。

---

## 你需要准备的东西

- [ ] **硬件**：已安装好 Raspberry Pi OS 的 Pi 3 / 4 / 5（建议使用 64 比特版本系统）
- [ ] **前置作业**：已完成 `sudo apt update && sudo apt upgrade`
- [ ] **ALFA 无线网卡**：监听模式强烈建议选用[内置于内核的芯片机型](/alfa-network/linux-compatibility-matrix/)，安装最省事
- [ ] **独立供电的 USB Hub**：如果你用的是高功率网卡，务必准备
- [ ] **驱动进程参考（GitHub）**：
  - MediaTek MT76 系列驱动（社群维护、含 DKMS，适用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（aircrack-ng 社群维护）：https://github.com/aircrack-ng/rtl8812au

---

## Step-by-Step 设置教学

### 步骤 1：识别无线网卡

插入 ALFA 网卡后，列出目前系统看到的所有接口——ALFA 应该会是「新出现」的那一个：

```bash
lsusb
iw dev
```

**预期结果**：你的网卡会出现在 `lsusb` 清单里，并且在 `iw dev` 里看到一个新接口，通常是 `wlan1`（Pi 内置的无线网卡多半是 `wlan0`）。

如果你的 ALFA 网卡是 Realtek 芯片，需要先安装 DKMS 驱动进程：

```bash
sudo apt install -y git dkms build-essential bc libelf-dev linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**预期结果**：最后一行显示 `DKMS: install completed.`（在 Pi OS 上这个步骤跟一般 Ubuntu 几乎一样）。

---

### 步骤 2：监听模式实验室工作站

激活监听模式：

```bash
sudo airmon-ng start wlan1
iwconfig wlan1mon
```

**预期结果**：`wlan1mon  IEEE 802.11  Mode:Monitor`——出现 `Mode:Monitor` 代表监听模式已经成功激活。

把截取到的数据包存成文档，之后拿到笔记本电脑上用 Wireshark 分析：

```bash
sudo tcpdump -i wlan1mon -w lab-capture.pcap
```

**预期结果**：终端显示 `listening on wlan1mon`，代表正在截取。想结束就按 `Ctrl-C`，然后把 `lab-capture.pcap` 这个文档传到你的笔记本电脑，用 Wireshark 打开分析。

---

### 步骤 3：把 Pi 变成一台 Wi-Fi 基地台（hostapd）

先安装需要的软件：

```bash
sudo apt install -y hostapd dnsmasq
```

把 ALFA 网卡设成固定 IP：

```bash
echo -e "interface wlan1\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant" | \
    sudo tee -a /etc/dhcpcd.conf
```

创建 hostapd 的设置档（示范用 2.4 GHz、发射功率 20 dBm）：

```bash
sudo tee /etc/hostapd/hostapd.conf > /dev/null <<'EOF'
interface=wlan1
driver=nl80211
ssid=alfa-lab
hw_mode=g
channel=6
wmm_enabled=1
auth_algs=1
wpa=2
wpa_passphrase=ChangeMe123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF
```

> 💡 记得把 `wpa_passphrase=ChangeMe123` 换成你自己设置的密码。

让 hostapd 读取这份设置档，并把服务全部启动：

```bash
echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a /etc/default/hostapd
sudo systemctl restart dhcpcd dnsmasq hostapd
sudo systemctl status hostapd --no-pager | head -10
```

**预期结果**：状态显示 `Active: active (running)`，这时候用手机或笔记本电脑搜索 Wi-Fi，应该就能看到 **alfa-lab** 这个网络，可以正常连上。

---

### 步骤 4：双无线电技巧（高端，可选读）

如果你想让 Pi 内置的 Wi-Fi 继续当作管理用的连接（例如 SSH 远程），同时让 ALFA 网卡专心当基地台，可以这样设置：

```bash
sudo systemctl stop wpa_supplicant@wlan1 2>/dev/null   # 确保 ALFA 不会去抢连接
sudo iw dev wlan1 set 4addr off
sudo systemctl restart hostapd
```

**预期结果**：`wlan0`（Pi 内置网卡）负责让你连上网际网络，`wlan1`（ALFA 网卡）专心服务你的实验室 Wi-Fi——一台 Pi，两个网络同时运作。

---

## 常见问题与排除指引

### Q1：网卡在笔记本电脑上可以用，插到 Pi 上就失效？
- **原因**：USB 供电不足。
- **解决方法**：改用独立供电的 USB Hub；或使用 Pi 官方原厂电源供应器；也可以尝试降低网卡的发射功率（`txpower`）。

### Q2：运行 `airmon-ng` 时显示「No such device」？
- **原因**：接口名称打错了。
- **解决方法**：先运行 `iw dev` 确认目前的接口名称——Pi 内置网卡通常是 `wlan0`，ALFA 网卡通常是 `wlan1`，但不一定每次都一样，务必先确认再操作。

### Q3：hostapd 启动失败，出现 `nl80211: Could not configure driver mode`？
- **原因**：驱动进程没有支持 AP（基地台）模式，或接口正被其他服务占用。
- **解决方法**：优先使用内置于内核的 MediaTek 芯片（`mt76` 系列对 AP 模式支持稳定）；并先运行 `sudo airmon-ng stop wlan1mon` 确保接口没有卡在监听模式。

### Q4：用户连上我的 Wi-Fi，但上不了网？
- **原因**：DHCP／NAT 没有正确设置，设备拿不到 IP 或流量没被转发出去。
- **解决方法**：
  ```bash
  sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
  sudo sysctl net.ipv4.ip_forward=1
  ```

### Q5：Pi 3 / 4 上的吞吐量感觉被限制住了？
- **原因**：Pi 3/4 的 USB 端口共用同一条 USB 2.0 总线，这是硬件本身的限制。
- **解决方法**：没有软件上的解法，如果需要更高吞吐量，升级到 Pi 5（USB 3.0）是目前唯一的路。

---

## 参考数据与延伸阅读

- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)——Pi 最好的搭配伙伴
- [ALFA 无线网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——驱动安装细节（Pi OS 上的步骤相同）
- [ALFA 无线网卡在 Kali Linux 上——监听模式与数据包注入](/alfa-network/linux-setup-kali/)——监听模式的延伸操作
- [ALFA 无线网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——规格更大的嵌入式主机集成方式
- [词汇表](/getting-started/glossary)——监听模式、hostapd 等名词的完整解释
- MediaTek MT76 系列驱动（社群维护，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动（aircrack-ng 社群维护）：https://github.com/aircrack-ng/rtl8812au
- [hostapd 官方文档](https://w1.fi/hostapd/)——官方 AP 守护程序说明

**标签：** `alfa` `raspberry-pi` `hostapd` `存取點` `监听模式` `新手指南`
