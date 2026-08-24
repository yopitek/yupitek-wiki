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

> **Quick Summary**: Hak5 official documentation ([docs.hak5.org](https://docs.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters/)) explicitly designates the **MediaTek MT7612U** chipset as the only 802.11ac external adapter guaranteed to work reliably in all penetration testing scenarios. The **ALFA AWUS036ACM** shares the exact same MT7612U chipset architecture as the Hak5 MK7AC OEM module, but provides higher antenna gain via dual RP-SMA ports and enhanced thermal dissipation for prolonged 5 GHz auditing and PineAP rogue AP campaigns.

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

Under embedded OpenWrt kernels, Realtek chipsets rely on out-of-tree drivers that frequently trigger kernel panics during high-throughput packet injection. The MediaTek `mt76x2u` driver in the AWUS036ACM is compiled directly into the OpenWrt kernel, offering superior DMA buffer reclamation and thermal stability.

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
