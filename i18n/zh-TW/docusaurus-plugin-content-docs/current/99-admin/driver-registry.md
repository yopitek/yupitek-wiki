---
slug: driver-registry
id: admin-driver-registry
title: 驅動程式登記表
sidebar_position: 2
description: Wiki 中每個已記錄的無線晶片組，對應到它所支援的 ALFA 網卡、驅動程式類型與內建於核心的狀態。
---

# 驅動程式登記表

驅動程式登記表把每個**無線晶片組**對應到使用它的 ALFA 網卡、**驅動程式類型**，以及現代 Linux 核心上的**內建於核心狀態**。這與 [`linux-compatibility-matrix`](/alfa-network/linux-compatibility-matrix/) 及 [`/alfa-network/drivers/`](/alfa-network/drivers/) 下的各晶片驅動程式指南互相呼應。

## 晶片組表格

| 晶片組 | 網卡 | 驅動程式綁定 | 內建於核心？ | 驅動程式指南 |
|---------|----------|----------------|------------|--------------|
| MT7612U | AWUS036ACM | `mt76x2u` | ✅ 內建於核心 | [指南](/alfa-network/drivers/mt7612u/) |
| MT7610U | AWUS036ACHM | `mt76x0u` | ✅ 內建於核心 | [指南](/alfa-network/drivers/mt7610u/) |
| MT7921AUN | AWUS036AXM、AWUS036AXML | `mt7921u` | ✅ 內建於核心 | [指南](/alfa-network/drivers/mt7921aun/) |
| RTL8812AU | AWUS036ACH | 樹外 / DKMS | ❌ 未內建於核心 | [指南](/alfa-network/drivers/rtl8812au/) |
| RTL8811AU | AWUS036ACS | 樹外 / DKMS | ❌ 未內建於核心 | [指南](/alfa-network/drivers/rtl8811au/) |
| RTL8832BU | AWUS036AX、AWUS036AXER | 樹外 / DKMS | ❌ 未內建於核心 | [指南](/alfa-network/drivers/rtl8832bu/) |
| RTL8821CU | AWUS036EACS | 樹外 / DKMS | ❌ 未內建於核心 | [指南](/alfa-network/drivers/rtl8821cu/) |

## 驅動程式類型

- **內建於核心（mainline）** — 已包含在 Linux 核心中；網卡在最新核心上通常開箱即用，不需要額外安裝。MediaTek（`mt76x2u` / `mt76x0u` / `mt7921u`）網卡屬於此類。
- **樹外 / DKMS** — 驅動程式原始碼維護在核心之外。必須編譯並安裝，理想上透過 DKMS 讓它在核心更新後仍然可用。本登記表中的所有 Realtek 晶片組都屬於此類。

## 核心更新

對樹外驅動程式而言，最常見的單一失敗原因是**核心更新**破壞模組——因為預先建置的模組不再符合執行中的核心。

```bash
# Rebuild DKMS modules for the currently running kernel
sudo dkms autoinstall

# Or, for a convenient apt-managed rebuild on Debian/Ubuntu
sudo apt install --reinstall linux-headers-$(uname -r)
```

另請參閱 [FAQ](/getting-started/faq/) 與 [`troubleshooting`](/alfa-network/troubleshooting/)。

## 驅動程式設定指南

- [`ubuntu`](/alfa-network/linux-setup-ubuntu/)、[`kali`](/alfa-network/linux-setup-kali/) 與 [`nethunter`](/alfa-network/linux-setup-nethunter/) 涵蓋完整的系統設定。
- [`shared ALFA Linux guide`](/sdrlab/shared/alfa-linux-guide/) 在 SDRLAB 中重複使用 ALFA 驅動程式知識時被引用。

## 維護

每當驅動程式指南、網卡產品頁面或相容性矩陣被編輯時，請保持本登記表同步，讓交叉引用永遠不會脫節。