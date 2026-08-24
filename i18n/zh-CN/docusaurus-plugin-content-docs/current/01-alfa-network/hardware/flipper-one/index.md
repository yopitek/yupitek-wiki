---
id: alfa-hardware-flipper-one
title: Flipper One × ALFA Network 兼容性与选型指南
sidebar_label: Flipper One
sidebar_position: 5
description: Flipper One 内置 MT7921AUN Wi-Fi 6E 芯片与外接 ALFA 网卡选型指南——搞懂 Flipper Zero 与 One 架构差异，双网卡并行与监听模式设置。
tags: [flipper, flipper-one, flipper-zero, alfa, awus036axml, mt7921aun, wifi-6e]
keywords: [Flipper One, Flipper Zero, AWUS036AXML, MT7921AUN, Wi-Fi 6E, USB Host]
---

# Flipper One × ALFA Network 兼容性與選型指南

> **一句話定位**：Flipper One 本身就內建了一顆 Wi-Fi 6E 芯片，很多情況下不用外接网卡就夠用。但如果你需要更遠的距離、更強的信号，或想同時做「连接」加「监听」兩件事，外接一支 ALFA 网卡會是更好的選擇。這篇文章幫你搞懂什麼時候該加裝、該怎麼接。

## 這篇文章適合你嗎？

- **難度**：中階（需要熟悉基本的 Linux 终端指令）
- **預估時間**：15〜25 分鐘
- **你會用到的技能**：基本终端操作
- **讀完你可以做到**：
  1. 搞懂 Flipper Zero 跟 Flipper One 在能不能外接网卡這件事上的根本差異
  2. 判斷自己的情境該用內建芯片還是外接 ALFA 网卡
  3. 實際把 ALFA 网卡接上 Flipper One 並驗證是否成功

---

## 概念說明：Flipper Zero 跟 Flipper One 差在哪？為什麼一個能接网卡、一個不能？

如果你是從 Flipper Zero 一路玩過來，可能會想問：「能不能買一條 USB-C 轉接線，把 ALFA 网卡接到 Flipper Zero 上？」

答案是：**在硬件層面完全不可能**，原因不是软件限制，而是兩者的硬件架構根本不同：

- **Flipper Zero** 的 USB-C 埠只支援「裝置模式（Device Mode）」——意思是它只能被电脑或手機當成一個周邊裝置來連接，它自己**沒有能力去驱动、供電給另一個外接裝置**，所以不管接什麼轉接線，都無法把一張网卡「接上去」讓系統辨識到。
- **Flipper One** 則不一樣：它搭載真正的 ARM Cortex-A 應用處理器，執行完整的 Linux 作業系統，並且真的具備 **USB Host（主機）模式**——這代表它可以像一台电脑一樣，透過 OTG（On-The-Go）轉接線去驱动並辨識外接的 USB 裝置，包括 ALFA 無線网卡。

> 📘 **名詞小教室**
> - **USB Host（主機）模式 vs Device（裝置）模式**：USB Host 模式代表這台設備能「主動」去驱动、供電給其他 USB 裝置（就像你的电脑可以接滑鼠、隨身碟）；Device 模式則相反，代表這台設備只能「被」別人（例如电脑）當成一個周邊裝置接上去，自己沒辦法反過來驱动別的裝置。這是判斷一台設備能不能外接网卡的關鍵。
> - **OTG（On-The-Go）**：一種讓行動裝置的 USB 埠可以在「裝置模式」和「主機模式」之間切換的技術，讓手機、Flipper One 這類小型裝置也能像电脑一樣外接周邊設備。
> - **Wi-Fi 6E**：Wi-Fi 6 的延伸版本，多了 6 GHz 這個相對空曠、干扰少的频段可以使用。

---

## 內建 MT7921AUN vs 外接 ALFA 网卡，怎麼選？

Flipper One 內建的芯片其實跟 **ALFA AWUS036AXML** 用的是同一顆——**MediaTek MT7921AUN**，支援完整的 Wi-Fi 6E（2.4 / 5 / 6 GHz）。差別主要在天線和發射功率：

| 比較項目 | Flipper One 內建芯片 | 外接 AWUS036AXML | 外接 AWUS036ACM |
| ------------ | ----------------------- | --------------------------------- | -------------------------------- |
| 芯片型号     | MediaTek MT7921AUN      | MediaTek MT7921AUN                | MediaTek MT7612U                 |
| 支援频段     | 2.4 / 5 / 6 GHz | 2.4 / 5 / 6 GHz           | 2.4 / 5 GHz                  |
| 天線     | 機身內部微型天線             | 外接 RP-SMA 天線（可自行更換）               | 外接 RP-SMA 天線（可自行更換）              |
| 發射功率     | 較低（隨身裝置的標準限制）     | 較高（有獨立功率放大器）               | 較高（有獨立功率放大器）              |
| 適合情境     | 日常隨身、輕量扫描                | 需要 6 GHz 全频段、想要更遠距離的监听情境 | 想要穩定的 5 GHz 数据包注入，且不需要 6 GHz |

**簡單判斷方式**：如果你只是想隨身帶著做輕量扫描，內建芯片就夠了；如果你需要更遠的距離、更強的信号，或想讓內建芯片專心負責连接（例如透過 SSH 遠端操作），外接的 ALFA 网卡專心負責监听，那就該加裝外接网卡。

---

## 你需要準備的東西

- [ ] **硬件**：Flipper One（確認你手上的是 Flipper One，不是 Flipper Zero——參考上一節的差異判斷）
- [ ] **ALFA 無線网卡**（依需求擇一）：
  - [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)——要用 6 GHz、要遠距離就選這支
  - [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)——穩定的 5 GHz 方案
- [ ] **USB Type-C OTG 轉接線**：用來連接 Flipper One 跟 ALFA 网卡
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动（適用 MT7921AUN / MT7612U，兩款 ALFA 网卡都用這個驱动家族）：https://github.com/morrownr/mt76

---

## Step-by-Step 设置教學

### 步骤 1：透過 OTG 轉接線接上 ALFA 网卡

用 Type-C OTG 轉接線，把 ALFA AWUS036AXML（或 ACM）接上 Flipper One。

---

### 步骤 2：確認网卡是否被正確辨識

在 Flipper One 的终端輸入：

```bash
lsusb
```

**預期結果**：你應該會看到類似這樣的一行輸出，代表系統已經認出這是一張 MediaTek 网卡：

```text
Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

接著檢查這張网卡實際支援哪些频段：

```bash
iw phy
```

**預期結果**：如果是 AWUS036AXML，輸出裡應該會列出三個频段的完整支援範圍：

```text
Band 1: 2.4 GHz (20/40 MHz)
Band 2: 5 GHz (20/40/80/160 MHz)
Band 4: 6 GHz (20/40/80/160 MHz HE channels)
```

---

### 步骤 3：建立「內建连接 + 外接监听」的雙网卡架構

這是外接网卡最實用的情境：讓 Flipper One 內建的网卡（`wlan0`）繼續保持连接（例如透過 SSH 或網頁操作），外接的 ALFA 网卡（`wlan1`）則專心切到监听模式：

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

**預期結果**：指令執行沒有錯誤訊息，代表 `mon0` 這個监听接口已經成功建立在外接的 ALFA 网卡上，這時候你可以繼續用 `wlan0` 保持连接操作，同時用 `mon0` 進行数据包擷取，兩者互不干扰。

---

## 常見問題與排除指引

### Q1：我可以把 ALFA 网卡接在 Flipper Zero 上嗎？
- **原因**：Flipper Zero 的 USB-C 埠只支援裝置模式（Device Mode），沒有 USB Host（主機）能力。
- **解決方法**：無法透過任何轉接線解決，這是硬件本身的限制。如果你需要外接网卡的功能，需要使用 Flipper One。

### Q2：6 GHz 频段可以正常连接，但某些数据包注入工具用不了？
- **原因**：目前部分開源的数据包注入（Frame Injection）工具，對 6 GHz 這個相對新的規範支援還不夠成熟，這是工具本身開發進度的問題，不是你的设置錯誤。
- **解決方法**：6 GHz 频段目前建議優先用於一般连接與扫描；如果你的專案一定需要数据包注入，可以先改用 5 GHz 频段測試（AWUS036ACM 或把 AXML 切到 5 GHz）。

### Q3：內建芯片跟外接网卡可以同時開监听模式嗎？
- **原因**：技術上可以，但因為兩者都是 MediaTek 芯片、可能共用部分系統資源，同時對兩個信道做监听在部分情境下可能不穩定。
- **解決方法**：建議採用步骤 3 的做法——一個負責连接、一個專心监听，而不是兩個都做监听，穩定性會好很多。

---

## 參考数据與延伸閱讀

- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)
- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [ALFA 無線网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——同樣使用 MT7921AUN 芯片的另一個整合情境
- [詞彙表](/getting-started/glossary)——USB Host 模式、OTG 等名詞的完整解釋
- MediaTek MT76 系列驱动（社群維護，含 DKMS）：https://github.com/morrownr/mt76

**標籤：** `flipper` `flipper-one` `flipper-zero` `alfa` `awus036axml` `mt7921aun` `wifi-6e` `新手指南`
