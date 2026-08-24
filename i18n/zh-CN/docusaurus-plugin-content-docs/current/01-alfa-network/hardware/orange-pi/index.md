---
id: alfa-hardware-orange-pi
title: Orange Pi & Rockchip RK3588 SBC × ALFA Network 整合指南
sidebar_label: Orange Pi / RK3588
sidebar_position: 8
description: Orange Pi 5 与 Rockchip RK3588 单板电脑搭配 ALFA 网卡——系统内核差异、Armbian Mainline 部署与供电设置，含每一步的预期结果。
tags: [orange-pi, rk3588, armbian, rockchip, alfa, awus036axml, awus036acm, sbc]
keywords: [Orange Pi 5, RK3588, Armbian mainline, vendor BSP, AWUS036AXML, AWUS036ACM, mt76]
---

# Orange Pi & Rockchip RK3588 SBC × ALFA Network 整合指南

> **一句話定位**：Orange Pi 5 系列這類搭載 Rockchip RK3588 芯片的單板电脑（SBC）算力很強，常被拿來做邊緣運算的無線閘道器或遠端感測節點。但很多人插入 ALFA 网卡後完全抓不到，誤以為是硬件不兼容——實際上關鍵是「你用的系統镜像文件」，這篇文章教你怎麼選對系統、正確安裝。

## 這篇文章適合你嗎？

- **難度**：入門〜中階（會下 Linux 终端指令即可）
- **預估時間**：30〜45 分鐘（含系統刷機時間）
- **你會用到的技能**：基本终端操作
- **讀完你可以做到**：
  1. 搞懂為什麼原廠系統插网卡常常抓不到，該用哪一種系統镜像文件
  2. 完成系統刷機與 ALFA 网卡的驱动確認
  3. 掌握供電與散熱上要注意的細節，避免長時間使用時斷線

---

## 概念說明：為什麼原廠系統插入网卡常常沒反應

很多人在 Orange Pi 原廠附的 Debian 系統上插入 ALFA 网卡，發現系統完全沒反應，第一直覺會以為「這張网卡跟我的板子不兼容」——但其實問題通常出在**系統内核版本**，不是硬件本身。

這跟 SBC（單板电脑）這類產品的系統生態有關：

- **原廠 Vendor BSP（Board Support Package）系統**：芯片廠商（這裡是 Rockchip）為了讓硬件能盡快出貨，會先基於一個比較舊的 Linux 内核版本（通常是 5.10）做客製化，讓螢幕、GPU 這些硬件能動。這類系統的内核版本比較舊，對新款 USB 网卡芯片的支援往往還沒跟上。
- **Armbian Mainline 系統**：Armbian 是一個第三方維護的社群專案，會持續把 SBC 的支援整合進最新的 Linux 主線内核（目前是 6.x 版本）。内核版本新，代表對新款 USB 网卡芯片（尤其是這幾年才推出的 MT7921AUN）的支援也比較完整，通常插入就能直接用。

**簡單判斷方式**：如果你剛買到板子，插入 ALFA 网卡完全沒反應，第一件事不是懷疑网卡壞了，是先確認自己現在裝的是不是原廠 Vendor BSP 系統——如果是，換成 Armbian Mainline 系統通常就能解決。

> 📘 **名詞小教室**
> - **SBC（Single Board Computer，單板电脑）**：把 CPU、記憶體、儲存控制器等元件整合在一片電路板上的迷你电脑，Orange Pi、Raspberry Pi 都屬於這類產品。
> - **BSP（Board Support Package）**：芯片廠商為了讓自家硬件能正常开机、驱动螢幕與周邊，提供的一整套客製化系統與驱动程序。BSP 系統通常内核版本比較舊，但對板子本身的硬件（例如特定的顯示輸出）支援反而可能更好。
> - **Mainline 内核**：Linux 官方維護的主線内核版本，社群持續在更新。使用 Mainline 内核的系統（如 Armbian）通常對新款周邊裝置的支援比 BSP 系統更新更快。

---

## ALFA 网卡在 RK3588 平台上的支援情況

| ALFA 型号         | 芯片型号                 | Armbian（内核 ≥6.x） | 原廠 Debian（内核 5.10） | 備註                    |
| --------------- | -------------------- | --------------------- | ----------------------- | ----------------------- |
| **AWUS036AXML** | MT7921AUN（Wi-Fi 6E） | ✅ 即插即用                | ⚠️ 需手動補上固件文件         | 支援 2.4G / 5G / 6G      |
| **AWUS036ACM**  | MT7612U（802.11ac）   | ✅ 即插即用                | ⚠️ 需手動加载 `mt76x2u`        | 监听與数据包注入的首選           |
| **AWUS036ACHM** | MT7610U（802.11ac）   | ✅ 即插即用                | ⚠️ 需手動加载 `mt76x0u`        | 單天線，適合長時間监听用途          |
| **AWUS036ACH**  | RTL8812AU            | ⚠️ 需自行编译 DKMS          | ⚠️ 需自行编译 DKMS            | 需先安裝 `linux-headers` |

**簡單判斷方式**：如果你想要最省事、插入就能用，建議直接刷 Armbian Mainline 系統（見下方步骤），可以完全避開原廠系統上手動補固件、載驱动的麻煩。

---

## 你需要準備的東西

- [ ] **硬件**：Orange Pi 5 / 5B / 5 Plus，或其他 Rockchip RK3588 / RK3588S 平台的單板电脑
- [ ] **一張 microSD 卡或 NVMe 硬碟**：用來刷入系統镜像文件
- [ ] **讀卡機**：用來把系統镜像文件寫入 microSD 卡
- [ ] **ALFA 無線网卡**：依上表選擇型号
- [ ] **至少 5V/4A（20W）的 Type-C 電源供應器**：詳見下方供電提醒
- [ ] **驱动程序參考（GitHub）**：
  - MediaTek MT76 系列驱动（Armbian Mainline 系統已內建，如需手動安裝可參考此專案）：https://github.com/morrownr/mt76
  - Realtek RTL8812AU 驱动（AWUS036ACH 適用）：https://github.com/aircrack-ng/rtl8812au
  - Armbian 建置專案（若想自行编译客製化镜像文件，而不是直接下載官方預编译版本）：https://github.com/armbian/build

---

## Step-by-Step 设置教學

### 步骤 1：下載並刷入 Armbian Mainline 镜像文件

前往 [Armbian 官方網站](https://www.armbian.com/orange-pi-5/)，下載適用於 Orange Pi 5 的 Armbian Linux（内核 6.x Mainline）镜像文件，並用刷機工具（如 balenaEtcher 或 Raspberry Pi Imager）寫入 microSD 卡或 NVMe 硬碟。

**預期結果**：刷機工具顯示寫入完成，沒有出現校驗失敗的錯誤訊息。

> 💡 **想自己编译客製化镜像文件？** 官網下載的是預编译好的版本，對大部分人來說已經夠用。但如果你的專案需要客製化内核選項（例如加裝額外的内核模块），可以改用 Armbian 官方的建置框架自行编译：
> ```bash
> git clone https://github.com/armbian/build
> cd build
> ./compile.sh
> ```
> 這個做法對新手來說門檻較高（需要至少 8GB 記憶體、約 50GB 硬碟空間的编译環境），一般情況下不需要，直接用官網預编译镜像文件就好。

---

### 步骤 2：开机並插入 ALFA 网卡

开机進入 Armbian 系統後，把 ALFA AWUS036AXML（或其他型号）插入板子上**藍色的 USB 3.0 Type-A 連接埠**（板子上會有藍色跟黑色兩種顏色的 USB 埠，藍色代表 USB 3.0，傳輸速度較快，優先使用這個）。

---

### 步骤 3：驗證驱动與無線接口

```bash
# 檢查内核是否有正確辨識网卡
dmesg | grep -i "mt7921"

# 檢查無線接口狀態
iw dev
```

**預期結果**：`dmesg` 應該會顯示類似下面的訊息，代表固件已經正確加载：

```text
mt7921u 2-1:1.0: ASIC revision: 79610000
mt7921u 2-1:1.0: firmware: mediatek/WIFI_MT7961_patch_mcu_1_2_tv.bin loaded
mt7921u 2-1:1.0: firmware: mediatek/WIFI_RAM_CODE_MT7961_1_2.bin loaded
```

`iw dev` 則會列出一個新的無線接口（通常是 `wlan1`），代表网卡已經可以正常使用。

---

## 供電與散熱注意事項

- **供電預算**：RK3588 全速運作時的功耗大約落在 10〜15W，再加上外接的 ALFA 高功率网卡（約 2〜4W），整機建議使用**至少 5V/4A（20W）的 Type-C 電源供應器**，避免瞬間負載尖峰造成 USB 供電不穩、网卡斷線。
- **連接埠選擇**：優先使用獨立 USB 3.0 控制器通道的連接埠，避免跟其他高速周邊（例如 NVMe USB 外接盒）共用同一個 Hub，共用時容易互相搶頻寬跟供電。

---

## 常見問題與排除指引

### Q1：插入网卡後系統完全沒反應？
- **原因**：目前使用的是原廠 Vendor BSP 系統（内核版本較舊），對這顆芯片的支援還沒跟上。
- **解決方法**：改用 Armbian Mainline 系統（見步骤 1），内核版本較新，通常插入就能直接用。

### Q2：一定要用原廠系統，該怎麼辦？
- **原因**：原廠 Vendor BSP 系統内核版本較舊，需要手動補齊固件或驱动模块。
- **解決方法**：依照上方兼容性表格，手動安裝對應的内核模块（例如 `mt76x2u`），並確認固件文件已經放在系統正確的路徑下；如果覺得麻煩，改用 Armbian Mainline 會是更省事的做法。

### Q3：使用一段時間後网卡會斷線？
- **原因**：通常是供電不足，尤其是同時外接了其他高速裝置時。
- **解決方法**：確認電源供應器至少是 5V/4A（20W）；並檢查 ALFA 网卡跟其他裝置有沒有共用同一個 USB Hub，如果有，建議分開接到不同的獨立通道。

---

## 參考数据與延伸閱讀

- [AWUS036AXML 產品頁面](/alfa-network/products/awus036axml/)
- [AWUS036ACM 產品頁面](/alfa-network/products/awus036acm/)
- [ALFA 無線网卡在 Raspberry Pi 上（3 / 4 / 5）](/alfa-network/hardware/raspberry-pi/)——另一款輕量嵌入式主機的整合方式，概念可互相參照
- [詞彙表](/getting-started/glossary)——SBC、BSP、Mainline 内核等名詞的完整解釋
- [Armbian 官方網站](https://www.armbian.com/orange-pi-5/)——Orange Pi 5 系列的 Mainline 镜像文件下載（一般使用者從這裡下載即可）
- Armbian 官方建置框架（GitHub，適合需要自行编译客製化镜像文件的進階使用者）：https://github.com/armbian/build
- MediaTek MT76 系列驱动：https://github.com/morrownr/mt76
- Realtek RTL8812AU 驱动：https://github.com/aircrack-ng/rtl8812au

**標籤：** `orange-pi` `rk3588` `armbian` `rockchip` `alfa` `awus036axml` `awus036acm` `sbc` `新手指南`
