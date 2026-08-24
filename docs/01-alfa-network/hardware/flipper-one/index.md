---
id: alfa-hardware-flipper-one
title: Flipper One × ALFA Network Compatibility & Selection Guide
sidebar_label: Flipper One
sidebar_position: 5
description: Technical architecture analysis of Flipper One (ARM Linux) with native MT7921AUN Wi-Fi 6E chipset, external ALFA AWUS036AXML / ACM selection, and Flipper Zero non-host limitations.
tags: [flipper, flipper-one, flipper-zero, alfa, awus036axml, mt7921aun, wifi-6e]
keywords: [Flipper One, Flipper Zero, AWUS036AXML, MT7921AUN, Wi-Fi 6E, USB Host]
---

# Flipper One × ALFA Network Compatibility & Selection Guide

> **Quick Summary**: Flipper One is powered by an ARM Cortex-A application processor running full embedded Linux. Its integrated Wi-Fi 6E module is powered by the **MediaTek MT7921AUN** chipset (the exact same silicon inside the **ALFA AWUS036AXML**). This guide analyzes Flipper One's internal radio architecture versus external high-gain ALFA USB adapters, and clarifies why **Flipper Zero (which lacks USB Host mode) cannot support external Wi-Fi adapters**.

---

## 1. Flipper Zero vs. Flipper One: Architectural Differences

A common community misconception is attempting to plug ALFA USB adapters into Flipper Zero via USB-C OTG adapters. This is physically and architecturally impossible:

```mermaid
flowchart TD
    subgraph Zero["Flipper Zero (Microcontroller Architecture)"]
        MCU["STM32WB55 MCU<br/>(Cortex-M4 + M0+)"]
        USBDev["USB Type-C Controller<br/>(Device / Client Mode Only)"]
        GPIO["GPIO Expansion Header (3.3V UART / SPI)"]
        LimitZero["❌ Cannot drive USB Wi-Fi adapters<br/>(Only supports external ESP32 Wi-Fi development boards)"]
        MCU --> USBDev
        MCU --> GPIO
        GPIO -.-> LimitZero
    end

    subgraph One["Flipper One (Single Board Computer Architecture)"]
        SoC["ARM Cortex-A Application Processor<br/>(Full Linux Kernel OS)"]
        BuiltinRadio["Internal Wi-Fi 6E / BT 5.2<br/>(MediaTek MT7921AUN Chipset)"]
        USBHost["USB Type-C OTG Controller<br/>(Supports True USB Host Mode)"]
        SupportOne["✅ Native Support for External ALFA USB Adapters<br/>(Built-in mt76 / mt7921u kernel drivers)"]
        SoC --> BuiltinRadio
        SoC --> USBHost
        USBHost --> SupportOne
    end
```

---

## 2. Integrated Radio vs. External ALFA Adapter Selection Matrix

| Comparison Dimension | Flipper One Internal Radio | External ALFA AWUS036AXML | External ALFA AWUS036ACM |
|---|---|---|---|
| **Chipset** | MediaTek MT7921AUN | MediaTek MT7921AUN | MediaTek MT7612U |
| **Protocols** | Wi-Fi 6E (802.11ax) | Wi-Fi 6E (802.11ax) | Wi-Fi 5 (802.11ac) |
| **Frequency Bands** | 2.4 GHz / 5 GHz / 6 GHz | 2.4 GHz / 5 GHz / 6 GHz | 2.4 GHz / 5 GHz |
| **Antenna Type** | Internal miniature PCB trace | 2× 5dBi Detachable RP-SMA | 2× 5dBi Detachable RP-SMA |
| **Tx Power (EIRP)** | Standard handheld limit (~15 dBm) | High-power amplifiers (~20-23 dBm) | High-power amplifiers (~20-23 dBm) |
| **Linux Driver** | `mt7921u` (In-kernel) | `mt7921u` (In-kernel) | `mt76x2u` (In-kernel) |
| **Recommendation** | Portable stealth scanning | 🏆 **Top Pick**: Long-range Wi-Fi 6E spectrum auditing | 🥈 **Best Value**: Ultra-stable 5 GHz packet injection |

---

## 3. Dual-Radio Architecture Configuration

By plugging an external ALFA AWUS036AXML into Flipper One, you establish a dual-radio setup:

```bash
# 1. Verify USB identification
lsusb
# Expected: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# 2. Inspect PHY capabilities
iw phy
# Bands: 2.4 GHz, 5 GHz, and 6 GHz HE channels

# 3. Configure dual-radio topology
# wlan0 (Internal): Maintains hotspot association for SSH / Web UI
# wlan1 (External ALFA): Dedicated monitor interface
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

---

## 4. Current Development Status & Limitations

1. **6 GHz Packet Injection**: While 6 GHz (Wi-Fi 6E) scanning and association are natively supported in Linux kernels ≥5.18, some open-source injection tools are still finalizing 6 GHz management frame injection specifications.
2. **Power Draw**: When running active high-power injection with AWUS036AXML, battery consumption increases. A powered USB-C hub is recommended for multi-hour lab engagements.
