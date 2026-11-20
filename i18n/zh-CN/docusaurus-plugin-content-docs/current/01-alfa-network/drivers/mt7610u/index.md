---
id: alfa-driver-mt7610u
title: MT7610U 驱动指南（AWUS036ACHM）
sidebar_position: 2
description: MT7610U 芯片组深度解析——AWUS036ACHM 使用的内核内置 mt76x0u 驱动，含监听模式、验证步骤与故障排查。
tags: [alfa, 驱动程序, mt7610u, 监听模式, 内核]
keywords: [MT7610U 驱动, AWUS036ACHM, mt76x0u, Linux 监听模式]
---

# MT7610U 驱动指南（AWUS036ACHM）

> **一句话定位（One-liner）**：**MediaTek MT7610U** 是 **AWUS036ACHM** 内部的 1T1R（单流）双频芯片组——一款预算友好的 AC600（150 + 433 Mbps）网卡适配器，其 `mt76x0u` 驱动**自 4.19 起就在 Linux 内核中**。和它的大哥 MT7612U 一样，在任何现代 Linux 上即插即用。

**实测平台**：ASUS GX10、Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia；USB ID `0e8d:7610`；固件 `mt7610u.bin`。Monitor 2.4 / 5 GHz ✅；注入 2.4 GHz 96–100%、5 GHz 仅广播注入可通过（逐台定向回应率未测量）；AP 2.4 / 5 GHz ✅（AP 请用纯 802.11g（2.4 GHz）／纯 802.11a（5 GHz））；WPA3-SAE ✅（须 `sae_pwe=0`，`sae_pwe=2` 时 iPhone 7 Plus 连不上）；VIF ✅；handshake 🟡（仅 2.4 GHz）；active monitor 🟡；IBSS / mesh 🟡（仅单机验证）；P2P 未测试。（kernel ≥ 4.19 同样无需 DKMS——mt76 自 4.19 起内置。）

## 概念：「小弟弟」芯片组

MT7612U 是 2×2 无线电，而 MT7610U 是 **1×1**——一个空间流，所以 5 GHz 上最高 433 Mbps 而不是 867。这正是 AWUS036ACHM 的 AC600（150 + 433 Mbps）规格。速度上的损失换来了简单和价格：它是仍能给你**内核内置驱动 + 双频 + 可用的监听模式**的最便宜 ALFA 网卡适配器。

驱动位于同一个主线 `mt76` 家族（`drivers/net/wireless/mediatek/mt76/mt76x0/`），所以体验与 MT7612U 完全相同：

- 插上 → 接口出现。无需安装。
- 无 DKMS → 内核更新时无需维护任何东西。
- 通过标准 `mac80211` 工具实现监听模式 + 注入。

```mermaid
flowchart LR
    A["AWUS036ACHM plugged in"] --> B["USB core sees 0e8d:7610"]
    B --> C["mt76x0u driver binds (in-kernel)"]
    C --> D["wlan0 appears"]
    D --> E["Managed mode: connect to AP"]
    E --> F["airmon-ng start wlan0 → wlan0mon"]
```

## 前置需求

- [ ] 内核 **4.19 或更新**的 Linux
- [ ] `sudo` 权限
- [ ] AWUS036ACHM（或任意 MT7610U 适配器）

## 第 1 步：验证驱动

```bash
lsusb | grep 0e8d:7610
sudo dmesg | grep mt76x0u | tail -3
```

**预期输出**（GX10 实测；总线／设备编号与 `wlx` MAC 因机器而异）：

```text
Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi
mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

如果 `lsusb` 能看到设备但没有 `mt76x0u` 行：`sudo modprobe mt76x0u`。

## 第 2 步：确认接口

```bash
iw dev
```

**预期输出**（示例；在 GX10 上接口名为 `wlx` + MAC）：

```text
phy#0
	Interface wlan0
		ifindex 3
		addr 00:c0:ca:xx:xx:xx
		type managed
```

## 第 3 步：连接

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**预期输出**：`Device 'wlan0' successfully activated with 'MySSID'.`

> 在相同距离下，吞吐量大约只有 AWUS036ACM 的**一半**——这就是 1×1 无线电。对于课堂练习、记笔记和轻度捕获，完全够用。

## 第 4 步：监听模式

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
iw dev
```

**预期输出**：`type monitor`。或使用 Aircrack-ng 的辅助工具：

```bash
sudo airmon-ng start wlan0
```

注入检查：

```bash
sudo aireplay-ng --test wlan0mon
```

**预期输出**：`Injection is working!`；2.4 GHz 实测回应率 96–100%，5 GHz 仅广播注入可用，逐台定向回应率未测量。在 GX10 或任何由 NetworkManager 提供网络的桌面机上，切勿执行 `airmon-ng check kill`；hcxdumptool 8.x 无法启动（failed to arm），请改用 airodump-ng + aireplay-ng。

## 第 5 步：恢复正常

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 不在 `lsusb` 中 | 供电 / 线缆 | 换端口、带供电的集线器——[故障排查索引](/alfa-network/troubleshooting/) |
| 没有接口 | 驱动未加载 | `sudo modprobe mt76x0u`；检查 `dmesg \| grep mt76` |
| 5 GHz 吞吐量卡在 ~150 Mbps | 这就是 1×1 硬件极限 | 不是 bug——5 GHz 链路速率最高 433 Mbps，实际约 150–250 Mbps |
| 监听模式被拒绝 | 内核 < 4.19 | 升级内核 / 操作系统 |
| 注入测试失败 | 信道无信号 / 射频区域 | `sudo iw wlan0mon set channel 6`，在接入点附近测试 |

## 参考

- [AWUS036ACHM 产品页面](/alfa-network/products/awus036achm/)
- [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)和 [Kali 设置指南](/alfa-network/linux-setup-kali/)
- [兼容性矩阵](/alfa-network/linux-compatibility-matrix/)
- 主线驱动源码：Linux 内核树中的 `drivers/net/wireless/mediatek/mt76/mt76x0/`