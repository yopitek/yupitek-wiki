---
id: alfa-hardware-raspberry-pi
title: ALFA 網卡在 Raspberry Pi 上的整合與設定指南
sidebar_label: Raspberry Pi
sidebar_position: 2
description: ALFA 無線網絡卡在 Raspberry Pi（3B+ / 4B / 5）上的整合教學——外接供電判斷、驅動安裝與雙網卡並行設定，含每一步的預期結果。
tags: [alfa, raspberry-pi, rpi, raspbian, wifi, monitor-mode]
keywords: [Raspberry Pi ALFA, 樹莓派 無線網卡, AWUS036ACH 樹莓派, AWUS036ACM 樹莓派, Raspberry Pi 監聽模式]
---

# ALFA 無線網絡卡在 Raspberry Pi 上（3 / 4 / 5）

> **一句話定位**：Raspberry Pi 內建的 Wi-Fi 只有單天線，訊號弱、範圍小。裝上一支 ALFA 無線網絡卡，就能把 Pi 變成一台平價的 Wi-Fi 實驗室工作站——拿來擷取封包做課堂作業，或當成一個真正有訊號範圍的無線基地台。

## 這篇文章適合你嗎？

- **難度**：入門（會下 Linux 終端機指令即可，不需要寫程式）
- **預估時間**：20〜40 分鐘
- **你會用到的技能**：基本終端機操作（複製貼上指令、看懂指令輸出）
- **讀完你可以做到**：
  1. 讓 ALFA 無線網絡卡在 Pi 上被正確辨識
  2. 用它做監聽模式封包擷取，並在 Wireshark 上分析
  3. 把 Pi 變成一台真正的 Wi-Fi 基地台（Access Point）

---

## 概念說明：為什麼 Pi 是很適合搭配 ALFA 網卡的主機

Raspberry Pi 內建的無線網卡是單天線設計，訊號本來就不強——拿來 SSH 遠端連線沒問題，但要做封包分析（嗅探）或幫整個房間提供 Wi-Fi，內建網卡完全不夠力。外接一支 ALFA 無線網絡卡可以解決這兩個問題：

- **監聽模式（Monitor Mode）實驗室工作站**：搭配內建於 Linux 核心的晶片，插上就能直接開始擷取封包，很適合做 Wireshark 課堂作業——插上、`airmon-ng start`、開始擷取。
- **存取點（hostapd Access Point）**：搭配外接天線的高功率網卡（如 AWUS036ACM/ACH），可以把 Pi 變成一台真正有效範圍的 Wi-Fi 基地台，訊號範圍比內建網卡好很多。
- **雙無線電技巧**：讓 Pi 內建的網卡負責「連上網路」，外接的 ALFA 網卡負責「當基地台廣播」——一台 Pi，同時服務兩個網路。

> 📘 **名詞小教室**
> - **監聽模式（Monitor Mode）**：讓網卡把空氣中飛過的所有無線封包都抓下來，而不只是接收「要給自己的」封包，是做無線網路分析的基礎模式。
> - **hostapd**：一套可以讓 Linux 裝置變成 Wi-Fi 基地台（Access Point）的軟體，裝好後你的 Pi 就能像家用路由器一樣廣播出一個 Wi-Fi 網路讓別人連。
> - **DHCP / NAT**：DHCP 是自動配發 IP 位址給連上你 Pi 的裝置的機制；NAT 則是讓這些裝置能透過 Pi 分享到的網路連上網際網路。這兩個沒設好，別人連得上你的 Wi-Fi 但上不了網。

各主機板的硬體差異，會直接影響你能不能順暢使用高功率網卡：

| 主機板  | USB 規格          | 使用注意事項                          |
| ---- | -------------- | ----------------------------- |
| Pi 3 | USB 2.0        | 支援機型中最舊的一款；AC433 等級或內建於核心的網卡沒問題 |
| Pi 4 | USB 2.0（共享匯流排） | 最受歡迎的選擇——用高功率網卡請務必加一個獨立供電的 USB Hub |
| Pi 5 | USB 3.0 + PCIe | 目前最快的 USB 規格；搭配 AC1200/AX1800 等級網卡吞吐量最佳 |

> ⚠️ **電源是 Pi 上最常見的故障原因**。Pi 3/4 的 USB 埠共用同一條 USB 2.0 匯流排；一支 500 mW 的 ALFA 網卡加上鍵盤，很容易讓整條匯流排電壓不足。只要你用的網卡功率高於 AWUS036ACS，就建議準備一個**獨立供電的 USB Hub**。

---

## 你需要準備的東西

- [ ] **硬體**：已安裝好 Raspberry Pi OS 的 Pi 3 / 4 / 5（建議使用 64 位元版本系統）
- [ ] **前置作業**：已完成 `sudo apt update && sudo apt upgrade`
- [ ] **ALFA 無線網絡卡**：監聽模式強烈建議選用[內建於核心的晶片機型](/alfa-network/linux-compatibility-matrix/)，安裝最省事
- [ ] **獨立供電的 USB Hub**：如果你用的是高功率網卡，務必準備
- [ ] **驅動程式參考（GitHub）**：
  - MediaTek MT76 系列驅動（社群維護、含 DKMS，適用 MT7612U / MT7921 系列晶片）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驅動（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au

---

## Step-by-Step 設定教學

### 步驟 1：識別無線網絡卡

插上 ALFA 網卡後，列出目前系統看到的所有介面——ALFA 應該會是「新出現」的那一個：

```bash
lsusb
iw dev
```

**預期結果**：你的網卡會出現在 `lsusb` 清單裡，並且在 `iw dev` 裡看到一個新介面，通常是 `wlan1`（Pi 內建的無線網卡多半是 `wlan0`）。

如果你的 ALFA 網卡是 Realtek 晶片，需要先安裝 DKMS 驅動程式：

```bash
sudo apt install -y git dkms build-essential bc libelf-dev linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**預期結果**：最後一行顯示 `DKMS: install completed.`（在 Pi OS 上這個步驟跟一般 Ubuntu 幾乎一樣）。

---

### 步驟 2：監聽模式實驗室工作站

啟用監聽模式：

```bash
sudo airmon-ng start wlan1
iwconfig wlan1mon
```

**預期結果**：`wlan1mon  IEEE 802.11  Mode:Monitor`——出現 `Mode:Monitor` 代表監聽模式已經成功啟用。

把擷取到的封包存成檔案，之後拿到筆電上用 Wireshark 分析：

```bash
sudo tcpdump -i wlan1mon -w lab-capture.pcap
```

**預期結果**：終端機顯示 `listening on wlan1mon`，代表正在擷取。想結束就按 `Ctrl-C`，然後把 `lab-capture.pcap` 這個檔案傳到你的筆電，用 Wireshark 打開分析。

---

### 步驟 3：把 Pi 變成一台 Wi-Fi 基地台（hostapd）

先安裝需要的軟體：

```bash
sudo apt install -y hostapd dnsmasq
```

把 ALFA 網卡設成固定 IP：

```bash
echo -e "interface wlan1\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant" | \
    sudo tee -a /etc/dhcpcd.conf
```

建立 hostapd 的設定檔（示範用 2.4 GHz、發射功率 20 dBm）：

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

> 💡 記得把 `wpa_passphrase=ChangeMe123` 換成你自己設定的密碼。

讓 hostapd 讀取這份設定檔，並把服務全部啟動：

```bash
echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a /etc/default/hostapd
sudo systemctl restart dhcpcd dnsmasq hostapd
sudo systemctl status hostapd --no-pager | head -10
```

**預期結果**：狀態顯示 `Active: active (running)`，這時候用手機或筆電搜尋 Wi-Fi，應該就能看到 **alfa-lab** 這個網路，可以正常連上。

---

### 步驟 4：雙無線電技巧（進階，可選讀）

如果你想讓 Pi 內建的 Wi-Fi 繼續當作管理用的連線（例如 SSH 遠端），同時讓 ALFA 網卡專心當基地台，可以這樣設定：

```bash
sudo systemctl stop wpa_supplicant@wlan1 2>/dev/null   # 確保 ALFA 不會去搶連線
sudo iw dev wlan1 set 4addr off
sudo systemctl restart hostapd
```

**預期結果**：`wlan0`（Pi 內建網卡）負責讓你連上網際網路，`wlan1`（ALFA 網卡）專心服務你的實驗室 Wi-Fi——一台 Pi，兩個網路同時運作。

---

## 常見問題與排除指引

### Q1：網卡在筆電上可以用，插到 Pi 上就失效？
- **原因**：USB 供電不足。
- **解決方法**：改用獨立供電的 USB Hub；或使用 Pi 官方原廠電源供應器；也可以嘗試降低網卡的發射功率（`txpower`）。

### Q2：執行 `airmon-ng` 時顯示「No such device」？
- **原因**：介面名稱打錯了。
- **解決方法**：先執行 `iw dev` 確認目前的介面名稱——Pi 內建網卡通常是 `wlan0`，ALFA 網卡通常是 `wlan1`，但不一定每次都一樣，務必先確認再操作。

### Q3：hostapd 啟動失敗，出現 `nl80211: Could not configure driver mode`？
- **原因**：驅動程式沒有支援 AP（基地台）模式，或介面正被其他服務占用。
- **解決方法**：優先使用內建於核心的 MediaTek 晶片（`mt76` 系列對 AP 模式支援穩定）；並先執行 `sudo airmon-ng stop wlan1mon` 確保介面沒有卡在監聽模式。

### Q4：使用者連上我的 Wi-Fi，但上不了網？
- **原因**：DHCP／NAT 沒有正確設定，裝置拿不到 IP 或流量沒被轉發出去。
- **解決方法**：
  ```bash
  sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
  sudo sysctl net.ipv4.ip_forward=1
  ```

### Q5：Pi 3 / 4 上的吞吐量感覺被限制住了？
- **原因**：Pi 3/4 的 USB 埠共用同一條 USB 2.0 匯流排，這是硬體本身的限制。
- **解決方法**：沒有軟體上的解法，如果需要更高吞吐量，升級到 Pi 5（USB 3.0）是目前唯一的路。

---

## 參考資料與延伸閱讀

- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)——Pi 最好的搭配夥伴
- [ALFA 無線網絡卡在 Ubuntu 上的完整設定指南](/alfa-network/linux-setup-ubuntu/)——驅動安裝細節（Pi OS 上的步驟相同）
- [ALFA 無線網絡卡在 Kali Linux 上——監聽模式與封包注入](/alfa-network/linux-setup-kali/)——監聽模式的延伸操作
- [ALFA 無線網絡卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——規格更大的嵌入式主機整合方式
- [詞彙表](/getting-started/glossary)——監聽模式、hostapd 等名詞的完整解釋
- MediaTek MT76 系列驅動（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驅動（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au
- [hostapd 官方文件](https://w1.fi/hostapd/)——官方 AP 守護程式說明

**標籤：** `alfa` `raspberry-pi` `hostapd` `存取點` `監聽模式` `新手指南`
