---
title：「Hak5 Shark Jack 原廠技術說明書與全功能操作手冊」
model：「Shark Jack」
manufacturer：「Hak5」
category：「可攜式網路滲透測試植入裝置」
docs_url：「https://docs.hak5.org/shark-jack/」
version：「2.0」
locale：「zh-tw」
---

# Hak5 Shark Jack 原廠技術說明書與全功能操作手冊

> Hak5 Shark Jack 是一款專為網路偵察與隱蔽滲透設計的口袋型網路攻擊硬體。外觀為精巧的 RJ-45 接頭外型，內建 Linux 系統、專屬鋰電池、580 MHz 處理器與快速乙太網路晶片，插入目標網路孔即可於數秒內全自動執行網路資產掃描與憑證外傳。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 Shark Jack 原廠介紹](#1-1-shark-jack-原廠介紹)
  - [1.2 核心運作原理與功能特性 (Shark Jack Basics)](#1-2-核心運作原理與功能特性-shark-jack-basics)
  - [1.3 原廠出廠預設值與連線參數 (Default Settings)](#1-3-原廠出廠預設值與連線參數-default-settings)
- [**2. 開箱入門、連線與 sharkjack.sh 核心公用程式**](#2-開箱入門連線與-sharkjacksh-核心公用程式)
  - [2.1 開箱與初始設定指引 (Unboxing and Setup)](#2-1-開箱與初始設定指引-unboxing-and-setup)
  - [2.2 sharkjack.sh 官方工具庫解析 (Using sharkjack.sh)](#2-2-sharkjacksh-官方工具庫解析-using-sharkjacksh)
  - [2.3 兩大核心維護指令 (Two Key Commands)](#2-3-兩大核心維護指令-two-key-commands)
  - [2.4 第一支網路酬載編寫實戰 (Writing a Simple Payload)](#2-4-第一支網路酬載編寫實戰-writing-a-simple-payload)
- [**3. 韌體更新與出廠維護程序**](#3-韌體更新與出廠維護程序)
  - [3.1 手動韌體升級程序 (Manual Upgrade)](#3-1-手動韌體升級程序-manual-upgrade)
  - [3.2 透過網路空中線上升級 (Over-the-Air Upgrade)](#3-2-透過網路空中線上升級-over-the-air-upgrade)
- [**4. 酬載開發與 DuckyScript 指令集參考**](#4-酬載開發與-duckyscript-指令集參考)
  - [4.1 酬載開發核心架構 (Payload Development Basics)](#4-1-酬載開發核心架構-payload-development-basics)
  - [4.2 NETMODE 網路模式設定指令 (The NETMODE Command)](#4-2-netmode-網路模式設定指令-the-netmode-command)
  - [4.3 LED 狀態指示燈指令 (The LED Command)](#4-3-led-狀態指示燈指令-the-led-command)
  - [4.4 SWITCH 硬體切換開關指令 (The SWITCH Command)](#4-4-switch-硬體切換開關指令-the-switch-command)
  - [4.5 BATTERY 電池狀態指令 (The BATTERY Command)](#4-5-battery-電池狀態指令-the-battery-command)
  - [4.6 SERIAL_WRITE 序列埠輸出指令 (The SERIAL_WRITE Command)](#4-6-serial_write-序列埠輸出指令-the-serial_write-command)
  - [4.7 Hak5 Cloud C² 整合指令 (The Cloud C2 Commands)](#4-7-hak5-cloud-c-整合指令-the-cloud-c2-commands)
  - [4.8 系統預先安裝之工具庫 (Included Tools)](#4-8-系統預先安裝之工具庫-included-tools)
- [**5. 酬載管理與 Cloud C² 整合**](#5-酬載管理與-cloud-c-整合)
  - [5.1 酬載儲存與管理架構 (Payload Management)](#5-1-酬載儲存與管理架構-payload-management)
  - [5.2 LIST 酬載清單查詢指令 (The LIST Command)](#5-2-list-酬載清單查詢指令-the-list-command)
  - [5.3 ACTIVATE 酬載動態啟用指令 (The ACTIVATE Command)](#5-3-activate-酬載動態啟用指令-the-activate-command)
- [**6. 故障排除、硬體改裝技巧與規格安全**](#6-故障排除硬體改裝技巧與規格安全)
  - [6.1 韌體救援與修復模式 (Firmware Recovery)](#6-1-韌體救援與修復模式-firmware-recovery)
  - [6.2 利用手機進行反向充電與供電技巧 (Charge from your Phone)](#6-2-利用手機進行反向充電與供電技巧-charge-from-your-phone)
  - [6.3 結合 Plunder Bug 實體接線技巧 (Using with Plunder Bug)](#6-3-結合-plunder-bug-實體接線技巧-using-with-plunder-bug)
  - [6.4 Android 序列埠連接線設定 (Android Serial Setup)](#6-4-android-序列埠連接線設定-android-serial-setup)
  - [6.5 官方技術規格基準表 (Hardware Specifications)](#6-5-官方技術規格基準表-hardware-specifications)
  - [6.6 重要安全指引與法規聲明 (Safety and Warnings)](#6-6-重要安全指引與法規聲明-safety-and-warnings)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 1.1 Shark Jack 原廠介紹

Hak5 Shark Jack 是一款精巧型攜帶式網路滲透測試植入裝置。外觀整合了標準 RJ-45 公頭，體積極其小巧，可隨身放入口袋或鑰匙圈。

與需要漫長開機設定的筆記型電腦不同，Shark Jack 專為極速實戰所打造：機身內建獨立充電式鋰電池，只要將其推入目標企業的任何區域網路（LAN）插座，Shark Jack 便會在數秒內完成開機、自動透過 DHCP 獲取 IP、以靜默方式進行周邊主機掃描、監聽敏感封包、或透過 Cloud C² 建立反向加密遠端連線，並在任務完成後藉由多色 LED 閃爍綠燈向操作員回報成功。

### 硬體技術規格與原廠校準基準表

| 硬體元件名稱 | 官方技術規格說明 |
|---|---|
| **核心處理器 (SoC / CPU)** | Single Core MIPS @ 580 MHz |
| **系統記憶體 (RAM)** | 64 MB DDR2 |
| **內部儲存空間 (Storage)** | 128 MB High-Speed Flash 高速快閃記憶體 |
| **乙太網路介面 (Network)** | 10/100 Fast Ethernet RJ-45 連接埠 |
| **內部自主電源 (Battery)** | 內建充電式鋰電池（支援獨立免插電作業）|
| **硬體模式切換開關** | 3 段式實體切換滑動開關（Arming 維護、Off 關閉/充電、Attack 攻擊）|
| **狀態指示模組** | 多色可程式化 RGB LED 指示燈 |
| **預設網路 IP / 子網路** | 172.16.24.1 / 255.255.255.0 |

---

<!-- section：features -->
### 1.2 核心運作原理與功能特性 (Shark Jack Basics)

Shark Jack 的核心作戰哲學在於「即插即跑、快速撤離」（Plug and Pwn）：
1. **獨立供電運作**：內建鋰電池可提供約 10 至 15 分鐘的獨立高負載作戰時間，完全無需外接電源線即可完成一次完整的內部網路勘察。
2. **三段實體模式開關**：
   - **Arming 模式（靠向 USB 孔側）**：維護模式，啟動內部 DHCP 伺服器與 SSH 服務，供工程師連接電腦除錯與管理酬載。
   - **Off / Charge 模式（中間位置）**：關閉系統，連接 USB-C 時對內建電池進行充電。
   - **Attack 模式（靠向 RJ-45 孔側）**：實戰攻擊模式，插入網路孔後自動執行當前啟用的酬載指令碼。
3. **即時視覺回饋**：內建可自訂 RGB LED，讓操作人員在不攜帶螢幕的情況下一目了然掌握掃描進度與狀態。

---

### 1.3 原廠出廠預設值與連線參數 (Default Settings)

當處於 Arming 維護模式下時，Shark Jack 提供下列標準管理參數：
- **乙太網路介面 IP**：`172.16.24.1`
- **子網路遮罩**：`255.255.255.0`
- **DHCP 配發範圍**：`172.16.24.10` 至 `172.16.24.250`
- **SSH 登入埠**：`22`
- **預設管理員帳號**：`root`
- **預設原廠密碼**：`armshark`

---

<!-- section：configuration -->
## 2. 開箱入門、連線與 sharkjack.sh 核心公用程式

### 2.1 開箱與初始設定指引 (Unboxing and Setup)

1. 將 Shark Jack 實體開關切換至中間「Off」位置，透過 USB-C 傳輸線連接電源充電 1 小時。
2. 切換開關至「Arming」模式，將 RJ-45 網路線一端接至 Shark Jack，另一端接至管理用電腦。
3. 管理電腦的網路卡將自動取得 `172.16.24.x` 的 IP 位址。
4. 開啟端點機，執行 SSH 連線：
   ```bash
   ssh root@172.16.24.1
   # 提示輸入密碼時鍵入：armshark
   ```
5. 連線成功後，系統將顯示 ASCII 鯊魚圖騰與端點機提示字元。

---

### 2.2 sharkjack.sh 官方工具庫解析 (Using sharkjack.sh)

`sharkjack.sh` 是 Shark Jack 系統的核心 API 指令庫，封裝了網路切換、LED 燈號控制與電源管理等底層操作：
- `LED R FAST`：紅色快速閃爍。
- `LED G SOLID`：綠色恆亮。
- `NETMODE DHCP_CLIENT`：要求網路晶片向環境 DHCP 伺服器申請 IP。
- `NETMODE STATIC 192.168.1.50 255.255.255.0 192.168.1.1`：設定靜態 IP。

---

### 2.3 兩大核心維護指令 (Two Key Commands)

原廠提供兩支極度便利的專用指令：
1. `sharkjack.sh`：直接在端點機列印完整的指令說明手冊。
2. `cloudc2_connect`：快速驗證與測試 Hak5 Cloud C² 雲端通道狀態。

---

### 2.4 第一支網路酬載編寫實戰 (Writing a Simple Payload)

所有酬載均為標準 Bash 指令碼，儲存於 `/root/payload/payload.sh`。以下為經典的內網資產探索酬載範例：

```bash
#!/bin/bash
# 標題：簡易 Nmap 內網資產探索酬載
# 說明：自動獲取 IP，掃描同網段活體主機並存檔

# 1. 設置 LED 為品紅色慢閃，提示正在取得 IP
LED M SLOW
NETMODE DHCP_CLIENT

# 2. 等待網路介面獲取有效預設閘道
while [ -z「$GATEWAY」]；do
    GATEWAY=$(route -n | grep『UG[ 	]』| awk『{print $2}』)
    sleep 1
done

# 3. 變更 LED 為黃色快閃，代表正在進行 Nmap 掃描
LED Y FAST
SUBNET=$(ip -o -f inet addr show eth0 | awk『{print $4}』)
nmap -sn $SUBNET -oN /root/loot/hosts.txt

# 4. 掃描完成，綠色恆亮 5 秒後安全關機
LED G SOLID
sleep 5
LED OFF
poweroff
```

---

<!-- section：maintenance -->
## 3. 韌體更新與出廠維護程序

### 3.1 手動韌體升級程序 (Manual Upgrade)

1. 由 Hak5 官方下載中心下載最新韌體檔案（`upgrade-x.x.bin`）。
2. 在 Arming 模式下透過 SCP 將韌體傳送至設備：
   ```bash
   scp upgrade-x.x.bin root@172.16.24.1:/tmp/
   ```
3. 在 SSH 端點機執行升級指令：
   ```bash
   sysupgrade -n /tmp/upgrade-x.x.bin
   ```
4. 升級期間 LED 將呈現藍紅交替閃爍，切勿斷電或撥動模式開關。

---

### 3.2 透過網路空中線上升級 (Over-the-Air Upgrade)

若 Shark Jack 已設定可連上外部網際網路，可直接執行：
```bash
upgrade
```
系統將自動檢測官方伺服器之最新韌體版本並完成一鍵升級。

---

## 4. 酬載開發與 DuckyScript 指令集參考

### 4.1 酬載開發核心架構 (Payload Development Basics)

Shark Jack 的酬載採用結合 Bash 與 Hak5 擴充語法架構。指令碼需賦予可執行權限（`chmod +x payload.sh`），且通常劃分為四個標準作戰階段：
1. **初始化階段**：設定 LED 與網路模式。
2. **獲取網路階段**：等待 DHCP 配發或設定靜態 IP。
3. **作戰執行階段**：執行 nmap、tcpdump、responder 或自訂 Python 探索腳本。
4. **回報與安全收尾**：將戰果（Loot）同步至 Cloud C² 或本機，並執行 `poweroff` 關機保護硬體。

---

### 4.2 NETMODE 網路模式設定指令 (The NETMODE Command)

- `NETMODE DHCP_CLIENT`：預設攻擊模式，充當一般端點設備向目標網段請求 IP。
- `NETMODE DHCP_SERVER`：啟用內建 dnsmasq 服務，向連接的對象發送 IP（用於 Arming 模式或隔離測試）。
- `NETMODE STATIC <IP> <NETMASK> <GATEWAY>`：手動指定靜態 IP，適合針對無 DHCP 伺服器之封閉工控或伺服器網段。

---

### 4.3 LED 狀態指示燈指令 (The LED Command)

語法為：`LED <顏色> <模式>`
- **顏色**：`R`（紅）、`G`（綠）、`B`（藍）、`Y`（黃）、`C`（青）、`M`（品紅）、`W`（白）、`OFF`（熄滅）。
- **模式**：`SOLID`（恆亮）、`SLOW`（慢閃）、`FAST`（快閃）、`VERYFAST`（極速閃爍）。

---

### 4.4 SWITCH 硬體切換開關指令 (The SWITCH Command)

透過 `SWITCH` 指令可在指令碼執行過程中即時判斷實體撥鍵是否被操作員撥動，以實現即時安全中斷。

---

### 4.5 BATTERY 電池狀態指令 (The BATTERY Command)

```bash
# 取得當前電池電量百分比
BATTERY_LEVEL=$(sharkjack.sh battery)
echo「Current Battery：$BATTERY_LEVEL%」
```

---

### 4.6 SERIAL_WRITE 序列埠輸出指令 (The SERIAL_WRITE Command)

當搭配專用除錯線時，可使用 `SERIAL_WRITE` 將除錯日誌同步輸出至實體序列埠端點機。

---

### 4.7 Hak5 Cloud C² 整合指令 (The Cloud C2 Commands)

Shark Jack 深度整合 Hak5 Cloud C²，支援下列核心 C2 指令：
- `C2CONNECT`：背景啟動 Cloud C² 代理程式並連線。
- `C2EXFIL <檔案路徑>`：自動將掃描結果或外傳檔案上傳至指定 Cloud C² 伺服器。

---

### 4.8 系統預先安裝之工具庫 (Included Tools)

系統內部整合眾多開源資安瑞士刀工具：
- **網路探測**：`nmap`、`arp-scan`、`netcat` (nc)
- **傳輸工具**：`curl`、`wget`、`scp`、`ssh`
- **直譯環境**：完整支援 Bash 與輕量化 Python 執行環境

---

## 5. 酬載管理與 Cloud C² 整合

### 5.1 酬載儲存與管理架構 (Payload Management)

Shark Jack 的酬載目錄位於 `/root/payload/`。實戰中可存放多組酬載指令碼（如 `payload1.sh`、`payload2.sh`）。

---

### 5.2 LIST 酬載清單查詢指令 (The LIST Command)

透過 `sharkjack.sh list` 可列出當前儲存於裝置內的所有可用攻擊酬載名稱與描述。

---

### 5.3 ACTIVATE 酬載動態啟用指令 (The ACTIVATE Command)

透過 `sharkjack.sh activate <名稱>`，可即時將指定酬載軟連結至當前攻擊模式啟動目標。

---

## 6. 故障排除、硬體改裝技巧與規格安全

### 6.1 韌體救援與修復模式 (Firmware Recovery)

若升級中斷導致裝置無法正常開機：
1. 將開關切至 Arming 模式。
2. 按住機身內部復原按鈕（若有配備），連接電源開機。
3. 透過預設復原 IP `192.168.1.1` 進入 Web 復原介面重新燒錄原廠韌體。

---

### 6.2 利用手機進行反向充電與供電技巧 (Charge from your Phone)

Shark Jack 的 USB Type-C 連接埠支援標準 5 V 輸入。在戶外行動測試中，只需一條 USB-C 雙頭 OTG 傳輸線，即可直接利用 Android 智慧型手機對 Shark Jack 進行緊急充電或長時間供電。

---

### 6.3 結合 Plunder Bug 實體接線技巧 (Using with Plunder Bug)

將 Shark Jack 插入 Hak5 Plunder Bug 乙太網路分流器（Tap），即可將 Shark Jack 轉變為便攜式隱蔽封包側錄站，實現對目標線路的透明 Sniffing。

---

### 6.4 Android 序列埠連接線設定 (Android Serial Setup)

透過專用 Serial-to-USB 線材搭配 Android 端點機模擬器 App，可直接在手機螢幕上查看 Shark Jack 開機日誌與互動式 Shell。

---

### 6.5 官方技術規格基準表 (Hardware Specifications)

- **處理器規格**：580 MHz MIPS 架構 Single Core
- **記憶體規格**：64 MB DDR2
- **儲存規格**：128 MB 快閃記憶體
- **尺寸與重量**：62 mm × 21 mm × 12 mm，重約 15 克
- **通訊標準**：IEEE 802.3 10/100 Base-T

---

### 6.6 重要安全指引與法規聲明 (Safety and Warnings)

1. **鋰電池維護**：切勿在高於 60°C 的極端高溫環境或車內曝曬存放 Shark Jack。
2. **網路安全授權**：嚴禁將本設備未經授權連接至未獲測試許可之第三方網路設施。
