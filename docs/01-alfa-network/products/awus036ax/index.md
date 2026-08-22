---
id: alfa-product-awus036ax
title: ALFA AWUS036AX — Wi-Fi 6 Dual-Band AX1800
sidebar_position: 10
description: ALFA AWUS036AX — Wi-Fi 6 RTL8832BU AX1800 dual-band adapter with WPA3, 2x2 MIMO and DKMS driver. Long-range upgrade over AC-class adapters.
tags: [alfa, adapter, rtl8832bu, wifi-6, wpa3, ax1800]
keywords: [AWUS036AX, RTL8832BU, Wi-Fi 6 adapter, WPA3, AX1800]
---

# ALFA AWUS036AX — Wi-Fi 6 Dual-Band AX1800

> **一句話定位（One-liner）**: The **AWUS036AX** is ALFA's Wi-Fi 6 entry — an **RTL8832BU AX1800** dual-band adapter with **WPA3** support, **2×2 MIMO** and two external antennas. If your campus or lab routers have gone WPA3-only, this is the adapter that still gets you in.

## 規格總覽 (Spec overview)

| Item | Spec |
|---|---|
| Chipset | Realtek RTL8832BU |
| Wi-Fi class | AX1800 (574 + 1201 Mbps) |
| Interface | USB 3.2 |
| Bands | 2.4 + 5 GHz |
| Antenna | 2 × external 6 dBi, RP-SMA |
| Security | WPA3 (alongside WPA2/WPA) |
| MIMO | 2×2 |
| Linux driver | `rtl88x2bu` (DKMS, not in-kernel) |
| Monitor mode | ✅ good |

## Overview

The AWUS036AX is the bridge between ALFA's famous AC generation and the Wi-Fi 6 world. Under the hood is the modern **RTL8832BU** 2×2 ax radio (AX1800), which brings two upgrades students actually notice:

1. **WPA3 support** — campus and 6 GHz-era networks are locking down to WPA3-SAE. Old AC adapters get refused; this one negotiates the new security handshake.
2. **Wi-Fi 6 efficiency** — OFDMA and better multi-user handling mean the AX holds up better in crowded lecture-hall RF than any AC adapter.

It keeps the classic ALFA DNA — two 6 dBi external antennas, high-power front-end, and DKMS-driven monitor mode when you want it. The driver is **not in the kernel**, so there is a one-time DKMS build.

## Install & drivers

Full steps on the [RTL8832BU driver page](/alfa-network/drivers/rtl8832bu/). Short version:

```bash
cd /opt && sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu && sudo make dkms_install
sudo modprobe 88x2bu
```

**Expected output**: `DKMS: install completed.` then an interface in `iw dev`.

```mermaid
flowchart LR
    A["AWUS036AX"] --> B["DKMS build (rtl88x2bu)"]
    B --> C["modprobe 88x2bu"]
    C --> D["Connect WPA3 network"]
    D --> E["airmon-ng start wlan0 (optional)"]
```

## Advanced usage

### Connect to a WPA3-only network

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
iw dev wlan0 link
```

**Expected output**: `Connected` and a 5 GHz link rate up to **1201 Mb/s** (2×2 80 MHz) close to the AP.

### Monitor mode (when needed)

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**Expected output**: `wlan0mon` + injection `30/30: 100%`.

## Compatibility

| Platform | Support | Notes |
|---|---|---|
| Kali Linux | ✅ | DKMS |
| Ubuntu | ✅ | DKMS |
| NetHunter / Android | ⚠️ | Realtek; may not build on phone kernels |
| Windows | ✅ | Official driver, WPA3 OK |
| Raspberry Pi / Jetson | ✅ | DKMS on ARM64 |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| WPA3 network invisible | Driver/wpa_supplicant too old | Update driver + OS |
| DKMS build fails | New kernel vs repo | `cd /opt/rtl88x2bu && git pull && make dkms_install` |
| Slow transfers despite high link | USB 2.0 port | Use a USB 3.x port (adapter is USB 3.2) |
| Injection 0/30 | Empty channel | `sudo iw wlan0mon set channel 6` |

## Related resources

- [RTL8832BU driver page](/alfa-network/drivers/rtl8832bu/)
- [AWUS036AXER](/alfa-network/products/awus036axer/) — the nano Wi-Fi 6 variant
- [AWUS036AXM](/alfa-network/products/awus036axm/) — the faster AX3000 + Bluetooth model
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/) / [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Adapter comparison](/alfa-network/wifi-adapter-comparison/)
