---
id: alfa-driver-rtl8832bu
title: RTL8832BU 驱动指南（AWUS036AX / AWUS036AXER）
sidebar_position: 6
description: RTL8832BU 芯片深入探讨——AWUS036AX 与 AWUS036AXER 背后的 Wi-Fi 6 芯片、kernel ≥ 6.17 内核内置 rtw89_8852bu 驱动（实测监听与注入可用）、旧内核的社区 rtl8852bu DKMS 驱动、WPA3。
tags: [alfa, 驱动, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU 驱动, RTL8852BU, AWUS036AX, rtl8852bu, Linux Wi-Fi 6, WPA3]
---

# RTL8832BU 驱动指南（AWUS036AX / AWUS036AXER）

> **一句话摘要**：**Realtek RTL8832BU** 是 **AWUS036AX** 及其 nano 版兄弟机型 **AWUS036AXER** 内部的 Wi-Fi 6（802.11ax）芯片。**kernel ≥ 6.17 起，内核内置 `rtw89_8852bu` 驱动**，插上即用，即可享有 AX1800 速度与 **WPA3** 支持（ASUS GX10、Ubuntu 24.04、kernel 6.17.0-1014-nvidia 实测，USB ID `0bda:b832`，固件 `rtw8852b_fw` 0.29.29.5）。只有旧内核（< 6.17）才需要构建社区的 `rtl8852bu` DKMS 驱动。内核内置驱动**实测支持监听模式与数据包注入**——请参阅[监听模式与数据包注入](#monitor-mode-and-injection)。

## 概念：Wi-Fi 6，Realtek 风格

RTL8832BU 是一颗 2×2 802.11ax 无线电（AX1800：574 + 1201 Mbps）。与较旧的 AC 网卡相比，用户最直接感受到的优势是 **WPA3**——只支持 WPA3 的现代路由器会拒绝你旧的 AC 网卡，但会欣然接受 AX。

在旧内核上，驱动的状况与其他 Realtek 芯片相同：**尚未纳入内核**，因此需使用社区驱动（**仅适用 kernel < 6.17**）。目前持续维护的 repo 是 **[`morrownr/rtl8852bu-20250826`](https://github.com/morrownr/rtl8852bu-20250826)**（「Linux Driver for USB WiFi Adapters that are based on the RTL8832BU and RTL8852BU Chipsets」）；其 README 列出 AWUS036AX 与 AWUS036AXER 为支持机型。其安装程序会将驱动注册到 DKMS，使其在内核更新后自动重新构建。

> 本指南早期版本使用 `aircrack-ng/rtl88x2bu`。该 repository 已不存在，且 88x2bu 系列（RTL8812BU / RTL8822BU）属于另一个 802.11ac 芯片家族——请勿将其用于 AWUS036AX / AXER。

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["Kernel >= 6.17: in-kernel rtw89_8852bu binds"]
    B --> C["Kernel < 6.17 only: build rtl8852bu via DKMS"]
    C --> D["8852bu module loaded"]
    D --> E["Connect: WPA3-capable"]
```

## 前置需求

- [ ] kernel ≥ 6.17（如 Ubuntu 24.04 + kernel 6.17）：不需要以下 DKMS 前置需求
- [ ] 仅 kernel < 6.17：`sudo apt install -y build-essential dkms git`
- [ ] `sudo` 权限
- [ ] AWUS036AX 或 AWUS036AXER

## 步骤 1（仅适用 kernel < 6.17）：构建驱动

**kernel ≥ 6.17 请直接跳到「步骤 2」确认**（`lsusb | grep -iE '0bda:b832'`、`sudo dmesg | grep rtw89_8852bu | tail -3`；预期可看到 `rtw89/rtw8852b_fw-1.bin ... Firmware version 0.29.29.5`）。`lsusb` 的描述字串在 AWUS036AX 为 `802.11ax WLAN Adapter`，在 AWUS036AXER 为 `802.11ac WLAN Adapter`，ID 相同。若 `lsusb` 显示 `0bda:1a2b`（光盘模式），请执行 `sudo usb_modeswitch -v 0bda -p 1a2b -K`。

```bash
cd /opt
sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo sh install-driver.sh
```

**预期输出**：脚本会以 DKMS 构建并安装驱动。请回答其提示，并在它要求时重启。

## 步骤 2：加载并验证

```bash
sudo modprobe 8852bu   # 仅 DKMS 方式（kernel < 6.17）需要
iw dev
```

**预期输出**：一行接口信息，例如 `Interface wlan0 ... type managed`（内置驱动时名称通常为 `wlx<MAC>`）。DKMS 安装程序通常会设置好重启后自动加载；若没有（仅 kernel < 6.17），请运行：

```bash
echo 8852bu | sudo tee /etc/modules-load.d/alfa.conf
```

## 步骤 3：连接（WPA3 开箱即用）

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**预期输出**：`Device 'wlan0' successfully activated with 'MySSID'.`

验证安全套件与连接速率：

```bash
iw dev wlan0 link
```

**预期输出**：显示 `SSID: MySSID` 以及协商后的速率——在 5 GHz 频段最高约 **1201 Mb/s**，或依距离而降至较低速率（2×2 80 MHz）。

## 监听模式与数据包注入 {#monitor-mode-and-injection}

旧版社区 DKMS 驱动的 README 曾指出不支持监听模式；但 **kernel ≥ 6.17 的内核内置 `rtw89_8852bu` 在 GX10 实测支持监听模式**：

| 项目 | AWUS036AX | AWUS036AXER |
|---|---|---|
| Monitor 2.4 GHz / 5 GHz | ✅（强） / ✅（强） | ✅（强） / ✅（强） |
| 注入 2.4 GHz | ✅ 96% | ✅ 73% |
| 注入 5 GHz | ✅ 可用 | ✅ 可用 |
| WPA handshake 抓取 | ✅ 端到端（`.22000`） | ✅ 端到端（`.22000`） |
| IBSS / Mesh / Active monitor | N/A | N/A |

本机实测没有蓝牙接口；P2P 未测试。监听与注入指令：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
```

5 GHz 注入前先 `sudo iw reg set US`，测完还原。`hcxdumptool` 8.x 在这两张卡上均 failed to arm，请改用 airodump-ng + aireplay-ng；切勿执行 `airmon-ng check kill`。请参阅[网卡比较](/alfa-network/wifi-adapter-comparison/)。

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| （仅 kernel < 6.17）在非常新的内核上构建失败 | repo 需要最新的 commit | `cd /opt/rtl8852bu-20250826 && sudo git pull && sudo sh install-driver.sh` |
| 看不到 WPA3 网络 | 驱动或 wpa_supplicant 太旧 | 更新驱动；`sudo apt update && sudo apt upgrade` |
| （仅 kernel < 6.17）内核升级后驱动失效 | DKMS 未重新构建 | `sudo dkms status`，然后重新运行 `sudo sh install-driver.sh` |
| （仅 kernel < 6.17）已安装针对同一硬件的另一个内核外驱动 | 模块冲突 | 安装程序能检测大多数冲突；请检查 `sudo dkms status` 并移除旧驱动 |
| 连接速率高但传输慢 | USB 2.0 端口瓶颈 | 使用 USB 3.x 端口（AX 为 USB 3.2） |

## 参考

- [AWUS036AX 产品页面](/alfa-network/products/awus036ax/)与 [AWUS036AXER 产品页面](/alfa-network/products/awus036axer/)
- [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)
- [故障排查索引](/alfa-network/troubleshooting/)
- 驱动 repo：[morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
