---
title：「Hak5 Screen Crab 原廠技術說明書與全功能操作手冊」
model：「Screen Crab」
manufacturer：「Hak5」
category：「HDMI 視訊中間人側錄植入裝置」
docs_url：「https://docs.hak5.org/screen-crab/」
version：「2.0」
locale：「zh-tw」
---

# Hak5 Screen Crab 原廠技術說明書與全功能操作手冊

> Hak5 Screen Crab 是一款極度隱蔽的 HDMI 視訊中間人（Video Man-in-the-Middle）側錄與串流植入硬體。串接於主機與螢幕之間，安靜擷取高解析度畫面截圖，並支援 2.4 GHz Wi-Fi 與 Hak5 Cloud C² 雲端帶外回傳。

---

## 目錄

- [**1. 產品概述與硬體架構**](#1-產品概述與硬體架構)
  - [1.1 Screen Crab 原廠介紹](#1-1-screen-crab-原廠介紹)
  - [1.2 運作架構與核心原理 (Screen Crab Basics)](#1-2-運作架構與核心原理-screen-crab-basics)
- [**2. 組態設定、Cloud C² 與操作模式**](#2-組態設定-cloud-c-與操作模式)
  - [2.1 組態設定檔解析 (Configuring the Screen Crab)](#2-1-組態設定檔解析-configuring-the-screen-crab)
  - [2.2 LED 狀態指示燈號診斷 (LED Status Indications)](#2-2-led-狀態指示燈號診斷-led-status-indications)
  - [2.3 Hak5 Cloud C² 雲端連線設定 (Configuring Cloud C²)](#2-3-hak5-cloud-c-雲端連線設定-configuring-cloud-c)
  - [2.4 2024 SSL 憑證安全更新 (2024 SSL Update)](#2-4-2024-ssl-憑證安全更新-2024-ssl-update)
- [**3. 硬體規格、安全性指南與故障排除**](#3-硬體規格安全性指南與故障排除)
  - [3.1 重要安全指引與法規聲明 (Safety and Warnings)](#3-1-重要安全指引與法規聲明-safety-and-warnings)
  - [3.2 官方技術規格基準表 (Hardware Specifications)](#3-2-官方技術規格基準表-hardware-specifications)
  - [3.3 常見故障排查指引 (Troubleshooting Guide)](#3-3-常見故障排查指引-troubleshooting-guide)

---

## 1. 產品概述與硬體架構

<!-- section：overview -->
### 1.1 Screen Crab 原廠介紹

Hak5 Screen Crab 是一款專為紅隊滲透測試、硬體安全稽核與系統管理員設計的隱蔽型 HDMI 視訊中間人植入裝置。

裝置本體串接於任何標準 HDMI 輸出源（例如工作站電腦、伺服器、KVM 切換器、視訊遊樂主機）與顯示裝置（例如液晶螢幕、投影機、電視）之間。在運作期間，Screen Crab 完全保持直通（Passthrough），目標端使用者與受測主機完全無法察覺任何延遲或畫質降階。

裝置在內部並聯擷取視訊畫面訊號，根據預設的時間間隔自動截取高畫質螢幕截圖，並可儲存於本機 MicroSD 記憶卡，或透過內建 Wi-Fi 天線即時將圖片加密傳輸至 Hak5 Cloud C² 雲端伺服器。

### 硬體技術規格與原廠校準基準表

| 硬體元件專案 | 官方技術規格說明 |
|---|---|
| **視訊直通介面 (Video Interface)** | HDMI 輸入 / 輸出（支援解析度最高達 1080 p @ 60 fps）|
| **無線傳輸模組 (Wireless)** | 2.4 GHz 802.11 b/g/n，提供帶外（Out-of-Band）隱蔽回傳 |
| **本機儲存介面 (Storage)** | MicroSD 記憶卡插槽（相容 FAT32 與 exFAT，容量最高支援 128 GB）|
| **供電介面 (Power)** | USB Type-C 5 V DC 供電 |
| **音訊側錄功能 (Audio Capture)** | 支援 HDMI PCM 內嵌音訊旁路側錄分析 |
| **狀態指示模組** | 多色 RGB 狀態診斷 LED 指示燈 |

---

<!-- section：features -->
### 1.2 運作架構與核心原理 (Screen Crab Basics)

Screen Crab 採用實體層直通訊號分流架構，其核心特點包含：
1. **無驅動程式需求**：在目標作業系統內完全不產生任何 USB 或 PCI 裝置識別碼，對目標主機而言完全透明。
2. **EDID 智慧模擬與複製**：自動轉發顯示器原生 EDID 參數，確保目標系統輸出最佳解析度，無解析度突波或閃爍。
3. **靈活觸發機制**：支援定時截圖、動態偵測畫面變更、或遠端 C2 指令即時手動截圖。
4. **影像壓縮引擎**：內建硬體 JPEG 編碼器，可在毫秒級別完成高解析度影像壓縮並寫入儲存裝置。

---

<!-- section：configuration -->
## 2. 組態設定、Cloud C² 與操作模式

### 2.1 組態設定檔解析 (Configuring the Screen Crab)

Screen Crab 的所有運作參數均記錄於 MicroSD 卡根目錄下的 `config.txt` 文字檔案中。使用文字編輯器即可完成全功能組態設定：

```ini
# Screen Crab 主要設定檔範例
# 截圖模式：INTERVAL（定時）或 MANUAL（手動）
CAPTURE_MODE=INTERVAL

# 截圖間隔時間（單位：秒）
INTERVAL=30

# 影像畫質設定（1-100）
QUALITY=85

# Wi-Fi 連線設定（選填，供 Cloud C2 雲端回傳使用）
WIFI_SSID=MyCorporateWiFi
WIFI_PASS=SecurePassword123

# Cloud C2 註冊連線檔存放於 MicroSD 根目錄：device.config
```

---

### 2.2 LED 狀態指示燈號診斷 (LED Status Indications)

Screen Crab 具備多色 RGB 狀態指示燈，開機後將依序呈現系統各階段狀態：

| 燈號狀態 | 意義說明 | 操作建議 |
|---|---|---|
| **綠燈恆亮** | 正常運作中，截圖正常執行 | 設備處於就緒狀態 |
| **綠燈閃爍** | 正在擷取當前畫面並寫入儲存媒體 | 正在進行 I/O 操作 |
| **藍燈閃爍** | Wi-Fi 正在嘗試連線中 | 確認 AP 訊號強度與密碼 |
| **藍燈恆亮** | 已成功連線至 Wi-Fi 與 Cloud C² | 雲端通道已建立 |
| **紅燈恆亮** | 錯誤狀態：未偵測到 MicroSD 卡或檔案系統損壞 | 檢查 MicroSD 是否格式化為 FAT32/exFAT |
| **黃燈閃爍** | 未偵測到有效 HDMI 輸入視訊來源 | 檢查訊號線接線順序 |

---

### 2.3 Hak5 Cloud C² 雲端連線設定 (Configuring Cloud C²)

透過整合 Hak5 Cloud C²，安全人員無需回收裝置即可進行即時監視：
1. 登入您的 Cloud C² 伺服器網頁管理介面。
2. 在「Devices」清單中點選「Add Device」，選擇 **Screen Crab**。
3. 下載產生的註冊設定檔 `device.config`。
4. 將 `device.config` 檔案放置於 MicroSD 記憶卡之根目錄。
5. 確保 `config.txt` 中已正確填寫可連外之 Wi-Fi 帳號密碼。
6. 將 Screen Crab 重新上電，裝置將自動連線並在 Cloud C² 儀表板上顯示「Online」，提供即時畫面串流瀏覽。

---

<!-- section：maintenance -->
### 2.4 2024 SSL 憑證安全更新 (2024 SSL Update)

> [!IMPORTANT]
> 針對 2024 年之後的 Cloud C² 雲端通訊，官方實施了全新的 TLS/SSL 憑證鏈路驗證標準。若設備出廠年份較早，請務必依原廠指南將更新的 root CA 憑證複製至 MicroSD 卡，以確保 HTTPS/WSS 加密通道不因憑證過期而中斷。

---

## 3. 硬體規格、安全性指南與故障排除

### 3.1 重要安全指引與法規聲明 (Safety and Warnings)

1. **合法授權原則**：Screen Crab 僅供具備完整書面授權之紅隊滲透測試、資安演練或企業自建網路環境安全檢驗之用。
2. **散熱與散熱通風**：視訊處理晶片在 1080 p 60 fps 連續編碼時會產生正常運作熱量，請確保設備周圍保留通風空間，切勿緊貼密閉高溫管線。
3. **電壓保護**：僅限使用合格之 5 V USB-C 供電源，避免使用具備非標準高壓快充協定之變壓器。

---

### 3.2 官方技術規格基準表 (Hardware Specifications)

- **處理架構**：專屬高頻視訊處理晶片
- **解析度相容性**：1080 p (1920x1080)、720 p (1280x720)、480 p 等標準數位視訊模式
- **儲存規格**：MicroSD 擴充槽，最高支援 128 GB
- **外殼設計**：消光黑隱蔽式小巧鋁合金外殼
- **耗電量**：約 5 V @ 500 mA - 800 mA

---

### 3.3 常見故障排查指引 (Troubleshooting Guide)

1. **螢幕無畫面輸出（黑畫面）**：
   - 確認 HDMI IN 與 HDMI OUT 方向是否接反（主機應接 IN，螢幕接 OUT）。
   - 檢查 USB-C 供電線是否有足夠 5 V 電流。
2. **截圖皆為全黑或雜訊**：
   - 目標設備可能啟用了 HDCP 數位內容保護機制。Screen Crab 遵循標準消費級規範，若訊號受 HDCP 保護將無法截圖。
3. **MicroSD 卡讀不到**：
   - 使用 SD Card Formatter 工具重新將記憶卡格式化為 FAT32 或 exFAT。
