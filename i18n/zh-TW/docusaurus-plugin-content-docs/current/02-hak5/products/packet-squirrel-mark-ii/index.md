---
title: "Hak5 Packet Squirrel Mark II 原廠技術說明書與全功能操作手冊"
model: "Packet Squirrel Mark II"
manufacturer: "Hak5"
category: "網路中間人串接側錄與遠端存取設備"
docs_url: "https://docs.hak5.org/packet-squirrel/"
version: "4.0"
locale: "zh-tw"
---

# Hak5 Packet Squirrel Mark II 原廠技術說明書與全功能操作手冊

> Hak5 出品的 Packet Squirrel Mark II 是口袋型乙太網路中間人（Device-in-the-Middle，DitM）多功能滲透測試工具的最新演進版本。專為隱蔽遠端存取、無痛封包截獲、安全 VPN 加密通道建立以及響應式網路攻擊酬載所設計，輕撥硬體開關即可瞬間切換作戰模式。

---

## 目錄

- [**1. 產品概述與核心硬體架構**](#1-產品概述與核心硬體架構)
  - [1.1 Packet Squirrel Mark II 原廠介紹](#1-1-packet-squirrel-mark-ii-原廠介紹)
  - [1.2 實體連接與接線指南 (Connecting the Packet Squirrel)](#1-2-實體連接與接線指南-connecting-the-packet-squirrel)
  - [1.3 初次開機設定步驟 (Setting up the Packet Squirrel)](#1-3-初次開機設定步驟-setting-up-the-packet-squirrel)
  - [1.4 Mark II 世代全新特性 (Changes & New features)](#1-4-mark-ii-世代全新特性-changes-new-features)
- [**2. 入門指南與核心操作**](#2-入門指南與核心操作)
  - [2.1 Packet Squirrel 運作原理 (Packet Squirrel Basics)](#2-1-packet-squirrel-運作原理-packet-squirrel-basics)
  - [2.2 存取與登入主控台 (Accessing the Packet Squirrel)](#2-2-存取與登入主控台-accessing-the-packet-squirrel)
  - [2.3 Web UI 網頁圖形化介面 (Web UI)](#2-3-web-ui-網頁圖形化介面-web-ui)
  - [2.4 讓設備連線上網 (Getting the Packet Squirrel online)](#2-4-讓設備連線上網-getting-the-packet-squirrel-online)
  - [2.5 LED 狀態指示燈號定義 (Status LED)](#2-5-led-狀態指示燈號定義-status-led)
  - [2.6 Hak5 Cloud C² 雲端納管 (Cloud C²)](#2-6-hak5-cloud-c-雲端納管-cloud-c)
  - [2.7 USB 儲存裝置支援 (USB storage support)](#2-7-usb-儲存裝置支援-usb-storage-support)
  - [2.8 選擇與編輯酬載 (Selecting and editing payloads)](#2-8-選擇與編輯酬載-selecting-and-editing-payloads)
  - [2.9 設定酬載參數 (Configuring payloads)](#2-9-設定酬載參數-configuring-payloads)
  - [2.10 執行酬載 (Running payloads)](#2-10-執行酬載-running-payloads)
  - [2.11 網路拓撲與運作模式 (Networking and modes)](#2-11-網路拓撲與運作模式-networking-and-modes)
- [**3. 網路基礎理論與封包操弄教學**](#3-網路基礎理論與封包操弄教學)
  - [3.1 網路技術詞彙表 (Networking Glossary)](#3-1-網路技術詞彙表-networking-glossary)
  - [3.2 OSI 七層模型實務解析 (OSI layers)](#3-2-osi-七層模型實務解析-osi-layers)
  - [3.3 私有 IP 網段劃分 (Private IP ranges)](#3-3-私有-ip-網段劃分-private-ip-ranges)
  - [3.4 子網路遮罩運算 (Network masks)](#3-4-子網路遮罩運算-network-masks)
  - [3.5 封包注入技術 (Packet injection)](#3-5-封包注入技術-packet-injection)
  - [3.6 網路位址轉譯與重定向 (Translation and redirection)](#3-6-網路位址轉譯與重定向-translation-and-redirection)
  - [3.7 封包截獲實戰 (Packet capture)](#3-7-封包截獲實戰-packet-capture)
- [**4. 酬載開發與 DuckyScript 指令集**](#4-酬載開發與-duckyscript-指令集)
  - [4.1 酬載開發基礎 (Payload development basics)](#4-1-酬載開發基礎-payload-development-basics)
  - [4.2 DuckyScript for Packet Squirrel 語法體系](#4-2-duckyscript-for-packet-squirrel-語法體系)
  - [4.3 BUTTON 微動按鈕監聽指令](#4-3-button-微動按鈕監聽指令)
  - [4.4 C2EXFIL 雲端資料外傳指令](#4-4-c2exfil-雲端資料外傳指令)
  - [4.5 C2NOTIFY 雲端告警通知指令](#4-5-c2notify-雲端告警通知指令)
  - [4.6 C2WATCHDIR 目錄自動同步指令](#4-6-c2watchdir-目錄自動同步指令)
  - [4.7 DYNAMICPROXY 動態代理通道指令](#4-7-dynamicproxy-動態代理通道指令)
  - [4.8 KILLPORT 通訊埠強制中斷指令](#4-8-killport-通訊埠強制中斷指令)
  - [4.9 KILLSTREAM 封包串流中斷指令](#4-9-killstream-封包串流中斷指令)
  - [4.10 LED 狀態指示燈控制指令](#4-10-led-狀態指示燈控制指令)
  - [4.11 MATCHPORT 通訊埠流量比對指令](#4-11-matchport-通訊埠流量比對指令)
  - [4.12 MATCHSTREAM 串流特徵匹配指令](#4-12-matchstream-串流特徵匹配指令)
  - [4.13 NETMODE 網路交換拓撲切換指令](#4-13-netmode-網路交換拓撲切換指令)
  - [4.14 SELFDESTRUCT 緊急資料銷毀指令](#4-14-selfdestruct-緊急資料銷毀指令)
  - [4.15 SSH_START 與 SSH_STOP 服務控制指令](#4-15-ssh_start-與-ssh_stop-服務控制指令)
  - [4.16 SPOOFDNS 網域名稱偽冒欺騙指令](#4-16-spoofdns-網域名稱偽冒欺騙指令)
  - [4.17 SWITCH 開關檔位查詢指令](#4-17-switch-開關檔位查詢指令)
  - [4.18 UI_START 與 UI_STOP 網頁介面控制指令](#4-18-ui_start-與-ui_stop-網頁介面控制指令)
  - [4.19 USB_FREE、USB_STORAGE 與 USB_WAIT 隨身碟控制指令](#4-19-usb_freeusb_storage-與-usb_wait-隨身碟控制指令)
- [**5. 高階酬載工程與自動化腳本技術**](#5-高階酬載工程與自動化腳本技術)
  - [5.1 高階酬載架構 (Advanced payloads)](#5-1-高階酬載架構-advanced-payloads)
  - [5.2 變數擴展與引號跳脫 (Quotes and expansions)](#5-2-變數擴展與引號跳脫-quotes-and-expansions)
  - [5.3 條件分支與流程控制 (Flow control)](#5-3-條件分支與流程控制-flow-control)
  - [5.4 標準輸出與重定向技巧 (Redirecting output)](#5-4-標準輸出與重定向技巧-redirecting-output)
  - [5.5 酬載自訂參數檔 (Payload configuration)](#5-5-酬載自訂參數檔-payload-configuration)
  - [5.6 返回碼驗證與成功判定 (Return codes & success)](#5-6-返回碼驗證與成功判定-return-codes--success)
  - [5.7 背景常駐任務管理 (Background commands)](#5-7-背景常駐任務管理-background-commands)
  - [5.8 指令群組化執行 (Command groups)](#5-8-指令群組化執行-command-groups)
  - [5.9 JSON 格式資料解析 (Processing JSON)](#5-9-json-格式資料解析-processing-json)
  - [5.10 USB 隨身碟硬體加密 (USB encryption)](#5-10-usb-隨身碟硬體加密-usb-encryption)
  - [5.11 VPN 服務端與客戶端設定 (VPN configuration)](#5-11-vpn-服務端與客戶端設定-vpn-configuration)
  - [5.12 網路封包深度操弄 (Network manipulation)](#5-12-網路封包深度操弄-network-manipulation)
  - [5.13 實戰避坑與排錯指南 (Tips，tricks，& pitfalls)](#5-13-實戰避坑與排錯指南-tips-tricks--pitfalls)
  - [5.14 Python 3 整合自動化開發 (Python on Packet Squirrel)](#5-14-python-3-整合自動化開發-python-on-packet-squirrel)
  - [5.15 官方酬載儲存庫 (Payload repository)](#5-15-官方酬載儲存庫-payload-repository)
- [**6. 故障排除、設備維護與韌體升級**](#6-故障排除設備維護與韌體升級)
  - [6.1 網路通訊排錯指引 (Troubleshooting networking)](#6-1-網路通訊排錯指引-troubleshooting-networking)
  - [6.2 酬載腳本除錯指引 (Troubleshooting payloads)](#6-2-酬載腳本除錯指引-troubleshooting-payloads)
  - [6.3 原廠出廠還原重置 (Factory reset)](#6-3-原廠出廠還原重置-factory-reset)
  - [6.4 韌體升級標準作業程序 (Upgrading firmware)](#6-4-韌體升級標準作業程序-upgrading-firmware)

---

## 1. 產品概述與核心硬體架構

<!-- section：overview -->
### 硬體技術規格與原廠校準基準表

| 硬體元件名稱 | 原廠技術規格說明 |
|---|---|
| **核心處理器 (CPU)** | Multi-Core Network Processor @ 580 MHz |
| **乙太網路連接埠 (Ethernet)** | 雙 Gigabit (10/100/1000) RJ-45 連接埠（具備硬體 Bypass 與透明串接能力）|
| **儲存擴充介面 (Storage)** | MicroSD 卡插槽 + USB-A 2.0 Host 隨身碟介面 |
| **供電介面 (Power)** | USB-C 匯流排供電（5 V DC，1 A）|
| **硬體控制開關** | 4 檔位實體切換開關（Switch 1，Switch 2，Switch 3，Arming Mode）與微動按鈕 |
| **VPN 加密協定支援** | 原生支援 OpenVPN 與 WireGuard 通道協議 |
| **狀態指示燈** | 多色可程式化 RGB LED 診斷燈 |

---

<!-- section：overview -->
### 1.1 Packet Squirrel Mark II 原廠介紹

Packet Squirrel Mark II 是由 Hak5 打造的最新一代微型硬體中間人（DitM）乙太網路滲透測試平台。具備手掌大小的輕巧體積，能夠神不知鬼不覺地串接於任何網路線路中，提供隱蔽的遠端外聯通道、無延遲流量封包截獲、端對端 VPN 加密通訊以及基於網路事件動態觸發的響應式酬載。

![Packet Squirrel Mark II](https://932701053-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F520JUF2JxB2RMXztRVAV%2Fuploads%2FhYoepPPoy8Pj5K8LI3E8%2Fsquirrelmk2_flat_halfres.png?alt=media&token=306f2cf9-1510-4238-9 ead-853396a45b4 d)

> [!WARNING]
> 本文檔專門適用於搭載韌體版本 **4.0.0 或更新版本** 之 Packet Squirrel Mark II。如需第一代舊款硬體說明，請查閱 Hak5 舊版文檔中心。

---

### 1.2 實體連接與接線指南 (Connecting the Packet Squirrel)

Packet Squirrel 具備兩個 RJ-45 乙太網路連接埠：
1. **Network 側連接埠 (標示為 Network 或網際網路符號)**：連接上游交換器（Switch）、路由器或牆面網路孔。
2. **Target 側連接埠 (標示為 Target 或電腦符號)**：連接受測目標主機、工作站或印表機。
3. **USB-C 供電連接埠**：連接 5 V 1 A 的 USB 電源變壓器、行動電源或受測主機後方的 USB 介面。

串接完成後，網路流量將無縫穿透 Packet Squirrel，目標主機與上游伺服器均無法察覺中間存在額外實體節點。

---

### 1.3 初次開機設定步驟 (Setting up the Packet Squirrel)

1. 將切換開關撥至最右側的 **維護模式 (Arming Mode)**。
2. 透過網路線將電腦連接至 Packet Squirrel 的 Target 連接埠，並插上 USB-C 電源開機。
3. 設備開機約需 30 秒，LED 將呈現藍燈慢速閃爍。
4. 電腦將自動取得 `172.16.32.x` 網段的 IP 位址。
5. 開啟瀏覽器存取 `http://172.16.32.1:1471`，進入 Web UI 引導式安裝精靈，設定 root 管理員密碼。

---

<!-- section：features -->
### 1.4 Mark II 世代全新特性 (Changes & New features)

相較於第一代 Packet Squirrel，Mark II 迎來全面革新：
* **雙 Gigabit 網路晶片**：支援 1000 BASE-T 極速線速轉發，告別百兆瓶頸。
* **全新 DuckyScript 語言核心**：引入高階封包比對指令（`MATCHPORT`，`MATCHSTREAM`）與雲端指令（`C2EXFIL`，`C2NOTIFY`）。
* **內建 Web UI 圖形化管理後台**：開機即提供視覺化儀表板，支援即時側錄下載與酬載拖曳上傳。
* **WireGuard 協定原生整合**：連線握手速度更快、耗損更低的高效加密 VPN。
* **USB-C 現代化供電規格**：全面升級 USB-C 介面。

---

## 2. 入門指南與核心操作

### 2.1 Packet Squirrel 運作原理 (Packet Squirrel Basics)

封包自 Network 端流入，由 Target 端流出；在此雙向轉發過程中，底層 Linux 核心可選擇：
* **純透傳模式 (Transparent Bridge)**：不分配 IP，完全隱匿無蹤，靜默側錄流量。
* **NAT 路由模式 (NAT Router)**：目標電腦經由 Packet Squirrel 轉發上網，支援連接埠轉發與流量劫持。
* **孤立阻斷模式 (Isolate / Drop)**：選擇性阻斷特定流量或切斷目標對外連線。

---

### 2.2 存取與登入主控台 (Accessing the Packet Squirrel)

在維護模式下，滲透人員可透過以下途徑登入系統：
* **SSH 端點連線**：
  ```bash
  ssh root@172.16.32.1
  ```
* **Web UI 瀏覽器**：造訪 `http://172.16.32.1:1471`。

---

### 2.3 Web UI 網頁圖形化介面 (Web UI)

Web UI 提供功能齊全的網頁儀表板：
* **系統狀態監控**：即時 CPU、記憶體使用率、網路流量速率曲線。
* **開關檔位酬載指派**：點選 Switch 1、2、3 直接線上下載或替換酬載。
* **外傳日誌檢索**：一鍵打包下載 `loot/` 目錄中的 pcap 封包截獲檔與登入憑證。
* **端點機 Web Terminal**：無需第三方客戶端，直接在瀏覽器視窗中操作 Linux Bash Shell。

---

### 2.4 讓設備連線上網 (Getting the Packet Squirrel online)

當 Network 埠連接至具備 DHCP 伺服器的企業局域網時，Packet Squirrel 會自動在背景取得 IP 並連上網際網路，以便執行軟體套件更新或與 Cloud C² 連線。

---

### 2.5 LED 狀態指示燈號定義 (Status LED)

| 燈號表現 | 系統運作狀態說明 |
|---|---|
| 綠燈閃爍 (Green blinking) | 系統初始化開機中 |
| 藍燈閃爍 (Blue blinking) | 維護模式就緒 (Arming Mode) |
| 紫燈/洋紅 (Magenta) | 酬載正在初始化設定中 (SETUP) |
| 黃燈 (Yellow) | 酬載執行中 (ATTACK) |
| 固態綠燈 (Solid Green) | 酬載執行圓滿成功 (SUCCESS) |
| 固態紅燈 (Solid Red) | 執行失敗或網路連線逾時 (FAIL) |
| 紅藍交替閃爍 | 韌體燒錄更新中，**切勿拔除電源** |

---

### 2.6 Hak5 Cloud C² 雲端納管 (Cloud C²)

透過 Cloud C²，滲透測試團隊可遠端集中管理散佈於各地的 Packet Squirrel：
1. 於 Cloud C² 伺服器新增 Packet Squirrel 設備並下載 `device.config`。
2. 透過 Web UI 或隨身碟將該檔案放入設備根目錄。
3. 只要設備接入任何可連外網路，即自動反彈建立 WebSocket 加密通道，實現跨防火牆遠端 Shell 與即時外發。

---

### 2.7 USB 儲存裝置支援 (USB storage support)

插入 USB 隨身碟時，系統會自動將其掛載至 `/mnt/loot/`。若偵測到隨身碟，封包抓取與大量外傳日誌將優先寫入外部隨身碟，以保護內部快閃記憶體壽命。

---

<!-- section：configuration -->
### 2.8 選擇與編輯酬載 (Selecting and editing payloads)

實體開關具備 4 個檔位：
* **Switch 1**：執行 `/root/payloads/switch1/payload.sh`
* **Switch 2**：執行 `/root/payloads/switch2/payload.sh`
* **Switch 3**：執行 `/root/payloads/switch3/payload.sh`
* **Arming Mode**：進入維護模式，不執行任何攻擊酬載

---

### 2.9 設定酬載參數 (Configuring payloads)

標準酬載多支援獨立的設定檔 `config.txt`，便於快速自訂目標 IP、監聽連接埠或外聯伺服器位址，無需修改核心 shell 腳本。

---

### 2.10 執行酬載 (Running payloads)

撥動切換開關至所需檔位（例如 Switch 1），將設備串接於目標網路線路並通電。系統開機後將依序執行初始化、環境檢查、網路架構設定，並以 LED 燈號即時回報執行進度。

---

### 2.11 網路拓撲與運作模式 (Networking and modes)

透過核心指令 `NETMODE`，可在酬載中隨意切換底層網路行為：
* `NETMODE BRIDGE`：硬體網橋模式，兩端直通，完全透明。
* `NETMODE NAT`：NAT 路由模式，設備充當目標的預設閘道器。
* `NETMODE ISOLATE`：切斷 Target 端網路，完全隔離。

---

## 3. 網路基礎理論與封包操弄教學

### 3.1 網路技術詞彙表 (Networking Glossary)
* **MAC 位址**：實體網路卡燒錄的 48 位元硬體識別碼。
* **ARP 協定**：將 IP 位址解析為實體 MAC 位址之協定。
* **DHCP**：動態主機設定協定，自動分配 IP、子網路遮罩與預設閘道。
* **DNS**：網域名稱系統，將網域名稱轉換為 IP 位址。

---

### 3.2 OSI 七層模型實務解析 (OSI layers)
* **實體層 (L1)**：雙絞線訊號傳輸。
* **資料鏈結層 (L2)**：乙太網路訊框 (Ethernet Frame) 與 MAC 路由。
* **網路層 (L3)**：IP 封包路由與 ICMP 控制。
* **傳輸層 (L4)**：TCP 連線與 UDP 資料報。
* **應用層 (L7)**：HTTP、SSH、DNS 等高階應用服務。

---

### 3.3 私有 IP 網段劃分 (Private IP ranges)
RFC 1918 規範之三大保留網段：
* `10.0.0.0/8`
* `172.16.0.0/12`（Packet Squirrel 本機預設使用 `172.16.32.0/24`）
* `192.168.0.0/16`

---

### 3.4 子網路遮罩運算 (Network masks)
遮罩決定了網路位址與主機位址的邊界。CIDR 標記法（如 `/24` 對應 `255.255.255.0`，可用主機數為 254 台）。

---

### 3.5 封包注入技術 (Packet injection)
封包注入允許未經請求逕向目標發送偽造資料包。透過原始套接字（Raw Socket）或 Scapy 工具，Packet Squirrel 能注入偽造的 TCP Reset 封包強制中斷特定連線，或注入惡意 DNS 回覆。

---

### 3.6 網路位址轉譯與重定向 (Translation and redirection)
利用 Linux `iptables` 核心能力，Packet Squirrel 能執行 DNAT（目的位址轉譯）與 SNAT（來源位址轉譯），將目標使用者的 HTTP 80 流量靜默重定向至本機搭建的釣魚伺服器。

---

### 3.7 封包截獲實戰 (Packet capture)
利用內建的 `tcpdump` 工具，可依條件精準側錄特定協議流量：
```bash
# 截獲目標所有 DNS 查詢封包並儲存為 pcap 格式
tcpdump -i br-lan -nn port 53 -w /mnt/loot/dns_traffic.pcap
```

---

## 4. 酬載開發與 DuckyScript 指令集

### 4.1 酬載開發基礎 (Payload development basics)
每個檔位的酬載均包含 `payload.sh` 執行檔。系統執行時以標準 POSIX Shell 環境載入，並預先注入 Packet Squirrel 專用指令集函式庫。

---

### 4.2 DuckyScript for Packet Squirrel 語法體系
相較於 Rubber Ducky 的單純按鍵注入，Packet Squirrel 的 DuckyScript 聚焦於**網路自動化操弄**、**背景行程監控**與**雲端聯動**。

---

### 4.3 BUTTON 微動按鈕監聽指令
* `BUTTON`：暫停酬載執行，等待使用者按下機身實體微動按鈕後方可繼續。適用於由現場滲透人員手動控制攻擊發動時機。

---

### 4.4 C2EXFIL 雲端資料外傳指令
* `C2EXFIL <檔案路徑>`：透過已連線的 Cloud C² 加密通道，將截獲之日誌或封包檔自動上傳至雲端伺服器。

---

### 4.5 C2NOTIFY 雲端告警通知指令
* `C2NOTIFY <訊息內容>`：向 Cloud C² 控制台發送高優先級警報事件通知。

---

### 4.6 C2WATCHDIR 目錄自動同步指令
* `C2WATCHDIR <目錄路徑>`：監控指定目錄，一旦目錄內產生新的檔案（如 pcap 或 txt），即時在背景自動排程上傳至 Cloud C²。

---

### 4.7 DYNAMICPROXY 動態代理通道指令
* `DYNAMICPROXY`：啟用本機 SOCKS5 動態代理通道，方便滲透測試人員透過遠端穿透進目標局域網內網。

---

### 4.8 KILLPORT 通訊埠強制中斷指令
* `KILLPORT <連接埠號>`：強制終止正在該通訊埠上傳輸的 TCP 連線。

---

### 4.9 KILLSTREAM 封包串流中斷指令
* `KILLSTREAM <連線特徵>`：針對特定來源與目的 IP 的連線串流發送 RST 封包予以切斷。

---

### 4.10 LED 狀態指示燈控制指令
* `LED SETUP`（設定中，洋紅）、`LED ATTACK`（攻擊中，黃燈）、`LED SUCCESS`（成功，固態綠燈）、`LED FAIL`（失敗，固態紅燈）、`LED OFF`（熄滅）。

---

### 4.11 MATCHPORT 通訊埠流量比對指令
* `MATCHPORT <連接埠號>`：在背景持續監聽，當受測主機發起針對該通訊埠的網路請求時觸發特定回呼函數。

---

### 4.12 MATCHSTREAM 串流特徵匹配指令
* `MATCHSTREAM <正則表達式>`：深度封包檢測（DPI），匹配 TCP/UDP 負載中的明文字串（如使用者名稱或金鑰）。

---

### 4.13 NETMODE 網路交換拓撲切換指令
* `NETMODE BRIDGE`：網橋透傳。
* `NETMODE NAT`：路由轉發。
* `NETMODE ISOLATE`：完全隔離。

---

### 4.14 SELFDESTRUCT 緊急資料銷毀指令
* `SELFDESTRUCT`：在遭遇現場查緝等極端狀況下，自動抹除本機儲存之金鑰、日誌與敏感設定，確保作戰安全。

---

### 4.15 SSH_START 與 SSH_STOP 服務控制指令
* `SSH_START`：動態開啟本機 Dropbear SSH 服務。
* `SSH_STOP`：動態關閉 SSH 服務以收斂系統暴露面。

---

### 4.16 SPOOFDNS 網域名稱偽冒欺騙指令
* `SPOOFDNS <網域名稱> <目標 IP>`：啟動本機 DNS 投毒引擎，將受測主機針對特定網址的查詢請求劫持導向至指定伺服器。

---

### 4.17 SWITCH 開關檔位查詢指令
* `SWITCH`：回傳目前硬體開關所在的位置程式碼（1，2，3 或 arming）。

---

### 4.18 UI_START 與 UI_STOP 網頁介面控制指令
* `UI_START`：啟動 Web UI 網頁伺服器。
* `UI_STOP`：在實戰攻擊期間關閉 Web UI 以節省系統資源並避免被目標發現。

---

### 4.19 USB_FREE、USB_STORAGE 與 USB_WAIT 隨身碟控制指令
* `USB_WAIT`：暫停執行，等待外部 USB 隨身碟插入。
* `USB_STORAGE`：取得目前掛載隨身碟之路徑。
* `USB_FREE`：查詢隨身碟剩餘可用儲存容量。

---

## 5. 高階酬載工程與自動化腳本技術

### 5.1 高階酬載架構 (Advanced payloads)
高階酬載能結合條件判斷、動態網路環境探測以及多協定聯動，具備自適應（Adaptive）作戰能力。

---

### 5.2 變數擴展與引號跳脫 (Quotes and expansions)
在編寫包含 awk 或 sed 的複雜 shell 指令時，應精確使用單引號 `'`（防止變數提前展開）與雙引號 `"`（允許變數替換）。

---

### 5.3 條件分支與流程控制 (Flow control)
透過標準 `if [ ... ]；then ... fi` 與 `case ... esac` 控制攻擊邏輯分支。

---

### 5.4 標準輸出與重定向技巧 (Redirecting output)
* `> /dev/null 2>&1`：靜默執行指令，避免日誌輸出干擾端點。
* `>> /mnt/loot/results.txt`：附加寫入日誌檔案。

---

### 5.5 酬載自訂參數檔 (Payload configuration)
在酬載資料夾建立 `config.env`，並於 `payload.sh` 開頭以 `source config.env` 載入，實現邏輯與組態參數解耦。

---

### 5.6 返回碼驗證與成功判定 (Return codes & success)
每條關鍵指令執行完畢後，檢查 `$?` 返回值，若不等於 0 則呼叫 `LED FAIL` 並記錄錯誤日誌。

---

### 5.7 背景常駐任務管理 (Background commands)
使用 `&` 將耗時的監聽行程放入背景運作，並利用 `$!` 記錄其行程 ID（PID），以便在收尾階段透過 `kill` 正確釋放資源。

---

### 5.8 指令群組化執行 (Command groups)
利用大括號 `{ cmd1；cmd2；}` 將多個指令綁定為單一執行區塊，方便統一重定向或實施逾時控制。

---

### 5.9 JSON 格式資料解析 (Processing JSON)
內建 `jq` 工具，可高效率提取 RESTful API 回傳之 JSON 節點資料：
```bash
TOKEN=$(curl -s http://api.internal/auth | jq -r .access_token)
```

---

### 5.10 USB 隨身碟硬體加密 (USB encryption)
支援 LUKS 加密磁區。只有在輸入正確金鑰後方可解密掛載外傳分區，即使設備於現場遺失亦能確保情報資料絕對保密。

---

### 5.11 VPN 服務端與客戶端設定 (VPN configuration)
* **WireGuard**：透過 `wg-quick up /etc/wireguard/wg0.conf` 建立毫秒級 VPN 隧道。
* **OpenVPN**：支援 TCP 443 偽裝流量，繞過嚴格的企業企業防火牆出口審查。

---

### 5.12 網路封包深度操弄 (Network manipulation)
結合 `iptables`、`ebtables` 與 `tc`（流量控制）工具，模擬網路延遲、封包遺失或進行中間人透明 SSL 降級。

---

### 5.13 實戰避坑與排錯指南 (Tips，tricks，& pitfalls)
* **避免在唯讀分區大量寫入**：確保暫存檔案寫入記憶體虛擬磁碟 `/tmp`。
* **妥善處理 DHCP 租約衝突**：切換 NETMODE 時務必重新啟動本機 dnsmasq 服務。

---

### 5.14 Python 3 整合自動化開發 (Python on Packet Squirrel)
Packet Squirrel 完整內建 Python 3 直譯器，可直接執行複雜的多執行緒掃描器、協定模擬伺服器及自訂封包解析腳本。

---

### 5.15 官方酬載儲存庫 (Payload repository)
Hak5 官方維護了龐大的開源酬載庫，涵蓋 TCP 劫持、DNS 偽冒、NTLMv2 憑證抓取等數十種戰術範本。

---

## 6. 故障排除、設備維護與韌體升級

### 6.1 網路通訊排錯指引 (Troubleshooting networking)
若目標主機無法取得 IP，請檢查實體網路線是否插反（Network vs Target），或使用 `ifconfig` 與 `brctl show` 檢查網橋狀態。

---

### 6.2 酬載腳本除錯指引 (Troubleshooting payloads)
於維護模式下以手動方式執行腳本：
```bash
bash -x /root/payloads/switch1/payload.sh
```
觀察每行指令展開後的詳細執行過程，迅速定位語法錯誤。

---

### 6.3 原廠出廠還原重置 (Factory reset)
若系統密碼遺失或設定損壞：
1. 拔除電源，將開關撥至維護模式。
2. 長按微動按鈕不放，同時插入 USB-C 電源開機。
3. 持續按住按鈕 10 秒以上，直到 LED 呈現紅燈快速閃爍後放開。
4. 設備將自動執行重置並恢復至原廠初始映像檔。

---

<!-- section：maintenance -->
### 6.4 韌體升級標準作業程序 (Upgrading firmware)

Hak5 團隊持續推出新韌體以提升系統效能與防護力：
1. 進入維護模式，由瀏覽器開啟 Web UI。
2. 進入「Settings」$ightarrow$「Firmware Update」分頁。
3. 點選「Check for Updates」進行線上自動升級，或上傳本地下載之韌體更新檔（`.bin`）。
4. 升級期間 LED 將紅藍交替閃爍，約耗時 3 至 5 分鐘。
5. 升級完成後系統將自動重新開機回到維護模式。

> [!CAUTION]
> 韌體升級進行中，**絕對不可中斷電源**，否則將造成系統啟動引導區損毀。
