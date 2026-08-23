---
id: alfa-driver-rtl8832bu
title: RTL8832BU Driver Guide (AWUS036AX / AWUS036AXER)
sidebar_position: 6
description: RTL8832BU chipset deep-dive — the Wi-Fi 6 RTL88x2BU driver behind the AWUS036AX and AWUS036AXER, DKMS install, WPA3 and monitor mode.
tags: [alfa, drivers, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU driver, AWUS036AX, rtl88x2bu, Wi-Fi 6 Linux, WPA3]
---

# RTL8832BU Driver Guide (AWUS036AX / AWUS036AXER)

> **Quick Summary**: The **Realtek RTL8832BU** is the Wi-Fi 6 (802.11ax) chipset inside the **AWUS036AX** and its nano sibling the **AWUS036AXER**. It is not in the kernel, so you build the `rtl88x2bu` DKMS driver once — then enjoy AX1800 speeds, **WPA3** support and working monitor mode.

## Concept: Wi-Fi 6, the Realtek way

The RTL8832BU is a 2×2 802.11ax radio (AX1800: 574 + 1201 Mbps). Compared to the older AC adapters, the big user-visible win is **WPA3** — modern routers that only speak WPA3 will refuse your old AC dongle but happily accept the AX.

The driver situation mirrors the other Realtek chipsets: **not upstreamed**, so we use the community driver. The go-to repo is **`aircrack-ng/rtl88x2bu`**, which covers the 88X2BU family (RTL8822BU and RTL8832BU) with monitor mode + VIF support. DKMS keeps it rebuilt across kernel updates.

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["No in-kernel driver for RTL8832BU"]
    B --> C["Build rtl88x2bu via DKMS"]
    C --> D["88x2bu module loaded"]
    D --> E["Connect: WPA3-capable"]
    E --> F["airmon-ng start wlan0 → monitor mode"]
```

## Prerequisites

- [ ] Linux (Ubuntu 20.04+ / Kali / Debian)
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` access
- [ ] AWUS036AX or AWUS036AXER

## Step 1: Build the driver

```bash
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl88x2bu.git
cd rtl88x2bu
sudo make dkms_install
```

**Expected output**:

```text
DKMS: install completed.
```

## Step 2: Load and verify

```bash
sudo modprobe 88x2bu
iw dev
```

**Expected output**: an interface line, e.g. `Interface wlan0 ... type managed`. Auto-load across reboots:

```bash
echo 88x2bu | sudo tee /etc/modules-load.d/alfa.conf
```

## Step 3: Connect (WPA3 works out of the box)

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**Expected output**: `Device 'wlan0' successfully activated with 'MySSID'.`

Verify the security suite and link speed:

```bash
iw dev wlan0 link
```

**Expected output**: shows `SSID: MySSID` plus the negotiated rate — on 5 GHz you should see **1201 Mb/s** or a lower fallback depending on distance (2×2 80 MHz).

## Step 4: Monitor mode + injection

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**Expected output**:

```text
PHY	Interface	Driver		Chipset
phy0	wlan0		88x2bu		Realtek
...
12:34:56  Injection is working!
12:34:56  30/30:  100%
```

> **You might be wondering** — *"Wi-Fi 6 and monitor mode? Do they mix?"* Yes — the community driver keeps the classic monitor/injection behavior that pentest tools need, while managed mode adds AX rates and WPA3. You do not have to choose one or the other.

## Step 5: Back to normal

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Build fails on a very new kernel | Repo needs the latest commit | `cd /opt/rtl88x2bu && sudo git pull && sudo make dkms_install` |
| WPA3 network not visible | Driver or wpa_supplicant too old | Update the driver; `sudo apt update && sudo apt upgrade` |
| Adapter only managed, no monitor | Kernel stub conflict (rare) | `dmesg` to confirm which module bound; blacklist the stub |
| Injection 0/30 | Empty channel | `sudo iw wlan0mon set channel 6`; test near an AP |
| High-speed link but slow transfers | USB 2.0 port bottleneck | Use a USB 3.x port (AX is USB 3.2) |

## References

- [AWUS036AX product page](/alfa-network/products/awus036ax/) and [AWUS036AXER product page](/alfa-network/products/awus036axer/)
- [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/)
- [Troubleshooting index](/alfa-network/troubleshooting/)
- Driver repo: [aircrack-ng/rtl88x2bu](https://github.com/aircrack-ng/rtl88x2bu)
