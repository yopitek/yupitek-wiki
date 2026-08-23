---
id: alfa-product-awus036acs
title: ALFA AWUS036ACS — Pocket-Size Dual-Band AC433
sidebar_position: 9
description: ALFA AWUS036ACS — tiny 55 mm RTL8811AU AC433 dual-band adapter with two 5 dBi antennas and DKMS-driven monitor mode. The pocket Kali companion.
tags: [alfa, adapter, rtl8811au, ac433, portable]
keywords: [AWUS036ACS, RTL8811AU, pocket adapter, portable Kali adapter]
---

# ALFA AWUS036ACS — Pocket-Size Dual-Band AC433

> **Quick Summary**: The **AWUS036ACS** is the 55 mm pocket ALFA — an **RTL8811AU AC433** dual-band adapter with two fold-out 5 dBi antennas and DKMS-driven monitor mode. It is the adapter you carry because "you never know when you will want to look at some Wi-Fi."

## Specifications Overview (Spec overview)

| Item | Spec |
|---|---|
| Chipset | Realtek RTL8811AU |
| Wi-Fi class | AC433 (150 + 433 Mbps) |
| Interface | USB 2.0 |
| Bands | 2.4 + 5 GHz |
| Antenna | 2 × external 5 dBi, RP-SMA |
| Body | ~55 mm — pocket sized |
| Linux driver | `rtl8811au` (DKMS, not in-kernel) |
| Monitor mode | ✅ good |
| Packet injection | ✅ good |

## Overview

The ACS is what happens when you shrink the classic ALFA formula without losing the essentials. It keeps dual-band, external antennas and working monitor mode, but wraps them in a **55 mm body** that vanishes in a laptop bag. Its 1×1 RTL8811AU radio is AC433-class — enough for management-frame capture, injection demos and light analysis, and honest about its throughput limits.

The trade-off mirrors the other Realtek ALFAs: the driver is **not in the kernel**, so there is a one-time DKMS build (which handles kernel updates for you afterward). If you would rather have zero driver work, spend a little more on the in-kernel [AWUS036ACM](/alfa-network/products/awus036acm/).

## Install & drivers

Full details on the [RTL8811AU driver page](/alfa-network/drivers/rtl8811au/). The short version:

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl8811au.git
cd rtl8811au && sudo make dkms_install
sudo modprobe 8811au
```

**Expected output**: `DKMS: install completed.` then an interface in `iw dev`.

```mermaid
flowchart LR
    A["AWUS036ACS in backpack"] --> B["DKMS driver build (once)"]
    B --> C["modprobe 8811au"]
    C --> D["airmon-ng start wlan0"]
    D --> E["wlan0mon — ready anywhere"]
```

## Advanced usage

### Monitor mode on the road

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**Expected output**: `wlan0mon` + `30/30: 100%`.

### Travel rig

Pair the fold-out antennas (they stay attached in transit) with a [Jetson](/alfa-network/hardware/jetson/) or laptop for a portable capture/analysis station. Fold the antennas, drop it in the pocket, done.

## Compatibility

| Platform | Support | Notes |
|---|---|---|
| Kali Linux | ✅ | DKMS; aircrack-ng repo |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | 🔧 | Realtek, so not guaranteed |
| Windows | ✅ | Official driver |
| Raspberry Pi / Jetson | ✅ | DKMS build on ARM64 |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| DKMS build fails | Missing headers / new kernel | `sudo apt install linux-headers-$(uname -r)`; `git pull && make dkms_install` |
| Managed-mode only | Kernel stub conflict | Blacklist `rtl8811au` (see [driver page](/alfa-network/drivers/rtl8811au/)) |
| Injection 0/30 | Empty channel | `sudo iw wlan0mon set channel 6` |
| Throughput low | 1×1 AC433 hardware | Not a bug |
| Not detected after reboot | Module not auto-loaded | Add `8811au` to `/etc/modules-load.d/alfa.conf` |

## Related resources

- [RTL8811AU driver page](/alfa-network/drivers/rtl8811au/)
- [Kali setup guide](/alfa-network/linux-setup-kali/)
- [AWUS036ACH](/alfa-network/products/awus036ach/) — the full-size high-power sibling
- [AWUS036ACM](/alfa-network/products/awus036acm/) — in-kernel alternative
- [Adapter comparison](/alfa-network/wifi-adapter-comparison/)
