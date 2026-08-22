---
id: alfa-driver-rtl8811au
title: RTL8811AU Driver Guide (AWUS036ACS)
sidebar_position: 5
description: RTL8811AU chipset deep-dive — the pocket-size AWUS036ACS, DKMS install of the rtl8811au driver, monitor mode and injection verification.
tags: [alfa, drivers, rtl8811au, dkms, monitor-mode]
keywords: [RTL8811AU driver, AWUS036ACS, rtl8811au, pocket adapter monitor mode]
---

# RTL8811AU Driver Guide (AWUS036ACS)

> **一句話定位（One-liner）**: The **Realtek RTL8811AU** is the 1×1 AC433 chipset inside the 55 mm **AWUS036ACS** — the pocket-sized monitor-mode companion. Like its big brother the RTL8812AU, it needs the community `rtl8811au` driver via DKMS, but the build is identical.

## Concept: same family, one stream

The RTL8811AU is essentially the 1×1 variant of the RTL8812AU family: one spatial stream, 433 Mbps max on 5 GHz, lower power draw, smaller board. ALFA wraps it in the tiny ACS body with two 5 dBi external antennas — you get the classic ALFA pen-testing behavior in a package that hides in a pencil case.

Driver-wise, nothing changes from the RTL8812AU story: **no in-kernel driver with monitor support**, so we use the community `rtl8811au` DKMS driver. Note the driver also covers the RTL8821AU variant, so do not panic if your `dkms status` shows the same module name on similar dongles.

```mermaid
flowchart LR
    A["AWUS036ACS plugged in"] --> B["No usable in-kernel driver"]
    B --> C["Build rtl8811au via DKMS"]
    C --> D["8811au module loaded"]
    D --> E["airmon-ng start wlan0"]
    E --> F["wlan0mon + injection test"]
```

## Prerequisites

- [ ] Linux (Ubuntu 20.04+ / Kali / Debian)
- [ ] `sudo apt install -y build-essential dkms git`
- [ ] `sudo` access
- [ ] AWUS036ACS

## Step 1: Clone and build

```bash
cd /opt
sudo git clone https://github.com/aircrack-ng/rtl8811au.git
cd rtl8811au
sudo make dkms_install
```

**Expected output**:

```text
DKMS: install completed.
```

## Step 2: Load and verify

```bash
sudo modprobe 8811au
iw dev
```

**Expected output**: an `Interface wlan0` (or `wlan1`) line. If the adapter only shows up after re-plug, add the module to auto-load:

```bash
echo 8811au | sudo tee /etc/modules-load.d/alfa.conf
```

## Step 3: Monitor mode + injection

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

**Expected output**:

```text
PHY	Interface	Driver		Chipset
phy0	wlan0		8811au		Realtek Semiconductor Corp. RTL8811AU
...
12:34:56  Injection is working!
12:34:56  30/30:  100%
```

## Step 4: Back to normal

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| DKMS build fails | Missing headers / too-new kernel | `sudo apt install linux-headers-$(uname -r)`; `sudo git pull && sudo make dkms_install` |
| Interface only in managed mode | Kernel stub `rtl8811au` grabbed it | `echo "blacklist rtl8811au" \| sudo tee /etc/modprobe.d/alfa-8811au.conf`; reboot |
| Injection 0/30 | Empty channel | `sudo iw wlan0mon set channel 6`; test near an AP |
| Throughput lower than expected | 1×1 radio (AC433) — hardware limit | Not a bug; expect ~150–250 Mbps real-world on 5 GHz |
| Not detected after reboot | Module not auto-loaded | Add `8811au` to `/etc/modules-load.d/alfa.conf` |

## References

- [AWUS036ACS product page](/alfa-network/products/awus036acs/)
- [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/)
- [Troubleshooting index](/alfa-network/troubleshooting/)
- Driver repo: [aircrack-ng/rtl8811au](https://github.com/aircrack-ng/rtl8811au)
