---
id: alfa-hardware-openwrt-router
title: OpenWrt 路由器 × ALFA Network 網路卡配置與已知限制
sidebar_label: OpenWrt 路由器
sidebar_position: 7
description: OpenWrt 路由器（含 GL.iNet）搭配 ALFA 無線網路卡——套件安裝、無線設定與上游已知 Bug 應對策略，含每一步的預期結果。
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt 路由器 × ALFA Network 配置與限制指南

> **一句話定位**：OpenWrt 路由器（包括 GL.iNet 系列、x86 軟路由等）可以透過 USB 外接 ALFA 無線網路卡，多出一組獨立的無線頻段，拿來當第二組無線中繼、廣播熱點，或是無線安全監聽節點。這篇文章教你怎麼裝、也老實告訴你目前有哪些已知的限制。

## 這篇文章適合你嗎？

- **難度**：中階（需要會用 SSH 操作路由器）
- **預估時間**：15〜25 分鐘
- **你會用到的技能**：基本終端機操作
- **讀完你可以做到**：
  1. 判斷自己的 ALFA 網路卡型號在 OpenWrt 上該裝哪個驅動套件
  2. 完成套件安裝與無線介面設定
  3. 知道目前有哪些已知的驅動限制，避免踩坑

---

## 概念說明：為什麼要在路由器上外接無線網路卡

OpenWrt 路由器（尤其是小型的 GL.iNet 系列）內建的無線模組數量有限，如果你的需求是下面任何一種，內建模組通常不夠用：

- **多一組獨立的無線中繼（WISP）**：讓路由器一邊連上既有的 Wi-Fi 當「用戶端」取得網路，一邊自己再廣播出一個新的 Wi-Fi 給你的裝置用。
- **多一組廣播熱點**：內建無線模組已經在用了，還想再開一個獨立的 SSID。
- **無線安全監聽節點**：把路由器變成一個長期擺著的封包擷取點。

外接 ALFA 網路卡就是在原本的無線模組之外，多插一張獨立的網路卡來做這些事。

> 📘 **名詞小教室**
> - **kmod（Kernel Module，核心模組）**：OpenWrt 上驅動程式的安裝單位，`kmod-mt7921u` 就是「MT7921U 這顆晶片的核心模組」，裝上之後系統才認得這張網路卡。
> - **opkg**：OpenWrt 專用的套件管理工具，跟一般 Linux 上的 `apt` 是類似的東西，用來安裝/更新軟體套件。
> - **WISP（Wireless ISP，無線網路服務供應）模式**：一種讓路由器「先連上別人的 Wi-Fi，再把網路分享出去」的運作方式，常用於延伸網路訊號。

---

## ALFA 網路卡型號在 OpenWrt 上的支援情況

| ALFA 型號 | 晶片 | OpenWrt 24.10 | OpenWrt 25.12 | 驅動套件 |
|---|---|---|---|---|
| **AWUS036ACM** | MediaTek MT7612U | ✅ 官方套件庫有提供 | ✅ 官方套件庫有提供 | `kmod-mt76x2u` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ 官方套件庫有提供（有已知限制，見下方） | ✅ 官方套件庫有提供（有已知限制，見下方） | `kmod-mt7921u` |
| **AWUS036ACHM** | MediaTek MT7610U | ✅ 官方套件庫有提供 | ✅ 官方套件庫有提供 | `kmod-mt76x0u` |
| **AWUS036ACH** | Realtek RTL8812AU | ✅ 官方套件庫有提供（社群維護的驅動） | ✅ 官方套件庫有提供（社群維護的驅動） | `kmod-rtl8812au-ct` |

上表只標示驅動套件是否存在於 OpenWrt 官方套件庫（已對照 downloads.openwrt.org 確認）。實際在特定路由器上的運作情形、監聽與注入支援度，取決於硬體平台與核心版本，請參閱 [openwrt.org](https://openwrt.org/) 與 [Table of Hardware](https://openwrt.org/toh/start)。

**簡單判斷方式**：如果你是第一次嘗試，建議優先選 **AWUS036ACM**（MT7612U）——不受下面提到的已知限制影響。想要更新的 Wi-Fi 6/6E（AWUS036AXML）也可以用，但要先看過下面的已知限制章節。

---

## 你需要準備的東西

- [ ] **硬體**：一台已刷好 OpenWrt 的路由器（含 GL.iNet 系列），且可透過 SSH 連線管理
- [ ] **ALFA 無線網路卡**：依上表選擇
- [ ] **驅動程式參考（GitHub）**：
  - MediaTek MT76 系列驅動原始碼（OpenWrt 官方維護，`kmod-mt7921u`、`kmod-mt76x2u` 等套件的來源）：https://github.com/openwrt/mt76

---

## Step-by-Step 設定教學

透過 SSH 登入路由器終端機，依序執行（以下指令使用 `opkg`；25.12 等較新版本可能改用 `apk`，請至 openwrt.org 確認）：

### 步驟 1：更新套件庫索引

```bash
opkg update
```

**預期結果**：終端機會列出一連串套件庫更新的訊息，沒有出現紅色錯誤訊息即代表成功。

---

### 步驟 2：安裝對應的驅動套件

依照你使用的網路卡型號，選擇對應的指令：

```bash
# 若使用 AWUS036AXML（Wi-Fi 6/6E）：
opkg install kmod-mt7921u kmod-mt76-core wireless-tools usbutils

# 若使用 AWUS036ACM（802.11ac）：
opkg install kmod-mt76x2u kmod-mt76-core wireless-tools usbutils
```

**預期結果**：畫面顯示套件下載與安裝完成的訊息，最後沒有出現錯誤。

---

### 步驟 3：重新偵測無線硬體並套用設定

```bash
wifi config
/etc/init.d/network restart
```

**預期結果**：網路服務重新啟動後，可以到 LuCI 網頁管理介面（路由器的網頁後台）的「網路 → 無線」頁面，應該會看到多出一組新的無線介面，代表 ALFA 網路卡已經被系統正確辨識並可以設定使用。

---

## 已知限制（老實跟你說，不隱瞞）

### 限制 1：AWUS036AXML 在主動監聽模式下會讓驅動停止運作

- **現象**：依上游 `openwrt/mt76` 的 [Issue #839](https://github.com/openwrt/mt76/issues/839)，在 AWUS036AXML（`mt7921u`）啟用「主動監聽（active monitor）」後，驅動程式會停止運作；同一份回報中，一般（被動）監聽模式則可正常擷取封包。
- **狀態**：該 Issue 在上游已標示為關閉；實際行為可能隨核心版本而異，請至 Issue 頁面確認最新情況。
- **實務建議**：
  - 如果你只需要**單純擷取封包**（被動監聽，例如用 Kismet 或 tcpdump），請使用一般監聽模式。
  - Issue 中指出主動監聽在 `mt76x0u` 與 `mt76x2u` 上可運作；需要主動監聽時，建議改用 **AWUS036ACM**（`mt76x2u`）或 **AWUS036ACHM**（`mt76x0u`）。

### 限制 2：6GHz 頻段的支援情形

6GHz 在 OpenWrt 上能否使用，取決於驅動程式、地區法規設定與 LuCI 版本，請以 [openwrt.org](https://openwrt.org/) 的最新說明為準。

---

## 常見問題與排除指引

### Q1：裝完套件後，LuCI 介面還是看不到新的無線介面？
- **原因**：可能是套件安裝過程中有錯誤被忽略了，或是網路服務沒有正確重啟。
- **解決方法**：重新執行 `opkg update` 確認套件庫索引是最新的，再重新執行步驟 2、3；也可以用 `dmesg | grep -i mt76` 或 `dmesg | grep -i mt7921` 檢查核心有沒有正確載入驅動。

### Q2：AWUS036ACH（Realtek 晶片）可以用嗎？
- **說明**：OpenWrt 官方套件庫有提供 `kmod-rtl8812au-ct`（社群維護的 RTL8812AU 驅動）。監聽與注入等功能是否可用，請參閱 [openwrt.org](https://openwrt.org/)；若你需要已知穩定的方案，優先考慮 AWUS036ACM。

---

## 參考資料與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)
- [ALFA 無線網路卡在 Orange Pi / RK3588 上](/alfa-network/hardware/orange-pi/)——另一個使用 MT76 系列驅動的整合情境
- [詞彙表](/getting-started/glossary)——kmod、opkg 等名詞的完整解釋
- MediaTek MT76 系列驅動原始碼（OpenWrt 官方維護）：https://github.com/openwrt/mt76
- 已知 Bug 追蹤：https://github.com/openwrt/mt76/issues/839

**標籤：** `openwrt` `glinet` `router` `alfa` `awus036axml` `mt7921u` `mt7612u` `kmod` `新手指南`
