---
title: "Hak5 Key Croc 原廠技術說明書與全功能操作手冊"
model: "Key Croc"
manufacturer: "Hak5"
category: "硬體滲透測試 / HitM 植入裝置"
docs_url: "https://docs.hak5.org/key-croc/"
version: "1.3"
locale: "zh-tw"
---

# Hak5 Key Croc 原廠技術說明書與全功能操作手冊

> Hak5 Key Croc 是一款偽裝為標準 USB 串接轉接頭的高階硬體按鍵記錄與注入植入裝置。內部搭載嵌入式 Linux 作業系統，支援即時關鍵字模式匹配、帶外無線資料回傳與多向量攻擊向量。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 Key Croc 原廠介紹 (The Key Croc by Hak5)](#1-1-key-croc-原廠介紹-the-key-croc-by-hak5)
- [**2. 操作模式與初始設定**](#2-操作模式與初始設定)
  - [2.1 Key Croc 基礎架構 (Key Croc Basics)](#2-1-key-croc-基礎架構-key-croc-basics)
  - [2.2 序列埠主控台存取 (Serial Console Access)](#2-2-序列埠主控台存取-serial-console-access)
  - [2.3 韌體升級指引 (Updating the Firmware)](#2-3-韌體升級指引-updating-the-firmware)
  - [2.4 原廠出廠重置 (Factory Reset)](#2-4-原廠出廠重置-factory-reset)
- [**3. 設備設定與鍵盤語言映射**](#3-設備設定與鍵盤語言映射)
  - [3.1 核心組態設定 (Configuration)](#3-1-核心組態設定-configuration)
  - [3.2 原廠預設值 (Default Settings)](#3-2-原廠預設值-default-settings)
  - [3.3 鍵盤語言與掃描碼解析 (Understanding Languages)](#3-3-鍵盤語言與掃描碼解析-understanding-languages)
- [**4. 檔案系統架構與目錄結構**](#4-檔案系統架構與目錄結構)
  - [4.1 檔案與目錄結構 (Files and Directory Structure)](#4-1-檔案與目錄結構-files-and-directory-structure)
  - [4.2 檔案系統深入剖析 (Understanding the File System)](#4-2-檔案系統深入剖析-understanding-the-file-system)
- [**5. 網路連線與遠端 Cloud C² 運作**](#5-網路連線與遠端-cloud-c-運作)
  - [5.1 讓 Key Croc 連線上網 (Getting the Key Croc Online)](#5-1-讓-key-croc-連線上網-getting-the-key-croc-online)
  - [5.2 設定 Hak5 Cloud C² (Configuring Cloud C²)](#5-2-設定-hak5-cloud-c-configuring-cloud-c)
- [**6. 酬載開發與 Ducky Script 指令集**](#6-酬載開發與-ducky-script-指令集)
  - [6.1 酬載開發基礎 (Payload Development)](#6-1-酬載開發基礎-payload-development)
  - [6.2 Ducky Script 語法架構 (Ducky Script Commands)](#6-2-ducky-script-語法架構-ducky-script-commands)
  - [6.3 常用指令快速速查表 (Command Quick Reference)](#6-3-常用指令快速速查表-command-quick-reference)
  - [6.4 MATCH 觸發匹配指令 (The MATCH Command)](#6-4-match-觸發匹配指令-the-match-command)
  - [6.5 SAVEKEYS 日誌儲存指令 (The SAVEKEYS Command)](#6-5-savekeys-日誌儲存指令-the-savekeys-command)
  - [6.6 ATTACKMODE 攻擊模式指令 (The ATTACKMODE Command)](#6-6-attackmode-攻擊模式指令-the-attackmode-command)
  - [6.7 USB 識別碼與硬體克隆 (USB Identifiers & Hardware ID Cloning)](#6-7-usb-識別碼與硬體克隆-usb-identifiers--hardware-id-cloning)
  - [6.8 QUACK 按鍵序列注入指令 (The QUACK Command)](#6-8-quack-按鍵序列注入指令-the-quack-command)
  - [6.9 進階 QUACK 擴充語法 (Advanced QUACK Commands)](#6-9-進階-quack-擴充語法-advanced-quack-commands)
  - [6.10 LED 狀態指示燈語法 (The LED Command)](#6-10-led-狀態指示燈語法-the-led-command)
- [**7. 進階實戰指南、技巧與實用範例**](#7-進階實戰指南技巧與實用範例)
  - [7.1 Key Croc 密碼嗅探實戰 (Password Sniffing with the Key Croc)](#7-1-key-croc-密碼嗅探實戰-password-sniffing-with-the-key-croc)
  - [7.2 Key Croc 1.3 新增功能深度解析 (New Features in Key Croc 1.3)](#7-2-key-croc-1-3-新增功能深度解析-new-features-in-key-croc-1-3)
  - [7.3 互動式酬載開發與除錯 (Interactive Payload Development)](#7-3-互動式酬載開發與除錯-interactive-payload-development)
  - [7.4 安裝額外工具（如 Metasploit）(Installing Extras like Metasploit)](#7-4-安裝額外工具如-metasploit-installing-extras-like-metasploit)
  - [7.5 高頻實用酬載程式碼片段 (Helpful Payload Snippets)](#7-5-高頻實用酬載程式碼片段-helpful-payload-snippets)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 硬體技術規格與原廠校準基準表

| 硬體元件名稱 | 原廠技術規格說明 |
|---|---|
| **核心處理器 (SoC)** | Quad-core ARM Cortex processor @ 1.2 GHz |
| **系統記憶體 (RAM)** | 512 MB DDR3 RAM |
| **內部儲存空間** | 8 GB SSD 高速快閃記憶體 |
| **無線通訊介面** | 2.4 GHz 802.11 b/g/n，內建高感度陶瓷天線 |
| **實體連接埠 (USB)** | USB-A 公頭（上游連接主機）/ USB-A 母座（下游連接鍵盤）|
| **機身外型尺寸** | 74 mm × 27 mm × 14 mm |
| **工作電源需求** | USB 匯流排供電（5 V DC，最大約 1 A）|
| **狀態指示燈** | 多色可程式化 RGB LED（攻擊模式下預設完全熄滅）|
| **硬體控制開關** | 機身底部針孔內隱藏式維護模式按鈕（需退卡針觸發）|
| **預設序列埠鮑率** | 115200 |
| **預設 SSH 登入憑證** | 使用者名稱：root / 密碼：hak5 croc |
| **預設網路 IP 位址** | 172.16.32.1 |

---

<!-- section：overview -->
### 1.1 Key Croc 原廠介紹 (The Key Croc by Hak5)

Key Croc 是一款具備模式匹配酬載系統與遠端雲端管理能力的智慧型鍵盤側錄與滲透測試植入裝置。本文檔涵蓋硬體運作與部署基礎、透過 Linux Shell 主控台進行高階滲透測試、Wi-Fi 網路連線設定、韌體升級維護以及 DuckyScript 酬載開發工程。

![Key Croc](https://212197980-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2 F-MhLOzjhonMdC6SLKqRt%2Fuploads%2F5ZxTlaKQGYZ03j3E4 bah%2Fkeycroc%400.5 x.png?alt=media&token=e7d21d21-bfcd-41c4-b1b6-99f8b6cb8295)

> [!WARNING]
> 本文檔產生的電子書 PDF 在某些檢視設備上可能無法正確排版。如需取得最新版本技術說明，請參閱官方文檔站點：[https://docs.hak5.org](https://docs.hak5.org)。

#### 原廠基礎規格指標
* 傳輸介面：標準 USB
* 支援協定：USB 2.0
* 頻率範圍：2.412 GHz ～ 2.4835 GHz
* 尺寸規格：74 mm × 27 mm × 14 mm
* 額定功率：5 W（USB 5 V 1 A）
* 作業溫度：35ºC ～ 45ºC
* 儲存溫度：-20ºC ～ 50ºC
* 相對濕度：0% 至 90%（非冷凝狀態）

#### 重要安全須知與法規警告
Key Croc 為專為經過授權的資安審計人員、滲透測試專家及學術研究人員設計的專業硬體工具。在未經系統所有權人明確書面授權的情況下，在任何主機或網路上部署側錄裝置均屬非法行為。使用者必須遵循當地相關法規。

---

## 2. 操作模式與初始設定

<!-- section：modes -->
### 2.1 Key Croc 基礎架構 (Key Croc Basics)

Key Croc 具備兩種完全獨立、互斥的運作狀態：**Attack Mode（攻擊模式）** 與 **Arming Mode（維護模式）**。

| 功能與行為指標 | Attack Mode（預設攻擊模式）| Arming Mode（維護模式）|
|---|---|---|
| **啟用條件** | 插入 USB 連接埠並在下游連接鍵盤開機 | 開機時按壓機身底部隱藏式按鈕，或透過指令觸發 |
| **LED 指示燈** | **完全熄滅**（極致隱蔽）| **藍燈慢速閃爍**（呼吸模式）|
| **鍵盤透傳轉發** | 啟用（零延遲即時轉發）| 暫停 |
| **按鍵側錄記錄** | 啟用（寫入 `croc_char.log` 等）| 暫停 |
| **模式匹配引擎** | 啟用（即時比對 `/payloads/`）| 暫停 |
| **主機端識別** | 複製自原鍵盤之 USB 裝置 | 大容量隨身碟磁區（「KeyCroc」）與序列埠 |
| **主要核心任務** | 隱蔽監聽、側錄與觸發攻擊酬載 | 參數設定、編輯酬載與導出外傳資料 |

#### 進入維護模式 (Arming Mode) 步驟
1. 將 Key Croc 插入電腦 USB 連接埠，暫不連接下游鍵盤。
2. 使用智慧型手機的 SIM 退卡針或迴紋針，輕按機身底部針孔內的隱藏式微動按鈕。
3. 觀察多色 LED 轉變為**藍燈閃爍**。
4. 目標作業系統將自動掛載標籤為 **`KeyCroc`** 的 FAT32 隨身碟大容量儲存磁區。

---

### 2.2 序列埠主控台存取 (Serial Console Access)

在維護模式下，Key Croc 會向目標主機提供 USB 序列埠 ACM 裝置端點：

1. **Windows 平台**：使用 PuTTY 連線，連線類型選擇 **Serial**，通訊埠填入相應的 COM 埠（如 COM3），設定鮑率為 **115200**。
2. **macOS / Linux 平台**：開啟端點機，執行連線指令：
   ```bash
   screen /dev/tty.usbmodem* 115200
   ```
3. 按下 Enter 鍵即可出現 Linux 登入提示，輸入預設帳號 `root` 與預設密碼 `hak5 croc` 進入完整 Linux Shell。

---

<!-- section：recovery -->
### 2.3 韌體升級指引 (Updating the Firmware)

Hak5 團隊定期發布韌體修補更新以強化系統穩定度並擴充功能模組：

1. 透過針孔按鈕將 Key Croc 啟動進入維護模式。
2. 存取掛載的隨身碟磁區，將由 Hak5 官網下載之升級套件（`upgrade-x.x.tar.gz`）直接放置於隨身碟根目錄。
3. 安全退出隨身碟磁區，並重新插拔 Key Croc。
4. 升級程序自動展開：LED 將顯示紅藍交替閃爍（約耗時數分鐘）。
5. 升級完成後系統自動重開機，LED 轉為藍燈閃爍，表示系統已升級完成。

> [!CAUTION]
> 韌體更新進行期間，**絕對不可拔除電源**，否則將導致晶片韌體損毀。

---

### 2.4 原廠出廠重置 (Factory Reset)

當設定檔混亂或系統運作異常時，可執行出廠還原：
1. 進入維護模式，在隨身碟磁區根目錄建立名為 `factoryreset` 的空白文字檔案。
2. 安全退出隨身碟並重新插拔 Key Croc。
3. 系統將偵測到還原標記，自動重構 FAT32 分割區並將系統檔案復原至出廠映像檔狀態。

---

## 3. 設備設定與鍵盤語言映射

### 3.1 核心組態設定 (Configuration)

Key Croc 的所有持久化全域組態均存放於隨身碟根目錄的 `config.txt` 中。此檔案採用直觀的鍵值對（Key-Value）設定格式：

```ini
# Key Croc 全域組態設定檔範例
DUCKY_LANG us
WIFI_SSID「Target_Office_WiFi」
WIFI_PASS「SecurePassword123」
```

---

### 3.2 原廠預設值 (Default Settings)

* **預設語系**：`us`（美式英語）
* **預設 Wi-Fi 狀態**：關閉（需於 `config.txt` 設定 SSID 與密碼後自動啟動）
* **預設本機 IP**：`172.16.32.1`（當啟用 RNDIS/ECM 網路模擬時）
* **預設 SSH 帳號**：`root`
* **預設 SSH 密碼**：`hak5 croc`

---

### 3.3 鍵盤語言與掃描碼解析 (Understanding Languages)

鍵盤傳送至主機的資料本質上為硬體掃描碼（Scancodes），而非 ASCII 字元。不同國家與地區的鍵盤設定對同一個掃描碼的符號映射截然不同：

* Key Croc 的 `languages/` 資料夾內建了全球數十種鍵盤設定映射檔案（如 `us.json`，`de.json`，`uk.json`，`fr.json`）。
* 在 `config.txt` 中宣告 `DUCKY_LANG <程式碼>`，系統在執行按鍵側錄解碼與 `QUACK` 按鍵序列注入時，即能完美還原正確字元，避免特殊符號錯位。

---

## 4. 檔案系統架構與目錄結構

<!-- section：filesystem -->
### 4.1 檔案與目錄結構 (Files and Directory Structure)

掛載於維護模式下的 `KeyCroc` 大容量儲存裝置包含以下標準目錄階層：

```
KeyCroc/
├── config.txt          # 全域裝置與 Wi-Fi 連網設定檔
├── payloads/           # 啟用中的攻擊酬載目錄（開機自動載入）
├── library/            # 酬載儲藏庫與備用腳本
├── loot/               # 側錄日誌與外傳機密儲存目錄
│   ├── croc_char.log   # 解碼後的可讀字元文字日誌
│   ├── croc_raw.log    # 底層十六進位原始掃描碼日誌
│   └── matches.log     # MATCH 觸發事件與執行歷史日誌
├── languages/          # 各國鍵盤語系映射資料表
├── tools/              # 自訂滲透腳本、第三方執行檔與工具包
└── version.txt         # 目前安裝之韌體版本號標記
```

---

### 4.2 檔案系統深入剖析 (Understanding the File System)

Key Croc 採用嵌入式 Linux 雙分區設計：
1. **內部 ext4 根分區 (`/`)**：唯讀與系統保護分區，承載完整的 Debian Linux 系統核心與背景常駐守護行程。
2. **udisk 大容量儲存分區 (`/root/udisk`)**：FAT32 分割區，供 USB Mass Storage 模式對外掛載。

> [!NOTE]
> 在攻擊模式下，Key Croc 核心常駐程序負責將側錄按鍵寫入快取。為避免快閃記憶體損耗並確保資料完整落盤，請於酬載中調用 `sync` 指令。

---

## 5. 網路連線與遠端 Cloud C² 運作

### 5.1 讓 Key Croc 連線上網 (Getting the Key Croc Online)

Key Croc 內建 2.4 GHz 802.11 b/g/n Wi-Fi 晶片。在 `config.txt` 中填妥無線網路連線資訊後，Key Croc 開機時將在背景自動嘗試連接指定無線基地台（AP）。

連線成功後，滲透測試人員可在同一局域網內直接透過 SSH 連線：
```bash
ssh root@<KeyCroc_IP>
```

---

### 5.2 設定 Hak5 Cloud C² (Configuring Cloud C²)

搭配 Hak5 Cloud C² 伺服器，Key Croc 能化身為跨越全球網際網路的帶外控制節點：

1. 由 Cloud C² 網頁主控台新增裝置並下載專屬設備憑證封包 `device.config`。
2. 將 `device.config` 複製放置於 Key Croc 隨身碟磁區根目錄。
3. 重新開機後，Key Croc 將自動與 Cloud C² 建立加密反向連線隧道。滲透測試人員無論身在何處，均可由瀏覽器直接監控即時按鍵流、下發攻擊指令或提取外傳日誌。

---

## 6. 酬載開發與 Ducky Script 指令集

<!-- section：payloads -->
### 6.1 酬載開發基礎 (Payload Development)

Key Croc 酬載是一組副檔名為 `.txt` 的 Bash 與 DuckyScript 混編腳本，放置於 `/payloads/` 目錄中。Key Croc 開機進入攻擊模式時，背景核心將自動解析並即時載入該目錄下的所有酬載。

一個標準的 Key Croc 酬載通常包含：
1. **觸發器 (Trigger)**：透過 `MATCH` 指定啟動酬載的關鍵字或正則表達式。
2. **前置設定 (Setup)**：調用 `ATTACKMODE` 準備攻擊設備，設定 `LED` 狀態。
3. **注入執行 (Execution)**：利用 `QUACK` 注入指令序列，或執行 Bash 腳本將資料外發。

---

### 6.2 Ducky Script 語法架構 (Ducky Script Commands)

Key Croc 原生相容 DuckyScript 2.0 指令集，包括條件控制、變數儲存以及專屬於 HitM 中間人架構的按鍵隔離與日誌提取語法。

---

### 6.3 常用指令快速速查表 (Command Quick Reference)

| 指令關鍵字 | 語法範例 | 核心功能說明 |
|---|---|---|
| `MATCH` | `MATCH password` | 監聽鍵盤輸入，一旦匹配指定關鍵字立即執行後續腳本 |
| `SAVEKEYS` | `SAVEKEYS /root/udisk/loot/keys.txt 20` | 將觸發前最後 N 個按鍵儲存至指定外傳路徑 |
| `ATTACKMODE` | `ATTACKMODE HID ETHERNET` | 宣告模擬之複合 USB 設備端點（HID / 網卡 / 序列埠）|
| `CLONE` | `CLONE_VID` / `CLONE_PID` | 即時複製下游插入之實體鍵盤的硬體描述符 |
| `QUACK` | `QUACK GUI r` | 向上游目標電腦模擬鍵盤擊鍵注入 |
| `QUACK LOCK` | `QUACK LOCK` | 暫時阻斷實體鍵盤轉發，防止使用者按鍵打亂腳本注入 |
| `LED` | `LED ATTACK` | 控制機身 RGB LED 指示燈顏色與閃爍行為 |

---

### 6.4 MATCH 觸發匹配指令 (The MATCH Command)

`MATCH` 指令是 Key Croc 的靈魂核心。它支援三種匹配策略：

#### 1. 精準字串匹配 (Exact Strings)
```bash
MATCH hello
QUACK STRING Target said hello!
```

#### 2. 多重關鍵字或條件分支 (Multiple Strings)
```bash
MATCH (root|admin|administrator)
# 當目標輸入以上任一使用者名稱時觸發
```

#### 3. 正規表達式模式匹配 (Regular Expressions)
```bash
# 匹配美國郵遞區號或特定格式的信用卡號
MATCH [0-9]{5}(?:-[0-9]{4})?
```

---

### 6.5 SAVEKEYS 日誌儲存指令 (The SAVEKEYS Command)

當 `MATCH` 成功攔截到目標輸入的關鍵字（如登入入口網址或帳號）時，密碼往往緊隨在後。`SAVEKEYS` 能擷取觸發點前後特定長度的按鍵日誌並儲存至獨立檔案中：

```bash
MATCH login.example.com
SAVEKEYS /root/udisk/loot/example_login.txt 50
```

---

### 6.6 ATTACKMODE 攻擊模式指令 (The ATTACKMODE Command)

Key Croc 支援動態切換 USB 身份：
* `ATTACKMODE HID`：僅模擬鍵盤注入。
* `ATTACKMODE HID ETHERNET`：同時模擬鍵盤與虛擬乙太網路卡（建立本機 TCP/IP 滲透通道）。
* `ATTACKMODE HID SERIAL`：同時模擬鍵盤與序列埠端點。

---

### 6.7 USB 識別碼與硬體克隆 (USB Identifiers & Hardware ID Cloning)

為達成完美隱形，Key Croc 預設支援自動硬體描述符克隆（Hardware Cloning）。當真實鍵盤插入下游母座時，Key Croc 會讀取該鍵盤的 VID（廠商 ID）、PID（產品 ID）、製造商字串及序號，並以此完全相同的硬體特徵向上游目標電腦註冊，徹底規避企業端點白名單防護！

---

### 6.8 QUACK 按鍵序列注入指令 (The QUACK Command)

`QUACK` 語法負責合成虛擬擊鍵：
```bash
QUACK GUI r
QUACK DELAY 200
QUACK STRING powershell -ep bypass -w hidden
QUACK ENTER
```

---

### 6.9 進階 QUACK 擴充語法 (Advanced QUACK Commands)

* `QUACK LOCK`：啟動實體鍵盤隔離機制，此時目標使用者敲擊鍵盤的訊號會被暫存阻斷，直到注入結束後釋放，避免字元交錯導致攻擊腳本崩潰。
* `QUACK UNLOCK`：解除鍵盤隔離。
* `QUACK CLEAR`：清除目前未處理完畢的按鍵緩衝區。

---

### 6.10 LED 狀態指示燈語法 (The LED Command)

在維護模式或除錯狀態下，可自由調用燈號反饋：
* `LED ATTACK`：黃燈閃爍
* `LED SUCCESS`：常亮綠燈
* `LED FAIL`：常亮紅燈
* `LED OFF`：完全熄滅（實戰隱蔽模式）

---

## 7. 進階實戰指南、技巧與實用範例

### 7.1 Key Croc 密碼嗅探實戰 (Password Sniffing with the Key Croc)

展示如何針對熱門網站或企業內部 SSO 登入頁面編寫 `MATCH` 規則。透過比對網址關鍵字後自動抓取接續輸入的帳密字串，將憑證精確提取至外傳檔案中。

---

### 7.2 Key Croc 1.3 新增功能深度解析 (New Features in Key Croc 1.3)

Key Croc 1.3 韌體帶來多項重磅突破：
* 大幅強化按鍵緩衝區正規表達式匹配效能。
* 擴充對複合式 USB 設備（如包含軌跡球或音量旋鈕的特殊鍵盤）的相容性。
* 最佳化 Wi-Fi 自動重連與 Cloud C² 斷線重試機制。

---

### 7.3 互動式酬載開發與除錯 (Interactive Payload Development)

透過序列埠連線直接登入 Key Croc，使用 `tail -f /root/udisk/loot/croc_char.log` 即時觀測當前打字流，並即時除錯自訂的 `MATCH` 語法，大幅縮短酬載開發驗證週期。

---

### 7.4 安裝額外工具（如 Metasploit）(Installing Extras like Metasploit)

因為 Key Croc 搭載標準 ARM Linux 系統，在連上網際網路後可直接利用 `apt-get` 安裝 Python3、Nmap、Responder 或甚至精簡版 Metasploit Framework，將 Key Croc 化身為插在鍵盤線上的自律型實體滲透主機！

---

### 7.5 高頻實用酬載程式碼片段 (Helpful Payload Snippets)

收錄官方社群精選的高頻實用範本：
* Windows 一鍵反彈 Meterpreter Shell 範本
* 敏感文件背景隱蔽外傳至 Cloud C² 腳本
* 目標使用者離開座位鎖定偵測器
