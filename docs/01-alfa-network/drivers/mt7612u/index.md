---
id: alfa-driver-mt7612u
title: MT7612U Driver Guide (AWUS036ACM)
sidebar_position: 1
description: MT7612U chipset deep-dive — the in-kernel mt76x2u driver used by the AWUS036ACM, with monitor mode, verify steps and troubleshooting.
tags: [alfa, drivers, mt7612u, monitor-mode, kernel]
keywords: [MT7612U driver, AWUS036ACM, mt76x2u, monitor mode Linux]
---

# MT7612U Driver Guide (AWUS036ACM)

> **Quick Summary**: The **MediaTek MT7612U** is the chipset inside the **AWUS036ACM** — and its `mt76x2u` driver has been **built into the Linux kernel since version 4.19**. That single fact makes the ACM the lowest-friction ALFA adapter on Linux: no installation, no DKMS, no maintenance.

> **Tested platform**: ASUS Ascent GX10 (NVIDIA GB10), Ubuntu 24.04 LTS ARM64, kernel `6.17.0-1014-nvidia` (2026-11-16 to 2026-11-19). The in-kernel `mt76x2u` driver bound automatically (USB ID `0e8d:7612`, firmware `mt7662.bin` + `mt7662_rom_patch.bin`); no DKMS and no installation were needed. Monitor and injection passed on 2.4 GHz (63–83 %) and 5 GHz (76 %), AP 2.4/5 GHz and WPA3-SAE passed.
> **Known quirk**: if the adapter was connected to Wi-Fi first, a later switch to monitor mode only received the last-used channel; unplug and replug before switching to monitor.

## Concept: what "in-kernel" means for MT7612U

The MT7612U is a **2T2R** (2 transmit / 2 receive) dual-band 802.11ac radio — the "300 + 867 Mbps" in the AC1200 spec. Because MediaTek upstreamed the driver into the mainline kernel (`drivers/net/wireless/mediatek/mt76/`), every Linux distribution ships it pre-compiled.

The practical consequences are huge for a student:

- **Ubuntu / Kali / Debian / Fedora**: plug in → `wlan0` exists. Zero commands needed.
- **No DKMS**: nothing to rebuild when the kernel updates. The adapter cannot "break after an upgrade" the way Realtek DKMS modules can.
- **Monitor mode + packet injection** work through the standard `mac80211` interface — no special tools required.

```mermaid
flowchart LR
    A["AWUS036ACM plugged in"] --> B["USB core sees 0e8d:7612"]
    B --> C["mt76x2u driver binds (in-kernel)"]
    C --> D["wlan0 appears"]
    D --> E["iw dev shows type managed"]
    E --> F["airmon-ng start wlan0 → wlan0mon"]
```

## Prerequisites

- [ ] Linux with kernel **4.19 or newer** (`uname -r` — Ubuntu 20.04+ / any recent Kali is fine)
- [ ] `sudo` access
- [ ] AWUS036ACM (or any MT7612U dongle)

## Step 1: Verify the driver is loaded

Plug in the adapter and check:

```bash
lsusb | grep 0e8d:7612
sudo dmesg | grep -E 'mt76x2u|usb .*: (Product|Manufacturer)' | tail -8
```

**Expected output** (measured on the GX10; the bus/device numbers and the `wlx` MAC differ on your machine):

```text
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
usb 3-1: Product: Wireless
usb 3-1: Manufacturer: MediaTek Inc.
mt76x2u 3-1:1.0: ASIC revision: 76120044
mt76x2u 3-1:1.0: ROM patch build: 20141115060606a
mt76x2u 3-1:1.0: Firmware Version: 0.0.00
mt76x2u 3-1:1.0: Build: 1
mt76x2u 3-1:1.0: Build Time: 201507311614____
mt76x2u 3-1:1.0 wlx00c0cabf874c: renamed from wlan0
```

The `mt76x2u` lines mean the driver claimed your adapter. (If `lsusb` sees the device but there is no `mt76x2u` line, run `sudo modprobe mt76x2u`.)

## Step 2: Confirm the interface

```bash
iw dev
```

**Expected output** (example; on the GX10 the interface is named `wlx` + MAC):

```text
phy#0
	Interface wlan0
		ifindex 3
		addr 00:c0:ca:xx:xx:xx
		type managed
```

> **You might be wondering** — *"Why is my MAC 00:c0:ca:...?"* Because `00:c0:ca` is the **ALFA MAC OUI** — every ALFA adapter starts with those three bytes. Handy when identifying adapters in a lab full of dongles.

## Step 3: Connect (managed mode)

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**Expected output**: `Device 'wlan0' successfully activated with 'MySSID'.`

## Step 4: Monitor mode (the fun part)

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
iw dev
```

> On a GX10 or any desktop where NetworkManager provides your network, **do not run `airmon-ng check kill`** (it stops NetworkManager). Use `iw` as shown, and operate only on the adapter's `wlx...` interface.

**Expected output**: the interface line now reads `type monitor`. Alternatively use the Aircrack-ng helper:

```bash
sudo airmon-ng start wlan0
```

**Expected output** (example only — `airmon-ng` was deliberately not used in our GX10 test, we used `iw`):

```text
PHY	Interface	Driver		Chipset
phy0	wlan0		mt76x2u		MediaTek Inc. MT7612U
		(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
```

Injection self-test (broadcast — safe on any channel):

```bash
sudo aireplay-ng --test wlan0mon
```

**Expected output**: `Injection is working!` (measured on the GX10: 63–83 % on 2.4 GHz, 76 % on 5 GHz; the exact percentage depends on the channel and distance)

## Step 5: Turn it back off

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `lsusb` shows nothing | Power / cable issue | Try another port, powered hub, another cable — see the [troubleshooting index](/alfa-network/troubleshooting/) |
| `lsusb` ok, no `wlan0` | Driver not loaded (very rare) | `sudo modprobe mt76x2u`; check `dmesg \| grep mt76` |
| `airmon-ng` reports "monitor mode not supported" | Kernel older than 4.19 | Upgrade your kernel / OS |
| Monitor mode works but injection fails | Wrong channel / dead RF zone | `sudo iw wlan0mon set channel 6`; test near an AP |
| Monitor mode only receives one channel | Adapter was connected to Wi-Fi before switching to monitor | Unplug and replug, then switch to monitor |
| WLAN disappears on suspend/resume | Known USB quirk on some laptops | Unplug/replug the adapter after resume |

## References

- [AWUS036ACM product page](/alfa-network/products/awus036acm/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/) and [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Compatibility matrix](/alfa-network/linux-compatibility-matrix/)
- Mainline driver source: `drivers/net/wireless/mediatek/mt76/mt76x2/` in the Linux kernel tree
