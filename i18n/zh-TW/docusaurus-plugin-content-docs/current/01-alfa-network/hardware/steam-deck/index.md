---
id: alfa-hardware-steam-deck
title: Steam Deck & UP Squared Pro × ALFA Network 整合指南
sidebar_label: Steam Deck / UP Squared
sidebar_position: 9
description: 無人機論文實測架構：UP Squared Pro 機載邊緣運算與 Steam Deck 地面站搭配 ALFA AWUS036ACH 實現 5.745GHz wfb-ng 長距離影像遙測鏈路設定教學。
tags: [steam-deck, steamos, up-squared, alfa, awus036ach, rtl8812au, wfb-ng, uav]
keywords: [Steam Deck, UP Squared Pro, AWUS036ACH, RTL8812AU, wfb-ng, 無人機, SteamOS 唯讀]
---

# Steam Deck & UP Squared Pro × ALFA Network 整合指南

> **一句話定位**：這是一個比較進階、專門的應用情境——用 UP Squared Pro 當機載邊緣運算主機、Steam Deck 當掌上型地面控制站，中間透過 ALFA AWUS036ACH 建立一條長距離、低延遲的單向影像與遙測傳輸鏈路，常見於無人載具系統（UAS，例如自製空拍機、地面機器人）的研究與實測專案。

## 這篇文章適合你嗎？

- **難度**：進階（需要熟悉 Linux 終端機操作，並對無線通訊的基本概念有一定了解）
- **預估時間**：45〜60 分鐘
- **你會用到的技能**：終端機操作、基本的無線網路概念（頻道、頻段）
- **讀完你可以做到**：
  1. 理解為什麼這類長距離遙測鏈路要用「單向廣播」而不是一般的雙向連線
  2. 在 SteamOS 這種唯讀系統上正確安裝驅動程式，且不破壞系統的安全性設計
  3. 知道系統更新後驅動程式為什麼會消失、該怎麼快速恢復

> ⚠️ **適用範圍提醒**：這篇文章記錄的是一個特定研究情境下的實測配置，跟前面幾篇「新手入門」性質的文章不太一樣，會用到比較多進階概念。如果你是第一次接觸 ALFA 網卡，建議先從 [Raspberry Pi 整合指南](/alfa-network/hardware/raspberry-pi/) 開始熟悉基本操作。

---

## 概念說明：這套鏈路架構在做什麼、為什麼這樣設計

一般空拍機或機器人的控制鏈路，通常需要「雙向」溝通——地面站送出控制指令，機載端回傳影像和感測器資料，兩邊要互相確認封包有沒有收到（也就是一般網路連線常見的 ACK 應答機制）。但這套機制在長距離、訊號不穩定的環境下有個缺點：每次應答都要花時間，距離一拉遠、訊號一變差，整體延遲就會明顯上升，畫面容易卡頓。

這裡採用的做法是 **`wfb-ng`（Wi-Fi Broadcast Next Generation）**，核心概念是把影像和遙測資料「單向廣播」出去，不等待對方確認收到與否：

- **機載端（UP Squared Pro）**：負責跑邊緣運算、擷取影像與感測器資料，透過 ALFA 網卡把資料廣播出去。
- **地面站（Steam Deck）**：帶著另一支 ALFA 網卡，接收機載端廣播出來的畫面與遙測資訊，讓操作者可以掌上型即時查看。

拿掉「等待確認」這個步驟，換來的是更低、更穩定的延遲——這對即時操控來說比「每個封包都保證送達」更重要，就算偶爾漏掉一兩幀畫面，也比整體延遲飆高來得好。

> 📘 **名詞小教室**
> - **wfb-ng（Wi-Fi Broadcast Next Generation）**：一套開源的無線影像/遙測廣播框架，專門為長距離、低延遲的單向資料傳輸設計，常見於自製空拍機、機器人的第一人稱視角（FPV）鏈路。
> - **ACK 應答機制**：一般網路連線中，接收方收到封包後會回傳一個「我收到了」的確認訊號給發送方；`wfb-ng` 這類單向廣播應用會刻意關閉這個機制，用犧牲一點可靠度換取更低的延遲。
> - **不可變（Immutable）唯讀檔案系統**：SteamOS 為了系統穩定性與安全性，預設把系統核心檔案設成「唯讀」，一般情況下不允許任意寫入或修改，這也是為什麼安裝驅動程式前需要先手動解除保護。

---

## 為什麼這個研究情境指定使用 AWUS036ACH？

在 `wfb-ng` 這類長距離單向廣播鏈路中，需要驅動程式能做到幾件比較特殊的事：把封包長度設到接近極限、關閉前面提到的 ACK 應答機制，並且能在非標準或特定的 5GHz 頻道（例如 5.745 GHz，頻道 149）上進行無連線的單向廣播。

**ALFA AWUS036ACH** 使用的 Realtek RTL8812AU 晶片，搭配獨立的功率放大器（PA）與訊號放大器（LNA），加上雙外接天線接口，是目前學術與社群社群驗證最扎實的長距離 `wfb-ng` 硬體方案。

> **老實說明**：目前有實際學術論文一手驗證的，僅限於 **AWUS036ACH（RTL8812AU 晶片）**。其他型號（如 AWUS036AXML、AWUS036ACM）在 `wfb-ng` 這個框架下，目前還沒有直接的實測數據可以佐證效果，這篇文章不對它們做過度推論。如果你想嘗試其他型號，建議先自行做小規模測試驗證。

---

## 你需要準備的東西

- [ ] **機載端硬體**：UP Squared Pro（或類似的邊緣運算主機）
- [ ] **地面站硬體**：Valve Steam Deck（SteamOS）
- [ ] **兩支 ALFA AWUS036ACH**：機載端和地面站各一支
- [ ] **驅動程式（GitHub）**：Realtek RTL8812AU 支援封包注入版本（aircrack-ng 社群維護）：https://github.com/aircrack-ng/rtl8812au

---

## Step-by-Step 設定教學（以 Steam Deck 端為例）

> UP Squared Pro 端通常執行一般的 Linux 發行版，驅動安裝方式可以參考 [ALFA 無線網絡卡在 Ubuntu 上的完整設定指南](/alfa-network/linux-setup-ubuntu/)。以下步驟示範難度較高的 Steam Deck（SteamOS）端安裝流程。

### 步驟 1：切換到桌面模式，並設定管理員密碼

從 Steam Deck 的電源選單切換到「桌面模式（Desktop Mode）」，打開內建的終端機程式 Konsole。如果你還沒設定過管理員密碼，先執行：

```bash
passwd
```

**預期結果**：系統要求你輸入並確認一組新密碼，設定完成後沒有錯誤訊息。

---

### 步驟 2：暫時解除唯讀保護

```bash
sudo steamos-readonly disable
```

**預期結果**：指令執行後沒有錯誤訊息，代表系統的根目錄檔案系統暫時切換成可寫入狀態，接下來才能安裝驅動程式。

---

### 步驟 3：安裝編譯工具並下載驅動原始碼

```bash
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman -Sy --needed base-devel linux-neptune-headers git dkms

git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**預期結果**：最後會看到 DKMS 安裝完成的訊息，代表驅動程式已經成功編譯並載入系統。這個步驟在 Steam Deck 上可能需要幾分鐘，請耐心等待，不要中途中斷。

---

### 步驟 4：重新啟用唯讀保護

```bash
sudo steamos-readonly enable
```

**預期結果**：指令執行後沒有錯誤訊息。**這一步不要跳過**——重新啟用唯讀保護是維護系統穩定性與安全性的重要步驟，跳過的話系統之後可能會出現不可預期的問題。

---

### 步驟 5：驗證網卡是否正確辨識

```bash
lsusb | grep -i realtek
iw dev
```

**預期結果**：`lsusb` 應該會看到 Realtek RTL8812AU 的裝置資訊，`iw dev` 則會列出一個新的無線介面，代表 ALFA 網卡已經可以被 `wfb-ng` 使用。

---

## SteamOS 系統更新防護提醒（重要踩坑點）

SteamOS 有一個容易讓人踩坑的機制：**A/B 分區覆蓋**。每次進行重大系統更新時，SteamOS 會把系統寫入一個全新的分區，這代表你先前手動編譯安裝在 `/usr/lib/modules/` 底下的 DKMS 驅動程式，會在更新後被還原成原本沒裝驅動的狀態——也就是說，**系統更新之後，你的 ALFA 網卡很可能又抓不到了**，這不是設定跑掉，是 SteamOS 更新機制本身的設計。

**建議做法**：把步驟 1〜4 的指令整理成一支腳本，存在 `/home/deck/scripts/rebuild_alfa.sh`，之後每次系統更新完，只需要重新執行這支腳本一次，就能快速恢復外接網卡的功能，不用每次都手動重打一遍指令。

---

## 常見問題與排除指引

### Q1：系統更新後網卡突然又抓不到了？
- **原因**：SteamOS 的 A/B 分區覆蓋機制，重大更新會清空先前手動安裝的 DKMS 驅動。
- **解決方法**：重新執行步驟 1〜4（建議先準備好前述的自動化腳本），驅動程式會重新編譯安裝一次。

### Q2：`sudo ./dkms-install.sh` 編譯失敗？
- **原因**：可能是 `linux-neptune-headers`（Steam Deck 專用的核心標頭檔）版本跟目前系統核心版本不匹配，尤其是剛更新完系統的情況下。
- **解決方法**：先執行 `sudo pacman -Syu` 確認套件庫是最新的，再重新執行 `sudo pacman -Sy --needed base-devel linux-neptune-headers git dkms`，確保標頭檔版本跟目前核心一致。

### Q3：忘記重新啟用唯讀保護會怎樣？
- **原因**：唯讀保護是 SteamOS 設計上的一部分，用來確保系統檔案不會被意外修改或損壞。
- **解決方法**：只要想起來，隨時執行 `sudo steamos-readonly enable` 補回來即可，不會有無法復原的問題，但建議養成安裝完立刻重新啟用的習慣，避免忘記。

### Q4：能不能用其他型號的 ALFA 網卡（AXML / ACM）試試看？
- **原因**：目前 `wfb-ng` 框架下，只有 AWUS036ACH 有實際學術論文驗證過的數據。
- **解決方法**：技術上可以嘗試，但目前沒有現成的實測數據可以參考，建議自己先做小規模、短距離的測試，確認延遲與可靠度符合你的需求後，再應用到正式場景。

---

## 參考資料與延伸閱讀

- [AWUS036ACH 產品頁面](/alfa-network/products/awus036ach/)
- [ALFA 無線網絡卡在 Ubuntu 上的完整設定指南](/alfa-network/linux-setup-ubuntu/)——UP Squared Pro 端的驅動安裝可參考此篇
- [詞彙表](/getting-started/glossary)——wfb-ng、ACK 應答機制等名詞的完整解釋
- Realtek RTL8812AU 驅動（aircrack-ng 社群維護，含封包注入支援）：https://github.com/aircrack-ng/rtl8812au
- [wfb-ng 官方專案](https://github.com/svpcom/wfb-ng)——開源的無線影像/遙測廣播框架

**標籤：** `steam-deck` `steamos` `up-squared` `alfa` `awus036ach` `rtl8812au` `wfb-ng` `無人載具系統` `進階`
