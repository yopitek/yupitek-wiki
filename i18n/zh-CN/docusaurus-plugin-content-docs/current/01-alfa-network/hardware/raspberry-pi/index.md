---
id: alfa-hardware-raspberry-pi
title: ALFA 网卡在 Raspberry Pi 上的集成与设置指南
sidebar_label: Raspberry Pi
sidebar_position: 2
description: ALFA 无线网卡在 Raspberry Pi（3B+ / 4B / 5）上的集成教程——外接供电判断、驱动安装与双网卡并行设置，含每一步的预期结果。
tags: [alfa, raspberry-pi, rpi, raspbian, wifi, monitor-mode]
keywords: [Raspberry Pi ALFA, 树莓派 无线网卡, AWUS036ACH 树莓派, AWUS036ACM 树莓派, Raspberry Pi 监听模式]
---

# ALFA 無線网卡在 Raspberry Pi 上（3 / 4 / 5）

> **一句話定位**：Raspberry Pi 內建的 Wi-Fi 只有單天線，信号弱、範圍小。裝上一支 ALFA 無線网卡，就能把 Pi 變成一台平價的 Wi-Fi 实验室工作站——拿來擷取数据包做課堂作業，或當成一個真正有信号範圍的無線基地台。

## 這篇文章適合你嗎？

- **難度**：入門（會下 Linux 终端指令即可，不需要寫程式）
- **預估時間**：20〜40 分鐘
- **你會用到的技能**：基本终端操作（複製貼上指令、看懂指令輸出）
- **讀完你可以做到**：
  1. 讓 ALFA 無線网卡在 Pi 上被正確辨識
  2. 用它做监听模式数据包擷取，並在 Wireshark 上分析
  3. 把 Pi 變成一台真正的 Wi-Fi 基地台（Access Point）

---

## 概念說明：為什麼 Pi 是很適合搭配 ALFA 网卡的主機

Raspberry Pi 內建的無線网卡是單天線設計，信号本來就不強——拿來 SSH 遠端连接沒問題，但要做数据包分析（嗅探）或幫整個房間提供 Wi-Fi，內建网卡完全不夠力。外接一支 ALFA 無線网卡可以解決這兩個問題：

- **监听模式（Monitor Mode）实验室工作站**：搭配內建於 Linux 内核的芯片，插入就能直接開始擷取数据包，很適合做 Wireshark 課堂作業——插入、`airmon-ng start`、開始擷取。
- **存取點（hostapd Access Point）**：搭配外接天線的高功率网卡（如 AWUS036ACM/ACH），可以把 Pi 變成一台真正有效範圍的 Wi-Fi 基地台，信号範圍比內建网卡好很多。
- **雙無線電技巧**：讓 Pi 內建的网卡負責「連上网络」，外接的 ALFA 网卡負責「當基地台廣播」——一台 Pi，同時服務兩個网络。

> 📘 **名詞小教室**
> - **监听模式（Monitor Mode）**：讓网卡把空氣中飛過的所有無線数据包都抓下來，而不只是接收「要給自己的」数据包，是做無線网络分析的基礎模式。
> - **hostapd**：一套可以讓 Linux 裝置變成 Wi-Fi 基地台（Access Point）的软件，裝好後你的 Pi 就能像家用路由器一樣廣播出一個 Wi-Fi 网络讓別人連。
> - **DHCP / NAT**：DHCP 是自動配發 IP 地址給連上你 Pi 的裝置的機制；NAT 則是讓這些裝置能透過 Pi 分享到的网络連上網際网络。這兩個沒設好，別人連得上你的 Wi-Fi 但上不了網。

各主機板的硬件差異，會直接影響你能不能順暢使用高功率网卡：

| 主機板  | USB 規格          | 使用注意事項                          |
| ---- | -------------- | ----------------------------- |
| Pi 3 | USB 2.0        | 支援機型中最舊的一款；AC433 等級或內建於内核的网卡沒問題 |
| Pi 4 | USB 2.0（共享匯流排） | 最受歡迎的選擇——用高功率网卡請務必加一個獨立供電的 USB Hub |
| Pi 5 | USB 3.0 + PCIe | 目前最快的 USB 規格；搭配 AC1200/AX1800 等級网卡吞吐量最佳 |

> ⚠️ **電源是 Pi 上最常見的故障原因**。Pi 3/4 的 USB 埠共用同一條 USB 2.0 匯流排；一支 500 mW 的 ALFA 网卡加上鍵盤，很容易讓整條匯流排電壓不足。只要你用的网卡功率高於 AWUS036ACS，就建議準備一個**獨立供電的 USB Hub**。

---

## 你需要準備的東西

- [ ] **硬件**：已安裝好 Raspberry Pi OS 的 Pi 3 / 4 / 5（建議使用 64 位元版本系統）
- [ ] **前置作業**：已完成 `sudo apt update && sudo apt upgrade`
- [ ] **ALFA 無線网卡**：监听模式強烈建議選用[內建於内核的芯片機型](/alfa-network/linux-compatibility-matrix/)，安裝最省事
- [ ] **獨立供電的 USB Hub**：如果你用的是高功率网卡，務必準備
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动（社群維護、含 DKMS，適用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au

---

## Step-by-Step 设置教學

### 步骤 1：識別無線网卡

插入 ALFA 网卡後，列出目前系統看到的所有接口——ALFA 應該會是「新出現」的那一個：

```bash
lsusb
iw dev
```

**預期結果**：你的网卡會出現在 `lsusb` 清单裡，並且在 `iw dev` 裡看到一個新接口，通常是 `wlan1`（Pi 內建的無線网卡多半是 `wlan0`）。

如果你的 ALFA 网卡是 Realtek 芯片，需要先安裝 DKMS 驱动程序：

```bash
sudo apt install -y git dkms build-essential bc libelf-dev linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**預期結果**：最後一行顯示 `DKMS: install completed.`（在 Pi OS 上這個步骤跟一般 Ubuntu 幾乎一樣）。

---

### 步骤 2：监听模式实验室工作站

啟用监听模式：

```bash
sudo airmon-ng start wlan1
iwconfig wlan1mon
```

**預期結果**：`wlan1mon  IEEE 802.11  Mode:Monitor`——出現 `Mode:Monitor` 代表监听模式已經成功啟用。

把擷取到的数据包存成文件，之後拿到笔记本电脑上用 Wireshark 分析：

```bash
sudo tcpdump -i wlan1mon -w lab-capture.pcap
```

**預期結果**：终端顯示 `listening on wlan1mon`，代表正在擷取。想結束就按 `Ctrl-C`，然後把 `lab-capture.pcap` 這個文件傳到你的笔记本电脑，用 Wireshark 打開分析。

---

### 步骤 3：把 Pi 變成一台 Wi-Fi 基地台（hostapd）

先安裝需要的软件：

```bash
sudo apt install -y hostapd dnsmasq
```

把 ALFA 网卡設成固定 IP：

```bash
echo -e "interface wlan1\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant" | \
    sudo tee -a /etc/dhcpcd.conf
```

建立 hostapd 的设置檔（示範用 2.4 GHz、發射功率 20 dBm）：

```bash
sudo tee /etc/hostapd/hostapd.conf > /dev/null <<'EOF'
interface=wlan1
driver=nl80211
ssid=alfa-lab
hw_mode=g
channel=6
wmm_enabled=1
auth_algs=1
wpa=2
wpa_passphrase=ChangeMe123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF
```

> 💡 記得把 `wpa_passphrase=ChangeMe123` 換成你自己设置的密碼。

讓 hostapd 讀取這份设置檔，並把服務全部啟動：

```bash
echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a /etc/default/hostapd
sudo systemctl restart dhcpcd dnsmasq hostapd
sudo systemctl status hostapd --no-pager | head -10
```

**預期結果**：狀態顯示 `Active: active (running)`，這時候用手機或笔记本电脑搜尋 Wi-Fi，應該就能看到 **alfa-lab** 這個网络，可以正常連上。

---

### 步骤 4：雙無線電技巧（進階，可選讀）

如果你想讓 Pi 內建的 Wi-Fi 繼續當作管理用的连接（例如 SSH 遠端），同時讓 ALFA 网卡專心當基地台，可以這樣设置：

```bash
sudo systemctl stop wpa_supplicant@wlan1 2>/dev/null   # 確保 ALFA 不會去搶连接
sudo iw dev wlan1 set 4addr off
sudo systemctl restart hostapd
```

**預期結果**：`wlan0`（Pi 內建网卡）負責讓你連上網際网络，`wlan1`（ALFA 网卡）專心服務你的实验室 Wi-Fi——一台 Pi，兩個网络同時運作。

---

## 常見問題與排除指引

### Q1：网卡在笔记本电脑上可以用，插到 Pi 上就失效？
- **原因**：USB 供電不足。
- **解決方法**：改用獨立供電的 USB Hub；或使用 Pi 官方原廠電源供應器；也可以嘗試降低网卡的發射功率（`txpower`）。

### Q2：執行 `airmon-ng` 時顯示「No such device」？
- **原因**：接口名稱打錯了。
- **解決方法**：先執行 `iw dev` 確認目前的接口名稱——Pi 內建网卡通常是 `wlan0`，ALFA 网卡通常是 `wlan1`，但不一定每次都一樣，務必先確認再操作。

### Q3：hostapd 啟動失敗，出現 `nl80211: Could not configure driver mode`？
- **原因**：驱动程序沒有支援 AP（基地台）模式，或接口正被其他服務占用。
- **解決方法**：優先使用內建於内核的 MediaTek 芯片（`mt76` 系列對 AP 模式支援穩定）；並先執行 `sudo airmon-ng stop wlan1mon` 確保接口沒有卡在监听模式。

### Q4：使用者連上我的 Wi-Fi，但上不了網？
- **原因**：DHCP／NAT 沒有正確设置，裝置拿不到 IP 或流量沒被轉發出去。
- **解決方法**：
  ```bash
  sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
  sudo sysctl net.ipv4.ip_forward=1
  ```

### Q5：Pi 3 / 4 上的吞吐量感覺被限制住了？
- **原因**：Pi 3/4 的 USB 埠共用同一條 USB 2.0 匯流排，這是硬件本身的限制。
- **解決方法**：沒有软件上的解法，如果需要更高吞吐量，升級到 Pi 5（USB 3.0）是目前唯一的路。

---

## 參考数据與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)——Pi 最好的搭配夥伴
- [ALFA 無線网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——驱动安裝細節（Pi OS 上的步骤相同）
- [ALFA 無線网卡在 Kali Linux 上——监听模式與数据包注入](/alfa-network/linux-setup-kali/)——监听模式的延伸操作
- [ALFA 無線网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——規格更大的嵌入式主機整合方式
- [詞彙表](/getting-started/glossary)——监听模式、hostapd 等名詞的完整解釋
- MediaTek MT76 系列驱动（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au
- [hostapd 官方文件](https://w1.fi/hostapd/)——官方 AP 守護程式說明

**標籤：** `alfa` `raspberry-pi` `hostapd` `存取點` `监听模式` `新手指南`
