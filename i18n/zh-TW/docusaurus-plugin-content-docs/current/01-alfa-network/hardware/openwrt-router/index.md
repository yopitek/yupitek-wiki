---
id: alfa-hardware-openwrt-router
title: OpenWrt 路由器 × ALFA Network 網卡配置與已知限制
sidebar_label: OpenWrt 路由器
sidebar_position: 7
description: OpenWrt 路由器（含 GL.iNet）搭配 ALFA 無線網絡卡——套件安裝、無線設定與上游已知 Bug 應對策略，含每一步的預期結果。
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt 路由器 × ALFA Network 配置與限制指南

> **一句話定位**：OpenWrt 路由器（包括 GL.iNet 系列、x86 軟路由等）可以透過 USB 外接 ALFA 無線網絡卡，多出一組獨立的無線頻段，拿來當第二組無線中繼、廣播熱點，或是無線安全監聽節點。這篇文章教你怎麼裝、也老實告訴你目前有哪些已知的限制。

## 這篇文章適合你嗎？

- **難度**：中階（需要會用 SSH 操作路由器）
- **預估時間**：15〜25 分鐘
- **你會用到的技能**：基本終端機操作
- **讀完你可以做到**：
  1. 判斷自己的 ALFA 網卡型號在 OpenWrt 上該裝哪個驅動套件
  2. 完成套件安裝與無線介面設定
  3. 知道目前有哪些已知的驅動限制，避免踩坑

---

## 概念說明：為什麼要在路由器上外接無線網絡卡

OpenWrt 路由器（尤其是小型的 GL.iNet 系列）內建的無線模組數量有限，如果你的需求是下面任何一種，內建模組通常不夠用：

- **多一組獨立的無線中繼（WISP）**：讓路由器一邊連上既有的 Wi-Fi 當「用戶端」取得網路，一邊自己再廣播出一個新的 Wi-Fi 給你的裝置用。
- **多一組廣播熱點**：內建無線模組已經在用了，還想再開一個獨立的 SSID。
- **無線安全監聽節點**：把路由器變成一個長期擺著的封包擷取點。

外接 ALFA 網卡就是在原本的無線模組之外，多插一張獨立的網卡來做這些事。

> 📘 **名詞小教室**
> - **kmod（Kernel Module，核心模組）**：OpenWrt 上驅動程式的安裝單位，`kmod-mt7921u` 就是「MT7921U 這顆晶片的核心模組」，裝上之後系統才認得這張網卡。
> - **opkg**：OpenWrt 專用的套件管理工具，跟一般 Linux 上的 `apt` 是類似的東西，用來安裝/更新軟體套件。
> - **WISP（Wireless ISP，無線網路服務供應）模式**：一種讓路由器「先連上別人的 Wi-Fi，再把網路分享出去」的運作方式，常用於延伸網路訊號。

---

## ALFA 網卡型號在 OpenWrt 上的支援情況

| ALFA 型號         | 核心晶片               | OpenWrt 22.03.3+ | OpenWrt 23.05+ | 需要安裝的套件                       |
| --------------- | ------------------ | ---------------- | -------------- | ------------------------------ |
| **AWUS036ACM**  | MediaTek MT7612U   | ✅ 完整支援           | ✅ 完整支援         | `kmod-mt76x2u` `mt76-firmware` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ 支援（有已知限制，見下方）    | ✅ 支援（有已知限制，見下方）  | `kmod-mt7921u`                 |
| **AWUS036ACHM** | MediaTek MT7610U   | ✅ 完整支援           | ✅ 完整支援         | `kmod-mt76x0u`                 |
| **AWUS036ACH**  | Realtek RTL8812AU  | ❌ 官方套件庫沒有提供         | ❌ 官方套件庫沒有提供       | 需自行用 OpenWrt SDK 編譯，不建議新手嘗試     |

**簡單判斷方式**：如果你是第一次嘗試，建議優先選 **AWUS036ACM**（MT7612U）——支援最完整、也沒有下面提到的已知限制。想要更新的 Wi-Fi 6/6E（AWUS036AXML）也可以用，但要先看過下面的已知限制章節。

---

## 你需要準備的東西

- [ ] **硬體**：一台已刷好 OpenWrt 的路由器（含 GL.iNet 系列），且可透過 SSH 連線管理
- [ ] **ALFA 無線網絡卡**：依上表選擇
- [ ] **驅動程式參考（GitHub）**：
  - MediaTek MT76 系列驅動原始碼（OpenWrt 官方維護，`kmod-mt7921u`、`kmod-mt76x2u` 等套件的來源）：https://github.com/openwrt/mt76

---

## Step-by-Step 設定教學

透過 SSH 登入路由器終端機，依序執行：

### 步驟 1：更新套件庫索引

```bash
opkg update
```

**預期結果**：終端機會列出一連串套件庫更新的訊息，沒有出現紅色錯誤訊息即代表成功。

---

### 步驟 2：安裝對應的驅動套件

依照你使用的網卡型號，選擇對應的指令：

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
wifi config >> /etc/config/wireless
/etc/init.d/network restart
```

**預期結果**：網路服務重新啟動後，可以到 LuCI 網頁管理介面（路由器的網頁後台）的「網路 → 無線」頁面，應該會看到多出一組新的無線介面，代表 ALFA 網卡已經被系統正確辨識並可以設定使用。

---

## 已知限制（老實跟你說，不隱瞞）

### 限制 1：AWUS036AXML 在主動監聽模式下可能當機

- **現象**：如果你在 OpenWrt 上對 AWUS036AXML（`mt7921u`）啟用「主動監聽 + 注入」（例如執行 `aireplay-ng --deauth`），驅動程式可能在幾秒內鎖死，系統日誌會出現 `mt7921u: failed to send tx packet`，網卡直接離線。
- **原因**：這是上游 `openwrt/mt76` 專案已知的問題（[Issue #839](https://github.com/openwrt/mt76/issues/839)），跟核心處理 USB 資料傳輸緩衝區釋放時的競爭狀態有關，不是你的設定錯誤。
- **實務建議**：
  - 如果你只需要**單純擷取封包**（被動監聽，例如用 Kismet 或 tcpdump），可以正常使用，不受這個問題影響。
  - 如果你需要**主動注入封包**（例如做滲透測試），目前建議改用 **AWUS036ACM**（`mt76x2u`），這顆晶片的驅動已經過多年驗證，沒有這個問題。

### 限制 2：6GHz 頻段目前支援不完整

目前 OpenWrt 穩定版（23.05）的網頁管理介面（LuCI）對 6GHz 頻段的設定選項還沒有完全支援。也就是說，AWUS036AXML 在 OpenWrt 上目前主要能穩定使用的是 2.4GHz 和 5GHz，6GHz 頻段的完整支援還在等上游持續開發。

---

## 常見問題與排除指引

### Q1：裝完套件後，LuCI 介面還是看不到新的無線介面？
- **原因**：可能是套件安裝過程中有錯誤被忽略了，或是網路服務沒有正確重啟。
- **解決方法**：重新執行 `opkg update` 確認套件庫索引是最新的，再重新執行步驟 2、3；也可以用 `dmesg | grep -i mt76` 或 `dmesg | grep -i mt7921` 檢查核心有沒有正確載入驅動。

### Q2：AWUS036ACH（Realtek 晶片）可以用嗎？
- **原因**：OpenWrt 官方套件庫目前沒有提供這顆晶片的預編譯套件。
- **解決方法**：技術上可以透過 OpenWrt SDK 自行編譯 out-of-tree 驅動模組，但這需要較進階的編譯環境知識，不建議新手嘗試；如果你需要穩定好裝的方案，優先考慮 AWUS036ACM。

---

## 參考資料與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)
- [ALFA 無線網絡卡在 Orange Pi / RK3588 上](/alfa-network/hardware/orange-pi/)——另一個使用 MT76 系列驅動的整合情境
- [詞彙表](/getting-started/glossary)——kmod、opkg 等名詞的完整解釋
- MediaTek MT76 系列驅動原始碼（OpenWrt 官方維護）：https://github.com/openwrt/mt76
- 已知 Bug 追蹤：https://github.com/openwrt/mt76/issues/839

**標籤：** `openwrt` `glinet` `router` `alfa` `awus036axml` `mt7921u` `mt7612u` `kmod` `新手指南`
