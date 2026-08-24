---
id: alfa-hardware-android-nethunter
title: Android Kali NetHunter × ALFA Network 整合与供电指南
sidebar_label: Android NetHunter
sidebar_position: 6
description: Kali NetHunter 手机搭配 ALFA 无线网卡——OTG Y-Cable 供电设置、驱动确认与监听模式启用指南，含每一步的预期结果。
tags: [kali, nethunter, android, otg, alfa, awus036ach, rtl8812au, monitor-mode]
keywords: [Kali NetHunter, Android OTG, AWUS036ACH, AWUS036NEH, AWUS036NHA, RTL8812AU, Y-cable]
---

# Android Kali NetHunter × ALFA Network 整合與供電指南

> **一句話定位**：手機的 USB 埠供電能力有限，直接接上高功率的 ALFA 网卡常常會讓手機重开机或网卡斷線。這篇文章教你怎麼用一條 Y-Cable 解決供電問題，並在 Kali NetHunter 上正確设置你的 ALFA 网卡。

## 這篇文章適合你嗎？

- **難度**：中階（需要熟悉基本的 Linux 终端指令，並已經在手機上安裝好 Kali NetHunter）
- **預估時間**：20〜30 分鐘
- **你會用到的技能**：基本终端操作
- **讀完你可以做到**：
  1. 選對兼容的 ALFA 网卡型号，並判斷需不需要額外供電
  2. 正確接線並在手機供電有限的情況下穩定使用高功率网卡
  3. 在 NetHunter 上驗證网卡辨識、啟用监听模式

---

## 概念說明：手機的供電限制是怎麼一回事

Android 手機的 USB-C（或 Micro-USB）埠在 **OTG Host 模式**下，硬件上能提供的供電上限通常只有 **500mA（2.5W）左右**。但像 ALFA AWUS036ACH 這類高功率网卡，在發射数据包的瞬間，峰值功率可能達到 **3.6W（720mA @ 5V）**——遠超過手機能穩定提供的供電量。

這就是為什麼很多人第一次把高功率网卡接上手機時，會遇到手機突然重开机，或网卡连接一直斷斷續續的狀況：不是网卡壞了，也不是设置錯了，單純是手機供電不夠用。

解決方法是使用一條 **Y-Cable（Y 形分线器）**：它有兩個輸入端和一個輸出端，讓你可以一邊透過手機傳輸数据給网卡，一邊從外部電源（例如充电宝）額外供電，把「数据傳輸」和「供電」這兩件事分開處理，网卡就不用只靠手機那 500mA 硬撐。

> 📘 **名詞小教室**
> - **OTG（On-The-Go）**：一種讓手機的 USB 埠可以切換成「主機模式」的技術，讓手機可以像电脑一樣外接滑鼠、隨身碟、网卡等裝置。
> - **Y-Cable（Y 形分线器）**：一條线材上有兩個 USB 輸入端、一個輸出端，可以同時接手機（傳輸数据）跟外部電源（供電），是解決 OTG 供電不足最直接的做法。
> - **监听模式（Monitor Mode）**：讓网卡把空氣中飛過的所有無線数据包都抓下來，而不只是接收「要給自己的」数据包，是做無線网络安全分析的基礎模式。

---

## 兼容的 ALFA 网卡型号怎麼選

Kali NetHunter 官方文件（[kali.org/docs/nethunter/wireless-cards/](https://www.kali.org/docs/nethunter/wireless-cards/)）列出了幾款官方支援的 ALFA 网卡，各自的供電需求不同：

| ALFA 型号        | 内核芯片              | 支援频段            | 供電建議                |
| -------------- | ----------------- | --------------- | ------------------- |
| **AWUS036ACH** | Realtek RTL8812AU | 2.4 GHz + 5 GHz | 功率較高，**建議搭配 Y-Cable 外接供電** |
| **AWUS036NEH** | Ralink RT3070     | 2.4 GHz         | 手機 OTG 直接供電即可，不需要額外接線 |
| **AWUS036NHA** | Atheros AR9271    | 2.4 GHz         | 手機 OTG 直接供電即可，不需要額外接線 |
| **AWUS036ACM** | MediaTek MT7612U  | 2.4 GHz + 5 GHz | 功率中等，建議準備 Y-Cable 以求穩定 |

**簡單判斷方式**：只要你選的是雙頻（2.4 + 5 GHz）且信号較強的機型（AWUS036ACH、AWUS036ACM），就準備一條 Y-Cable；如果是單純 2.4 GHz 的入門機型（AWUS036NEH、AWUS036NHA），手機直接供電通常就夠了。

---

## 你需要準備的東西

- [ ] **硬件**：已安裝好 Kali NetHunter 的 Android 手機
- [ ] **ALFA 無線网卡**：依上一節選擇合適型号
- [ ] **USB OTG Y-Cable**：如果你選的是高功率型号（AWUS036ACH / ACM），務必準備
- [ ] **充电宝或外部電源**：搭配 Y-Cable 使用，提供网卡額外供電
- [ ] **驱动程序參考（GitHub）**：
  - Realtek RTL8812AU 驱动（適用 AWUS036ACH）：https://github.com/aircrack-ng/rtl8812au
  - MediaTek MT76 系列驱动（適用 AWUS036ACM）：https://github.com/morrownr/mt76
- [ ] **Kali NetHunter 官方專案**：目前官方原始碼已搬遷到 GitLab（不是 GitHub），如需查閱原始碼或回報問題請至：https://gitlab.com/kalilinux/nethunter

---

## Step-by-Step 设置教學

### 步骤 1：用 Y-Cable 正確接線

1. 把 Y-Cable 其中一個輸入端接上手機的 USB 埠。
2. 另一個輸入端接上充电宝或外部電源（負責供電）。
3. 輸出端接上 ALFA 网卡。

> ⚠️ **供電提醒**：如果你跳過 Y-Cable，直接把高功率网卡插在手機上，很可能會遇到手機重开机或网卡反覆斷線的狀況——這不是设置問題，是供電不足，回到這一步接好线材即可解決。

---

### 步骤 2：驗證硬件辨識

打開 NetHunter Terminal（Root 模式），輸入：

```bash
lsusb
```

**預期結果**：清单裡應該會出現你的 ALFA 网卡型号資訊，代表手機已經正確辨識到這張网卡。

再檢查無線接口是否出現：

```bash
iwconfig
# 或
ip link show
```

**預期結果**：應該會看到一個新的無線接口（通常是 `wlan1`），代表网卡已經可以被系統使用。如果 Realtek 芯片的機型（如 AWUS036ACH）沒有出現，代表可能需要先確認 NetHunter 内核是否已包含對應驱动——可以參考文末的第四節「進階：自訂内核注意事項」。

---

### 步骤 3：啟動监听模式並進行数据包稽核

```bash
# 1. 終止可能干扰的系統服務
airmon-ng check kill

# 2. 開啟监听模式（假設网卡接口為 wlan1）
airmon-ng start wlan1

# 3. 驗證 monitor 接口（通常會變成 wlan1mon）
iwconfig wlan1mon
```

**預期結果**：`iwconfig wlan1mon` 應該會顯示 `Mode:Monitor`，代表监听模式已經成功啟用。

接著可以啟動自動化的無線安全稽核工具進行測試：

```bash
wifite -i wlan1mon
```

**預期結果**：`wifite` 會開始扫描附近的無線网络，列出偵測到的基地台清单。

---

## 進階：自訂内核注意事項（選讀）

這一段只有在你使用的是**非官方預编译 NetHunter 内核的自訂 ROM** 時才需要參考，一般直接使用官方預编译内核的讀者可以跳過這一節。

如果你需要自己编译内核，記得啟用以下设置項目，才能正確支援無線网卡：

```ini
CONFIG_NET_RADIO=y
CONFIG_WIRELESS_EXT=y
CONFIG_WEXT_PRIV=y
CONFIG_CFG80211=m
CONFIG_MAC80211=m
CONFIG_CFG80211_WEXT=y

# RTL8812AU 驱动模块（AWUS036ACH 適用）
CONFIG_RTL8812AU=m

# Ralink / Atheros 內建驱动（AWUS036NEH / AWUS036NHA 適用）
CONFIG_RT2800USB=m
CONFIG_ATH9K_HTC=m
```

---

## 常見問題與排除指引

### Q1：接上网卡後手機直接重开机？
- **原因**：手機 OTG 供電不足（上限約 500mA），高功率网卡瞬間需求超過這個上限。
- **解決方法**：改用 Y-Cable 搭配外部電源供電（見步骤 1），不要讓手機獨自負擔网卡的全部供電。

### Q2：`lsusb` 看不到我的网卡？
- **原因**：接線方式錯誤，或是 Y-Cable 本身的数据傳輸端沒有正確接到手機。
- **解決方法**：確認 Y-Cable 的兩端沒有接反——負責数据傳輸的一端要接手機，負責供電的一端接電源；也可以換一條 Y-Cable 測試排除线材本身的問題。

### Q3：Realtek 芯片的网卡（AWUS036ACH）辨識不到？
- **原因**：目前使用的 NetHunter 内核可能沒有內建 RTL8812AU 驱动。
- **解決方法**：確認你安裝的是官方支援該网卡的 NetHunter 内核版本；如果你是自行编译内核，請參考上方「進階：自訂内核注意事項」章節，確認有勾選對應的驱动選項。

### Q4：监听模式啟用後信号斷斷續續？
- **原因**：通常還是供電不穩，或者是天線位置不佳。
- **解決方法**：優先確認供電是否穩定（Y-Cable 接線、電源容量足夠）；也可以嘗試調整网卡天線的角度與位置。

---

## 參考数据與延伸閱讀

- [AWUS036ACH 產品頁面](/alfa-network/products/awus036ach/)
- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [ALFA 無線网卡在 NetHunter（Android）上——OTG 设置指南](/alfa-network/linux-setup-nethunter)
- [ALFA 無線网卡在 Kali Linux 上——监听模式與数据包注入](/alfa-network/linux-setup-kali/)
- [詞彙表](/getting-started/glossary)——OTG、监听模式等名詞的完整解釋
- Realtek RTL8812AU 驱动（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au
- MediaTek MT76 系列驱动（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- [Kali NetHunter 官方無線网卡兼容清单](https://www.kali.org/docs/nethunter/wireless-cards/)
- Kali NetHunter 官方專案（已搬遷至 GitLab）：https://gitlab.com/kalilinux/nethunter

**標籤：** `kali` `nethunter` `android` `otg` `alfa` `awus036ach` `rtl8812au` `monitor-mode` `新手指南`
