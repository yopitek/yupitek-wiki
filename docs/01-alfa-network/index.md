---

id: alfa-index
title: ALFA Network
sidebar_position: 1
description: ALFA Network Wi-Fi adapters, antennas, Linux drivers, Kali/NetHunter setup guides, hardware integrations and compatibility matrix.
tags: [alfa, wifi, kali, monitor-mode, adapter, antenna]
keywords: [ALFA Network, AWUS036ACM, AWUS036AXML, Wi-Fi adapter, monitor mode, Kali Linux]
slug: /alfa-network/
---

# ALFA Network

> **Quick Summary**: ALFA Network makes the external Wi-Fi adapters and antennas that penetration testers, drone pilots and robotics labs reach for — because they combine **high-gain radios**, **external antenna connectors**, and (the part students love most) **serious Linux support**.

If you have ever watched a Kali Linux tutorial where someone plugs a black stick into a USB port, flips the interface into monitor mode and starts sniffing packets, the stick was almost certainly an ALFA. The brand has been the default choice in the security community for over a decade — from the legendary **AWUS036ACH** to the brand-new **Wi-Fi 6E AWUS036AXML**.

This wiki is your step-by-step companion: every adapter and antenna we sell, every chipset driver, every "why doesn't my adapter show up" answer, and hardware integration guides for Jetson, Raspberry Pi and Unitree robots.

```mermaid
flowchart TD
    A["You want Wi-Fi gear for Linux / security / robotics"] --> B{"What do you actually need?"}
    B -->|"Pen-testing, packet sniffing, monitor mode"| C["AC-class adapter with external antenna<br/>(AWUS036EACS / AWUS036ACH / AWUS036ACS)"]
    B -->|"Fast everyday client, Wi-Fi 6E"| D["AWUS036AXML / AWUS036AXM / AWUS036AX"]
    B -->|"Streaming / robotics on Jetson or Pi"| E["Hardware integration guides"]
    B -->|"Extend range of an existing adapter"| F["External antennas<br/>(APA / ARS series)"]
    C --> G["Linux setup guides"]
    D --> G
    E --> G
    F --> G
    G --> H["Plug in, install, verify — done!"]
```

## What's inside this section

| Page | What you get |
|---|---|
| [Wi-Fi adapter comparison](/alfa-network/wifi-adapter-comparison/) | Every USB adapter side by side: chipset, speed class, bands, monitor-mode support — plus "which one for you" by use case |
| [Linux compatibility matrix](/alfa-network/linux-compatibility-matrix/) | Which kernel version each adapter needs, and what we tested on Ubuntu 24.04 (Kali and NetHunter/Android: not tested on real hardware) |
| [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/) | Step-by-step: in-kernel drivers (plug & play on kernel 6.17) and DKMS builds only for older kernels |
| [Kali Linux setup guide](/alfa-network/linux-setup-kali/) | monitor mode, packet injection — the full pen-test workflow (Kali itself not tested on real hardware) |
| [NetHunter (Android) setup guide](/alfa-network/linux-setup-nethunter/) | Turn an Android phone + OTG into a mobile auditing rig |
| [Troubleshooting index](/alfa-network/troubleshooting/) | Symptom → diagnosis → root cause → fix for every common ALFA problem |
| [Drivers](/alfa-network/drivers/mt7612u/) | Chipset-focused guides: MT7612U, MT7610U, MT7921AUN, RTL8812AU, RTL8811AU, RTL8832BU, RTL8821CU |
| [Hardware integrations](/alfa-network/hardware/jetson/) | NVIDIA Jetson, Raspberry Pi, Unitree robots |
| [Products](/alfa-network/products/awus036acm/) | Full spec sheets and per-product guides for every adapter and antenna |

## How to choose an adapter (5-minute crash course)

Choosing an adapter is really choosing a **chipset**, because the chipset decides:

1. **Which driver you need** — and whether it is in the Linux kernel (plug & play) or, on an older kernel, requires a DKMS build.
2. **Whether monitor mode + packet injection work** — the core requirement for Kali / Wireshark / Aircrack-ng work.
3. **How fast and how far** the adapter is.

Here is the simplified map — details in the [comparison page](/alfa-network/wifi-adapter-comparison/):

| Chipset | Adapters | In-kernel driver? | Monitor mode? | Best for |
|---|---|---|---|---|
| **MT7612U** | AWUS036ACM | ✅ `mt76x2u` (mainline since kernel 4.19) | ✅ monitor + injection (63–83 % on 2.4 GHz, 76 % on 5 GHz) | Mesh / IBSS experiments, general monitor mode |
| **MT7610U** | AWUS036ACHM | ✅ `mt76x0u` (mainline since kernel 4.19) | ✅ monitor; injection 96–100 % on 2.4 GHz, 5 GHz broadcast only | Single-antenna budget adapter, mesh / IBSS experiments |
| **MT7921AUN** | AWUS036AXM / AWUS036AXML | ✅ `mt7921u` (mainline since kernel 5.18) | 🟡 weak monitor; ❌ injection fails on stock kernel 6.17 | Wi-Fi 6 client / AP hotspot with BT; AXML 6 GHz verified (AXM 6 GHz not tested); not for injection |
| **RTL8812AU** | AWUS036ACH | ✅ `rtw88_8812au` (mainline since kernel 6.13) | ✅ monitor + injection 100 % on both bands | Injection + handshake capture, long-range monitor |
| **RTL8811AU** | AWUS036ACS | ✅ `rtw88_8821au` (mainline since kernel 6.13) | ✅ monitor + injection (100 % on 2.4 GHz, 96 % on 5 GHz) | Tiny pocket adapter for injection + handshake capture |
| **RTL8832BU** | AWUS036AX / AWUS036AXER | ✅ `rtw89_8852bu` (mainline since kernel 6.17) | ✅ strong monitor; injection 96 % (AX) / 73 % (AXER) on 2.4 GHz | Wi-Fi 6 + AP hotspot; AXER for the strongest RX |
| **RTL8821CU** | AWUS036EACS | ✅ `rtw88_8821cu` (mainline since kernel 6.2) | ✅ monitor + injection 100 % on both bands | Wi-Fi + Bluetooth combo, 100% injection both bands |

All seven chipsets use in-kernel drivers on our test platform (ASUS GX10, Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) — no DKMS.

> **You might be wondering** — *"What is DKMS?"* It is a system that rebuilds a third-party driver automatically every time your Linux kernel updates. You only need it when your kernel is older than the version in the table above (for example, the RTL8812AU driver is in the kernel from 6.13); on an older kernel DKMS keeps a community driver alive across updates. We explain it step by step in the [Ubuntu guide](/alfa-network/linux-setup-ubuntu/).

## Getting started

If this is your first ALFA adapter, the recommended path is:

1. Read the [comparison](/alfa-network/wifi-adapter-comparison/) and pick your adapter.
2. Check your OS in the [compatibility matrix](/alfa-network/linux-compatibility-matrix/).
3. Follow the [Ubuntu](/alfa-network/linux-setup-ubuntu/) or [Kali](/alfa-network/linux-setup-kali/) guide.
4. Something odd? Head to the [troubleshooting index](/alfa-network/troubleshooting/).

Happy sniffing — and remember: only ever test on networks you own or have written permission to test.
