---
id: alfa-hardware-jetson
title: ALFA 网卡在 NVIDIA Jetson (Orin Nano / NX) 上的集成与设置指南
sidebar_label: NVIDIA Jetson
sidebar_position: 1
description: ALFA 无线网卡在 NVIDIA Jetson Orin Nano / NX 上的集成教程——6 GHz Wi-Fi 6E 流媒体、监听模式启用与 JetPack 内核驱动设置，含每一步的预期结果。
tags: [alfa, jetson, nvidia, robotics, wifi-6e, monitor-mode]
keywords: [Jetson Orin ALFA, Jetson Wi-Fi 6E, AWUS036AXML Jetson, 机器人无线传输, JetPack 驱动]
---

# ALFA 無線网卡在 NVIDIA Jetson 上（Orin Nano / NX）

> **一句話定位**：Jetson 內建的 Wi-Fi 天線很弱，做机器人或电脑視覺專案時常常撐不住。裝上一支 ALFA 無線网卡，就能讓 Jetson 用 6 GHz 频段（Wi-Fi 6E）低延遲串流影像，或啟用监听模式做無線研究。

## 這篇文章適合你嗎？

- **難度**：入門〜中階（會下 Linux 终端指令即可，不需要寫程式）
- **預估時間**：30〜60 分鐘（含系統更新與驱动编译時間）
- **你會用到的技能**：基本终端操作（複製貼上指令、看懂指令輸出）
- **讀完你可以做到**：
  1. 確認自己的 Jetson 該走哪一條驱动安裝路徑
  2. 讓 ALFA 無線网卡在 Jetson 上被正確辨識
  3. 用 6 GHz 频段做低延遲攝影機串流，或啟用监听模式做数据包擷取

---

## 概念說明：為什麼 Jetson 需要外接無線网卡

Jetson Orin Nano / NX 主機板（含它的載板）出廠就帶了一顆無線网卡，但那顆网卡的設計目標只是「能上網、能 `apt update`」，不是為了机器人或电脑視覺這種對頻寬、延遲要求更高的應用設計的。如果你的專案需要下面任何一項，內建网卡通常不夠用：

- **6 GHz（Wi-Fi 6E）频段**：Jetson 載板的內建网卡只有 2.4 GHz 和 5 GHz。6 GHz 是一個相對「空曠」、雜訊少的频段，很適合拿來即時傳攝影機畫面或光達（LiDAR）點雲数据，不用跟同一間实验室裡一堆人的 2.4 GHz 裝置搶頻寬。
- **穩定的高吞吐量连接**：目前 ALFA 產品線裡唯一支援 6 GHz 的無線网卡是 **AWUS036AXML**，芯片是 MT7921AUN，而且它的驱动程序從 Linux 内核 5.18 版之後就已經內建，不用自己编译。
- **监听模式（Monitor Mode）**：如果你的專案是做無線网络研究（例如分析数据包），可以透過標準的 `mac80211` 驱动路徑，在支援的芯片上直接啟用监听模式。

> 📘 **名詞小教室**
> - **监听模式（Monitor Mode）**：讓网卡不只接收「要給自己的」数据包，而是把空氣中飛過的所有無線数据包都抓下來，是做無線网络分析、Wireshark 課程作業的基礎模式。一般上網用的「Managed 模式」做不到這件事。
> - **DKMS（Dynamic Kernel Module Support）**：一種讓驱动程序「跟著内核版本自動重新编译」的機制。白話說：以後系統更新内核版本，DKMS 會自動幫你的网卡驱动重新编译一次，不用每次都手動重裝。
> - **JetPack**：NVIDIA 官方為 Jetson 系列準備的完整系統套件（包含客製化的 Linux 内核、驱动程序、開發工具）。JetPack 的版本會直接決定你的 Jetson 用的是哪個内核版本，這對能不能用某些网卡芯片有直接影響。
> - **L4T（Linux for Tegra）**：Jetson 專用的 Linux 内核，不是一般 Ubuntu 桌機用的内核，所以内核版本命名和更新方式跟一般 Linux 教學看到的不太一樣。

Jetson 能用哪種驱动路徑，關鍵在於你的 **JetPack 版本**（決定内核版本）：

| JetPack 版本 | L4T 内核版本 | `mt7921u`（AWUS036AXM / AXML 適用） | `mt76x2u`（AWUS036ACM / ACHM 適用） |
| ------------ | ------------ | ------------------------------------ | ------------------------------------ |
| JetPack 5.x  | 5.10         | ❌ 内核太舊，不支援                  | ✅ 支援                              |
| JetPack 6.x  | 6.6          | ✅ 支援                              | ✅ 支援                              |

**記住這條規則**：如果你買的是 **AWUS036AXML**（要用 6 GHz），你的 Jetson 一定要是 **JetPack 6**。如果你用的是經典款 **AWUS036ACM**，JetPack 5 或 6 都可以用。

---

## 你需要準備的東西

- [ ] **硬件**：已安裝好 JetPack 的 NVIDIA Jetson Orin Nano 或 Orin NX
- [ ] **网络環境**：第一次设置建議先接乙太网络線（避免因為 Wi-Fi 沒設好而連不上機器除錯）
- [ ] **ALFA 無線网卡**：
  - 要用 6 GHz（Wi-Fi 6E）：[AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)（需要 JetPack 6）
  - 一般用途、兼容性最廣：[AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)（JetPack 5 / 6 都可以）
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动（社群維護的獨立可安裝版本，含 DKMS，適用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（aircrack-ng 社群維護，支援 ARM64）：https://github.com/aircrack-ng/rtl8812au
- [ ] 若使用高功率無線网卡，建議準備一個**有獨立供電的 USB Hub**（Jetson 的 USB 連接埠在高負載時可能供電不足）

---

## Step-by-Step 设置教學

### 步骤 1：檢查你的 JetPack 版本與内核版本

在開始之前，先確認自己屬於上面表格的哪一列。打開终端，輸入：

```bash
uname -r
dpkg -l | grep nvidia-l4t-core | head -1
```

**預期結果**：你會看到類似下面兩種其中一種輸出：

```text
6.6.0-tegra            # JetPack 6 — 支援 mt7921u（AXM / AXML 系列）
# 或
5.10.104-tegra          # JetPack 5 — 只支援 MT7612U 這類舊芯片（ACM / ACHM 系列）
```

如果你看到的是 `5.10.x`，代表你目前只能用 AWUS036ACM 這類 MT7612U 芯片的网卡；如果要用支援 6 GHz 的 AWUS036AXML，需要先把 Jetson 升級到 JetPack 6。

---

### 步骤 2：MediaTek 內建於内核的路徑（建議優先嘗試）

這是最省事的路徑：MediaTek 芯片的驱动已經寫進 Linux 内核裡，插入网卡通常不用額外裝任何東西。

把 ALFA 無線网卡插入 Jetson 的 USB 埠，然後：

```bash
lsusb | grep -i mediatek
iw dev
```

**預期結果**：`lsusb` 那行應該會看到類似這樣的輸出：

```text
Bus 001 Device 002: ID 0e8d:7961 MediaTek Corp. MT7921U
```

`iw dev` 則會看到一個新的無線接口，例如：

```text
phy#0
	Interface wlan0
		ifindex 3
		type managed
```

如果你用的是 JetPack 6 + AWUS036AXML，可以再確認 6 GHz 信道有沒有被系統看見：

```bash
iwlist wlan0 freq | grep -E "6 GHz|Channel 1|Channel 233" | head
```

**如果什麼都沒出現**：通常是法規領域（國家代碼）還沒设置，執行以下指令後重新啟用接口即可：

```bash
sudo iw reg set TW
sudo ip link set wlan0 down && sudo ip link set wlan0 up
```

> 💡 這裡的 `TW` 是台灣的國家代碼，如果你人在其他國家，請換成對應的代碼。

---

### 步骤 3：连接並測試串流

先確認网卡能正常連上一個 Wi-Fi 网络：

```bash
nmcli device wifi connect "你的SSID" password "你的密碼"
```

**預期結果**：

```text
Device 'wlan0' successfully activated with 'MySSID'.
```

連上之後，如果你的專案是要串流攝影機畫面，可以用下面這段指令測試（示例用 GStreamer，走 6 GHz 频段的低延遲串流）：

```bash
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! \
    x264enc tune=zerolatency bitrate=8000 ! rtph264pay ! \
    udpsink host=192.168.1.50 port=5000
```

**預期結果**：畫面應該是連續、低延遲的串流（把指令裡的 `192.168.1.50` 換成你接收端的實際 IP）。這就是 6 GHz 频段的價值所在——空曠、少人搶頻寬，延遲會比擠在 2.4 GHz 上明顯低。

---

### 步骤 4：Realtek 機型的安裝路徑（如果你的网卡不是 MediaTek 芯片）

如果 `lsusb` 抓不到 MediaTek 裝置，代表你的网卡可能是 Realtek 芯片，需要額外编译安裝驱动程序（也就是前面提到的 DKMS）。

Jetson 的 ARM64（aarch64）架構也可以编译 DKMS 驱动，只是编译時間會比一般桌機 Linux 慢一些，尤其在 Orin Nano 上請耐心等待：

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

在 Orin Nano 上這個步骤可能需要幾分鐘，不要中途中斷。

---

### 步骤 5：啟用监听模式（無線研究 / 实验室用途）

如果你的專案需要做数据包分析而不只是連網，可以啟用监听模式測試：

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**預期結果**：接口會變成 `wlan0mon`，並在測試時看到類似 `30/30: 100%` 的注入成功率，代表监听模式運作正常。

> ⚠️ **供電提醒**：Orin Nano 的 USB 連接埠在高負載下可能供電不穩。如果你的网卡是高功率型号，建議搭配**有獨立供電的 USB Hub**。另外也留意 Jetson 的電源模式（`nvpmodel`）——如果目前是降頻的省電模式，也可能影響 USB 供電穩定度，可以嘗試切換到較高效能的電源模式。

---

## 常見問題與排除指引

### Q1：AWUS036AXML 在 JetPack 5 上完全看不到？
- **原因**：JetPack 5 的内核版本（5.10）還沒有內建 `mt7921u` 驱动模块。
- **解決方法**：升級到 JetPack 6（内核版本 6.6），或改用支援 MT7612U 芯片的 AWUS036ACM。

### Q2：明明设置好了，卻找不到 6 GHz 信道？
- **原因**：法規領域（國家代碼）沒有设置，系統不知道該開放哪些信道。
- **解決方法**：執行 `sudo iw reg set <你的國家代碼>`，再重新啟用网卡接口。

### Q3：跑攝影機串流時网卡常常斷線？
- **原因**：USB 供電不足，高負載時電壓不穩。
- **解決方法**：改用有獨立供電的 USB Hub；或把 Jetson 的電源模式（`nvpmodel`）調到較高效能等級。

### Q4：DKMS 编译很慢，甚至失敗？
- **原因**：ARM64 架構本身编译速度較慢，加上有時候缺少對應的内核標頭檔（headers）。
- **解決方法**：
  ```bash
  sudo apt install -y linux-headers-$(uname -r)
  ```
  裝好標頭檔後再重新執行 `sudo make dkms_install`。

### Q5：监听模式怎麼樣都啟用不了？
- **原因**：通常是 Realtek 网卡的 stub 驱动程序（系統默认但功能陽春的驱动）跟你要用的完整版驱动互相打架。
- **解決方法**：確認你已經按照步骤 4 安裝好 aircrack-ng 版本的驱动程序，而不是系統自帶的陽春版。

---

## 參考数据與延伸閱讀

- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)——想用 6 GHz 就選這支
- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)——兼容性最廣的全能款
- [ALFA 無線网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——JetPack 骨子裡就是 Ubuntu，很多概念可以互通
- [ALFA 無線网卡在 Kali Linux 上——监听模式與数据包注入](/alfa-network/linux-setup-kali/)——监听模式的延伸細節
- [ALFA 無線网卡在 Raspberry Pi 上（3 / 4 / 5）](/alfa-network/hardware/raspberry-pi/)——另一款輕量嵌入式主機的整合方式
- [詞彙表](/getting-started/glossary)——监听模式、DKMS 等名詞的完整解釋
- MediaTek MT76 系列驱动（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au
- [NVIDIA Jetson 官方文件](https://docs.nvidia.com/jetson/)

**標籤：** `alfa` `jetson` `nvidia` `机器人` `wifi-6e` `监听模式` `新手指南`
