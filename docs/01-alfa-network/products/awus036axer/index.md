---
id: alfa-product-awus036axer
title: ALFA AWUS036AXER — Wi-Fi 6 Nano (Internal Antenna)
sidebar_position: 11
description: ALFA AWUS036AXER — the 10.5 g Wi-Fi 6 nano adapter with internal antenna, RTL8832BU AX1800, WPA3 and USB 3.2. Minimal-bulk everyday AX.
tags: [alfa, adapter, rtl8832bu, wifi-6, nano, internal-antenna]
keywords: [AWUS036AXER, RTL8832BU nano, 10.5g adapter, internal antenna Wi-Fi 6]
---

# ALFA AWUS036AXER — Wi-Fi 6 Nano (Internal Antenna)

> **一句話定位（One-liner）**: The **AWUS036AXER** is ALFA's **10.5 g nano** — the same **RTL8832BU AX1800** Wi-Fi 6 engine as the big AWUS036AX, but with an **internal antenna** and USB 3.2, so it sits flush in the port and disappears. Wi-Fi 6 + WPA3 for the everyday-carry crowd.

## 規格總覽 (Spec overview)

| Item | Spec |
|---|---|
| Chipset | Realtek RTL8832BU |
| Wi-Fi class | AX1800 (574 + 1201 Mbps) |
| Interface | USB 3.2 |
| Bands | 2.4 + 5 GHz |
| Antenna | **Internal** (no external RP-SMA) |
| Weight | 10.5 g |
| Security | WPA3 |
| MIMO | 2×2 |
| Linux driver | `rtl88x2bu` (DKMS) |
| Monitor mode | ✅ (internal antenna — see note) |

## Overview

The AXER takes the AWUS036AX's radio and strips away the bulk. Instead of two external antennas, it uses an **integrated antenna** folded into a **10.5 g body** — the result plugs into a laptop port and barely protrudes. You keep Wi-Fi 6 speeds, WPA3 and 2×2 MIMO; you trade the external-antenna range and the antenna-upgrade path.

This is a **client-first adapter**: it is for the student in a lecture hall who wants fast, secure Wi-Fi 6 without carrying a dongle-and-antennas everywhere. It is *not* the pick for long-range monitoring — see the note in Advanced usage.

## Install & drivers

Identical driver story to the [AWUS036AX](/alfa-network/products/awus036ax/) — full steps on the [RTL8832BU driver page](/alfa-network/drivers/rtl8832bu/):

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu && sudo make dkms_install
sudo modprobe 88x2bu
```

**Expected output**: `DKMS: install completed.` then an interface in `iw dev`.

```mermaid
flowchart LR
    A["AWUS036AXER (10.5 g)"] --> B["DKMS build rtl88x2bu"]
    B --> C["modprobe 88x2bu"]
    C --> D["Connect — fast and flush"]
```

## Advanced usage

### Client-mode excellence

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**Expected output**: connected; up to **1201 Mb/s** link rate on 5 GHz near the AP.

### Monitor mode — with a caveat

The internal antenna means range and sensitivity are limited. Monitor mode *works* (the driver supports it), but for serious capture work the external-antenna [AWUS036AX](/alfa-network/products/awus036ax/) or [AWUS036ACM](/alfa-network/products/awus036acm/) is the better instrument. NetHunter compatibility is also marginal with this one.

## Compatibility

| Platform | Support | Notes |
|---|---|---|
| Kali Linux | ✅ | DKMS, but internal antenna limits range |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek, internal antenna, low priority |
| Windows | ✅ | Official driver, WPA3 |
| Raspberry Pi / Jetson | ✅ | DKMS on ARM64 |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Short range vs external-antenna ALFAs | Internal antenna by design | Expected — use for client work, not long links |
| WPA3 network not visible | Stale driver | Update `rtl88x2bu` + OS |
| DKMS build fails | New kernel | `git pull && make dkms_install` |
| Slow on USB 2.0 port | Bandwidth cap | Use a USB 3.x port |

## Related resources

- [RTL8832BU driver page](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AX](/alfa-network/products/awus036ax/) — same engine, external antennas, more range
- [AWUS036AXM](/alfa-network/products/awus036axm/) — faster + Bluetooth
- [Adapter comparison](/alfa-network/wifi-adapter-comparison/)
