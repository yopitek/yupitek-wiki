---
id: alfa-hardware-orange-pi
title: Orange Pi & Rockchip RK3588 SBC × ALFA Network 集成指南
sidebar_label: Orange Pi / RK3588
sidebar_position: 8
description: Orange Pi 5 与 Rockchip RK3588 单板电脑搭配 ALFA 网卡——系统内核差异、Armbian Mainline 部署与供电设置，含每一步的预期结果。
tags: [orange-pi, rk3588, armbian, rockchip, alfa, awus036axml, awus036acm, sbc]
keywords: [Orange Pi 5, RK3588, Armbian mainline, vendor BSP, AWUS036AXML, AWUS036ACM, mt76]
---

# Orange Pi & Rockchip RK3588 SBC × ALFA Network 集成指南

> **一句话定位**：Orange Pi 5 系列这类搭载 Rockchip RK3588 芯片的单板电脑（SBC）算力很强，常被拿来做边缘运算的无线网关或远程传感节点。但很多人插入 ALFA 网卡后完全抓不到，误以为是硬件不兼容——实际上关键是「你用的系统镜像文档」，这篇文章教你怎么选对系统、正确安装。

## 这篇文章适合你吗？

- **难度**：入门〜中阶（会下 Linux 终端指令即可）
- **预估时间**：30〜45 分钟（含系统刷机时间）
- **你会用到的技能**：基本终端操作
- **读完你可以做到**：
  1. 搞懂为什么原厂系统插网卡常常抓不到，该用哪一种系统镜像文档
  2. 完成系统刷机与 ALFA 网卡的驱动确认
  3. 掌握供电与散热上要注意的细节，避免长时间使用时断线

---

## 概念说明：为什么原厂系统插入网卡常常没反应

很多人在 Orange Pi 原厂附的 Debian 系统上插入 ALFA 网卡，发现系统完全没反应，第一直觉会以为「这张网卡跟我的板子不兼容」——但其实问题通常出在**系统内核版本**，不是硬件本身。

这跟 SBC（单板电脑）这类产品的系统生态有关：

- **原厂 Vendor BSP（Board Support Package）系统**：芯片厂商（这里是 Rockchip）为了让硬件能尽快出货，会先基于一个比较旧的 Linux 内核版本（通常是 5.10）做客制化，让屏幕、GPU 这些硬件能动。这类系统的内核版本比较旧，对新款 USB 网卡芯片的支持往往还没跟上。
- **Armbian Mainline 系统**：Armbian 是一个第三方维护的社群项目，会持续把 SBC 的支持集成进最新的 Linux 主线内核（目前是 6.x 版本）。内核版本新，代表对新款 USB 网卡芯片（尤其是这几年才推出的 MT7921AUN）的支持也比较完整，通常插入就能直接用。

**简单判断方式**：如果你刚买到板子，插入 ALFA 网卡完全没反应，第一件事不是怀疑网卡坏了，是先确认自己现在装的是不是原厂 Vendor BSP 系统——如果是，换成 Armbian Mainline 系统通常就能解决。

> 📘 **名词小教室**
> - **SBC（Single Board Computer，单板电脑）**：把 CPU、内存、保存控制器等组件集成在一片电路板上的迷你电脑，Orange Pi、Raspberry Pi 都属于这类产品。
> - **BSP（Board Support Package）**：芯片厂商为了让自家硬件能正常开机、驱动屏幕与周边，提供的一整套客制化系统与驱动进程。BSP 系统通常内核版本比较旧，但对板子本身的硬件（例如特定的显示输出）支持反而可能更好。
> - **Mainline 内核**：Linux 官方维护的主线内核版本，社群持续在更新。使用 Mainline 内核的系统（如 Armbian）通常对新款周边设备的支持比 BSP 系统更新更快。

---

## ALFA 网卡在 RK3588 平台上的支持情况

| ALFA 型号         | 芯片型号                 | Armbian（内核 ≥6.x） | 原厂 Debian（内核 5.10） | 备注                    |
| --------------- | -------------------- | --------------------- | ----------------------- | ----------------------- |
| **AWUS036AXML** | MT7921AUN（Wi-Fi 6E） | ✅ 即插即用                | ⚠️ 需手动补上固件文档         | 支持 2.4G / 5G / 6G      |
| **AWUS036ACM**  | MT7612U（802.11ac）   | ✅ 即插即用                | ⚠️ 需手动加载 `mt76x2u`        | 监听与数据包注入的首选           |
| **AWUS036ACHM** | MT7610U（802.11ac）   | ✅ 即插即用                | ⚠️ 需手动加载 `mt76x0u`        | 单天线，适合长时间监听用途          |
| **AWUS036ACH**  | RTL8812AU            | ⚠️ 需自行编译 DKMS          | ⚠️ 需自行编译 DKMS            | 需先安装 `linux-headers` |

**简单判断方式**：如果你想要最省事、插入就能用，建议直接刷 Armbian Mainline 系统（见下方步骤），可以完全避开原厂系统上手动补固件、载驱动的麻烦。

---

## 你需要准备的东西

- [ ] **硬件**：Orange Pi 5 / 5B / 5 Plus，或其他 Rockchip RK3588 / RK3588S 平台的单板电脑
- [ ] **一张 microSD 卡或 NVMe 硬盘**：用来刷入系统镜像文档
- [ ] **读卡机**：用来把系统镜像文档写入 microSD 卡
- [ ] **ALFA 无线网卡**：依上表选择型号
- [ ] **至少 5V/4A（20W）的 Type-C 电源供应器**：详见下方供电提醒
- [ ] **驱动进程参考（GitHub）**：
  - MediaTek MT76 系列驱动（Armbian Mainline 系统已内置，如需手动安装可参考此项目）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（AWUS036ACH 适用）：https://github.com/aircrack-ng/rtl8812au
  - Armbian 建置项目（若想自行编译客制化镜像文档，而不是直接下载官方预编译版本）：https://github.com/armbian/build

---

## Step-by-Step 设置教学

### 步骤 1：下载并刷入 Armbian Mainline 镜像文档

前往 [Armbian 官方网站](https://www.armbian.com/orange-pi-5/)，下载适用于 Orange Pi 5 的 Armbian Linux（内核 6.x Mainline）镜像文档，并用刷机工具（如 balenaEtcher 或 Raspberry Pi Imager）写入 microSD 卡或 NVMe 硬盘。

**预期结果**：刷机工具显示写入完成，没有出现校验失败的错误消息。

> 💡 **想自己编译客制化镜像文档？** 官网下载的是预编译好的版本，对大部分人来说已经够用。但如果你的项目需要客制化内核选项（例如加装额外的内核模块），可以改用 Armbian 官方的建置框架自行编译：
> ```bash
> git clone https://github.com/armbian/build
> cd build
> ./compile.sh
> ```
> 这个做法对新手来说门槛较高（需要至少 8GB 内存、约 50GB 硬盘空间的编译环境），一般情况下不需要，直接用官网预编译镜像文档就好。

---

### 步骤 2：开机并插入 ALFA 网卡

开机进入 Armbian 系统后，把 ALFA AWUS036AXML（或其他型号）插入板子上**蓝色的 USB 3.0 Type-A 连接端口**（板子上会有蓝色跟黑色两种颜色的 USB 端口，蓝色代表 USB 3.0，传输速度较快，优先使用这个）。

---

### 步骤 3：验证驱动与无线接口

```bash
# 检查内核是否有正确辨识网卡
dmesg | grep -i "mt7921"

# 检查无线接口状态
iw dev
```

**预期结果**：`dmesg` 应该会显示类似下面的消息，代表固件已经正确加载：

```text
mt7921u 2-1:1.0: ASIC revision: 79610000
mt7921u 2-1:1.0: firmware: mediatek/WIFI_MT7961_patch_mcu_1_2_tv.bin loaded
mt7921u 2-1:1.0: firmware: mediatek/WIFI_RAM_CODE_MT7961_1_2.bin loaded
```

`iw dev` 则会列出一个新的无线接口（通常是 `wlan1`），代表网卡已经可以正常使用。

---

## 供电与散热注意事项

- **供电预算**：RK3588 全速运作时的功耗大约落在 10〜15W，再加上外置的 ALFA 高功率网卡（约 2〜4W），整机建议使用**至少 5V/4A（20W）的 Type-C 电源供应器**，避免瞬间负载尖峰造成 USB 供电不稳、网卡断线。
- **连接端口选择**：优先使用独立 USB 3.0 控制器信道的连接端口，避免跟其他高速周边（例如 NVMe USB 外置盒）共用同一个 Hub，共用时容易互相抢带宽跟供电。

---

## 常见问题与排除指引

### Q1：插入网卡后系统完全没反应？
- **原因**：目前使用的是原厂 Vendor BSP 系统（内核版本较旧），对这颗芯片的支持还没跟上。
- **解决方法**：改用 Armbian Mainline 系统（见步骤 1），内核版本较新，通常插入就能直接用。

### Q2：一定要用原厂系统，该怎么办？
- **原因**：原厂 Vendor BSP 系统内核版本较旧，需要手动补齐固件或驱动模块。
- **解决方法**：依照上方兼容性表格，手动安装对应的内核模块（例如 `mt76x2u`），并确认固件文档已经放在系统正确的路径下；如果觉得麻烦，改用 Armbian Mainline 会是更省事的做法。

### Q3：使用一段时间后网卡会断线？
- **原因**：通常是供电不足，尤其是同时外置了其他高速设备时。
- **解决方法**：确认电源供应器至少是 5V/4A（20W）；并检查 ALFA 网卡跟其他设备有没有共用同一个 USB Hub，如果有，建议分开接到不同的独立信道。

---

## 参考数据与延伸阅读

- [AWUS036AXML 产品页面](/alfa-network/products/awus036axml/)
- [AWUS036ACM 产品页面](/alfa-network/products/awus036acm/)
- [ALFA 无线网卡在 Raspberry Pi 上（3 / 4 / 5）](/alfa-network/hardware/raspberry-pi/)——另一款轻量嵌入式主机的集成方式，概念可互相参照
- [词汇表](/getting-started/glossary)——SBC、BSP、Mainline 内核等名词的完整解释
- [Armbian 官方网站](https://www.armbian.com/orange-pi-5/)——Orange Pi 5 系列的 Mainline 镜像文档下载（一般用户从这里下载即可）
- Armbian 官方建置框架（GitHub，适合需要自行编译客制化镜像文档的高端用户）：https://github.com/armbian/build
- MediaTek MT76 系列驱动：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动：https://github.com/aircrack-ng/rtl8812au

**标签：** `orange-pi` `rk3588` `armbian` `rockchip` `alfa` `awus036axml` `awus036acm` `sbc` `新手指南`
