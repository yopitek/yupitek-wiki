---
id: alfa-hardware-openwrt-router
title: OpenWrt Routers × ALFA Network Configuration & Known Limitations
sidebar_label: OpenWrt Routers
sidebar_position: 7
description: Guide to configuring ALFA AWUS036AXML (MT7921U) and AWUS036ACM (MT7612U) on OpenWrt and GL.iNet routers, package installation, and upstream bug #839 workarounds.
tags: [openwrt, glinet, router, alfa, awus036axml, mt7921u, mt7612u, kmod]
keywords: [OpenWrt, GL.iNet, AWUS036AXML, AWUS036ACM, kmod-mt7921u, mt76, active monitor bug]
---

# OpenWrt Routers × ALFA Network Configuration & Limitations Guide

> **Quick Summary**: Adding an external ALFA USB adapter to OpenWrt routers (including GL.iNet travel routers, x86 soft routers, and Raspberry Pi gateways) creates a dedicated secondary WAN (WISP repeater), high-gain AP hotspot, or dedicated wireless sniffer node. The **ALFA AWUS036AXML** (MT7921U) is supported via package feeds in OpenWrt 22.03.3+ (kernel 5.10 backport) and 23.05+ (kernel 5.15), while **AWUS036ACM** (MT7612U) is supported across all branches. This guide covers setup and discloses **upstream GitHub Issue #839 (Active Monitor Lockup)**.

---

## 1. Kernel & Compatibility Matrix

```mermaid
flowchart TD
    subgraph OpenWrt["OpenWrt Release Branches"]
        V22["OpenWrt 22.03.3+<br/>(Kernel 5.10 Backport)"]
        V23["OpenWrt 23.05+<br/>(Kernel 5.15 Mainline)"]
        OldGL["Legacy GL.iNet Firmware (v3.x / Kernel 4.14)"]
    end

    subgraph Adapters["ALFA Hardware Support Status"]
        MT7612["AWUS036ACM (MT7612U)<br/>✅ Fully Supported (kmod-mt76x2u)"]
        MT7921["AWUS036AXML (MT7921U)<br/>⚠️ Conditional Support (kmod-mt7921u)"]
        RTL["AWUS036ACH (RTL8812AU)<br/>❌ No official packages (Requires custom SDK build)"]
    end

    V22 --> MT7612
    V22 --> MT7921
    V23 --> MT7612
    V23 --> MT7921
    OldGL --> MT7612
    OldGL -.->|Unsupported| MT7921
```

| ALFA Model | Chipset | OpenWrt 22.03.3+ | OpenWrt 23.05+ | Required Kernel Packages |
|---|---|---|---|---|
| **AWUS036ACM** | MediaTek MT7612U | ✅ Fully Supported | ✅ Fully Supported | `kmod-mt76x2u` `mt76-firmware` |
| **AWUS036AXML** | MediaTek MT7921AUN | ✅ Supported (Known Bug) | ✅ Supported (Known Bug) | `kmod-mt7921u` |
| **AWUS036ACHM** | MediaTek MT7610U | ✅ Fully Supported | ✅ Fully Supported | `kmod-mt76x0u` |
| **AWUS036ACH** | Realtek RTL8812AU | ❌ Not in official feed | ❌ Not in official feed | Requires building custom out-of-tree package |

---

## 2. Package Installation & Wireless Setup

```bash
# 1. Update package database
opkg update

# 2. Install kernel modules for your ALFA adapter
# For AWUS036AXML (Wi-Fi 6/6E):
opkg install kmod-mt7921u kmod-mt76-core wireless-tools usbutils

# For AWUS036ACM (802.11ac):
opkg install kmod-mt76x2u kmod-mt76-core wireless-tools usbutils

# 3. Detect and generate configuration
wifi config >> /etc/config/wireless

# 4. Restart network stack
/etc/init.d/network restart
```

---

## 3. Crucial Upstream Limitations & Bug Disclosure

### ⚠️ Upstream Bug: AWUS036AXML Active Monitor Crash (Issue #839)
- **Symptom**: Enabling active monitor mode and continuous frame injection (e.g. `aireplay-ng --deauth`) on `mt7921u` under OpenWrt causes the driver to lock up within seconds (`mt7921u: failed to send tx packet`).
- **Root Cause**: Upstream `openwrt/mt76` Issue #839 (DMA concurrency locking error in 5.10/5.15 kernels).
- **Engineering Recommendation**:
  1. For **passive packet capture** (Kismet / tcpdump), AWUS036AXML works normally.
  2. For **high-rate packet injection / deauth testing**, use **ALFA AWUS036ACM** (`mt76x2u`).

### ⚠️ 6 GHz Configuration Status
Current LuCI Web UI (OpenWrt 23.05) lacks complete 6 GHz channel selectors. AWUS036AXML operates primarily as an ultra-high performance 2.4 GHz / 5 GHz radio under OpenWrt.
