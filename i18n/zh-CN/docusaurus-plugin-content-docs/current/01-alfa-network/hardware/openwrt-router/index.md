---
id: alfa-hardware-openwrt-router
title: OpenWrt 路由器 × ALFA Network 网卡配置与已知限制
sidebar_label: OpenWrt 路由器
sidebar_position: 7
description: OpenWrt 路由器（含 GL.iNet）搭配 ALFA 无线网卡——软件包安装、无线设置与上游已知 Bug 应对策略，含每一步的预期结果。
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt 路由器 × ALFA Network 配置與限制指南

> **一句話定位**：OpenWrt 路由器（包括 GL.iNet 系列、x86 軟路由等）可以透過 USB 外接 ALFA 無線网卡，多出一組獨立的無線频段，拿來當第二組無線中繼、廣播熱點，或是無線安全监听節點。這篇文章教你怎麼裝、也老實告訴你目前有哪些已知的限制。

## 這篇文章適合你嗎？

- **難度**：中階（需要會用 SSH 操作路由器）
- **預估時間**：15〜25 分鐘
- **你會用到的技能**：基本终端操作
- **讀完你可以做到**：
  1. 判斷自己的 ALFA 网卡型号在 OpenWrt 上該裝哪個驱动软件包
  2. 完成软件包安裝與無線接口设置
  3. 知道目前有哪些已知的驱动限制，避免踩坑

---

## 概念說明：為什麼要在路由器上外接無線网卡

OpenWrt 路由器（尤其是小型的 GL.iNet 系列）內建的無線模块數量有限，如果你的需求是下面任何一種，內建模块通常不夠用：

- **多一組獨立的無線中繼（WISP）**：讓路由器一邊連上既有的 Wi-Fi 當「用戶端」取得网络，一邊自己再廣播出一個新的 Wi-Fi 給你的裝置用。
- **多一組廣播熱點**：內建無線模块已經在用了，還想再開一個獨立的 SSID。
- **無線安全监听節點**：把路由器變成一個長期擺著的数据包擷取點。

外接 ALFA 网卡就是在原本的無線模块之外，多插一張獨立的网卡來做這些事。

> 📘 **名詞小教室**
> - **kmod（Kernel Module，内核模块）**：OpenWrt 上驱动程序的安裝單位，`kmod-mt7921u` 就是「MT7921U 這顆芯片的内核模块」，裝上之後系統才認得這張网卡。
> - **opkg**：OpenWrt 專用的软件包管理工具，跟一般 Linux 上的 `apt` 是類似的東西，用來安裝/更新软件软件包。
> - **WISP（Wireless ISP，無線网络服務供應）模式**：一種讓路由器「先連上別人的 Wi-Fi，再把网络分享出去」的運作方式，常用於延伸网络信号。

---

## ALFA 网卡型号在 OpenWrt 上的支援情況

| ALFA 型号         | 内核芯片               | OpenWrt 22.03.3+ | OpenWrt 23.05+ | 需要安裝的软件包                       |
| --------------- | ------------------ | ---------------- | -------------- | ------------------------------ |
| **AWUS036ACM**  | MediaTek MT7612U   | ✅ 完整支援           | ✅ 完整支援         | `kmod-mt76x2u` `mt76-firmware` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ 支援（有已知限制，見下方）    | ✅ 支援（有已知限制，見下方）  | `kmod-mt7921u`                 |
| **AWUS036ACHM** | MediaTek MT7610U   | ✅ 完整支援           | ✅ 完整支援         | `kmod-mt76x0u`                 |
| **AWUS036ACH**  | Realtek RTL8812AU  | ❌ 官方软件包庫沒有提供         | ❌ 官方软件包庫沒有提供       | 需自行用 OpenWrt SDK 编译，不建議新手嘗試     |

**簡單判斷方式**：如果你是第一次嘗試，建議優先選 **AWUS036ACM**（MT7612U）——支援最完整、也沒有下面提到的已知限制。想要更新的 Wi-Fi 6/6E（AWUS036AXML）也可以用，但要先看過下面的已知限制章節。

---

## 你需要準備的東西

- [ ] **硬件**：一台已刷好 OpenWrt 的路由器（含 GL.iNet 系列），且可透過 SSH 连接管理
- [ ] **ALFA 無線网卡**：依上表選擇
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动原始碼（OpenWrt 官方維護，`kmod-mt7921u`、`kmod-mt76x2u` 等软件包的來源）：https://github.com/openwrt/mt76

---

## Step-by-Step 设置教學

透過 SSH 登入路由器终端，依序執行：

### 步骤 1：更新软件包庫索引

```bash
opkg update
```

**預期結果**：终端會列出一連串软件包庫更新的訊息，沒有出現紅色錯誤訊息即代表成功。

---

### 步骤 2：安裝對應的驱动软件包

依照你使用的网卡型号，選擇對應的指令：

```bash
# 若使用 AWUS036AXML（Wi-Fi 6/6E）：
opkg install kmod-mt7921u kmod-mt76-core wireless-tools usbutils

# 若使用 AWUS036ACM（802.11ac）：
opkg install kmod-mt76x2u kmod-mt76-core wireless-tools usbutils
```

**預期結果**：畫面顯示软件包下載與安裝完成的訊息，最後沒有出現錯誤。

---

### 步骤 3：重新偵測無線硬件並套用设置

```bash
wifi config >> /etc/config/wireless
/etc/init.d/network restart
```

**預期結果**：网络服務重新啟動後，可以到 LuCI 網頁管理接口（路由器的網頁后台）的「网络 → 無線」頁面，應該會看到多出一組新的無線接口，代表 ALFA 网卡已經被系統正確辨識並可以设置使用。

---

## 已知限制（老實跟你說，不隱瞞）

### 限制 1：AWUS036AXML 在主動监听模式下可能當機

- **現象**：如果你在 OpenWrt 上對 AWUS036AXML（`mt7921u`）啟用「主動监听 + 注入」（例如執行 `aireplay-ng --deauth`），驱动程序可能在幾秒內鎖死，系統日誌會出現 `mt7921u: failed to send tx packet`，网卡直接離線。
- **原因**：這是上游 `openwrt/mt76` 專案已知的問題（[Issue #839](https://github.com/openwrt/mt76/issues/839)），跟内核處理 USB 数据傳輸緩衝區釋放時的競爭狀態有關，不是你的设置錯誤。
- **實務建議**：
  - 如果你只需要**單純擷取数据包**（被動监听，例如用 Kismet 或 tcpdump），可以正常使用，不受這個問題影響。
  - 如果你需要**主動注入数据包**（例如做滲透測試），目前建議改用 **AWUS036ACM**（`mt76x2u`），這顆芯片的驱动已經過多年驗證，沒有這個問題。

### 限制 2：6GHz 频段目前支援不完整

目前 OpenWrt 穩定版（23.05）的網頁管理接口（LuCI）對 6GHz 频段的设置選項還沒有完全支援。也就是說，AWUS036AXML 在 OpenWrt 上目前主要能穩定使用的是 2.4GHz 和 5GHz，6GHz 频段的完整支援還在等上游持續開發。

---

## 常見問題與排除指引

### Q1：裝完软件包後，LuCI 接口還是看不到新的無線接口？
- **原因**：可能是软件包安裝過程中有錯誤被忽略了，或是网络服務沒有正確重啟。
- **解決方法**：重新執行 `opkg update` 確認软件包庫索引是最新的，再重新執行步骤 2、3；也可以用 `dmesg | grep -i mt76` 或 `dmesg | grep -i mt7921` 檢查内核有沒有正確加载驱动。

### Q2：AWUS036ACH（Realtek 芯片）可以用嗎？
- **原因**：OpenWrt 官方软件包庫目前沒有提供這顆芯片的預编译软件包。
- **解決方法**：技術上可以透過 OpenWrt SDK 自行编译 out-of-tree 驱动模块，但這需要較進階的编译環境知識，不建議新手嘗試；如果你需要穩定好裝的方案，優先考慮 AWUS036ACM。

---

## 參考数据與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)
- [ALFA 無線网卡在 Orange Pi / RK3588 上](/alfa-network/hardware/orange-pi/)——另一個使用 MT76 系列驱动的整合情境
- [詞彙表](/getting-started/glossary)——kmod、opkg 等名詞的完整解釋
- MediaTek MT76 系列驱动原始碼（OpenWrt 官方維護）：https://github.com/openwrt/mt76
- 已知 Bug 追蹤：https://github.com/openwrt/mt76/issues/839

**標籤：** `openwrt` `glinet` `router` `alfa` `awus036axml` `mt7921u` `mt7612u` `kmod` `新手指南`
