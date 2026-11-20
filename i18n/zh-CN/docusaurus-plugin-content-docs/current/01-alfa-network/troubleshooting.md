---
slug: troubleshooting
id: alfa-troubleshooting
title: ALFA 网卡适配器——故障排查索引
sidebar_position: 7
description: 诊断任何 ALFA Wi-Fi 网卡适配器问题——症状、诊断命令、根本原因与修复方法，并附各芯片组专属驱动页面的链接。
tags: [alfa, 故障排查, 驱动程序, 监听模式, dkms]
keywords: [ALFA 故障排查, 网卡适配器未检测到, 监听模式不工作, DKMS 失败, WiFi 网卡修复]
---

# ALFA 网卡适配器——故障排查索引

> **排查铁律（Diagnosis iron rule）**：**先查硬件 → 再查驱动程序 → 最后查配置。** 多数「我的 ALFA 坏了」的报告，最终都证明是供电问题、内核版本过旧（内核低于该型号的内置版本：EACS 6.2、ACH / ACS 6.13、AX / AXER 6.17 的 Realtek 型号缺少驱动或 DKMS 重建）、或内核更新的副作用——而不是网卡适配器坏了。在责怪硬件之前，先按下面的决策树排查。

```mermaid
flowchart TD
    A["Adapter misbehaving?"] --> B{"Does lsusb see it?"}
    B -->|"No"| C["Hardware / power path:<br/>try another port, powered hub,<br/>another cable, another PC"]
    C -->|"Still invisible"| D["Return / RMA the adapter"]
    B -->|"Yes"| E{"Does iw dev list an interface?"}
    E -->|"No"| F["Driver problem:<br/>check kernel vs card (EACS 6.2 / ACH, ACS 6.13 / AX, AXER 6.17),<br/>older kernel: DKMS,<br/>check dmesg for firmware errors"]
    E -->|"Yes"| G{"Works in managed mode?"}
    G -->|"No"| H["Config problem:<br/>NetworkManager, rfkill, reg domain"]
    G -->|"Yes"| I{"Monitor mode is the goal?"}
    I -->|"Yes, but fails"| J["Check chipset notes:<br/>mt7921u injection fails on stock 6.17,<br/>older kernel: aircrack-ng driver repos"]
    I -->|"All fine"| K["You are done — enjoy!"]
```


![ALFA 适配器故障排查决策树——先硬件、再驱动、最后配置](/img/troubleshooting/troubleshooting-decision-tree.svg)
## 问题分类索引

| 类别 | 典型问题 |
|---|---|
| **检测** | 网卡适配器不在 `lsusb` 中、没有接口、重启后消失 |
| **驱动程序** | 旧内核上 DKMS 构建失败、模块未加载、`dmesg` 中出现固件错误 |
| **连接** | 无法关联、频繁掉线、链路缓慢 |
| **监听模式** | `airmon-ng` 失败、注入测试失败、捕获不到任何帧 |
| **供电** | 网卡适配器在高负载下死机、在一台电脑上正常另一台不行 |
| **法规** | 信道设置错误、发射功率被限制、「5 GHz 信道缺失」 |

**每个芯片组都有自己的深度解析页面**——请收藏你的：

| 芯片组 | 网卡适配器 | 驱动页面 |
|---|---|---|
| MT7612U | AWUS036ACM | [mt7612u](/alfa-network/drivers/mt7612u/) |
| MT7610U | AWUS036ACHM | [mt7610u](/alfa-network/drivers/mt7610u/) |
| MT7921AU / MT7921AUN | AWUS036AXM / AWUS036AXML | [mt7921aun](/alfa-network/drivers/mt7921aun/) |
| RTL8812AU | AWUS036ACH | [rtl8812au](/alfa-network/drivers/rtl8812au/) |
| RTL8811AU | AWUS036ACS | [rtl8811au](/alfa-network/drivers/rtl8811au/) |
| RTL8832BU | AWUS036AX / AWUS036AXER | [rtl8832bu](/alfa-network/drivers/rtl8832bu/) |
| RTL8821CU | AWUS036EACS | [rtl8821cu](/alfa-network/drivers/rtl8821cu/) |

---

## 问题 1：网卡适配器完全检测不到（`lsusb` 为空）

### 症状
已插入，LED 可能亮也可能不亮，`lsusb` 中没有任何 Realtek/MediaTek 条目。

### 诊断
```bash
lsusb
dmesg | tail -30
```
在 `dmesg` 中查找 `device descriptor read/64, error -71` 或 `device not accepting address`——这是典型的供电握手失败。

### 根本原因
几乎总是 **USB 供电或线缆**——尤其是高功率型号（AWUS036AXM/AXML、AWUS036AX）接到前置面板端口或无供电的集线器上时。

### 修复
1. 尝试**机箱后置 USB 端口**（或通过转接头使用 USB-C 端口）。
2. 尝试**不同的线缆**——有些廉价 USB-C 线只支持充电。
3. 使用**带供电的 USB 集线器**。
4. 在笔记本上，拔掉其他高功率 USB 设备。
5. 如果在*两台不同的电脑*上仍然不可见，说明网卡适配器已损坏——请联系支持。

---

## 问题 2：`lsusb` 能看到，但没有 `wlanX` 接口

### 症状
`lsusb` 显示网卡适配器；`iw dev` / `ip link` 却什么都没有。

### 诊断
```bash
dmesg | grep -iE "wlan|firmware|error"
lsmod | grep -iE "mt76|8812|8811|88x2|8821"
```

### 根本原因
常见原因：
- **Realtek 芯片组、内核低于内置版本（EACS 6.2、ACH / ACS 6.13、AX / AXER 6.17）**：内核没有内置驱动，DKMS 模块从未加载（或内核更新后构建失败）。内核够新时驱动已内置，不会有这个问题。
- **MediaTek Wi-Fi 6 / 6E**：内核版本低于 5.18（缺少 `mt7921u`），或固件 blob 缺失。
- **EACS / AXML（蓝牙 + Wi-Fi 组合设备）**：重新插拔后 Wi-Fi probe 卡死，`lsusb` 看得到但不产生 `wlx*` 接口。

### 修复
- Realtek（**仅旧内核**）：`sudo modprobe 8812au`（匹配你的芯片组），并把它加入 `/etc/modules-load.d/alfa.conf` 以便开机自动加载。如果 `modprobe` 提示 `Module not found`，重建：`sudo dkms autoinstall`。内核够新则先升级内核或安装 HWE 内核，不需要 DKMS。
- EACS / AXML：**换一个 USB 口**重新插上。
- MediaTek：`sudo apt install linux-firmware` 然后重启。内核太旧？升级操作系统——参见[兼容性矩阵](/alfa-network/linux-compatibility-matrix/)。

---

## 问题 3：内核更新后 DKMS 构建失败（仅旧内核上的 Realtek DKMS 驱动）

> 内核够新（EACS ≥ 6.2、ACH / ACS ≥ 6.13、AX / AXER ≥ 6.17）时，Realtek 型号使用内核内置驱动（`rtw88_*` / `rtw89_*`），不会遇到此问题。

### 症状
刚执行完 `apt upgrade` 就「网卡适配器停止工作」；`dmesg` 显示 `8812au: version magic ... should be ...`。

### 诊断
```bash
dkms status
```
如果你的模块显示 `Error!` 或出现损坏的内核版本条目，那就是问题所在。

### 根本原因
驱动程序的 DKMS 配方无法针对新内核重新构建——通常是缺少内核头文件，或仓库对全新内核来说太旧。

### 修复
1. 安装头文件：`sudo apt install linux-headers-$(uname -r)`
2. 强制重建：`sudo dkms autoinstall`
3. 仍然失败？更新驱动仓库并重新安装：
   ```bash
   cd /opt/rtl8812au && sudo git pull && sudo make dkms_install
   ```
4. 重启并再次检查 `dkms status`——它应该把你的模块列为 `installed`。

---

## 问题 4：监听模式能启动，但注入测试失败

### 症状
`airmon-ng start` 成功，`wlan0mon` 存在，但 `aireplay-ng --test` 报告 `0/30` 或 `Failed`。

### 诊断
```bash
sudo aireplay-ng --test wlan0mon
sudo iw dev wlan0mon info   # confirm it really is type monitor
```

### 根本原因
驱动程序构建时未包含正确的监听/注入支持（仅旧内核上的 DKMS 驱动），**或者**你使用的是 AXM / AXML（`mt7921u`）——它们在 stock kernel 6.17 上注入测试未通过（主因是 kernel 6.16 起的 mac80211 chanctx 回归；固件另把注入速率锁在 1/6 Mbps），`aireplay-ng --test` 会回 `No Answer` / `Found 0 APs`，**或者**你所在的信道没有任何接入点在使用（注入需要一个 AP 信标来回应），**或者**射频环境是空的（隔离实验室）。

### 修复
1. 锁定一个有活跃接入点的信道：`sudo iw dev wlan0mon set channel 6`
2. 5 GHz 注入先 `sudo iw reg set US` 解锁发射，测完还原（如 `sudo iw reg set TW`）。
3. 重新测试。仍然是 0/30？若是 AXM / AXML，这是已知限制，请改用 ACM / ACHM / ACH / ACS / EACS / AX / AXER 等网卡（2.4 GHz 均通过）；若是低于内置版本的旧内核上的 Realtek，改用 aircrack-ng 驱动仓库重建（仅适用旧内核），这些仓库默认启用监听 + VIF：
   - [rtl8812au](/alfa-network/drivers/rtl8812au/)、[rtl8811au](/alfa-network/drivers/rtl8811au/)、[rtl8832bu](/alfa-network/drivers/rtl8832bu/)
4. 在无射频信号的区域，用手机热点在同一信道创建你自己的接入点。
---

## 平台共通注意事项（ASUS GX10 / Ubuntu 24.04 ARM64 实测）

- **不要执行 `airmon-ng check kill`**：它会关闭 NetworkManager，使主机断网；改用 `iw` 手动切换，或直接 `airmon-ng start`。
- **RX stall**：反复切换 monitor / AP 之后收不到任何数据包 → **拔插网卡**即可恢复。
- **EACS / AXML 重新插拔**：Wi-Fi probe 可能卡死而不产生 `wlx*` 接口 → **换一个 USB 口**。
- **5 GHz 注入 / deauth**：先 `sudo iw reg set US`，测完还原。
- **hcxdumptool 8.x**：除 EACS 外，其余网卡均 failed to arm（需要 active monitor；EACS 在 2.4 GHz 可启动、5 GHz 失败）→ 改用 airodump-ng + aireplay-ng。
- **ARM64**：aircrack-ng 需自原始码编译（apt 版依赖与 wifite 冲突时，wifite 用 git 版）。
- 仅对**自有或已授权的网络**进行监听 / 注入测试。

---

## 问题 5：Wi-Fi 频繁掉线或速度慢

### 症状
链路连上后每隔几分钟就掉线；吞吐量远低于等级标称值。

### 诊断
```bash
iw dev wlan0 link          # signal + tx rate
iw reg get | head -20      # regulatory domain
```

### 根本原因
- **法规域**：如果 `iw reg get` 显示 `country 00`（未设置），发射功率会被限制在默认的 20 dBm。
- **省电**：激进的 USB 电源管理会限制无线电性能。
- **过热**：高功率网卡适配器持续发射。

### 修复
1. 设置你的地区：`sudo iw reg set TW`（或你的国家代码）。
2. 设置发射功率：`sudo iwconfig wlan0 txpower 30`（你所在法规域允许的最大值）。
3. 关闭省电：`sudo iwconfig wlan0 power off`。
4. AC1200+ 网卡适配器优先使用 USB 3.0 端口——USB 2.0 会限制吞吐量。

---

## 问题 6：5 GHz 信道缺失

### 症状
只能看到 2.4 GHz 网络；`iwlist wlan0 freq` 没有任何 5 GHz 条目。

### 根本原因
法规域未设置或被限制（全新安装时通常是 `country 00`），因此驱动程序拒绝使用 5 GHz 信道。

### 修复
```bash
sudo iw reg set TW    # replace with your country code
sudo ip link set wlan0 down && sudo ip link set wlan0 up
```

---

## 仍未解决？

在放弃之前，收集以下确切信息并联系我们（或[驱动项目](/alfa-network/drivers/mt7612u/)）——这是维护者帮助你所需的信息：

```bash
uname -r
lsusb
dkms status   # 仅旧内核上的 DKMS 驱动才有输出
dmesg | tail -50
iw dev
```

附上以上全部内容，再加上：你的网卡适配器型号、操作系统/内核，以及输出让你意外的确切命令。还有一件值得检查的事——如果你运行的是 Jetson、Raspberry Pi 或 Unitree 机器人，请查看[硬件集成指南](/alfa-network/hardware/jetson/)；嵌入式板卡有自己独特的供电和驱动问题。