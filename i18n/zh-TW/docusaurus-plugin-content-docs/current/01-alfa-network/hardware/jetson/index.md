---
id: alfa-hardware-jetson
title: ALFA 網卡在 NVIDIA Jetson (Orin Nano / NX) 上的整合與設定指南
sidebar_label: NVIDIA Jetson
sidebar_position: 1
description: ALFA 無線網絡卡在 NVIDIA Jetson Orin Nano / NX 上的整合教學——6 GHz Wi-Fi 6E 串流、監聽模式啟用與 JetPack 核心驅動設定，含每一步的預期結果。
tags: [alfa, jetson, nvidia, robotics, wifi-6e, monitor-mode]
keywords: [Jetson Orin ALFA, Jetson Wi-Fi 6E, AWUS036AXML Jetson, 機器人無線傳輸, JetPack 驅動]
---

# ALFA 無線網絡卡在 NVIDIA Jetson 上（Orin Nano / NX）

> **一句話定位**：Jetson 內建的 Wi-Fi 天線很弱，做機器人或電腦視覺專案時常常撐不住。裝上一支 ALFA 無線網絡卡，就能讓 Jetson 用 6 GHz 頻段（Wi-Fi 6E）低延遲串流影像，或啟用監聽模式做無線研究。

## 這篇文章適合你嗎？

- **難度**：入門〜中階（會下 Linux 終端機指令即可，不需要寫程式）
- **預估時間**：30〜60 分鐘（含系統更新與驅動編譯時間）
- **你會用到的技能**：基本終端機操作（複製貼上指令、看懂指令輸出）
- **讀完你可以做到**：
  1. 確認自己的 Jetson 該走哪一條驅動安裝路徑
  2. 讓 ALFA 無線網絡卡在 Jetson 上被正確辨識
  3. 用 6 GHz 頻段做低延遲攝影機串流，或啟用監聽模式做封包擷取

---

## 概念說明：為什麼 Jetson 需要外接無線網絡卡

Jetson Orin Nano / NX 主機板（含它的載板）出廠就帶了一顆無線網卡，但那顆網卡的設計目標只是「能上網、能 `apt update`」，不是為了機器人或電腦視覺這種對頻寬、延遲要求更高的應用設計的。如果你的專案需要下面任何一項，內建網卡通常不夠用：

- **6 GHz（Wi-Fi 6E）頻段**：Jetson 載板的內建網卡只有 2.4 GHz 和 5 GHz。6 GHz 是一個相對「空曠」、雜訊少的頻段，很適合拿來即時傳攝影機畫面或光達（LiDAR）點雲資料，不用跟同一間實驗室裡一堆人的 2.4 GHz 裝置搶頻寬。
- **穩定的高吞吐量連線**：目前 ALFA 產品線裡唯一支援 6 GHz 的無線網絡卡是 **AWUS036AXML**，晶片是 MT7921AUN，而且它的驅動程式從 Linux 核心 5.18 版之後就已經內建，不用自己編譯。
- **監聽模式（Monitor Mode）**：如果你的專案是做無線網路研究（例如分析封包），可以透過標準的 `mac80211` 驅動路徑，在支援的晶片上直接啟用監聽模式。

> 📘 **名詞小教室**
> - **監聽模式（Monitor Mode）**：讓網卡不只接收「要給自己的」封包，而是把空氣中飛過的所有無線封包都抓下來，是做無線網路分析、Wireshark 課程作業的基礎模式。一般上網用的「Managed 模式」做不到這件事。
> - **DKMS（Dynamic Kernel Module Support）**：一種讓驅動程式「跟著核心版本自動重新編譯」的機制。白話說：以後系統更新核心版本，DKMS 會自動幫你的網卡驅動重新編譯一次，不用每次都手動重裝。
> - **JetPack**：NVIDIA 官方為 Jetson 系列準備的完整系統套件（包含客製化的 Linux 核心、驅動程式、開發工具）。JetPack 的版本會直接決定你的 Jetson 用的是哪個核心版本，這對能不能用某些網卡晶片有直接影響。
> - **L4T（Linux for Tegra）**：Jetson 專用的 Linux 核心，不是一般 Ubuntu 桌機用的核心，所以核心版本命名和更新方式跟一般 Linux 教學看到的不太一樣。

Jetson 能用哪種驅動路徑，關鍵在於你的 **JetPack 版本**（決定核心版本）：

| JetPack 版本 | L4T 核心版本 | `mt7921u`（AWUS036AXM / AXML 適用） | `mt76x2u`（AWUS036ACM / ACHM 適用） |
| ------------ | ------------ | ------------------------------------ | ------------------------------------ |
| JetPack 5.x  | 5.10         | ❌ 核心太舊，不支援                  | ✅ 支援                              |
| JetPack 6.x  | 6.6          | ✅ 支援                              | ✅ 支援                              |

**記住這條規則**：如果你買的是 **AWUS036AXML**（要用 6 GHz），你的 Jetson 一定要是 **JetPack 6**。如果你用的是經典款 **AWUS036ACM**，JetPack 5 或 6 都可以用。

---

## 你需要準備的東西

- [ ] **硬體**：已安裝好 JetPack 的 NVIDIA Jetson Orin Nano 或 Orin NX
- [ ] **網路環境**：第一次設定建議先接乙太網路線（避免因為 Wi-Fi 沒設好而連不上機器除錯）
- [ ] **ALFA 無線網絡卡**：
  - 要用 6 GHz（Wi-Fi 6E）：[AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)（需要 JetPack 6）
  - 一般用途、相容性最廣：[AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)（JetPack 5 / 6 都可以）
- [ ] **驅動程式參考（GitHub）**：
  - MediaTek MT76 系列驅動（社群維護的獨立可安裝版本，含 DKMS，適用 MT7612U / MT7921 系列晶片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驅動（aircrack-ng 社群維護，支援 ARM64）：https://github.com/aircrack-ng/rtl8812au
- [ ] 若使用高功率無線網絡卡，建議準備一個**有獨立供電的 USB Hub**（Jetson 的 USB 連接埠在高負載時可能供電不足）

---

## Step-by-Step 設定教學

### 步驟 1：檢查你的 JetPack 版本與核心版本

在開始之前，先確認自己屬於上面表格的哪一列。打開終端機，輸入：

```bash
uname -r
dpkg -l | grep nvidia-l4t-core | head -1
```

**預期結果**：你會看到類似下面兩種其中一種輸出：

```text
6.6.0-tegra            # JetPack 6 — 支援 mt7921u（AXM / AXML 系列）
# 或
5.10.104-tegra          # JetPack 5 — 只支援 MT7612U 這類舊晶片（ACM / ACHM 系列）
```

如果你看到的是 `5.10.x`，代表你目前只能用 AWUS036ACM 這類 MT7612U 晶片的網卡；如果要用支援 6 GHz 的 AWUS036AXML，需要先把 Jetson 升級到 JetPack 6。

---

### 步驟 2：MediaTek 內建於核心的路徑（建議優先嘗試）

這是最省事的路徑：MediaTek 晶片的驅動已經寫進 Linux 核心裡，插上網卡通常不用額外裝任何東西。

把 ALFA 無線網絡卡插上 Jetson 的 USB 埠，然後：

```bash
lsusb | grep -i mediatek
iw dev
```

**預期結果**：`lsusb` 那行應該會看到類似這樣的輸出：

```text
Bus 001 Device 002: ID 0e8d:7961 MediaTek Corp. MT7921U
```

`iw dev` 則會看到一個新的無線介面，例如：

```text
phy#0
	Interface wlan0
		ifindex 3
		type managed
```

如果你用的是 JetPack 6 + AWUS036AXML，可以再確認 6 GHz 頻道有沒有被系統看見：

```bash
iwlist wlan0 freq | grep -E "6 GHz|Channel 1|Channel 233" | head
```

**如果什麼都沒出現**：通常是法規領域（國家代碼）還沒設定，執行以下指令後重新啟用介面即可：

```bash
sudo iw reg set TW
sudo ip link set wlan0 down && sudo ip link set wlan0 up
```

> 💡 這裡的 `TW` 是台灣的國家代碼，如果你人在其他國家，請換成對應的代碼。

---

### 步驟 3：連線並測試串流

先確認網卡能正常連上一個 Wi-Fi 網路：

```bash
nmcli device wifi connect "你的SSID" password "你的密碼"
```

**預期結果**：

```text
Device 'wlan0' successfully activated with 'MySSID'.
```

連上之後，如果你的專案是要串流攝影機畫面，可以用下面這段指令測試（範例用 GStreamer，走 6 GHz 頻段的低延遲串流）：

```bash
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! \
    x264enc tune=zerolatency bitrate=8000 ! rtph264pay ! \
    udpsink host=192.168.1.50 port=5000
```

**預期結果**：畫面應該是連續、低延遲的串流（把指令裡的 `192.168.1.50` 換成你接收端的實際 IP）。這就是 6 GHz 頻段的價值所在——空曠、少人搶頻寬，延遲會比擠在 2.4 GHz 上明顯低。

---

### 步驟 4：Realtek 機型的安裝路徑（如果你的網卡不是 MediaTek 晶片）

如果 `lsusb` 抓不到 MediaTek 裝置，代表你的網卡可能是 Realtek 晶片，需要額外編譯安裝驅動程式（也就是前面提到的 DKMS）。

Jetson 的 ARM64（aarch64）架構也可以編譯 DKMS 驅動，只是編譯時間會比一般桌機 Linux 慢一些，尤其在 Orin Nano 上請耐心等待：

```bash
sudo apt install -y build-essential dkms git
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

**預期結果**：最後一行會出現：

```text
DKMS: install completed.
```

在 Orin Nano 上這個步驟可能需要幾分鐘，不要中途中斷。

---

### 步驟 5：啟用監聽模式（無線研究 / 實驗室用途）

如果你的專案需要做封包分析而不只是連網，可以啟用監聽模式測試：

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**預期結果**：介面會變成 `wlan0mon`，並在測試時看到類似 `30/30: 100%` 的注入成功率，代表監聽模式運作正常。

> ⚠️ **供電提醒**：Orin Nano 的 USB 連接埠在高負載下可能供電不穩。如果你的網卡是高功率型號，建議搭配**有獨立供電的 USB Hub**。另外也留意 Jetson 的電源模式（`nvpmodel`）——如果目前是降頻的省電模式，也可能影響 USB 供電穩定度，可以嘗試切換到較高效能的電源模式。

---

## 常見問題與排除指引

### Q1：AWUS036AXML 在 JetPack 5 上完全看不到？
- **原因**：JetPack 5 的核心版本（5.10）還沒有內建 `mt7921u` 驅動模組。
- **解決方法**：升級到 JetPack 6（核心版本 6.6），或改用支援 MT7612U 晶片的 AWUS036ACM。

### Q2：明明設定好了，卻找不到 6 GHz 頻道？
- **原因**：法規領域（國家代碼）沒有設定，系統不知道該開放哪些頻道。
- **解決方法**：執行 `sudo iw reg set <你的國家代碼>`，再重新啟用網卡介面。

### Q3：跑攝影機串流時網卡常常斷線？
- **原因**：USB 供電不足，高負載時電壓不穩。
- **解決方法**：改用有獨立供電的 USB Hub；或把 Jetson 的電源模式（`nvpmodel`）調到較高效能等級。

### Q4：DKMS 編譯很慢，甚至失敗？
- **原因**：ARM64 架構本身編譯速度較慢，加上有時候缺少對應的核心標頭檔（headers）。
- **解決方法**：
  ```bash
  sudo apt install -y linux-headers-$(uname -r)
  ```
  裝好標頭檔後再重新執行 `sudo make dkms_install`。

### Q5：監聽模式怎麼樣都啟用不了？
- **原因**：通常是 Realtek 網卡的 stub 驅動程式（系統預設但功能陽春的驅動）跟你要用的完整版驅動互相打架。
- **解決方法**：確認你已經按照步驟 4 安裝好 aircrack-ng 版本的驅動程式，而不是系統自帶的陽春版。

---

## 參考資料與延伸閱讀

- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)——想用 6 GHz 就選這支
- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)——相容性最廣的全能款
- [ALFA 無線網絡卡在 Ubuntu 上的完整設定指南](/alfa-network/linux-setup-ubuntu/)——JetPack 骨子裡就是 Ubuntu，很多概念可以互通
- [ALFA 無線網絡卡在 Kali Linux 上——監聽模式與封包注入](/alfa-network/linux-setup-kali/)——監聽模式的延伸細節
- [ALFA 無線網絡卡在 Raspberry Pi 上（3 / 4 / 5）](/alfa-network/hardware/raspberry-pi/)——另一款輕量嵌入式主機的整合方式
- [詞彙表](/getting-started/glossary)——監聽模式、DKMS 等名詞的完整解釋
- MediaTek MT76 系列驅動（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驅動（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au
- [NVIDIA Jetson 官方文件](https://docs.nvidia.com/jetson/)

**標籤：** `alfa` `jetson` `nvidia` `機器人` `wifi-6e` `監聽模式` `新手指南`
