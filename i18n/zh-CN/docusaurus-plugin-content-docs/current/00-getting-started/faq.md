---
slug: faq
id: getting-started-faq
title: 常见问题
sidebar_position: 3
description: 关于 Yupitek 产品、Linux 驱动程序支持和下载的常见问题。
---

# 常见问题

关于 Yupitek 产品、Linux 支持和下载的最常见问题解答。

## 我的 Wi-Fi adapter（无线网卡）在 Linux 上开箱即用吗？

这取决于芯片组。采用 **MediaTek** 芯片组（`mt7612u`、`mt7610u`、`mt7921aun`）的无线网卡使用内核内置 driver（驱动程序）——在较新的 Ubuntu、Kali 和 Fedora 上无需安装任何东西即可使用。采用 **Realtek** 芯片组（`rtl8812au`、`rtl8811au`、`rtl8832bu`、`rtl8821cu`）的无线网卡通常需要树外 DKMS 驱动程序。完整说明请参阅 [Linux 兼容性矩阵](/alfa-network/linux-compatibility-matrix/)。

## 我在哪里下载驱动程序和固件？

产品固件和驱动程序托管在我们的 Cloudflare R2 下载服务器 **dl.yupitek.com** 上。每个产品页面都会链接其所需的精确驱动程序和固件，[ALFA Network](/alfa-network/) 下的驱动程序页面按芯片组对文件进行分组。请始终从 Yupitek 官方链接下载，而不要使用第三方镜像，以避免固件被篡改。

## 支持哪些操作系统？

**ALFA Network** 无线网卡支持 **Kali Linux**、**Ubuntu** 和 **Android NetHunter**，以及注明支持的 Windows 和 macOS。在硬件集成方面，ALFA 无线网卡提供了与 **NVIDIA Jetson**、**Raspberry Pi 3/4/5** 和 **Unitree** 机器人的文档。分步说明请参阅 [Linux 设置](/alfa-network/linux-setup-ubuntu/) 指南。

## 什么是 monitor mode（监听模式），如何启用？

监听模式让无线网卡无需关联到网络即可捕获和注入原始 802.11 帧。使用 `airmon-ng` 和 `airodump-ng` 进行审计时需要它。并非所有芯片组都支持得很好。我们的 [监听模式](/alfa-network/linux-setup-kali/) 指南逐步介绍了受支持的芯片组。

## 如何知道我的芯片组是否支持 packet injection（数据包注入）？

芯片组支持情况各不相同。ALFA 无线网卡使用的 MediaTek 和 Realtek 芯片组通常支持监听模式和数据包注入，但具体行为取决于所使用的驱动程序。在开始测试工作之前，请务必先用 `aireplay-ng --test` 快速测试。

## 内核更新后我的驱动程序停止工作了

Realtek 树外 DKMS 驱动程序偶尔会在内核升级后失效。解决方法通常是重新构建模块：

```bash
sudo dkms autoinstall
sudo modprobe <chipset-module>
```

有关确切的模块名称，请参阅适用于您无线网卡的 [芯片组驱动程序](/alfa-network/drivers/) 指南。

## HAK5 工具需要 Hak5 云（o.mg.lol）吗？

**不需要。** 您可以完全离线配置和运行大多数 HAK5 设备。但是，**O.MG** 产品系列与 `o.mg.lol` 云平台绑定：每台 O.MG 设备在首次使用前都必须使用 **O.MG Programmer** 激活并注册到 `o.mg.lol` 账户。设备特定的设置请参阅 [HAK5 板块](/hak5/)。

## 使用 Flipper Zero 合法吗？

Flipper Zero 是用于学习、研究和无线电测试的合法工具。特定用途是否合法取决于您当地的法律，以及您是否获得所发射或接收信号的许可。我们鼓励负责任、合乎道德的使用。

## 我可以将 ACS 读卡器用于基于 Web 的 NFC 吗？

- **ACR1252U**：可与 Android 版 Chrome 中的 **Web NFC API** 配合使用，也可通过 PC/SC + WebUSB 桥接与桌面浏览器配合使用。
- **ACR122U** 和 **ACR1552U**：使用 **PC/SC** 框架（ACR122U 还支持 libnfc）。

读卡器特定的指南请参阅 [ACS 板块](/acs/)。

## 你们托管 SDRLAB TRX-duo 的 SD 镜像吗？

TRX-duo 是一款兼容 Red Pitaya 的开发板。其 SD 卡镜像由上游开源项目维护，因此我们链接到**官方**下载（trx-duo.com 和 Red Pitaya 社区仓库），而不是托管可能过时的副本。其他所有内容我们都托管在 **dl.yupitek.com** 上。

## 在哪里可以获得更多帮助？

- 搜索本维基 — 顶部导航的搜索涵盖所有品牌。
- 查看品牌的 **Troubleshooting（故障排查）** 页面（例如 [ALFA 故障排查](/alfa-network/troubleshooting/)）。
- 访问 [Yupitek 官方网站](https://www.yupitek.com) 获取联系方式和销售支持。