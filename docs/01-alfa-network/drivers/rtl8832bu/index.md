---
id: alfa-driver-rtl8832bu
title: RTL8832BU Driver Guide (AWUS036AX / AWUS036AXER)
sidebar_position: 6
description: RTL8832BU chipset deep-dive — the Wi-Fi 6 chipset behind the AWUS036AX and AWUS036AXER, the community rtl8852bu DKMS driver, WPA3. Monitor mode is not supported by this driver.
tags: [alfa, drivers, rtl8832bu, wifi-6, dkms, wpa3]
keywords: [RTL8832BU driver, RTL8852BU, AWUS036AX, rtl8852bu, Wi-Fi 6 Linux, WPA3]
---

# RTL8832BU Driver Guide (AWUS036AX / AWUS036AXER)

> **Quick Summary**: The **Realtek RTL8832BU** is the Wi-Fi 6 (802.11ax) chipset inside the **AWUS036AX** and its nano sibling the **AWUS036AXER**. It is not in the kernel, so you build the community `rtl8852bu` DKMS driver once — then enjoy AX1800 speeds and **WPA3** support. **This driver does not support monitor mode** — see [Monitor mode and injection](#monitor-mode-and-injection).

## Concept: Wi-Fi 6, the Realtek way

The RTL8832BU is a 2×2 802.11ax radio (AX1800: 574 + 1201 Mbps). Compared to the older AC adapters, the big user-visible win is **WPA3** — modern routers that only speak WPA3 will refuse your old AC dongle but happily accept the AX.

The driver situation mirrors the other Realtek chipsets: **not upstreamed**, so we use a community driver. The maintained repo is **[`morrownr/rtl8852bu-20250826`](https://github.com/morrownr/rtl8852bu-20250826)** ("Linux Driver for USB WiFi Adapters that are based on the RTL8832BU and RTL8852BU Chipsets"); its README lists the AWUS036AX and AWUS036AXER as supported. Its installer registers the driver with DKMS so it is rebuilt across kernel updates.

> Earlier versions of this guide used `aircrack-ng/rtl88x2bu`. That repository no longer exists, and the 88x2bu family (RTL8812BU / RTL8822BU) is a different, 802.11ac chipset family — do not use it for the AWUS036AX / AXER.

```mermaid
flowchart LR
    A["AWUS036AX / AXER plugged in"] --> B["No in-kernel driver for RTL8832BU"]
    B --> C["Build rtl8852bu via DKMS"]
    C --> D["8852bu module loaded"]
    D --> E["Connect: WPA3-capable"]
```

## Prerequisites

- [ ] Linux (Ubuntu 20.04+ / Kali / Debian)
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` access
- [ ] AWUS036AX or AWUS036AXER

## Step 1: Build the driver

```bash
cd /opt
sudo git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo sh install-driver.sh
```

**Expected output**: the script builds and installs the driver with DKMS. Answer its prompts and reboot when it asks.

## Step 2: Load and verify

```bash
sudo modprobe 8852bu
iw dev
```

**Expected output**: an interface line, e.g. `Interface wlan0 ... type managed`. The installer normally sets up auto-load across reboots; if not:

```bash
echo 8852bu | sudo tee /etc/modules-load.d/alfa.conf
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

**Expected output**: shows `SSID: MySSID` plus the negotiated rate — on 5 GHz up to about **1201 Mb/s**, or a lower fallback depending on distance (2×2 80 MHz).

## Monitor mode and injection

The driver's README states that **monitor mode is not supported** by this driver. If you need monitor mode and packet injection, use an adapter with an in-kernel MediaTek driver (for example the [AWUS036ACM](/alfa-network/products/awus036acm/) or the [AWUS036AXML](/alfa-network/products/awus036axml/)) or the [AWUS036ACH](/alfa-network/products/awus036ach/) with its community driver. See the [adapter comparison](/alfa-network/wifi-adapter-comparison/).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Build fails on a very new kernel | Repo needs the latest commit | `cd /opt/rtl8852bu-20250826 && sudo git pull && sudo sh install-driver.sh` |
| WPA3 network not visible | Driver or wpa_supplicant too old | Update the driver; `sudo apt update && sudo apt upgrade` |
| Driver stops working after a kernel upgrade | DKMS did not rebuild | `sudo dkms status`, then re-run `sudo sh install-driver.sh` |
| Another out-of-kernel driver for the same hardware is installed | Conflicting modules | The installer detects most conflicts; check `sudo dkms status` and remove the old driver |
| High-speed link but slow transfers | USB 2.0 port bottleneck | Use a USB 3.x port (AX is USB 3.2) |

## References

- [AWUS036AX product page](/alfa-network/products/awus036ax/) and [AWUS036AXER product page](/alfa-network/products/awus036axer/)
- [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/)
- [Troubleshooting index](/alfa-network/troubleshooting/)
- Driver repo: [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
