---
title: "Hak5 WiFi Pineapple Mark VII 原廠技術說明書與全功能操作手冊"
model: "WiFi Pineapple Mark VII"
manufacturer: "Hak5"
category: "無線網路安全稽核與流氓 AP 測試平台"
docs_url: "https://docs.hak5.org/wifi-pineapple/"
version: "2.0"
locale: "zh-tw"
---

# Hak5 WiFi Pineapple Mark VII 原廠技術說明書與全功能操作手冊

> Hak5 出品的 WiFi Pineapple Mark VII 是全球無線網路安全審計、紅隊滲透測試與流氓 AP（Rogue AP）攻擊演練的業界黃金標準。配備 3 組專屬特化 2.4 GHz 射頻晶片、單核心 MIPS 580 MHz 網路處理器、256 MB 記憶體與 2 GB eMMC 高速儲存，結合專屬 PineAP 攻擊套件與 Campaigns 自動化作戰引擎。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 WiFi Pineapple Mark VII 原廠介紹](#1-1-wifi-pineapple-mark-vii-原廠介紹)
  - [1.2 硬體技術規格與原廠校準基準表](#1-2-硬體技術規格與原廠校準基準表)
- [**2. 初次設定、系統連線與網際網路共用**](#2-初次設定系統連線與網際網路共用)
  - [2.1 實體連接與通電指示 (Connecting)](#2-1-實體連接與通電指示-connecting)
  - [2.2 設定精靈與初始化 (Setting up)](#2-2-設定精靈與初始化-setting-up)
  - [2.3 Linux 系統連線設定指南](#2-3-linux-系統連線設定指南)
  - [2.4 Windows 系統連線設定指南](#2-4-windows-系統連線設定指南)
  - [2.5 透過無線 Wi-Fi 進行無網線設定](#2-5-透過無線-wi-fi-進行無網線設定)
  - [2.6 USB 隨身碟離線自動部署 (Setup by USB Disk)](#2-6-usb-隨身碟離線自動部署-setup-by-usb-disk)
- [**3. Web UI 圖形化介面、Recon、PineAP 與 Cloud C²**](#3-web-ui-圖形化介面 reconpineap-與-cloud-c)
  - [3.1 Web UI 介面架構導覽 (Introduction to the UI)](#3-1-web-ui-介面架構導覽-introduction-to-the-ui)
  - [3.2 儀表板監控與即時狀態 (Dashboard)](#3-2-儀表板監控與即時狀態-dashboard)
  - [3.3 Campaigns 自動化作戰任務 (Campaigns)](#3-3-campaigns-自動化作戰任務-campaigns)
  - [3.4 PineAP 流氓 AP 攻擊引擎核心 (PineAP)](#3-4-pineap-流氓-ap-攻擊引擎核心-pineap)
  - [3.5 Recon 全頻段無線頻譜偵查 (Recon)](#3-5-recon-全頻段無線頻譜偵查-recon)
  - [3.6 Handshake 握手包收集與管理 (Handshakes)](#3-6-handshake-握手包收集與管理-handshakes)
  - [3.7 Modules 擴充模組管理系統 (Modules)](#3-7-modules-擴充模組管理系統-modules)
  - [3.8 系統設定、更新與偏好設定 (Settings)](#3-8-系統設定更新與偏好設定-settings)
  - [3.9 Hak5 Cloud C² 雲端集中納管 (Cloud C²)](#3-9-hak5-cloud-c-雲端集中納管-cloud-c)
- [**4. Wi-Fi 基礎理論、射頻技術與 802.11 訊框架構**](#4-wi-fi-基礎理論射頻技術與-80211-訊框架構)
  - [4.1 無線網路通訊原理 (Introduction to WiFi)](#4-1-無線網路通訊原理-introduction-to-wifi)
  - [4.2 射頻晶片與角色分工 (Radios and Chipsets)](#4-2-射頻晶片與角色分工-radios-and-chipsets)
  - [4.3 Station 與 AP 運作模式剖析](#4-3-station-與-ap-運作模式剖析)
  - [4.4 發射功率與高增益天線原理 (Power & Antennas)](#4-4-發射功率與高增益天線原理-power--antennas)
  - [4.5 頻道劃分與全球區域法規限制](#4-5-頻道劃分與全球區域法規限制)
  - [4.6 802.11 訊框結構與管理訊框解析](#4-6-80211-訊框結構與管理訊框解析)
  - [4.7 訊框注入與客戶端狀態機 (Frame Injection)](#4-7-訊框注入與客戶端狀態機-frame-injection)
- [**5. 開發者資源與自訂模組開發**](#5-開發者資源與自訂模組開發)
  - [5.1 官方開發者資源庫 (Developer Resources)](#5-1-官方開發者資源庫-developer-resources)
  - [5.2 模組架構與社群套件庫貢獻指南](#5-2-模組架構與社群套件庫貢獻指南)
- [**6. 常見問答、故障排除、韌體升級與硬體改裝**](#6-常見問答故障排除韌體升級與硬體改裝)
  - [6.1 macOS 平台連線支援 (macOS Support)](#6-1-macos-平台連線支援-macos-support)
  - [6.2 網際網路共用連線建立與排查](#6-2-網際網路共用連線建立與排查)
  - [6.3 忘記密碼還原與原廠出廠重置 (Factory Reset)](#6-3-忘記密碼還原與原廠出廠重置-factory-reset)
  - [6.4 韌體升級與救援復原模式 (Firmware Recovery)](#6-4-韌體升級與救援復原模式-firmware-recovery)
  - [6.5 相容 802.11 ac 5 GHz 網卡清單 (Compatible Adapters)](#6-5-相容-80211 ac-5-ghz-網卡清單-compatible-adapters)
  - [6.6 MK7 LED 改裝與 Kismet 保護外殼安裝](#6-6-mk7-led-改裝與-kismet-保護外殼安裝)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 1.1 WiFi Pineapple Mark VII 原廠介紹

Hak5 WiFi Pineapple Mark VII 是專為網路安全從業人員、紅隊演練專家以及合規性稽核人員量身打造的第七代旗艦級無線滲透測試硬體。

相較於前代產品，Mark VII 進行了徹底的架構重構，內建 3 組獨立且各司其職的 2.4 GHz 802.11 b/g/n 射頻晶片，實現了同頻段下「一組專職被動頻譜偵察、一組專職流氓 AP 廣播與憑證誘捕、一組專職連線注入與干擾」的三工並行能力，徹底消除了以往單一射頻在切換模式時所造成的頻譜監聽盲區。

配合直覺流暢的 Web UI 與 Hak5 Cloud C² 雲端納管平台，安全團隊可將 Mark VII 隱蔽部署於目標建築物內，並由千里之外的遠端指揮中心進行即時的無線資產測繪與憑證側錄。

### 1.2 硬體技術規格與原廠校準基準表

| 硬體元件專案 | 官方技術規格基準說明 |
|---|---|
| **核心處理器 (SoC / CPU)** | Single Core MIPS 24 KEc 580 MHz |
| **系統記憶體 (RAM)** | 256 MB DDR2 |
| **內部儲存空間 (Storage)** | 2 GB eMMC 高速快閃記憶體 |
| **無線射頻模組** | 3 組獨立特化之 2.4 GHz 802.11 b/g/n 晶片組（硬體濾波防干擾）|
| **擴充連接介面** | USB-C 供電/乙太網路介面、USB 2.0 Host（支援 5 GHz 雙頻擴充）|
| **天線設定** | 3 支高增益全向式 RP-SMA 旋鈕式天線 |
| **狀態指示模組** | 多色可程式化 RGB LED 系統狀態指示燈 |
| **預設管理 IP / 子網路** | 172.16.42.1 / 255.255.255.0 |

---

<!-- section：configuration -->
## 2. 初次設定、系統連線與網際網路共用

### 2.1 實體連接與通電指示 (Connecting)

1. 將隨附的 3 支天線旋緊安裝至 Mark VII 機身上的 RP-SMA 接頭。
2. 使用 USB Type-C 連接線將設備連接至測試電腦或合格之 5 V 2 A 電源供應器。
3. 機身 LED 將亮起藍燈閃爍，代表嵌入式 Linux 作業系統正在啟動（約耗時 30 至 60 秒）。
4. 當 LED 呈現恆亮狀態時，代表系統已開機完成並進入就緒模式。

---

### 2.2 設定精靈與初始化 (Setting up)

1. 開啟瀏覽器，輸入管理位址：`http://172.16.42.1:1471`。
2. 系統將自動導向「Setup Wizard」初次設定精靈。
3. 依序設定 root 管理者密碼、時區以及管理用 Wi-Fi AP 之 SSID 與連線金鑰。
4. 儲存設定後重新載入，即可使用新密碼登入正式管理控制台。

---

### 2.3 Linux 系統連線設定指南

在 Linux 環境下，可使用原廠提供的 `wp7.sh` 設定腳本，一鍵設定 iptables 轉發與網路共用：
```bash
sudo ./wp7.sh
```
選擇對應對外網卡與 USB 網卡介面，腳本將自動建立 NAT 規則，使 Mark VII 具備連外網能力。

---

### 2.4 Windows 系統連線設定指南

在 Windows 10 / 11 中：
1. 進入「網路和共用中心」$ightarrow$「變更介面卡設定」。
2. 在連上網際網路的網卡（Wi-Fi 或乙太網路）上按右鍵選擇「內容」。
3. 切換至「共用」標籤頁，勾選「允許其他網路使用者透過這台電腦的網際網路連線來連線」，並在下拉選單中選擇 WiFi Pineapple 的虛擬乙太網路網卡。

---

### 2.5 透過無線 Wi-Fi 進行無網線設定

在無 USB 連接線的環境下，Mark VII 開機後會自動廣播名為 `Pineapple_xxxx` 的開放式設定 AP。管理員可直接以筆電或手機 Wi-Fi 連入該熱點完成設定。

---

### 2.6 USB 隨身碟離線自動部署 (Setup by USB Disk)

將設定好的 `pineapple.tar.gz` 映像檔放置於 FAT32 格式隨身碟根目錄，插入 Mark VII 開機，系統將全自動完成靜默設定，無需任何人機互動。

---

<!-- section：features -->
## 3. Web UI 圖形化介面、Recon、PineAP 與 Cloud C²

### 3.1 Web UI 介面架構導覽 (Introduction to the UI)

Mark VII 擁有經過徹底美化與響應式設計的現代化管理介面，左側導航欄分為：
- **Dashboard（儀表板）**
- **Campaigns（作戰任務）**
- **PineAP（流氓 AP 核心）**
- **Recon（全頻段偵察）**
- **Modules（擴充模組）**
- **Settings（系統設定）**

---

### 3.2 儀表板監控與即時狀態 (Dashboard)

儀表板即時彙整當前系統資源負載、CPU 使用率、記憶體消耗、網路傳輸量、已關聯客戶端以及當前正在進行的作戰模式。

---

### 3.3 Campaigns 自動化作戰任務 (Campaigns)

Campaigns 功能允許安全專家預先定義複合式作戰情境：
- 定時自動啟動 Recon 掃描周圍 5 分鐘。
- 自動將發現的所有未加密熱點加入 SSID Pool。
- 啟動 PineAP 開放熱點誘捕與憑證釣魚。
- 任務結束後全自動產出專業 PDF / HTML 稽核成果報告。

---

### 3.4 PineAP 流氓 AP 攻擊引擎核心 (PineAP)

PineAP 是 WiFi Pineapple 系列聞名全球的核心引擎：
- **Beacon Response**：監聽客戶端發送的 Probe Request 廣播，並偽裝為該 SSID 予以回應。
- **SSID Pool**：維護動態熱點名稱資料庫，支援以千計之熱點輪播。
- **Karma 攻擊現代演進版**：完美適配現代智慧型手機之隨機 MAC 與加密保護機制。

---

### 3.5 Recon 全頻段無線頻譜偵查 (Recon)

利用獨立的監聽晶片進行全頻道掃描，即時分析各 AP 的頻道佔用度、加密標準（WEP、WPA、WPA2、WPA3-SAE、OWE），並精確捕捉每一個空中封包的訊號強度變化。

---

### 3.6 Handshake 握手包收集與管理 (Handshakes)

支援自動監聽並擷取 WPA/WPA2 4-way Handshake 與 PMKID。捕獲之握手包可於 Web UI 中直接一鍵下載為相容 hashcat 與 John the Ripper 之標準格式。

---

### 3.7 Modules 擴充模組管理系統 (Modules)

透過豐富的社群模組中心，可一鍵安裝 Nmap 網路掃描、Evil Portal 客製化強制入口門戶、DNS 劫持轉向等第三方高階攻擊工具。

---

### 3.8 系統設定、更新與偏好設定 (Settings)

管理 root 密碼、修改主機名、設定時區、調整 LED 燈號顏色以及一鍵備份所有作戰設定。

---

### 3.9 Hak5 Cloud C² 雲端集中納管 (Cloud C²)

將 Mark VII 註冊綁定至企業私有 Cloud C² 伺服器，可在任何具備網際網路的地方，穿越 NAT 與防火牆，實現遠端雲端操作與即時警報接收。

---

## 4. Wi-Fi 基礎理論、射頻技術與 802.11 訊框架構

### 4.1 無線網路通訊原理 (Introduction to WiFi)

深入解析 IEEE 802.11 射頻傳播特性、2.4 GHz 與 5 GHz 頻段衰減差異以及半雙工（Half-Duplex）CSMA/CA 碰撞避免機制。

---

### 4.2 射頻晶片與角色分工 (Radios and Chipsets)

詳細剖析 Mark VII 內部 3 組無線網卡的微架構分工：
- **Radio 0 (wlan0)**：預設負責 AP 廣播與客戶端連線。
- **Radio 1 (wlan1)**：預設作為客戶端外網連線（Client Mode）或二次注入。
- **Radio 2 (wlan2)**：專職被動監聽與 Recon 頻譜偵測。

---

### 4.3 Station 與 AP 運作模式剖析

對比 Station（STA 端點客戶端）與 Access Point（AP 基地台）在空中協調機制中的角色差異。

---

### 4.4 發射功率與高增益天線原理 (Power & Antennas)

說明 dBm 與毫瓦（mW）之轉換公式，以及全向性天線（Omni-directional）在垂直與水平方向之輻射方向圖特性。

---

### 4.5 頻道劃分與全球區域法規限制

比較全球各國（FCC、ETSI、MKK）在 2.4 GHz 頻道（1-11 vs 1-13 vs 14）與發射功率上限（EIRP）的法規差異。

---

### 4.6 802.11 訊框結構與管理訊框解析

詳細拆解 802.11 訊框的三大分類：
1. **管理訊框（Management Frames）**：Beacon、Probe Request/Response、Authentication、Association、Deauthentication。
2. **控制訊框（Control Frames）**：RTS、CTS、ACK。
3. **資料訊框（Data Frames）**：封裝上層 IP 封包之實際載荷。

---

### 4.7 訊框注入與客戶端狀態機 (Frame Injection)

說明原始訊框注入（Raw Frame Injection）的實作機制，以及如何透過發送偽造的 Deauth 管理訊框打斷連線，迫使客戶端重新執行四次握手。

---

## 5. 開發者資源與自訂模組開發

### 5.1 官方開發者資源庫 (Developer Resources)

Hak5 官方提供模組開發 SDK 與前端 API 規範，支援 HTML5、JavaScript 與後端 PHP / Python / Go 撰寫自訂擴充插件。

---

### 5.2 模組架構與社群套件庫貢獻指南

介紹模組目錄結構、`module.info` 設定檔撰寫規範，以及如何透過 GitHub 提交 PR 將自製模組發佈至全球官方套件庫。

---

<!-- section：maintenance -->
## 6. 常見問答、故障排除、韌體升級與硬體改裝

### 6.1 macOS 平台連線支援 (macOS Support)

針對 macOS 系統缺少原生 RNDIS 驅動程式之情況，建議透過 Wi-Fi 連線或使用 HoRNDIS 核心擴充元件進行連線。

---

### 6.2 網際網路共用連線建立與排查

排查無法連外網之常見原因：DNS 設定缺失、預設閘道衝突或本機防火牆阻擋。

---

### 6.3 忘記密碼還原與原廠出廠重置 (Factory Reset)

若忘記 root 密碼：
1. 長按機身底部針孔內之重置按鈕 10 秒以上。
2. LED 呈現快速紅燈閃爍後放開。
3. 設備將自動格式化並恢復出廠預設值。

---

### 6.4 韌體升級與救援復原模式 (Firmware Recovery)

在 Web UI 檢查更新，或在無法正常開機時，長按 Reset 鍵同時上電進入 Web Recovery 模式（預設 IP `192.168.1.1`）手動刷入官方救援映像。

---

### 6.5 相容 802.11 ac 5 GHz 網卡清單 (Compatible Adapters)

支援透過 USB 2.0 Host 介面外接原廠 **MK7 AC** 雙頻無線網卡（採用 MediaTek MT7610 U 晶片），立即為 Mark VII 賦予 5 GHz 802.11 ac 頻段的偵查與注入能力。

---

### 6.6 MK7 LED 改裝與 Kismet 保護外殼安裝

詳細圖解官方 Kismet 外殼安裝步驟，最佳化內部被動散熱並支援額外外接散熱風扇模組。
