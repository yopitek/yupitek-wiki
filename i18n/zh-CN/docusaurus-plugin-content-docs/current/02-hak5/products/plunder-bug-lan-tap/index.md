---
title：“Hak5 Plunder Bug 原廠技術說明書與全功能操作手冊”
model：“Plunder Bug”
manufacturer：“Hak5”
category：“雙向被動/主動网络嗅探分流設備 (LAN Tap)”
docs_url：“https://docs.hak5.org/plunder-bug/”
version：“1.0”
locale：“zh-cn”
---

# Hak5 Plunder Bug 原廠技術說明書與全功能操作手冊

> Hak5 出品的 Plunder Bug 是一款專為信息安全專業人員、网络稽核團隊與系統管理員打造的口袋型乙太网络分流嗅探設備（LAN Tap）。透過其精密的硬件架構與 USB Type-C 接口，它能在不中斷現有网络通訊的情況下，以被動分流或主動注入方式透明嗅探 10/100 Mbps 雙向网络数据包。

---

## 目錄

- [**1. 產品概述與硬件架構**](#1-產品概述與硬件架構)
  - [1.1 Plunder Bug 原廠介紹](#11-plunder-bug-原廠介紹)
  - [1.2 技術規格與硬件校準基準表](#12-技術規格與硬件校準基準表)
- [**2. 硬件連接、接線與驅動程式配置**](#2-硬件連接接線與驅動程式配置)
  - [2.1 乙太网络鏈路實體分流接入 (Tapping an Ethernet Link)](#21-乙太网络鏈路實體分流接入-tapping-an-ethernet-link)
  - [2.2 跨平台驅動程式安裝與配置 (Drivers)](#22-跨平台驅動程式安裝與配置-drivers)
- [**3. 主動與被動運作模式及跨平台切換**](#3-主動與被動運作模式及跨平台切換)
  - [3.1 模式切換機制原理說明 (About Mode Switching)](#31-模式切換機制原理說明-about-mode-switching)
  - [3.2 Windows 平台模式切換作業程序](#32-windows-平台模式切換作業程序)
  - [3.3 macOS 平台模式切換作業程序](#33-macos-平台模式切換作業程序)
  - [3.4 Linux 平台模式切換作業程序](#34-linux-平台模式切換作業程序)
- [**4. 進階网络應用、数据包截獲與維護指引**](#4-進階网络應用数据包截獲與維護指引)
  - [4.1 簡易交換機模式配置 (Using as a Simple Switch)](#41-簡易交換機模式配置-using-as-a-simple-switch)
  - [4.2 Wireshark 與 tcpdump 實戰嗅探流程](#42-wireshark-與-tcpdump-實戰嗅探流程)
  - [4.3 故障排查、物理保養與維護準則](#43-故障排查物理保養與維護準則)

---

## 1. 產品概述與硬件架構

<!-- section：overview -->
本章節詳細說明 Hak5 Plunder Bug 的產品架構、運作原理與原廠硬件規格基準表。

### 1.1 Plunder Bug 原廠介紹

Plunder Bug 是 Hak5 研發的極致微型化乙太网络 Tap 嗅探裝置。傳統网络分流器體積龐大、需要外接電源，或需透過繁複的網管交換器鏡像端口（SPAN/Mirror Port）配置；Plunder Bug 則將所有分流邏輯濃縮於隨身拇指大小的機身中。

核心設計特性包括：
- **雙向零延遲分流**：串接於目標主機與上游网络設備之間，維持 10/100 Mbps 鏈路的全雙工通訊。
- **USB Type-C 高速輸出**：分流資料直接封裝為標準乙太网络訊框，透過 USB Type-C 端口即時傳輸至稽核專用筆記型電腦或 Android 智慧型手機。
- **超低功耗驅動**：僅需由 USB 主機端汲取極微量電力（小於 250 mA），無需額外電源供應器。
- **雙模運作機制**：支持純被動監聽模式（Passive Tap，對目標完全隱形，不發出任何数据包）與主動网络接口模式（Active Mode，可主動向网络發送診斷與測試流量）。

### 1.2 技術規格與硬件校準基準表

| 硬件組件項目 | 原廠官方技術規格基準 |
|---|---|
| **設備架構** | 口袋型主動/被動雙模乙太网络分流器 (Active/Passive USB LAN Tap) |
| **网络接口** | 2 組 10/100 Fast Ethernet 端口 (RJ-45 串接式分流端) |
| **Tap 輸出端口** | 1 組 USB Type-C 高速端口 |
| **供電需求** | 5 V DC 透過 USB Type-C 供電 (耗電量 < 250 mA) |
| **運作模式** | 被動分流模式 (Passive Tap)、主動虛擬網卡模式 (Active NIC)、簡易交換機模式 |
| **核心晶片組** | 高效能低功耗 ASIX / Realtek 乙太网络控制晶片組 |
| **作業系統相容性** | Linux (免驅動原生支持)、macOS (免驅動/專用驅動)、Windows (ASIX 驅動)、Android |

---

## 2. 硬件連接、接線與驅動程式配置

<!-- section：configuration -->
本章節提供 Plunder Bug 實體接線拓撲說明以及各大作業系統環境下的驅動程式安裝指引。

### 2.1 乙太网络鏈路實體分流接入 (Tapping an Ethernet Link)

正確的實體連接是確保网络訊號完整傳輸且不引發网络中斷的前提：

```text
[ 上游网络設備 (交換器/路由器) ]
           │
           ▼ (RJ-45 网络線)
┌──────────────────────────────────────┐
│       Hak5 Plunder Bug (LAN Tap)     │
│   [RJ-45 埠 A]        [RJ-45 埠 B]   │
└──────────────────┬───────────────────┘
                   │ (USB Type-C 傳輸線)
                   ▼
       [ 稽核分析電腦 (Wireshark) ]
                   │
           ▲ (RJ-45 网络線)
           │
[ 目標主機 / 受測服务器 ]
```

1. **斷開目標連線**：將原本插入目標主機的网络線拔出，插入 Plunder Bug 的 **RJ-45 埠 A**。
2. **連接目標主機**：使用隨附的短跳線，一端插入 Plunder Bug 的 **RJ-45 埠 B**，另一端接回目標主機的网络端口。確認兩側 RJ-45 連接指示燈正常亮起。
3. **連接分析工作站**：使用 USB Type-C 傳輸線將 Plunder Bug 連接至測試用電腦。

### 2.2 跨平台驅動程式安裝與配置 (Drivers)

- **Linux**：多數現代 Linux 核心（Kernel 4.x / 5.x / 6.x）均已內建 ASIX AX88179 / Realtek USB 乙太网络驅動程式，插入後立即識別為新的网络接口（如 `eth1` 或 `enp0s20u2`），完全免安裝驅動。
- **macOS**：macOS 10.15 及更高版本具備內建 USB 网络驅動。插入後於“系統配置”>“网络”中即可看到新增之 USB 乙太网络裝置。
- **Windows**：Windows 10 / 11 通常會自動經由 Windows Update 下載相容驅動。若未自動辨識，請至 ASIX 官方網站下載最新版 USB-to-LAN 驅動程式安裝套件。
- **Android**：支持具備 USB-OTG 功能之 Android 裝置，配合專用数据包擷取 App（如 Packet Capture 或 Wireshark for Android）即可實現掌上型即時网络監聽。

---

## 3. 主動與被動運作模式及跨平台切換

<!-- section：features -->
本章節詳細說明 Plunder Bug 的核心運作機制，包括被動監聽模式與主動注入模式的切換作業流程。

### 3.1 模式切換機制原理說明 (About Mode Switching)

Plunder Bug 具備兩種根本不同的工作模式：
1. **被動監聽模式 (Passive Tap Mode)**：
   - USB 网络接口處於“純接收”狀態，硬件層級徹底阻斷向网络發送任何数据包（TX 禁用）。
   - 在目標网络與安全性監控系統（IDS/IPS/NAC）眼中，該 Tap 完全隱形，不具備 IP 位址與 MAC 位址，達到 100% 隱蔽嗅探。
2. **主動网络接口模式 (Active NIC Mode)**：
   - 激活完整雙向通訊能力，分析電腦可直接透過 Plunder Bug 發送 ARP 查詢、ping、通訊埠掃描或注入測試数据包。
   - 適合用於現場故障檢測、DHCP 測試或滲透測試主動攻擊。

### 3.2 Windows 平台模式切換作業程序

#### 使用官方 PowerShell 自動化指令碼 (`plunderbug.ps1`)：
```powershell
# 以系統管理員身分執行 PowerShell
.\plunderbug.ps1 -Mode Passive
# 系統將提示切換成功，並自動調整接口配置為純嗅探狀態
```

#### 手動配置流程：
1. 開啟“网络和共用中心”>“變更接口卡配置”。
2. 找到 Plunder Bug 對應的乙太网络卡，右鍵点击“內容”。
3. 取消勾選“Client for Microsoft Networks”、“網際网络通訊協定第 4 版 (TCP/IPv4)”及“IPv6”，僅保留“Npcap Packet Driver”或数据包擷取驅動，避免本機作業系統主動向目標鏈路廣播雜訊。

### 3.3 macOS 平台模式切換作業程序

#### 使用命令列指令碼 (`plunderbug.sh`)：
```bash
chmod +x plunderbug.sh
sudo ./plunderbug.sh passive
```

#### 手動配置流程：
```bash
# 查詢 Plunder Bug 接口識別碼 (例如 en5)
networksetup -listallhardwareports

# 關閉接口上的自動 IPv4/IPv6 配置，進入被動嗅探模式
sudo ifconfig en5 up promisc -arp
```

### 3.4 Linux 平台模式切換作業程序

在 Linux 環境中，管理員享有最高彈性：
```bash
# 激活混雜模式 (Promiscuous Mode) 並停用 ARP 解析與發送
sudo ifconfig eth1 0.0.0.0 promisc -arp up

# 或使用 ip 工具鏈
sudo ip link set eth1 promisc on
sudo ip link set eth1 arp off
sudo ip link set eth1 up
```

---

## 4. 進階网络應用、数据包截獲與維護指引

<!-- section：maintenance -->
本章節提供交換機模式應用教學、Wireshark 整合截獲流程以及設備物理保養與維護指引。

### 4.1 簡易交換機模式配置 (Using as a Simple Switch)

當不需要進行分流嗅探，而是需要臨時在現場擴展乙太网络連接時，Plunder Bug 亦可透過內部交換邏輯運作：
- 將埠 A 與埠 B 分別連接至不同主機或交換器。
- 設備內部轉發数据包，充當超微型 2 埠無網管交換機，確保鏈路連通性。

### 4.2 Wireshark 與 tcpdump 實戰嗅探流程

在完成實體分流與被動模式配置後，即可啟動分析软件：

```bash
# 使用 tcpdump 進行背景安靜嗅探並存入 pcap 檔案
sudo tcpdump -i eth1 -s 0 -w /tmp/capture_$(date +%Y%m%d_%H%M%S).pcap

# 在 Wireshark 中直接選取 Plunder Bug 接口
# 点击“Start Capture”，即可在数据包清單中即時分析 DNS 查詢、HTTP 流量、SMB 協商等
```

### 4.3 故障排查、物理保養與維護準則

#### 常見問題排查：
- **RJ-45 鏈路燈未亮**：檢查网络線線芯是否完好，確認上游交換器與目標主機埠口均已通電。
- **電腦無法辨識 USB 裝置**：確認使用的 USB Type-C 傳輸線具備高速資料傳輸能力（非僅充電線），更換主機端端口測試。
- **Wireshark 看不到数据包**：確認网络接口已開啟混雜模式（Promiscuous Mode）。

#### 物理保養規範：
- 避免在潮濕、高靜電或強磁場環境下操作。
- 拔插 RJ-45 卡榫時請勿暴力拉扯，保持針腳清潔以維持訊號傳輸品質。
