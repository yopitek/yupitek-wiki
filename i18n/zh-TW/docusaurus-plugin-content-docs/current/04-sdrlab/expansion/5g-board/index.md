---
title: Flipper Zero 5G 擴充板 — 完整指南
source_url: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/
revision: 2026-10-03
status: 待上架確認稿（稽核紀錄另存 audit_wiki.md，不含在此檔）
---

# Flipper Zero 5G 擴充板 — 完整指南

> **一句話**：5G 擴充板把雙頻 **2.4GHz + 5GHz Wi-Fi** 工具裝到你的 Flipper Zero 上 — 一顆 ESP32-C5 跑 Marauder 韌體，加上 GPS 接收器、2.8 吋螢幕與內建電池，全部整合在一個小模組裡。

---

## 規格概覽

| 項目 | 規格 |
|---|---|
| **Wi-Fi 模組** | **ESP32-C5**（2.4GHz + 5GHz），出廠預燒 Marauder 5G 韌體 |
| **Sub-GHz** | **433MHz** A07 射頻模組，**10 dBm** 輸出（需在 Flipper 設為 External） |
| **GPS** | 內建 GPS 模組，可由 Flipper 或板上電池供電 |
| **螢幕** | **2.8 吋彩色 TFT**，內建 Marauder UI |
| **電池** | **800 mAh** 電池；充飽電後充電指示燈熄滅 |
| **天線** | SMA 接頭；隨附雙頻 Wi-Fi 天線（3 dBi）、GPS 天線（20 dBi）、433MHz 天線（3 dBi） |
| **microSD** | **FAT32 格式** — 抓包存 `.pcap`，wardrive 存 `wardrive_*.csv` |
| **保護** | 所有腳位鍍金，每個訊號腳內建 **TVS** 保護元件 |
| **燒錄** | USB-C 埠（前左側）；按住背面按鍵再插入 USB 進入燒錄模式 |
| **操作** | Flipper Zero 應用程式：`[ESP32] WiFiMarauder`、`GPS` |
| **連接** | Flipper Zero GPIO 排針 |
| **藍牙** | **BLE（Bluetooth LE）** ⚠️ 不支援 Bluetooth Classic |

### 天線

本板使用 SMA 天線接頭。廠商列出的隨附天線共三支：雙頻 Wi-Fi 天線（3 dBi，無須區分頻段）、GPS 天線（20 dBi）與 433MHz 天線（3 dBi）。請依板上標示將天線接到對應接頭。

---

## 這塊板子能用來做什麼

ESP32-C5 是 Wi-Fi 的主力：搭配 **Marauder 韌體**可以掃描 AP 與客戶端、嗅探 beacon 與 probe request、執行 deauth 與 PMKID 擷取測試，並記錄 Wi-Fi 活動 — **現在包含 5GHz 網路，這是舊 ESP32 板看不到的**。

GPS 模組把你的 wardrive 記錄變成帶座標的資料。內建電池讓 Wi-Fi 側不必一直吃 Flipper 的電，也可以脫離 Flipper 單機運作。

433MHz Sub-GHz 模組讓你可以從 Flipper Zero 的 Sub-GHz 選單操作 433MHz 訊號研究 — 對 Flipper 內建收訊不良的環境特別有用。

> **請只在你自己的網路與設備上使用。** Deauth 與 probe 嗅探會干擾他人，且在多數國家受管制。這是實驗／教學工具。

---

## 開始之前

- Flipper 需要**含 WiFi Marauder 與 GPS 應用的客製韌體** — 例如 **Momentum**。（韌體基礎見 [Flipper Zero 章節](/flipper-zero/)。）
- **本板已內建** 433MHz Sub-GHz 模組、2.8 吋 Marauder 螢幕、800mAh 電池。
- 準備一張 **FAT32** 格式的 microSD。

---

## 設定：GPIO 腳位（Momentum 韌體）

在 **Momentum** 上：

1. 開啟 `Protocol Settings → GPIO Pin Settings`
2. 將 **GPS Pin** 設為 **13** 或 **14**（UART 腳位）
3. 將 **ESP32 Pin** 設為 **15、16**（與 ESP32-C5 對話的 UART）
4. 離開設定並重新啟動 Flipper

> ⚠️ **GPS 與 ESP32 是兩組不同的 UART 腳位。**
> 本板出廠配置為：GPS = 13／14，ESP32 = 15／16。
> **不可把兩者設成同一組腳位**，否則 GPS 與 Wi-Fi 都會沒有回應。
> 若使用其他韌體，設定路徑可能略有差異，請參照各韌體自身的 GPIO 設定選單。

---

## 使用本板

### WiFi Marauder

1. 裝好本板後，開啟 `Apps → GPIO → [ESP32] WiFiMarauder`
2. 執行 **Scan AP**：附近的 AP 會顯示 SSID、頻道、RSSI、加密方式
3. 執行 **Packet Monitor** 或 **Beacon Sniff** 觀察 beacon／probe 流量
4. **Wardrive**（搭配 GPS）會把記錄輸出為 CSV，之後可匯出分析

掃描結果範例（**僅為示意格式，非實際擷取資料**）：

```
SSID              CH  RSSI  ENC     AUTH
yupitek-lab       6   -55   WPA2    PSK
Campus_Guest      11  -72   OPEN
```

### GPS

1. 接上 GPS 天線，朝向開闊天空方向放置（靠近窗戶可以，戶外更好）
2. 開啟 `Apps → GPIO → GPS`，等待 — **首次定位需數分鐘（冷啟動）**
3. 衛星定位後位置資料就會進來。搭配 Marauder 即可取得帶座標的 Wi-Fi 記錄

> ℹ️ GPS 時間固定回報 **UTC+0**。台灣時間（UTC+8）請自行加 8 小時。韌體選單沒有時區設定選項。

### 433MHz Sub-GHz

1. `Flipper Zero → Sub-GHz → Advanced Settings → Module`
2. 改為 **External**
3. 從 Sub-GHz 選單使用 433MHz 頻段

> 不做這一步，Flipper 會繼續使用內建的 CC1101，本板的 433MHz 模組不會被啟用。

### microSD 記錄

1. 將 microSD 格式化為 **FAT32**（**不支援 exFAT／NTFS**）
2. 插入機身記憶卡槽
3. 在模組內 `Device → Settings` 確認 **PCAP saving 已開啟**
4. 擷取結果存為 `.pcap`（用 [Wireshark](https://www.wireshark.org) 開啟）；wardrive 另存 `wardrive_*.csv`

---

## 更新 ESP32-C5 韌體

本板出廠**已預燒 Marauder 5G**，正常情況下不需要重新燒錄。

若確實需要更新，請先向原廠或經銷商索取**本板專用**的韌體檔案與版本號後再進行 — 開源 Marauder 釋出頁的通用 ESP32-C5 版本是否完全相容本板的螢幕、SD 卡、GPS 與腳位配置，目前尚待原廠確認，請勿直接套用未經確認的版本，以免造成裝置無法開機。

### 進入燒錄模式（USB-C）

1. 按住背面按鍵
2. 保持按住的同時插入 USB-C 線（前左側燒錄埠）
3. 使用確認支援 **ESP32-C5** 的燒錄工具燒入韌體
4. 拔線、重開 Flipper Zero

> ⚠️ 燒錄前請確認所用工具支援 ESP32-C5 晶片；不確定時請以原廠／經銷商提供的說明為準。

---

## 疑難排解

| 問題 | 原因 | 解法 |
|---|---|---|
| 應用程式顯示「no module」 | GPIO 腳位未設定 | 重新檢查 `GPIO Pin Settings`；重新啟動 Flipper |
| 掃不到任何網路 | ESP32 UART 腳位設錯 | 設定 ESP32 Pin 為 **15、16**；重新啟動 |
| 5GHz 網路看不到或掃描不穩定 | 可能為韌體版本相關限制 | 以掃描／監測為主；建議至 [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) 查詢目前版本狀態 |
| 5GHz deauth 沒反應 | 已知韌體限制 | 2.4GHz 較成熟穩定，建議優先使用 |
| GPS 一直無法定位 | 天線未接／室內／未滿足定位時間 | 接上 GPS 天線、朝向開闊天空、走到戶外或窗邊，等待數分鐘完成冷啟動 |
| 模組有電但 Flipper 沒反應 | Flipper 韌體沒有對應應用程式 | 安裝含 WiFi Marauder／GPS 應用的客製韌體（例如 Momentum） |
| SD 卡無法辨識 | 格式不符 | 必須 FAT32；重新格式化 |
| 沒有 PCAP 檔 | PCAP 儲存未開啟 | `Device → Settings` 開啟 PCAP saving |
| 開機時模組沒反應 | GPIO 連接器未完全密合 | 輕壓至 flush；確認電池有電或已接 USB-C |

更多協助：見 [SDRLAB 疑難排解中心](/sdrlab/troubleshooting/)。

---

## 已知限制

- **5GHz Deauth 的穩定度取決於韌體版本。** 開源 Marauder 韌體在 ESP32-C5 上的 5GHz deauth 支援仍在持續改進，建議以 2.4GHz 進行 deauth 測試為主；5GHz 建議以掃描、訊號監測、wardrive 記錄為主要用途。使用前建議至 [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) 確認當前版本狀態。
- **5GHz PMKID／EAPOL 可用性尚無定論。** 建議自行實測後再據以宣稱支援與否。
- **microSD 僅 FAT32**，不支援 exFAT、NTFS。
- **藍牙僅 BLE**，ESP32-C5 無 Bluetooth Classic（BR/EDR）。
- **兩個 USB-C 埠功能不同** — 上緣前面為充電埠；前左側為 ESP32-C5 燒錄埠。

---

## 相關頁面

- [WiFi multiboard（ESP32-S2）](/sdrlab/expansion/wifi-multiboard/) — 僅 2.4GHz 的小弟弟
- [NRF24 模組](/sdrlab/expansion/nrf24/) — 2.4GHz 封包無線電嗅探
- [Flipper Zero 章節](/flipper-zero/) — 基礎韌體與裝置說明

**標籤**：`sdrlab` · `flipper-zero` · `5g-board` · `esp32-c5` · `marauder` · `gps`
