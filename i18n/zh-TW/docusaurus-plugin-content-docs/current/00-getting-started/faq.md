---
slug: faq
id: getting-started-faq
title: 常見問題
sidebar_position: 3
description: 關於 Yupitek 產品、Linux 驅動程式支援與下載的常見問題。
---

# 常見問題

關於 Yupitek 產品、Linux 支援與下載的常見問題解答。

## 我的 Wi-Fi 無線網絡卡在 Linux 上可以開箱即用嗎？

這取決於晶片組。使用 **MediaTek** 晶片組（`mt7612u`、`mt7610u`、`mt7921aun`）的無線網絡卡具備**內建核心（in-kernel）**驅動程式 — 在較新的 Ubuntu、Kali 與 Fedora 上無需安裝任何東西即可使用。使用 **Realtek** 晶片組（`rtl8812au`、`rtl8811au`、`rtl8832bu`、`rtl8821cu`）的無線網絡卡通常需要安裝樹外（out-of-tree）DKMS 驅動程式。完整的詳細說明請參閱 [Linux 相容性矩陣](/alfa-network/linux-compatibility-matrix/)。

## 我要去哪裡下載驅動程式與韌體？

產品韌體與驅動程式託管在我們的 Cloudflare R2 下載伺服器 **dl.yupitek.com** 上。每個產品頁面都會連結到它所需的確切驅動程式與韌體，而 [ALFA Network](/alfa-network/) 下的驅動程式頁面則依晶片組分類檔案。請務必從 Yupitek 官方連結下載，而非第三方映象站，以避免取得被竄改的韌體。

## 支援哪些作業系統？

**ALFA Network** 無線網絡卡支援 **Kali Linux**、**Ubuntu** 與 **Android NetHunter**，另外在標示處也支援 Windows 與 macOS。在硬體整合方面，ALFA 無線網絡卡已針對 **NVIDIA Jetson**、**Raspberry Pi 3/4/5** 與 **Unitree** 機器人撰寫檔案。逐步操作說明請參閱 [Linux 設定](/alfa-network/linux-setup-ubuntu/) 指南。

## 什麼是 monitor mode（監聽模式），我要如何啟用它？

監聽模式讓無線網絡卡無需連線到任何網路，即可擷取與注入原始的 802.11 訊框。使用 `airmon-ng` 與 `airodump-ng` 進行稽核時需要此模式。並非每個晶片組都能良好支援。我們的 [監聽模式](/alfa-network/linux-setup-kali/) 指南會逐步說明受支援的晶片組。

## 我要如何知道我的晶片組是否支援封包注入（packet injection）？

晶片組的支援程度不一。ALFA 無線網絡卡所使用的 MediaTek 與 Realtek 晶片組通常支援監聽模式與封包注入，但確切行為取決於所使用的驅動程式。在開始任何測試任務前，請務必先用 `aireplay-ng --test` 快速測試。

## 我的驅動程式在核心更新後無法運作

Realtek 的樹外 DKMS 驅動程式偶爾會在核心升級後失效。修復方式通常是重建模組：

```bash
sudo dkms autoinstall
sudo modprobe <chipset-module>
```

請參閱適用於您無線網絡卡的特定 [晶片組驅動程式](/alfa-network/drivers/) 指南，以取得確切的模組名稱。

## Hak5 工具需要 Hak5 雲端（o.mg.lol）嗎？

**不需要。** 您可以完全離線設定與執行大多數 Hak5 裝置。不過，**O.MG** 產品系列與 `o.mg.lol` 雲端平臺繫結：每臺 O.MG 裝置在首次使用前，都必須使用 **O.MG Programmer** 啟用，並註冊到 `o.mg.lol` 帳號。裝置專屬的設定方式請參閱 [Hak5 專區](/hak5/)。

## 使用 Flipper Zero 合法嗎？

Flipper Zero 是學習、研究與無線電測試的合法工具。特定用途是否合法，取決於您當地的法律，以及您是否獲得傳送或接收這些訊號的許可。我們鼓勵負責任且合乎道德的使用方式。

## 我可以將 ACS 讀卡機用於網頁 NFC 嗎？

- **ACR1252U**：可搭配 Android 版 Chrome 的 **Web NFC API** 使用，也可透過 PC/SC + WebUSB 橋接器搭配桌面瀏覽器使用。
- **ACR122U** 與 **ACR1552U**：使用 **PC/SC** 框架（ACR122U 另可使用 libnfc）。

讀卡機專屬的指引請參閱 [ACS 區塊](/acs/)。

## 你們有託管 SDRLAB TRX-duo 的 SD 映像檔嗎？

TRX-duo 是與 Red Pitaya 相容的開發板。其 SD 卡映像檔由上游開源專案維護，因此我們連結到**官方**下載（trx-duo.com 與 Red Pitaya 社群儲存庫），而不是託管可能過期的副本。其他所有檔案我們都託管在 **dl.yupitek.com**。

## 我可以在哪裡獲得更多協助？

- 搜尋本 Wiki — 頂端導覽列的搜尋涵蓋所有品牌。
- 檢視品牌的**疑難排解**頁面（例如 [ALFA 疑難排解](/alfa-network/troubleshooting/)）。
- 造訪 [Yupitek 官方網站](https://www.yupitek.com) 以取得聯絡與銷售支援。