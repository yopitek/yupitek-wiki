---
id: alfa-hardware-unitree
title: ALFA 網卡在 Unitree 機器狗上的整合與遠距遙測指南
sidebar_label: Unitree 機器狗
sidebar_position: 3
description: ALFA 無線網絡卡在宇樹 Unitree（Go2 / B2）機器狗上的整合教學——解決內建天線訊號弱與馬達電磁干擾，實現低延遲影像串流與遠距遙測控制。
tags: [alfa, unitree, robotics, quadruped, wifi-6e, telemetry]
keywords: [Unitree ALFA, 宇樹 機器狗 無線網卡, Go2 遙測, AWUS036AXML Unitree, 機器人 5GHz 串流]
---

# ALFA 無線網絡卡在 Unitree 機器人上（Go2 / B2 / A1）

> **一句話定位**：Unitree 機器狗（Go2、B2、A1）機載的是 NVIDIA Jetson，但隨附的內建 Wi-Fi 天線很弱。裝上一支搭配外接天線的 ALFA 無線網絡卡，能把機器人的無線控制連結範圍，從「只能跟著你在房間裡走」變成「在場地另一端也能穩定指揮它」。

## 這篇文章適合你嗎？

- **難度**：中階（需要會用 SSH 連線操作機載電腦）
- **預估時間**：30〜45 分鐘
- **你會用到的技能**：基本 Linux 終端機操作、SSH 遠端連線
- **讀完你可以做到**：
  1. 讓 ALFA 無線網絡卡在機器人的機載電腦上被正確辨識
  2. 建立一個專用的 5 GHz 控制連線，避開 2.4 GHz 的干擾
  3. 用實際的延遲/遺失率數據驗證連線品質好不好

---

## 概念說明：機器狗的無線控制連結問題

機器狗其實是一套「長了腿的神經系統」：機載的 Jetson 電腦要把影像、光達（LiDAR）與慣性感測器（IMU）的遙測資料即時傳給你，同時接收你下達的步態、任務指令。這條連結需要**低延遲、高可靠性，而且要有一定的範圍**。

問題是，機器人運算模組上出廠內建的天線，表現跟你手機、筆電內建的天線差不多——大概 30 公尺就已經很勉強，而且 2.4 GHz 頻段在實驗室環境裡常常被其他 Wi-Fi 裝置、藍牙裝置，甚至機器人自己的馬達電磁干擾（EMI）吃得亂七八糟。

解決方式跟 [Jetson 整合指南](/alfa-network/hardware/jetson/)是同一套邏輯——用外接的 ALFA 無線網絡卡取代原本的無線連結路徑，實際上有效的做法是：

1. **優先用 5 GHz 頻段**：機器人上的 2.4 GHz 頻段很容易被馬達與其他裝置干擾，能避開就避開。
2. **外接天線位置很重要**：無線網絡卡的外接天線效果比機器人機殼上任何內建天線都好，而且你可以把它擺在金屬機殼上方、訊號不會被遮蔽的位置。
3. **依需求選網卡**：入門選 [AWUS036ACM](/alfa-network/products/awus036acm/)（相容性最廣）；想要 Wi-Fi 6 加藍牙選 [AWUS036AXM](/alfa-network/products/awus036axm/)；想要 6 GHz 頻段選 [AWUS036AXML](/alfa-network/products/awus036axml/)。

> 📘 **名詞小教室**
> - **遙測（Telemetry）**：機器人把自己身上的感測器資料（影像、位置、姿態等）即時回傳給你的過程，方便你在遠端掌握機器人的狀態。
> - **EMI（電磁干擾）**：機器人身上的馬達運轉時會產生電磁波，這些電磁波可能會干擾附近的無線訊號，這也是為什麼機器人上的 Wi-Fi 常常比想像中不穩定。
> - **iperf3**：一個專門用來測試網路吞吐量和延遲品質的工具，這篇文章會用它來確認連線設好之後品質到底好不好，而不是只憑感覺判斷。

---

## 你需要準備的東西

- [ ] **硬體**：Unitree 機器人（Go2 / B2 / A1），機載電腦可透過 SSH 存取（出廠預設 IP 通常是 `192.168.123.161`）
- [ ] **地面站筆電**：執行 Ubuntu 系統（可參考 [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/)）
- [ ] **ALFA 無線網絡卡**：依需求從上一節挑選型號
- [ ] **獨立供電的 USB Hub**：如果機器人的 USB 供電不足以驅動高功率網卡時使用
- [ ] **驅動程式參考（GitHub）**：
  - MediaTek MT76 系列驅動（適用 MT7612U / MT7921 系列晶片）：https://github.com/morrownr/mt76
  - Unitree 官方 SDK（如果你後續要做更進階的程式化控制）：https://github.com/unitreerobotics/unitree_sdk2
  - 社群維護的 ROS2 / Wi-Fi 整合專案（想串接 ROS2 生態系可以參考）：https://github.com/abizovnuralem/go2_ros2_sdk

---

## Step-by-Step 設定教學

### 步驟 1：連上機器人並確認核心版本

```bash
ssh unitree@<機器人IP>
uname -r
```

**預期結果**：你會看到一個 L4T（NVIDIA Jetson 專用）核心版本，例如 `5.10.65-tegra` 或 `6.6.0-tegra`。

跟 [Jetson 整合指南](/alfa-network/hardware/jetson/)裡提到的規則一樣：MT7921AUN 晶片的網卡（AWUS036AXM / AXML）需要核心版本 5.18 以上；MT7612U 晶片（AWUS036ACM）則在任何近期核心版本上都能用。

---

### 步驟 2：插上 ALFA 無線網絡卡

在機器人的機載電腦上執行：

```bash
lsusb | grep -iE "mediatek|realtek"
iw dev
```

**預期結果**：你的網卡出現在 `lsusb` 清單裡，同時多出一個新的無線介面（通常是 `wlan1`）。

如果是 Realtek 晶片，請依照 [Ubuntu 設定指南](/alfa-network/linux-setup-ubuntu/) 安裝 DKMS 驅動程式；如果是 MediaTek 內建於核心的晶片，這一步做完就直接可以用，不用額外安裝任何東西。

---

### 步驟 3：建立專用的 5 GHz 控制連線

用一個獨立的無線基地台（可以是你的地面站筆電開熱點，或另一台路由器）建立專用連線，讓機器人的控制連結跟實驗室裡其他 Wi-Fi 流量分開，互不干擾：

```bash
sudo nmcli device wifi connect "robot-link" password "你的密碼"
iw dev wlan1 link
```

**預期結果**：畫面顯示 `Connected to robot-link`，並附帶一行顯示目前頻道與連線速率的資訊。

接著確認這條連線走的真的是 5 GHz 頻段：

```bash
iw dev wlan1 info | grep channel
```

**預期結果**：顯示類似 `channel 36 (5180 MHz)` 這樣的 5 GHz 頻道資訊。如果顯示的是 2.4 GHz 的頻道，代表你的基地台目前設定成 2.4 GHz，需要回去基地台端切換成 5 GHz。

---

### 步驟 4：鎖定 5 GHz 頻段，避免自動切回吵雜的 2.4 GHz

有些系統在訊號不穩時會自動切回 2.4 GHz 頻段，這樣一來前面選 5 GHz 的努力就白費了。用下面這行指令，直接把機器人端的連線鎖定在 5 GHz 頻段：

```bash
sudo nmcli connection modify robot-link 802-11-wireless.band a
sudo nmcli connection up robot-link
```

> 💡 **設定小提醒**：這裡的參數是 `802-11-wireless.band a`，代表鎖定 5 GHz 頻段（`a` 對應 802.11a/5GHz）。如果你之後查其他資料看到 `band bg`，那個參數指的是鎖定 2.4 GHz（`b`/`g` 對應 2.4GHz），跟這裡的目的正好相反，記得不要混用。

**預期結果**：連線會在 5 GHz 頻段重新建立。可以再跑一次步驟 3 的檢查指令 `iw dev wlan1 info | grep channel` 確認頻道確實停留在 5 GHz。

接著，把發射功率調到你所在地區的法規上限，讓訊號更穩：

```bash
sudo iw reg set TW   # 換成你所在地的國家代碼
sudo iwconfig wlan1 txpower 30
```

**預期結果**：指令執行沒有出現錯誤訊息，且 `iwconfig` 顯示 `Tx-Power=30 dBm`（實際數值會受你所在地區的法規上限約束，不一定every次都是 30）。

---

### 步驟 5：用遙測連線測試驗證連線品質

單純的 ICMP（也就是一般的 `ping`）沒辦法準確反映真實的連線延遲，這一步改用 UDP 封包測試工具 `iperf3`，量測實際吞吐量與封包遺失率：

在機器人端執行：

```bash
iperf3 -s &
```

在地面站筆電上執行：

```bash
iperf3 -c <機器人IP> -u -b 100M -t 10
```

**預期結果**：畫面會顯示一個吞吐量數字（Mbits/sec）以及封包遺失率（通常應該落在 0〜1%）。如果你在實際工作距離上量到的遺失率超過大約 1%，代表天線位置或頻道需要調整——可以試試切換到另一個 5 GHz 頻道（重新設定連線後執行 `sudo iw dev wlan1 set channel 149`），或者把網卡移到機殼上方更不容易被遮蔽的位置。

---

## 常見問題與排除指引

### Q1：馬達啟動運轉時，連線就會斷斷續續？
- **原因**：馬達產生的電磁干擾（EMI），加上天線位置不夠好。
- **解決方法**：把無線網絡卡的天線移到金屬機殼上方；改用 5 GHz 頻段；並檢查目前頻道是否壅塞。

### Q2：無線網絡卡插上機器人後完全看不到？
- **原因**：機器人的 USB 連接埠供電受限。
- **解決方法**：改用獨立供電的 USB Hub；或嘗試插到機器人上不同的 USB 連接埠。

### Q3：MT7921AUN 網卡（AXM / AXML）偵測不到？
- **原因**：機器人上的 JetPack 版本太舊，核心版本低於 5.18。
- **解決方法**：升級機器人機載電腦的 JetPack 版本；或改用 MT7612U 晶片等級的網卡（如 AWUS036ACM）。

### Q4：距離拉遠之後連線又自動回落到 2.4 GHz？
- **原因**：基地台或連線設定沒有真正鎖定 5 GHz 頻段。
- **解決方法**：重新確認步驟 4 的指令有正確執行（`802-11-wireless.band a`），並用步驟 3 的檢查指令再次確認頻道。

### Q5：連線量測時出現高延遲的尖峰值？
- **原因**：目前使用的頻道壅塞，附近有其他裝置在搶同一個頻道。
- **解決方法**：挑一個比較乾淨的 5 GHz 頻道測試；如果你的基地台支援，也可以考慮改用 6 GHz 頻段（需搭配 AWUS036AXML）。

---

## 參考資料與延伸閱讀

- [ALFA 無線網絡卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——同樣的核心版本判斷邏輯，內容更深入
- [AWUS036AXM 產品頁面](/alfa-network/products/awus036axm/)——適合機器人控制連結的 Wi-Fi 6 + 藍牙機型
- [ALFA 無線網絡卡在 Ubuntu 上的完整設定指南](/alfa-network/linux-setup-ubuntu/)——驅動安裝細節
- [詞彙表](/getting-started/glossary)——遙測、EMI 等名詞的完整解釋
- MediaTek MT76 系列驅動（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Unitree 官方 SDK：https://github.com/unitreerobotics/unitree_sdk2
- 社群維護的 ROS2 / Wi-Fi 整合專案：https://github.com/abizovnuralem/go2_ros2_sdk
- [Unitree 官方文件](https://support.unitree.com/)——機器人 SDK 與網路設定參考

**標籤：** `alfa` `unitree` `機器人` `機器狗` `無線控制` `新手指南`
