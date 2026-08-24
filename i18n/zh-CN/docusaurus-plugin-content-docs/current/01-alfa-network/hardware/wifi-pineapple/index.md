---
id: alfa-hardware-wifi-pineapple
title: Hak5 WiFi Pineapple × ALFA Network 整合指南
sidebar_label: Hak5 WiFi Pineapple
sidebar_position: 4
description: Hak5 WiFi Pineapple Mark VII 搭配 ALFA AWUS036ACM 网卡——5GHz 频段扩展设置、Web 后台配置与天线搭配建议，含每一步的预期结果。
tags: [hak5, wifi-pineapple, mk7, alfa, awus036acm, mt7612u, 5ghz]
keywords: [WiFi Pineapple, Hak5, AWUS036ACM, MT7612U, 5GHz 监听模式, PineAP, MK7AC]
---

# Hak5 WiFi Pineapple × ALFA Network 整合指南

> **一句話定位**：Hak5 WiFi Pineapple Mark VII 出廠只涵蓋 2.4 GHz 频段，要涵蓋 5 GHz 频段（現在大部分裝置都會用到）就需要外接网卡。ALFA AWUS036ACM 用的芯片跟 Hak5 原廠擴充卡完全同款，但天線增益更高、散熱更好，是目前最推薦的搭配選擇。

## 這篇文章適合你嗎？

- **難度**：中階（需要熟悉基本的 SSH 操作跟網頁后台设置）
- **預估時間**：20〜30 分鐘
- **你會用到的技能**：基本终端操作、瀏覽器操作
- **讀完你可以做到**：
  1. 幫 WiFi Pineapple 正確接上並辨識 ALFA 無線网卡
  2. 在 Web 后台设置同時涵蓋 2.4 GHz 和 5 GHz 的扫描與廣播
  3. 依照你的使用情境挑選合適的天線

---

## 概念說明：為什麼 WiFi Pineapple 需要外接网卡

WiFi Pineapple Mark VII 這台設備本身內建了兩組 2.4 GHz 無線電模块（一組用來當管理连接，另外一到兩組負責扫描附近的 Wi-Fi 信号並廣播）。但如果你的實驗或課程需要涵蓋 **5 GHz 频段**（802.11a/n/ac），內建的無線電就不夠用了，必須透過機身上的 USB 埠外接一張支援 5 GHz 的网卡。

Hak5 官方文件明確指出，**MediaTek MT7612U** 芯片是唯一保證能在 WiFi Pineapple 上穩定運作的 5 GHz 网卡芯片。原因跟软件架構有關：WiFi Pineapple 使用的是 OpenWrt 這套嵌入式系統，Realtek 系列芯片（例如 RTL8812AU）在這個環境下需要額外的驱动程序，在高負載（大量数据包同時處理）時容易讓系統當機或無預警重开机；而 MediaTek 的 `mt76x2u` 驱动則是直接寫進 OpenWrt 内核裡，穩定性好很多。

**ALFA AWUS036ACM** 使用的正是同一顆 MT7612U 芯片，跟 Hak5 官方擴充卡 MK7AC 系統辨識起來完全一樣，差別在於 ALFA 网卡用的是標準 RP-SMA 天線接頭（可以自己換天線），而且散熱設計更好，長時間使用比較不容易過熱降速。

> 📘 **名詞小教室**
> - **Recon（偵察扫描）**：WiFi Pineapple 裡的一個功能模块，用來扫描附近有哪些 Wi-Fi 基地台（AP）和连接中的裝置。
> - **PineAP**：WiFi Pineapple 的内核功能之一，可以模擬廣播 Wi-Fi 信号，常用於無線网络安全教學與研究情境。
> - **USB VID:PID**：每個 USB 裝置出廠時都有一組「廠商代碼:產品代碼」，系統可以靠這組代碼辨識裝置是什麼型号，等一下驗證网卡有沒有被正確辨識時會用到。

---

## 你需要準備的東西

- [ ] **硬件**：Hak5 WiFi Pineapple Mark VII 主機
- [ ] **ALFA 無線网卡**：[AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [ ] **供電設備**：一個能穩定輸出 **5V/3A（15W）以上**、支援 QC 或 PD 快充協定的電源供應器或充电宝（原因見下方「供電注意事項」）
- [ ] **天線（依使用情境挑選，詳見第四節）**：全向天線或指向性平板天線
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动原始碼（WiFi Pineapple 的固件與此驱动家族同源）：https://github.com/openwrt/mt76
- [ ] **官方兼容性文件**：[Hak5 官方兼容 802.11ac 网卡清单](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)

---

## Step-by-Step 设置教學

### 步骤 1：硬件連接與供電確認

> ⚠️ **供電注意事項（請先看這段再動手）**：WiFi Pineapple Mark VII 主機本身耗電約 3〜5W，加上 AWUS036ACM 在 5GHz 滿載發射時瞬間電流可達 900mA（約 4.5W），整機總功耗最高可能到 9.5W。
> - ❌ **不要用**：笔记本电脑的 USB 供電埠（通常只有 500mA）或便宜的 5V/1A 豆腐頭充電器，功率不夠會導致設備不穩定甚至自動重开机。
> - ✅ **請用**：能穩定輸出 5V/3A（15W）以上、支援 QC 或 PD 快充協定的專用電源供應器或充电宝。

1. 將 ALFA AWUS036ACM 接上 WiFi Pineapple Mark VII 主機側邊或頂部的 **USB Host** 埠。
2. 建議先接上网卡，**再**接通 Pineapple 主機電源，這樣可以避免开机瞬間供電不足的問題。

---

### 步骤 2：透過 SSH 確認网卡是否被正確辨識

用 SSH 连接進入 WiFi Pineapple 控制台（默认 IP 是 `172.16.42.1`）：

```bash
ssh root@172.16.42.1
```

連上之後，依序執行以下指令確認网卡狀態：

```bash
# 1. 檢視 USB 匯流排裝置清单
lsusb
```

**預期結果**：

```text
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

```bash
# 2. 檢視内核加载日誌，確認驱动有沒有正確加载
dmesg | grep -E "mt76|wlan"
```

**預期結果**：應該會看到類似這樣的幾行訊息，代表驱动程序和固件都加载成功：

```text
mt76x2u 1-1:1.0: ASIC revision: 76120011 mac 00110000
mt76x2u 1-1:1.0: firmware: mt7662u.bin loaded
ieee80211phy3: mt76x2u registered as wlan3
```

```bash
# 3. 檢查目前所有無線接口
iw dev
```

**預期結果**：清单裡會多出一個新的接口（通常是 `wlan3`），代表 ALFA 网卡已經成功被系統辨識為一張獨立的無線网卡。

---

### 步骤 3：在 Web 后台设置 5GHz 扫描與廣播

1. 打開瀏覽器，前往 `http://172.16.42.1:1471` 登入 Pineapple 的 Web 管理接口。
2. 進入 **Recon（偵察扫描）** 模块：
   - 接口選擇下拉選單裡應該會自動出現 `wlan3 (5GHz)`。
   - 勾選同時扫描 **2.4 GHz + 5 GHz**，扫描週期可以设置為 `Continuous`（持續）或 `1 min`（每分鐘）。
   - 點擊 **Start Scan**，系統就會開始同時扫描 5GHz 信道（36〜165）上的基地台與连接裝置。
3. 進入 **PineAP** 模块：
   - 在 **PineAP Settings** 裡，可以把 5GHz 的廣播指派給 `wlan3`，這樣就能讓 2.4GHz（`wlan1`）和 5GHz（`wlan3`）兩個频段同時廣播。

**預期結果**：Recon 頁面上開始出現偵測到的裝置與基地台清单，代表 5GHz 频段已經成功納入扫描範圍。

---

## 天線搭配建議（依使用情境挑選）

- **想要大範圍、四面八方都能收到信号**（例如一般走動測試、涵蓋整個會議室）：
  搭配兩支 **ALFA ARS-NT5B7** 雙頻全向天線（2.4GHz 5dBi / 5GHz 7dBi），信号在水平 360 度範圍內收發均勻，適合會議室或走廊這類需要環繞覆蓋的場景。
- **想要對準特定方向、拉長距離**（例如定點觀測特定樓層或區域）：
  搭配兩片 **ALFA APA-M25** 雙頻指向性平板天線（2.4GHz 8dBi / 5GHz 10dBi，指向角約 60 度），可以有效過濾掉背後方向的雜訊，適合對準特定樓層或辦公區域進行精準測試。

---

## 常見問題與排除指引

### Q1：插入 AWUS036ACM 之後，Pineapple 燈號突然熄滅、自動重开机？
- **原因**：USB 瞬間電壓下降。插入高功率网卡的瞬間，電容充電加上射頻模块初始化，需要的電流超過供電端能負荷的範圍。
- **解決方法**：
  1. 先把 AWUS036ACM 插入 Pineapple，再接通 Pineapple 主機電源开机（不要开机狀態下插拔）。
  2. 更換輸出能力達 5V/3A 以上的電源供應器。

### Q2：接口卡在 `wlan2`，Web 后台看不到 5GHz 選項？
- **原因**：如果之前曾經插過其他 USB 网卡，系統裡 `/etc/config/wireless` 這個设置檔可能殘留了舊的衝突设置。
- **解決方法**：透過 SSH 執行以下指令重置無線设置：
  ```bash
  rm -f /etc/config/wireless
  wifi config
  /etc/init.d/network restart
  ```

---

## 參考数据與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [Hak5 官方兼容 802.11ac 网卡清单](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)
- [ALFA 無線网卡在 Unitree 机器人上（Go2 / B2 / A1）](/alfa-network/hardware/unitree/)——另一個 5GHz 频段應用情境的整合方式
- [詞彙表](/getting-started/glossary)——Recon、PineAP 等名詞的完整解釋
- MediaTek MT76 系列驱动原始碼：https://github.com/openwrt/mt76

**標籤：** `hak5` `wifi-pineapple` `mk7` `alfa` `awus036acm` `mt7612u` `5ghz` `新手指南`
