---
id: hak5-product-omg-programmer
title: O.MG Programmer
sidebar_position: 13
description: 所有 O.MG 设备的通用编程器 — 激活、升级固件、从自我销毁中恢复、制作鉴识备份。
tags: [hak5, omg, omg-programmer, 固件, 设置, 激活]
keywords: [O.MG Programmer, WebFlasher, 激活 O.MG, 固件升级, 鉴识备份, 自我销毁恢复]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-programmer
category: product
difficulty: intermediate
toc: true
---

# O.MG Programmer — 完整指南

> **一句话定位**：O.MG Programmer 是启用与维护所有 O.MG 设备（Cable、Plug、Adapter、UnBlocker）的唯一入口——一支编程器就能完成激活、免费固件升级、自我销毁救援，以及鉴识备份。

每台 O.MG 设备出于法律原因出厂**停用**。在它能做任何事之前，必须先激活 — 这就是 **O.MG Programmer** 的用途。它是一个小 USB 加密狗，插在你的电脑和任何 O.MG 设备之间，配合一个基于浏览器的 **WebFlasher** 工具。一支 Programmer 服务*整个* O.MG 产品线，所以你永远不用按设备买硬件。

除了首次激活，它还是你的管理工具：固件升级、意外自我销毁后的恢复，以及在把设备交给别人之前做鉴识备份。

> **为什么「停用」？** O.MG 植入物能力太强，法规要求它们出厂时保持惰性。Programmer 既是法律闸门，也是你的日常控制面板。

---

## 规格一览

| 项目 | 规格 |
|---|---|
| 外形 | USB 加密狗（电脑 ↔ O.MG 设备） |
| 兼容性 | O.MG Cable、O.MG Plug、O.MG Adapter、O.MG UnBlocker |
| 接口 | USB-A 接你的电脑；承载连接的 O.MG 设备 |
| 控制工具 | WebSerial 浏览器（Chrome / Edge）里的 WebFlasher；Python 刷写器替代方案 |
| 操作 | 激活、固件升级、自我销毁恢复、鉴识备份/转储、批量安装 |
| 官方文档 | https://o.mg.lol/setup/ |

## 它能做什么

| 操作 | 会发生什么 |
|---|---|
| **激活** | 初始 3 步设置，让休眠的 O.MG 设备可运行 |
| **固件升级** | 免费更新；Elite 设备无需新硬件即可获得未来能力 |
| **自我销毁恢复** | 恢复你远程清除的设备（例如意外触发地理围栏） |
| **鉴识转储/备份** | 拉取任何兼容 O.MG 设备内存的镜像 |
| **批量安装** | 一次刷写多台设备，用于批量部署 |

---

## 激活工作流

```mermaid
%% name: hak5-product-omg-programmer-activation
flowchart TD
    A[Connect O.MG device to Programmer] --> B[Connect Programmer to a Chrome/Edge computer]
    B --> C[Open WebFlasher at o.mg.lol/setup]
    C --> D[Select your O.MG model]
    D --> E[Step 1: detect device (WebSerial prompt)]
    E --> F[Step 2: optionally forensic backup]
    F --> G[Step 3: flash firmware & activate]
    G --> H[Boot device — WebUI now available over WiFi]
```

### 第 1 步 — 物理设置
1. 把 O.MG 设备插进 Programmer。
2. 把 Programmer 插进一台运行 **Chrome 或 Edge** 的电脑（它们支持 WebSerial；Firefox/Safari 不支持）。
3. **在向导要求之前，保持 O.MG 设备与 Programmer 断开。** 引导加载程序检测期望一次干净的连接。

### 第 2 步 — 打开 WebFlasher
浏览到 **https://o.mg.lol/setup/** 并选择你的设备型号（Cable、Plug、Adapter 或 UnBlocker）。

### 第 3 步 — 按向导操作
- 浏览器会提示你**选择串口** — 选择 Programmer。
- （推荐）先做可选的**鉴识备份** — 一个安全网。
- 开始刷写。它会安装最新固件并激活设备。

预期结果：

```text
[+] Device detected
[+] Backup complete (optional)
[+] Firmware flashed successfully
[+] Device activated — connecting to WiFi...
```

### 第 4 步 — 验证
加入 O.MG 设备的 Wi-Fi，打开它的 WebUI，确认固件版本。它现在可以运行了。

> **Python 刷写器替代方案：** O.MG 固件仓库为没有 WebSerial 浏览器的用户提供了一个 Python 刷写器。查看 O.MG 固件文档。

---

## 进阶

| 能力 | 怎么做 |
|---|---|
| 自我销毁恢复 | 重新连接设备 → WebFlasher → 重新刷写，从清除中恢复 |
| 鉴识取证 | 备份任何 O.MG 设备；用转储做恶意软件/培训分析 |
| 批量供应 | 为红队实验室或培训课批量刷写一批 O.MG 设备 |
| Beta 固件访问 | Elite 用户安装 Beta 固件以获得即将推出的功能 |

> **你可能会问：** *「如果我只有一条 O.MG 线，需要 Programmer 吗？」* 需要 — 它是激活任何 O.MG 设备的唯一受支持方式，而且一支 Programmer 覆盖所有设备。它不是可选的。

---

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| WebFlasher 显示「No device found」 | 设备没接好，或浏览器不对 | 用 Chrome/Edge；只在提示时连接设备 |
| 浏览器选错串口 | 有多个 USB 串口设备 | 断开其他设备；选向导高亮的串口 |
| 激活卡在「detecting」 | 设备不在引导加载程序模式 | 断电重启；在提示时干净地重新连接 |
| 设备显示旧版本 | 跳过了固件步骤 | 重新运行 WebFlasher 并完成固件步骤 |
| Python 刷写器报错 | 驱动程序 / 权限 | 用适当的权限运行；操作系统注意事项见 O.MG 固件文档 |

---

## 相关资源

- [O.MG Cable](/hak5/products/omg-cable/) — 这支 Programmer 服务的旗舰植入物
- [O.MG Plug](/hak5/products/omg-plug/) / [O.MG Adapter](/hak5/products/omg-adapter/) / [O.MG UnBlocker](/hak5/products/omg-unblocker/)
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — 防御对应物
- [固件与下载](/hak5/firmware-downloads/) — O.MG 固件与 WebFlasher 链接
- [故障排查索引](/hak5/troubleshooting-index/)
- [Hak5 概览](/hak5/)