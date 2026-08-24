---
id: alfa-hardware-flipper-one
title: Flipper One × ALFA Network Compatibility & Selection Guide
sidebar_label: Flipper One
sidebar_position: 5
description: Architecture analysis of Flipper One (ARM Linux) with native MT7921AUN Wi-Fi 6E chipset, external ALFA adapter selection, and Flipper Zero non-host limitations.
tags: [flipper, flipper-one, flipper-zero, alfa, awus036axml, mt7921aun, wifi-6e]
keywords: [Flipper One, Flipper Zero, AWUS036AXML, MT7921AUN, Wi-Fi 6E, USB Host]
---

# Flipper One × ALFA Network Compatibility & Selection Guide

> **Quick Summary**: Flipper One is powered by an ARM Cortex-A application processor running full embedded Linux. Its integrated Wi-Fi 6E module is powered by the **MediaTek MT7921AUN** chipset (the exact same silicon inside the **ALFA AWUS036AXML**). This guide analyzes Flipper One's internal radio architecture versus external high-gain ALFA USB adapters, and clarifies why **Flipper Zero (which lacks USB Host mode) cannot support external Wi-Fi adapters**.

## Architectural Differences: Flipper Zero vs. Flipper One

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

## Dual-Radio Operation on Flipper One

By connecting an external ALFA AWUS036AXML via USB-C OTG, you can establish a dual-radio setup:
- **Internal MT7921AUN (`wlan0`)**: Maintains connection to a phone hotspot or local network for SSH/Web management.
- **External ALFA Adapter (`wlan1`)**: Dedicated high-power radio for monitor mode and packet capture.

```bash
# Verify USB connection
lsusb

# Enable monitor mode on external adapter
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```
