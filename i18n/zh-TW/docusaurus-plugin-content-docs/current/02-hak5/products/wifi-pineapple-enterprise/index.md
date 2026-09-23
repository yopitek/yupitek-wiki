---
title: "Hak5 WiFi Pineapple Enterprise 原廠技術說明書與全功能操作手冊"
model: "WiFi Pineapple Enterprise"
manufacturer: "Hak5"
category: "企業級無線安全稽核與流氓 AP 測試平台"
docs_url: "https://docs.hak5.org/wifi-pineapple-enterprise/"
version: "2.0"
locale: "zh-tw"
---

# Hak5 WiFi Pineapple Enterprise 原廠技術說明書與全功能操作手冊

> Hak5 WiFi Pineapple Enterprise 是專為大型企業環境、金融機構與政府機關設計的機架式/桌面型無線安全稽核設備。配備多核心高速網路處理器、Gigabit 乙太網路與 SFP 連接埠、高功率雙頻併發射頻晶片陣列與 MIMO 天線系統，支援大規模即時頻譜監聽、自動化 Campaigns 任務與雲端集中管理。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 WiFi Pineapple Enterprise 原廠介紹](#1-1-wifi-pineapple-enterprise-原廠介紹)
  - [1.2 企業級硬體技術規格與校準基準表](#1-2-企業級硬體技術規格與校準基準表)
- [**2. 初次設定、實體接線與網路共用**](#2-初次設定實體接線與網路共用)
  - [2.1 實體連接與機架部署指引 (Physical Connections)](#2-1-實體連接與機架部署指引-physical-connections)
  - [2.2 初始設定精靈與帳號初始化 (Setting up)](#2-2-初始設定精靈與帳號初始化-setting-up)
  - [2.3 企業網路環境連線設定 (Linux / Windows / Wi-Fi)](#2-3-企業網路環境連線設定-linux--windows--wi-fi)
  - [2.4 USB 隨身碟離線自動部署 (Setup by USB Disk)](#2-4-usb-隨身碟離線自動部署-setup-by-usb-disk)
- [**3. Web UI 圖形化介面、Recon、PineAP 與 Cloud C²**](#3-web-ui-圖形化介面 reconpineap-與-cloud-c)
  - [3.1 Web UI 企業控制台架構 (Introduction to the UI)](#3-1-web-ui-企業控制台架構-introduction-to-the-ui)
  - [3.2 儀表板資源監控與即時狀態 (Dashboard)](#3-2-儀表板資源監控與即時狀態-dashboard)
  - [3.3 Campaigns 企業級自動化作戰任務 (Campaigns)](#3-3-campaigns-企業級自動化作戰任務-campaigns)
  - [3.4 PineAP 企業流氓 AP 攻擊引擎 (PineAP)](#3-4-pineap-企業流氓-ap-攻擊引擎-pineap)
  - [3.5 全頻段頻譜偵察與訊號測繪 (Recon)](#3-5-全頻段頻譜偵察與訊號測繪-recon)
  - [3.6 企業 WPA 握手包收集與管理 (Handshakes)](#3-6-企業-wpa-握手包收集與管理-handshakes)
  - [3.7 Hak5 Cloud C² 企業集權納管 (Cloud C²)](#3-7-hak5-cloud-c-企業集權納管-cloud-c)
- [**4. Wi-Fi 基礎理論、射頻技術與 802.11 訊框架構**](#4-wi-fi-基礎理論射頻技術與-80211-訊框架構)
  - [4.1 企業無線通訊底層技術 (Introduction to WiFi)](#4-1-企業無線通訊底層技術-introduction-to-wifi)
  - [4.2 射頻晶片、MIMO 天線與功率規劃](#4-2-射頻晶片 mimo-天線與功率規劃)
  - [4.3 802.11 訊框結構與訊框注入機制 (Frame Injection)](#4-3-80211-訊框結構與訊框注入機制-frame-injection)
- [**5. 常見問題排查、韌體維護與出廠重置**](#5-常見問題排查韌體維護與出廠重置)
  - [5.1 連網故障排查與管理埠診斷](#5-1-連網故障排查與管理埠診斷)
  - [5.2 密碼重置與原廠出廠復原 (Factory Reset)](#5-2-密碼重置與原廠出廠復原-factory-reset)
  - [5.3 韌體線上與離線升級標準作業程序 (Updates)](#5-3-韌體線上與離線升級標準作業程序-updates)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 1.1 WiFi Pineapple Enterprise 原廠介紹

WiFi Pineapple Enterprise 是 Hak5 專為大規模企業環境安全評估打造的高效能無線安全設備。

相較於便攜型產品，Enterprise 版本專注於持續性的全天候監控與高負載無線滲透測試。具備企業級多核心處理器、多組 Gigabit 乙太網路與高速光纖介面、高靈敏度 MIMO 天線陣列，可無死角監聽園區內的所有無線頻段，即時發現未經授權的個人熱點、影子 Wi-Fi 以及潛在的無線網路入侵行為。

### 1.2 企業級硬體技術規格與校準基準表

| 硬體元件專案 | 原廠官方技術規格說明 |
|---|---|
| **機身規格架構** | 企業級機架式 / 桌面型金屬散熱機身 |
| **處理器規格 (CPU)** | 高效能多核心網路處理器 SoC |
| **系統記憶體 (RAM)** | 大容量高速 DDR4 記憶體 |
| **網路連接介面** | 多組 Gigabit 乙太網路 RJ-45 連接埠與高速 SFP 光纖插槽 |
| **無線射頻模組** | 多組高功率雙頻併發（Dual-Concurrent）企業級無線收發器 |
| **天線設定** | 外接式高增益多天線 MIMO 全向天線陣列 |
| **集中管理支援** | 支援 Hak5 Cloud C² 企業版全生命週期納管 |

---

<!-- section：configuration -->
## 2. 初次設定、實體接線與網路共用

### 2.1 實體連接與機架部署指引 (Physical Connections)

1. 將高增益天線安裝於機身後面板之對應 RP-SMA 接頭。
2. 使用標準網路線將 Management 介面連接至管理交換器或設定電腦。
3. 連接交流電源線並開啟電源開關，確認面板電源指示燈恆亮。

---

### 2.2 初始設定精靈與帳號初始化 (Setting up)

1. 於瀏覽器中開啟 `http://172.16.42.1:1471` 進入 Setup Wizard。
2. 設定強固之 root 管理員密碼與系統主機名稱。
3. 依據企業網段規劃設定靜態 IP 或 DHCP 使用者端模式。

---

### 2.3 企業網路環境連線設定 (Linux / Windows / Wi-Fi)

詳細說明在企業伺服器機房環境下，如何透過 VLAN Tagging、網路介面橋接或 Linux iptables 建立出站網際網路共用通道。

---

### 2.4 USB 隨身碟離線自動部署 (Setup by USB Disk)

將包含組態參數的部署隨身碟插入機身 USB 連接埠，開機時系統將自動讀取並完成初始化設定，大幅簡化大量站點的快速部署難度。

---

<!-- section：features -->
## 3. Web UI 圖形化介面、Recon、PineAP 與 Cloud C²

### 3.1 Web UI 企業控制台架構 (Introduction to the UI)

專為資安運維中心（SOC）設計的直覺式儀表板，提供多維度無線資產視覺化圖表與警報即時通知。

---

### 3.2 儀表板資源監控與即時狀態 (Dashboard)

即時監控 CPU 溫度、記憶體使用量、各射頻模組的工作負載、空中訊框密度與關聯客戶端清單。

---

### 3.3 Campaigns 企業級自動化作戰任務 (Campaigns)

支援排程週期性安全巡檢任務，自動掃描未授權 AP、誘捕影子設備、截獲握手包並自動產出合規性 PDF 稽核報告。

---

### 3.4 PineAP 企業流氓 AP 攻擊引擎 (PineAP)

支援 Beacon Response 智慧回應、SSID Pool 大容量熱點廣播、以及針對企業內部特定 SSID 的定向授權稽核測試。

---

### 3.5 全頻段頻譜偵察與訊號測繪 (Recon)

全面掃描 2.4 GHz 與 5 GHz 頻譜，繪製涵蓋所有頻道之無線電磁環境熱圖，精準標記各設備之 RSSI 訊號強度。

---

### 3.6 企業 WPA 握手包收集與管理 (Handshakes)

自動攔截與分析 WPA2-Enterprise 與 WPA3 驗證流程，支援將握手包集中歸檔並透過 API 匯出至後端密碼雜湊叢集破解。

---

### 3.7 Hak5 Cloud C² 企業集權納管 (Cloud C²)

將園區內部署的所有 Enterprise 設備統一綁定至 Hak5 Cloud C² 雲端伺服器，實現跨分部、跨廠區的單一管理窗格。

---

## 4. Wi-Fi 基礎理論、射頻技術與 802.11 訊框架構

### 4.1 企業無線通訊底層技術 (Introduction to WiFi)

深度探討 802.11 a/b/g/n/ac/ax 標準演進、正交頻分多工（OFDM）調變技術與企業級漫遊協定（802.11 k/v/r）。

---

### 4.2 射頻晶片、MIMO 天線與功率規劃

分析多天線空間串流（Spatial Streams）、波束成形（Beamforming）原理以及企業機房天線佈建之最佳實務。

---

### 4.3 802.11 訊框結構與訊框注入機制 (Frame Injection)

解析 Management、Control 與 Data 訊框之欄位定義，並說明高負載訊框注入與 Deauthentication 斷線攻擊之防禦機制。

---

<!-- section：maintenance -->
## 5. 常見問題排查、韌體維護與出廠重置

### 5.1 連網故障排查與管理埠診斷

說明管理介面無法存取、DHCP 配發失敗或 SFP 光纖模組未識別之診斷排除步驟。

---

### 5.2 密碼重置與原廠出廠復原 (Factory Reset)

若管理者密碼遺失或系統設定毀損，可透過後面板之實體重置孔進行出廠復原重設。

---

### 5.3 韌體線上與離線升級標準作業程序 (Updates)

支援透過 Web 管理介面自動檢查更新，或於隔離內網環境中透過本地上傳 `.bin` 映像檔完成無痛熱升級。
