---
id: alfa-driver-rtl8832bu
title: RTL8832BU 驱动指南（AWUS036AX / AWUS036AXER）
sidebar_position: 6
description: RTL8832BU 芯片组深度解析——AWUS036AX 与 AWUS036AXER 背后的 Wi-Fi 6 RTL88x2BU 驱动，DKMS 安装、WPA3 与监听模式。
tags: [alfa, 驱动程序, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU 驱动, AWUS036AX, rtl88x2bu, Linux Wi-Fi 6, WPA3]
---

# RTL8832BU 驱动指南（AWUS036AX / AWUS036AXER）

> **一句话定位（One-liner）**：**Realtek RTL8832BU** 是 **AWUS036AX** 及其纳米兄弟 **AWUS036AXER** 内部的 Wi-Fi 6（802.11ax）芯片组。它不在内核中，所以你需要构建一次 `rtl88x2bu` DKMS 驱动——然后享受 AX1800 速度、**WPA3** 支持和可用的监听模式。

## 概念：Realtek 风格的 Wi-Fi 6

RTL8832BU 是一款 2×2 802.11ax 无线电（AX1800：574 + 1201 Mbps）。与较旧的 AC 网卡适配器相比，用户能明显感受到的最大进步是 **WPA3**——只支持 WPA3 的现代路由器会拒绝你的旧 AC 适配器，但会愉快地接受 AX。

驱动情况与其他 Realtek 芯片组如出一辙：**未上游**，所以我们使用社区驱动。首选仓库是 **`aircrack-ng/rtl88x2bu`**，它覆盖 88X2BU 家族（RTL8822BU 和 RTL8832BU），带监听模式 + VIF 支持。DKMS 让它在历次内核更新中保持重建。

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["No in-kernel driver for RTL8832BU"]
    B --> C["Build rtl88x2bu via DKMS"]
    C --> D["88x2bu module loaded"]
    D --> E["Connect: WPA3-capable"]
    E --> F["airmon-ng start wlan0 → monitor mode"]
```

## 前置需求

- [ ] Linux（Ubuntu 20.04+ / Kali / Debian）
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` 权限
- [ ] AWUS036AX 或 AWUS036AXER

## 第 1 步：构建驱动

```bash
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu
sudo make dkms_install
```

**预期输出**：

```text
DKMS: install completed.
```

## 第 2 步：加载并验证

```bash
sudo modprobe 88x2bu
iw dev
```

**预期输出**：一个接口行，例如 `Interface wlan0 ... type managed`。跨重启自动加载：

```bash
echo 88x2bu | sudo tee /etc/modules-load.d/alfa.conf
```

## 第 3 步：连接（WPA3 开箱即用）

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**预期输出**：`Device 'wlan0' successfully activated with 'MySSID'.`

验证安全套件和链路速度：

```bash
iw dev wlan0 link
```

**预期输出**：显示 `SSID: MySSID` 以及协商速率——在 5 GHz 上，靠近接入点时你应该看到 **1201 Mb/s** 或根据距离降级（2×2 80 MHz）。

## 第 4 步：监听模式 + 注入

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**预期输出**：

```text
PHY	Interface	Driver		Chipset
phy0	wlan0		88x2bu		Realtek
...
12:34:56  Injection is working!
12:34:56  30/30:  100%
```

> **你可能想知道**——*「Wi-Fi 6 和监听模式？它们能共存吗？」* 能——社区驱动保留了渗透测试工具需要的经典监听/注入行为，而 managed 模式增加了 AX 速率和 WPA3。你不需要二选一。

## 第 5 步：恢复正常

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 在非常新的内核上构建失败 | 仓库需要最新提交 | `cd /opt/rtl88x2bu && sudo git pull && sudo make dkms_install` |
| WPA3 网络不可见 | 驱动或 wpa_supplicant 太旧 | 更新驱动；`sudo apt update && sudo apt upgrade` |
| 网卡适配器只能 managed，没有监听 | 内核桩模块冲突（罕见） | 用 `dmesg` 确认哪个模块绑定了；黑名单桩模块 |
| 注入 0/30 | 空信道 | `sudo iw wlan0mon set channel 6`；在接入点附近测试 |
| 链路高速但传输慢 | USB 2.0 端口瓶颈 | 使用 USB 3.x 端口（AX 是 USB 3.2） |

## 参考

- [AWUS036AX 产品页面](/alfa-network/products/awus036ax/)和 [AWUS036AXER 产品页面](/alfa-network/products/awus036axer/)
- [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)
- [故障排查索引](/alfa-network/troubleshooting/)
- 驱动仓库：[aircrack-ng/rtl88x2bu](https://github.com/aircrack-ng/rtl88x2bu)