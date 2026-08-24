---
id: alfa-hardware-unitree
title: ALFA 网卡在 Unitree 机器狗上的集成与远距遥测指南
sidebar_label: Unitree 机器狗
sidebar_position: 3
description: ALFA 无线网卡在宇树 Unitree（Go2 / B2）机器狗上的集成教程——解决内置天线信号弱与电机电磁干扰，实现低延迟图传与远距遥测控制。
tags: [alfa, unitree, robotics, quadruped, wifi-6e, telemetry]
keywords: [Unitree ALFA, 宇树 机器狗 无线网卡, Go2 遥测, AWUS036AXML Unitree, 机器人 5GHz 图传]
---

# ALFA 無線网卡在 Unitree 机器人上（Go2 / B2 / A1）

> **一句話定位**：Unitree 机器狗（Go2、B2、A1）機載的是 NVIDIA Jetson，但隨附的內建 Wi-Fi 天線很弱。裝上一支搭配外接天線的 ALFA 無線网卡，能把机器人的無線控制連結範圍，從「只能跟著你在房間裡走」變成「在場地另一端也能穩定指揮它」。

## 這篇文章適合你嗎？

- **難度**：中階（需要會用 SSH 连接操作機載电脑）
- **預估時間**：30〜45 分鐘
- **你會用到的技能**：基本 Linux 终端操作、SSH 遠端连接
- **讀完你可以做到**：
  1. 讓 ALFA 無線网卡在机器人的機載电脑上被正確辨識
  2. 建立一個專用的 5 GHz 控制连接，避開 2.4 GHz 的干扰
  3. 用實際的延遲/遺失率數據驗證连接品質好不好

---

## 概念說明：机器狗的無線控制連結問題

机器狗其實是一套「長了腿的神經系統」：機載的 Jetson 电脑要把影像、光達（LiDAR）與慣性感測器（IMU）的遥测数据即時傳給你，同時接收你下達的步態、任務指令。這條連結需要**低延遲、高可靠性，而且要有一定的範圍**。

問題是，机器人運算模块上出廠內建的天線，表現跟你手機、笔记本电脑內建的天線差不多——大概 30 公尺就已經很勉強，而且 2.4 GHz 频段在实验室環境裡常常被其他 Wi-Fi 裝置、藍牙裝置，甚至机器人自己的馬達電磁干扰（EMI）吃得亂七八糟。

解決方式跟 [Jetson 整合指南](/alfa-network/hardware/jetson/)是同一套邏輯——用外接的 ALFA 無線网卡取代原本的無線連結路徑，實際上有效的做法是：

1. **優先用 5 GHz 频段**：机器人上的 2.4 GHz 频段很容易被馬達與其他裝置干扰，能避開就避開。
2. **外接天線位置很重要**：無線网卡的外接天線效果比机器人機殼上任何內建天線都好，而且你可以把它擺在金屬機殼上方、信号不會被遮蔽的位置。
3. **依需求選网卡**：入門選 [AWUS036ACM](/alfa-network/products/awus036acm/)（兼容性最廣）；想要 Wi-Fi 6 加藍牙選 [AWUS036AXM](/alfa-network/products/awus036axm/)；想要 6 GHz 频段選 [AWUS036AXML](/alfa-network/products/awus036axml/)。

> 📘 **名詞小教室**
> - **遥测（Telemetry）**：机器人把自己身上的感測器数据（影像、位置、姿態等）即時回傳給你的過程，方便你在遠端掌握机器人的狀態。
> - **EMI（電磁干扰）**：机器人身上的馬達運轉時會產生電磁波，這些電磁波可能會干扰附近的無線信号，這也是為什麼机器人上的 Wi-Fi 常常比想像中不穩定。
> - **iperf3**：一個專門用來測試网络吞吐量和延遲品質的工具，這篇文章會用它來確認连接設好之後品質到底好不好，而不是只憑感覺判斷。

---

## 你需要準備的東西

- [ ] **硬件**：Unitree 机器人（Go2 / B2 / A1），機載电脑可透過 SSH 存取（出廠默认 IP 通常是 `192.168.123.161`）
- [ ] **地面站笔记本电脑**：執行 Ubuntu 系統（可參考 [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/)）
- [ ] **ALFA 無線网卡**：依需求從上一節挑選型号
- [ ] **獨立供電的 USB Hub**：如果机器人的 USB 供電不足以驱动高功率网卡時使用
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动（適用 MT7612U / MT7921 系列芯片）：https://github.com/morrownr/mt76
  - Unitree 官方 SDK（如果你後續要做更進階的程式化控制）：https://github.com/unitreerobotics/unitree_sdk2
  - 社群維護的 ROS2 / Wi-Fi 整合專案（想串接 ROS2 生態系可以參考）：https://github.com/abizovnuralem/go2_ros2_sdk

---

## Step-by-Step 设置教學

### 步骤 1：連上机器人並確認内核版本

```bash
ssh unitree@<机器人IP>
uname -r
```

**預期結果**：你會看到一個 L4T（NVIDIA Jetson 專用）内核版本，例如 `5.10.65-tegra` 或 `6.6.0-tegra`。

跟 [Jetson 整合指南](/alfa-network/hardware/jetson/)裡提到的規則一樣：MT7921AUN 芯片的网卡（AWUS036AXM / AXML）需要内核版本 5.18 以上；MT7612U 芯片（AWUS036ACM）則在任何近期内核版本上都能用。

---

### 步骤 2：插入 ALFA 無線网卡

在机器人的機載电脑上執行：

```bash
lsusb | grep -iE "mediatek|realtek"
iw dev
```

**預期結果**：你的网卡出現在 `lsusb` 清单裡，同時多出一個新的無線接口（通常是 `wlan1`）。

如果是 Realtek 芯片，請依照 [Ubuntu 设置指南](/alfa-network/linux-setup-ubuntu/) 安裝 DKMS 驱动程序；如果是 MediaTek 內建於内核的芯片，這一步做完就直接可以用，不用額外安裝任何東西。

---

### 步骤 3：建立專用的 5 GHz 控制连接

用一個獨立的無線基地台（可以是你的地面站笔记本电脑開熱點，或另一台路由器）建立專用连接，讓机器人的控制連結跟实验室裡其他 Wi-Fi 流量分開，互不干扰：

```bash
sudo nmcli device wifi connect "robot-link" password "你的密碼"
iw dev wlan1 link
```

**預期結果**：畫面顯示 `Connected to robot-link`，並附帶一行顯示目前信道與连接速率的資訊。

接著確認這條连接走的真的是 5 GHz 频段：

```bash
iw dev wlan1 info | grep channel
```

**預期結果**：顯示類似 `channel 36 (5180 MHz)` 這樣的 5 GHz 信道資訊。如果顯示的是 2.4 GHz 的信道，代表你的基地台目前设置成 2.4 GHz，需要回去基地台端切換成 5 GHz。

---

### 步骤 4：鎖定 5 GHz 频段，避免自動切回吵雜的 2.4 GHz

有些系統在信号不穩時會自動切回 2.4 GHz 频段，這樣一來前面選 5 GHz 的努力就白費了。用下面這行指令，直接把机器人端的连接鎖定在 5 GHz 频段：

```bash
sudo nmcli connection modify robot-link 802-11-wireless.band a
sudo nmcli connection up robot-link
```

> 💡 **设置小提醒**：這裡的參數是 `802-11-wireless.band a`，代表鎖定 5 GHz 频段（`a` 對應 802.11a/5GHz）。如果你之後查其他数据看到 `band bg`，那個參數指的是鎖定 2.4 GHz（`b`/`g` 對應 2.4GHz），跟這裡的目的正好相反，記得不要混用。

**預期結果**：连接會在 5 GHz 频段重新建立。可以再跑一次步骤 3 的檢查指令 `iw dev wlan1 info | grep channel` 確認信道確實停留在 5 GHz。

接著，把發射功率調到你所在地區的法規上限，讓信号更穩：

```bash
sudo iw reg set TW   # 換成你所在地的國家代碼
sudo iwconfig wlan1 txpower 30
```

**預期結果**：指令執行沒有出現錯誤訊息，且 `iwconfig` 顯示 `Tx-Power=30 dBm`（實際數值會受你所在地區的法規上限約束，不一定every次都是 30）。

---

### 步骤 5：用遥测连接測試驗證连接品質

單純的 ICMP（也就是一般的 `ping`）沒辦法準確反映真實的连接延遲，這一步改用 UDP 数据包測試工具 `iperf3`，量測實際吞吐量與数据包遺失率：

在机器人端執行：

```bash
iperf3 -s &
```

在地面站笔记本电脑上執行：

```bash
iperf3 -c <机器人IP> -u -b 100M -t 10
```

**預期結果**：畫面會顯示一個吞吐量數字（Mbits/sec）以及数据包遺失率（通常應該落在 0〜1%）。如果你在實際工作距離上量到的遺失率超過大約 1%，代表天線位置或信道需要調整——可以試試切換到另一個 5 GHz 信道（重新设置连接後執行 `sudo iw dev wlan1 set channel 149`），或者把网卡移到機殼上方更不容易被遮蔽的位置。

---

## 常見問題與排除指引

### Q1：馬達啟動運轉時，连接就會斷斷續續？
- **原因**：馬達產生的電磁干扰（EMI），加上天線位置不夠好。
- **解決方法**：把無線网卡的天線移到金屬機殼上方；改用 5 GHz 频段；並檢查目前信道是否壅塞。

### Q2：無線网卡插入机器人後完全看不到？
- **原因**：机器人的 USB 連接埠供電受限。
- **解決方法**：改用獨立供電的 USB Hub；或嘗試插到机器人上不同的 USB 連接埠。

### Q3：MT7921AUN 网卡（AXM / AXML）偵測不到？
- **原因**：机器人上的 JetPack 版本太舊，内核版本低於 5.18。
- **解決方法**：升級机器人機載电脑的 JetPack 版本；或改用 MT7612U 芯片等級的网卡（如 AWUS036ACM）。

### Q4：距離拉遠之後连接又自動回落到 2.4 GHz？
- **原因**：基地台或连接设置沒有真正鎖定 5 GHz 频段。
- **解決方法**：重新確認步骤 4 的指令有正確執行（`802-11-wireless.band a`），並用步骤 3 的檢查指令再次確認信道。

### Q5：连接量測時出現高延遲的尖峰值？
- **原因**：目前使用的信道壅塞，附近有其他裝置在搶同一個信道。
- **解決方法**：挑一個比較乾淨的 5 GHz 信道測試；如果你的基地台支援，也可以考慮改用 6 GHz 频段（需搭配 AWUS036AXML）。

---

## 參考数据與延伸閱讀

- [ALFA 無線网卡在 NVIDIA Jetson 上（Orin Nano / NX）](/alfa-network/hardware/jetson/)——同樣的内核版本判斷邏輯，內容更深入
- [AWUS036AXM 產品頁面](/alfa-network/products/awus036axm/)——適合机器人控制連結的 Wi-Fi 6 + 藍牙機型
- [ALFA 無線网卡在 Ubuntu 上的完整设置指南](/alfa-network/linux-setup-ubuntu/)——驱动安裝細節
- [詞彙表](/getting-started/glossary)——遥测、EMI 等名詞的完整解釋
- MediaTek MT76 系列驱动（社群維護，含 DKMS）：https://github.com/morrownr/mt76
- Unitree 官方 SDK：https://github.com/unitreerobotics/unitree_sdk2
- 社群維護的 ROS2 / Wi-Fi 整合專案：https://github.com/abizovnuralem/go2_ros2_sdk
- [Unitree 官方文件](https://support.unitree.com/)——机器人 SDK 與网络设置參考

**標籤：** `alfa` `unitree` `机器人` `机器狗` `無線控制` `新手指南`
