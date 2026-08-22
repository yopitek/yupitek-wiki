---
id: hak5-product-omg-cable
title: O.MG Cable
sidebar_position: 10
description: 藏有隐藏 Wi-Fi 植入芯片的恶意 USB 线 — 隐蔽键盘注入、通过 Wi-Fi 跑 DuckyScript、自我销毁与地理围栏。
tags: [hak5, omg, omg-cable, 恶意线材, 远程访问, duckyscript]
keywords: [O.MG Cable, 恶意 USB 线, 通过 Wi-Fi 的键盘注入, DuckyScript, 自我销毁, 地理围栏, ESP32]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-cable
category: product
difficulty: advanced
toc: true
---

# O.MG Cable — 完整指南

> **一句话定位**：O.MG Cable 是一条「外观正常、内部藏了一颗无线植入芯片」的 USB 充电/传输线——你以为只是条线，它却能通过 Wi-Fi 被远程操控，随时注入键盘敲击、执行载荷，甚至自我销毁。红队的终极社会工程武器。

如果你在会议上随手拿起的充电线其实是一台带 Wi-Fi 无线电的电脑呢？这就是 O.MG Cable。在这种工具出现之前，这一类植入物（想想 NSA 的 COTTONMOUTH）要花数万美元。O.MG 把它放进了一条量产、手工制作的 USB 线里。

这条线看起来、用起来都像普通 USB 2.0 线 — 5V 充电、480 Mbps 数据 — 但内部藏着一颗保持**休眠**（在数据线上不可见）的植入芯片，直到你通过 Wi-Fi 触发它。然后它部署 DuckyScript 载荷、注入键盘敲击，或横向进入目标的网络，全部可以从浏览器控制。

> **⚠️ 仅限授权测试 — 而且这个很特别。** O.MG 设备在法律上*必须出厂停用*，因为它们太强大了。只把它们用于授权的红队工作、教学，以及测试你自己的检测能力 — 防御对应物见 [Malicious Cable Detector](/hak5/products/malicious-cable-detector/)。

---

## 规格一览

| 项目 | 规格 |
|---|---|
| 外形 | 手工制作 USB 2.0 线（标准 1 m；可定制 2 m） |
| 植入物 | 支持 Wi-Fi 的无线 HID 芯片（板载 WebUI + 802.11 无线电） |
| 载荷语言 | DuckyScript 3.0（Elite）/ DuckyScript 2.0（Basic） |
| 远程控制 | 通过 Wi-Fi 的任何网页浏览器 |
| 激活 | 必须通过 [O.MG Programmer](/hak5/products/omg-programmer/)（出厂停用） |
| 特色功能 | 自我销毁、地理围栏、Wi-Fi 触发、伪造 VID/PID/MAC |
| Elite 额外功能 | 加密 C²、HIDX StealthLink、硬件键盘记录器、扩展 Wi-Fi 范围 |
| 数据直通 | 休眠时正常 USB 2.0 充电 + 数据 |
| 官方文档 | https://docs.hak5.org/omg-cable |

## Basic vs Elite（硬件等级）

| 功能 | Basic（Gen 1） | Elite（Gen 3） |
|---|---|---|
| 键盘注入 | DuckyScript 2 | DuckyScript 3 |
| 载荷槽位 | 8 | 50–300 |
| 最大载荷大小 | 约 4,000 次敲击 | 约 1,500,000 次敲击 |
| 最大速度 | 120 键/秒 | 890 键/秒 |
| 自我销毁 / 地理围栏 / Wi-Fi 触发 | ✅ | ✅ |
| FullSpeed 硬件键盘记录器 | — | ✅ |
| HIDX StealthLink / 加密 C² / 扩展范围 | — | ✅ |

---

## 攻击如何运作

```mermaid
%% name: hak5-product-omg-cable-attack
sequenceDiagram
    participant A as Attacker (browser)
    participant C as O.MG Cable (dormant)
    participant T as Target computer
    A->>C: joins cable's WiFi, opens WebUI
    A->>C: deploys payload / triggers
    C->>T: re-enumerates as HID "keyboard"
    C->>T: injects keystrokes / exfiltrates
    T-->>C: (USB 2.0 data passthrough still works)
    A->>C: commands; optional self-destruct
```

关键洞察：*休眠*时，这条线只是一条线。只有你告诉它时它才会变成键盘 — 这正是没有正确工具就很难检测它的原因。

---

## 快速入门 — 激活与第一个载荷

O.MG 设备出厂**停用**（法律要求）。你必须用 Programmer 激活：

### 第 1 步 — 用 O.MG Programmer 激活
1. 把 O.MG Cable 的 micro USB 端插进 [O.MG Programmer](/hak5/products/omg-programmer/)。
2. 把 Programmer 插进一台运行 **Chrome 或 Edge** 的电脑（WebSerial）。
3. 打开 WebFlasher（https://o.mg.lol/setup/），选择型号，按 3 步向导操作。向导会可选地先做一次鉴识备份。

### 第 2 步 — 连接线的 Wi-Fi
激活后，这条线会广播自己的 Wi-Fi。从浏览器加入。

### 第 3 步 — 部署 DuckyScript 载荷
打开线的 WebUI 并粘贴/启动一个载荷 — 无需针对特定设备重新编译；DuckyScript 直接运行。

```text
REM Example: open notepad and type a proof-of-concept
DELAY 1000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 800
STRING Hello from an O.MG Cable!
ENTER
```

在 WebUI 里点击 **Run**。片刻之后目标机器显示打出的文本。

---

## 隐身功能

| 功能 | 作用 |
|---|---|
| 端口隐身 | 植入物保持休眠（不枚举 USB），直到载荷部署 |
| 可伪造身份 | 克隆任何 VID/PID、扩展 USB ID 和 MAC 地址 |
| 无日志 / 无检测 | 休眠时数据线上什么都没有 |
| 自我销毁 | 远程命令清除载荷 + 战利品，让线失效（可通过 Programmer 恢复） |
| 地理围栏 | 基于位置自动触发/自我销毁 — 让工具保持在范围内 |
| Wi-Fi 触发 | 用单个信标远程触发载荷 |
| 加密 C²（Elite） | 加密控制信道；需要时可以禁用板载 WebUI |

> **你可能会问：** *「有什么能抓住这条线吗？」* [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) 的存在正是因为这些线很难靠肉眼或数据线嗅探发现 — 它用**侧信道电力分析**看到植入物。防御是存在的，但它必须有目的性。

---

## 进阶

| 能力 | 怎么做 |
|---|---|
| 鼠标注入 | 注入光标移动/点击（Elite+） |
| 硬件键盘记录器（Elite） | FullSpeed USB 键盘记录器附加组件（带额外存储） |
| 加密网络 C² | 通过到你自己服务器的加密隧道从任何地方触达这条线 |
| HIDX StealthLink（Elite） | 双向隧道：目标 ↔ O.MG ↔ 控制机 |
| 恢复自我销毁 | 重新接上 Programmer 恢复 |
| 批量固件 | Programmer 支持批量固件安装 |

---

## 故障排查

| 症状 | 原因 | 修复 |
|---|---|---|
| 不出现 WebUI | 设备未激活 | 先用 Programmer 激活 |
| WebFlasher 找不到东西 | 浏览器不支持 WebSerial / 设备不在引导加载程序 | 用 Chrome/Edge；在向导要求之前保持线未插电 |
| 敲击慢 / 乱码 | 键盘布局或 DuckyScript 版本不对 | 用正确的布局编译/重载；检查 Basic vs Elite 版本 |
| 找不到线的 Wi-Fi | 休眠 / 不在设置模式 | 通过 Programmer 重新触发，或按板载按钮序列 |
| 意外自我销毁 | 载荷/地理围栏规则触发 | 用 Programmer 恢复（完全重置）。复查地理围栏范围 |

---

## 相关资源

- [O.MG Plug](/hak5/products/omg-plug/) — 同款植入物，钥匙圈 USB 插头
- [O.MG Adapter](/hak5/products/omg-adapter/) — 植入物在 USB-A 转 C 转接头里
- [O.MG UnBlocker](/hak5/products/omg-unblocker/) — 植入物在「安全」数据阻断器里
- [O.MG Programmer](/hak5/products/omg-programmer/) — 激活/升级 O.MG 设备必需
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — 防御检测工具
- [USB Rubber Ducky](/hak5/products/usb-rubber-ducky/) — DuckyScript 语言参考
- [固件与下载](/hak5/firmware-downloads/) — O.MG 固件与 WebFlasher
- [故障排查索引](/hak5/troubleshooting-index/)
- [Hak5 概览](/hak5/)