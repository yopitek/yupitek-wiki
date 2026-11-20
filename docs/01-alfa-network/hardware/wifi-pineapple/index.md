---
id: alfa-hardware-wifi-pineapple
title: Hak5 WiFi Pineapple × ALFA Network Integration Guide
sidebar_label: Hak5 WiFi Pineapple
sidebar_position: 4
description: Complete integration guide for Hak5 WiFi Pineapple Mark VII & Enterprise with ALFA AWUS036ACM for 5GHz dual-band Recon, PineAP injection, and antenna selection.
tags: [hak5, wifi-pineapple, mk7, alfa, awus036acm, mt7612u, 5ghz]
keywords: [WiFi Pineapple, Hak5, AWUS036ACM, MT7612U, 5GHz monitor mode, PineAP, MK7AC]
---

# Hak5 WiFi Pineapple × ALFA Network Integration Guide

> **Quick Summary**: Hak5 official documentation ([docs.hak5.org](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)) explicitly designates the **MediaTek MT7612U** chipset as the only 802.11ac external adapter guaranteed to work reliably in all penetration testing scenarios. The **ALFA AWUS036ACM** shares the exact same MT7612U chipset architecture as the Hak5 MK7AC OEM module, but exposes two RP-SMA antenna ports so you can fit higher-gain antennas for 5 GHz auditing and PineAP rogue AP campaigns.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **The WiFi Pineapple has not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. On the GX10 test platform the ACM supported monitor mode on 2.4 / 5 GHz, injection at 63-83% (2.4 GHz) and 76% (5 GHz), and AP mode on both bands. Only test networks you own or are authorized to test.

## Is This Guide for You?

- **Difficulty**: Intermediate.
- **Estimated Time**: 20–30 minutes.
- **Skills Used**: Terminal commands, Web UI administration.
- **What You Will Achieve**:
  1. Correctly connect and identify the ALFA adapter on the WiFi Pineapple.
  2. Configure dual-band 2.4 GHz + 5 GHz Recon scanning and rogue AP broadcasting in the Web UI.
  3. Select optimal antenna configurations for omnidirectional or directional audits.

---

## Why the WiFi Pineapple Requires an External Adapter

The WiFi Pineapple Mark VII features internal 2.4 GHz radios. To audit modern enterprise 5 GHz (802.11a/n/ac) networks, an external USB radio module is required.

On older embedded OpenWrt kernels (before Linux 6.13 for ACH / ACS, 6.2 for EACS, 6.17 for AX / AXER), Realtek chipsets rely on out-of-tree drivers, and Hak5 guarantees only the MT7612U chipset for 802.11ac adapters. The MediaTek `mt76x2u` driver used by the AWUS036ACM has been in the mainline kernel since 4.19 and is available in the OpenWrt kernel.

---

## Step-by-Step Setup

### Step 1: Hardware Connection & Power
1. Plug the ALFA AWUS036ACM into the **USB Host** port of the WiFi Pineapple Mark VII.
2. Use a dedicated 5V/3A (15W) power adapter to prevent voltage drop.

### Step 2: SSH Verification
```bash
# Verify USB device detection
lsusb
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check kernel driver binding
dmesg | grep -E "mt76|wlan"
# Expected: ieee80211phy3: mt76x2u registered as wlan3
```

### Step 3: Web UI Configuration
1. Open your browser and navigate to `http://172.16.42.1:1471`.
2. Navigate to **Recon**: Select `wlan3 (5GHz)` from the interface dropdown, check **2.4 GHz + 5 GHz**, and click **Start Scan**.
3. Navigate to **PineAP**: Assign `wlan3` as the 5 GHz target interface for dual-band rogue AP broadcasting.
