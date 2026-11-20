---
id: alfa-hardware-android-nethunter
title: Android Kali NetHunter × ALFA Network Integration & Power Guide
sidebar_label: Android NetHunter
sidebar_position: 6
description: Kali NetHunter mobile wireless auditing guide with ALFA USB adapters — OTG Y-cable power configuration, in-kernel modules, and packet injection workflows.
tags: [kali, nethunter, android, otg, alfa, awus036ach, rtl8812au, monitor-mode]
keywords: [Kali NetHunter, Android OTG, AWUS036ACH, AWUS036NEH, AWUS036NHA, RTL8812AU, Y-cable]
---

# Android Kali NetHunter × ALFA Network Integration & Power Guide

> **Quick Summary**: Kali NetHunter official documentation ([kali.org/docs/nethunter/wireless-cards/](https://www.kali.org/docs/nethunter/wireless-cards/)) certifies the **ALFA AWUS036ACH**, **AWUS036NEH**, and **AWUS036NHA** for mobile wireless auditing. When using high-power external adapters on Android smartphones, the **OTG Power Budget** is the single most critical factor for stability. This guide details proper Y-cable cabling, kernel modules, and penetration testing workflows.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **Kali NetHunter on Android hardware has not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. The adapter list comes from the Kali NetHunter documentation; whether a driver is available depends on the NetHunter kernel version on your phone. Only test networks you own or are authorized to test.

## Power Budget: Overcoming Mobile OTG Current Limits

Standard Android USB-C / Micro-USB ports in OTG Host mode are restricted to **500mA (2.5W)**. High-power adapters like the ALFA AWUS036ACH (equipped with dual power amplifiers) draw up to **3.6W (720mA @ 5V)** during active packet transmission, triggering immediate smartphone brownouts or USB resets without external power.

```mermaid
flowchart LR
    subgraph Phone["Rooted Android Smartphone"]
        NetHunter["Kali NetHunter Chroot<br/>(aircrack-ng / wifite)"]
        Kernel["NetHunter Kernel<br/>(Wireless Driver Modules)"]
        USBPort["USB Type-C OTG Host"]
    end

    subgraph Cable["USB-C OTG Y-Cable Splitter"]
        DataLine["Data Lines (D+ / D-)"]
        PowerIn["External 5V Power Line"]
    end

    PowerBank["External Power Bank<br/>(5V 2A Output)"]
    ALFA["ALFA AWUS036ACH / NHA<br/>(High-Power Adapter)"]

    Phone <-->|OTG Data| DataLine
    PowerBank -->|Injected Power| PowerIn
    DataLine --> ALFA
    PowerIn --> ALFA
```

---

## Step-by-Step Setup

### Step 1: Connect via USB-C OTG Y-Cable
1. Connect the data branch of the Y-cable to the smartphone.
2. Connect the power branch to an external 5V/2A power bank.
3. Connect the output port to your ALFA adapter.

### Step 2: Verify in NetHunter Terminal
```bash
# Check USB device detection
lsusb

# Check network interfaces
ip link show
```

### Step 3: Enable Monitor Mode and Run Wifite
```bash
# Start monitor mode on wlan1
# (do NOT run `airmon-ng check kill`: it terminates NetworkManager)
airmon-ng start wlan1

# Launch automated audit
wifite -i wlan1mon
```
