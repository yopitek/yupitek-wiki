---
id: alfa-hardware-openwrt-router
title: OpenWrt Routers × ALFA Network Configuration & Known Limitations
sidebar_label: OpenWrt Routers
sidebar_position: 7
description: Guide to configuring ALFA AWUS036AXML (MT7921U) and AWUS036ACM (MT7612U) on OpenWrt and GL.iNet routers, package installation, and upstream bug #839 workarounds.
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt Routers × ALFA Network Configuration & Known Limitations

> **Quick Summary**: Adding an external ALFA USB adapter to an OpenWrt router (or GL.iNet travel router) creates a dedicated second WAN (WISP repeater), high-gain hotspot AP, or wireless sniffer node. This guide covers package installation and openly discloses **upstream GitHub Issue #839 (Active Monitor Driver Crash)** with workarounds.

## Is This Guide for You?

- **Difficulty**: Intermediate (familiarity with OpenWrt LuCI web interface and SSH terminal).
- **Estimated Time**: 20–30 minutes.
- **Skills Used**: Basic terminal operations, `opkg` package management, network configuration.
- **What You Will Achieve**:
  1. Determine compatibility between your OpenWrt version and ALFA adapter models.
  2. Install drivers via `opkg` and verify adapter detection in LuCI / UCI.
  3. Understand and work around upstream Active Monitor Mode bugs.

---

## Why Connect an External ALFA Adapter to an OpenWrt Router?

OpenWrt routers and x86 soft routers typically have built-in Wi-Fi radios. Connecting an external ALFA adapter unlocks key operational capabilities:

1. **Independent Secondary Radio (WISP / Repeater)**: Keep the router's internal radio dedicated to local LAN broadcasting while using the high-gain ALFA adapter to bridge long-range upstream public Wi-Fi.
2. **Dedicated Wireless Sniffing Node**: Turn a compact router (like a GL.iNet) into a standalone 24/7 wireless auditing probe without tying up a laptop.
3. **Upgrade Older Hardware**: Add 802.11ac or Wi-Fi 6 capabilities to older routers via USB without replacing the router.

---

## OpenWrt Version & ALFA Chipset Compatibility Matrix

| ALFA Model | Chipset | OpenWrt 22.03.3+ | OpenWrt 23.05+ | Required Kernel Packages |
|---|---|---|---|---|
| **AWUS036ACM** | MediaTek MT7612U | ✅ Fully Supported | ✅ Fully Supported | `kmod-mt76x2u` `mt76-firmware` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ Supported (Known Bug) | ✅ Supported (Known Bug) | `kmod-mt7921u` |
| **AWUS036ACHM** | MediaTek MT7610U | ✅ Fully Supported | ✅ Fully Supported | `kmod-mt76x0u` |
| **AWUS036ACH** | Realtek RTL8812AU | ❌ Not in official feed | ❌ Not in official feed | Requires custom SDK compilation |

---

## Prerequisites & Checklist

- [ ] OpenWrt router (running OpenWrt 22.03.3+ or 23.05+) with an active internet connection.
- [ ] ALFA USB adapter: **AWUS036ACM** (Recommended for penetration testing) or **AWUS036AXML** (Recommended for Wi-Fi 6 high throughput).
- [ ] SSH client access to the router.

---

## Step-by-Step Configuration

### Step 1: Install Kernel Drivers via `opkg`

SSH into your OpenWrt router and run:

```bash
# Update package index
opkg update

# For AWUS036AXML (Wi-Fi 6/6E):
opkg install kmod-mt7921u kmod-mt76-core wireless-tools usbutils

# For AWUS036ACM (802.11ac):
opkg install kmod-mt76x2u kmod-mt76-core wireless-tools usbutils
```

### Step 2: Plug in Adapter and Verify Detection

```bash
lsusb
dmesg | grep -E "mt7921|mt76"
```

### Step 3: Generate Wireless Config and Restart Network

```bash
wifi config >> /etc/config/wireless
/etc/init.d/network restart
```

Log in to the LuCI Web UI (`Network → Wireless`). You will see a new radio device (e.g. `radio1` or `radio2`) ready for AP or Client configuration.

---

## Important Upstream Limitations & Bug Warnings

### ⚠️ Known Bug: AWUS036AXML Active Monitor Mode Driver Crash (Issue #839)
- **Symptom**: Enabling active monitor mode and continuous frame injection (such as deauth frames) on `mt7921u` under OpenWrt causes the driver to lock up within seconds (`mt7921u: failed to send tx packet`), taking the adapter offline.
- **Root Cause**: Upstream `openwrt/mt76` Issue #839 (DMA concurrency locking bug in 5.10/5.15 kernels).
- **Engineering Workaround**:
  1. For **passive packet capture** (Kismet / tcpdump), AWUS036AXML works normally.
  2. For **high-rate packet injection / deauth testing**, use **ALFA AWUS036ACM** (`mt76x2u`), which has proven rock-solid over years of upstream testing.

### ⚠️ 6 GHz Configuration Status
Current LuCI Web UI (OpenWrt 23.05) lacks complete 6 GHz channel selectors. AWUS036AXML operates primarily as an ultra-high performance 2.4 GHz / 5 GHz radio under OpenWrt.
