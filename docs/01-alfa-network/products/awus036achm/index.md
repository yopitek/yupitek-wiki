---
id: alfa-product-awus036achm
title: ALFA AWUS036ACHM — Budget Dual-Band AC600
sidebar_position: 7
description: ALFA AWUS036ACHM — budget MT7610U AC600 dual-band adapter with in-kernel driver (mt76x0u) and working monitor mode and injection. Tested on ASUS GX10 / Ubuntu 24.04 ARM64. Great budget Kali starter.
tags: [alfa, adapter, mt7610u, ac433, budget]
keywords: [AWUS036ACHM, MT7610U, budget adapter, AC600 Kali]
---

# ALFA AWUS036ACHM — Budget Dual-Band AC600

> **Quick Summary**: The **AWUS036ACHM** is the budget dual-band ALFA — a **MT7610U AC600** adapter with one detachable 5 dBi dual-band antenna and, crucially, an **in-kernel driver** (`mt76x0u` since Linux 4.19). Verified on ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17): monitor on 2.4/5 GHz, injection on 2.4 GHz (96–100 %), AP mode, a WPA3 AP (AP side only; WPA3 client not tested) and an end-to-end WPA handshake capture on our own network all work. Use only on your own or authorized networks.

## Specifications Overview (Spec overview)

| Item | Spec |
|---|---|
| Chipset | MediaTek MT7610U |
| Wi-Fi class | AC600 (150 + 433 Mbps) |
| Interface | USB 2.0 |
| Bands | 2.4 + 5 GHz |
| Antenna | 1 × detachable 5 dBi dual-band dipole, RP-SMA |
| Linux driver | `mt76x0u` — **in-kernel since 4.19** |
| Monitor mode | ✅ 2.4 + 5 GHz (tested on GX10) |
| Packet injection | ✅ 2.4 GHz 96–100 %; 5 GHz broadcast only (tested on GX10) |

## Tested on ASUS GX10 / Ubuntu 24.04 ARM64

**Test environment**: ASUS Ascent GX10 (NVIDIA GB10), Ubuntu 24.04 LTS ARM64, kernel `6.17.0-1014-nvidia`, tested 2026-11-16 to 2026-11-19 against an iPhone 7 Plus (WPA3 also with an iPhone 15 Pro).

| Item | Result |
|---|---|
| Chipset | MediaTek MT7610U |
| USB ID | `0e8d:7610` |
| Kernel driver | `mt76x0u` (in-kernel) |
| Firmware | `mt7610u.bin` (linux-firmware) |
| DKMS needed? | No (kernel ≥ 4.19: not needed) |

| Feature | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor | ✅ | ✅ |
| Injection | ✅ 96–100 % | ⚠️ broadcast only |
| AP | ✅ (pure 802.11g) | ✅ (pure 802.11a, 20 MHz) |
| WPA3-SAE (AP side) | ✅ (`sae_pwe=0`) | Not tested |

| Advanced feature | Result |
|---|---|
| WPA handshake capture | ✅ end-to-end on our own network (captured on 5 GHz ch36: deauth own iPhone 7 Plus, full 4-way M1–M4, converted to hashcat `.22000`) |
| VIF | ✅ |
| Active monitor | 🟡 can be configured, ACK not verified |
| IBSS (ad-hoc) | 🟡 single-device only |
| Mesh (802.11s) | 🟡 single-device only |
| Wi-Fi Direct (P2P) | Not tested (needs a second device) |

Verify on your own machine:

```bash
lsusb | grep 0e8d:7610
sudo dmesg | grep mt76x0u | tail -3
iw phy $(cat /sys/class/net/$(ls /sys/class/net | grep '^wlx' | head -1)/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
iw dev
```

Full test report: [AWUS036ACHM on ASUS GX10 / Ubuntu](https://yupitek.com/en/blog/awus036achm-asus-gx10-ubuntu-test-report/).

**Notes**:
- Single-antenna 1×1 card (AC600 class). We did not benchmark it against the ACM; the STA+AP VIF test downloaded at 198 Mbit/s over a 5 GHz link.
- To start an AP, disable 802.11n: pure `hw_mode=g` on 2.4 GHz and pure `hw_mode=a` on 5 GHz. With `ieee80211n=1` the iPhone fails to associate and shows "wrong password".
- WPA3 requires `sae_pwe=0`; with `sae_pwe=2` the iPhone 7 Plus could not connect.
- 5 GHz per-client injection response rate was not measured (broadcast injection works).
- 6 GHz: not applicable. Kali and NetHunter: not tested on real hardware.

## Overview

The ACHM is the "little brother" of the [AWUS036ACM](/alfa-network/products/awus036acm/). It uses the **1×1 MT7610U** radio, so its AC600 speed ceiling is about half the ACM's AC1200 — but for the two things university students actually need it for, it competes hard:

1. **It is in the kernel.** No DKMS, no compilation, no "broke after an upgrade." Plug it in on Ubuntu or Kali and the interface exists.
2. **Monitor mode + injection work** through the standard `mac80211` path, thanks to the MediaTek mainline driver.

If your coursework is "capture and analyze Wi-Fi management frames" or "demonstrate packet injection," the ACHM does it at the lowest price in the ALFA line. Buy the [ACM](/alfa-network/products/awus036acm/) instead if you want a 2×2 radio and a measured per-AP 5 GHz injection rate (76 % on the ACM; not measured on the ACHM).

## Install & drivers

Because the driver is in the kernel, **there is nothing to install** — see the [MT7610U driver page](/alfa-network/drivers/mt7610u/). Verify with:

```bash
lsusb | grep -i mediatek
iw dev
```

**Expected output**:

```text
Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi
phy#0
	Interface wlx00c0cababcd2
		ifindex 3
		type managed
```

```mermaid
flowchart LR
    A["AWUS036ACHM"] --> B["In-kernel driver (nothing to do)"]
    B --> C["iw dev shows the interface"]
    C --> D["iw set type monitor"]
    D --> E["monitor + 2.4 GHz injection"]
```

## Advanced usage

### Monitor mode (no install needed)

Do not run `airmon-ng check kill` on a desktop/GX10 (it stops NetworkManager); use `iw`:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
```

**Expected output**: `Injection is working!` (measured 96–100 % on 2.4 GHz).

### Antenna upgrade

The RP-SMA ports accept [ALFA antennas](/alfa-network/products/apa-m25/) if you outgrow the stock dipoles — with the caveat that a 1×1 radio cannot use two antennas for MIMO, so run a single high-gain antenna for range.

## Compatibility

| Platform | Support | Notes |
|---|---|---|
| Ubuntu 24.04 ARM64 (GX10, kernel 6.17) | ✅ Tested | In-kernel `mt76x0u` |
| Kali Linux | ✅ In-kernel (not tested on real hardware by us) | |
| Ubuntu (other versions) | ✅ | In-kernel since 4.19 |
| NetHunter / Android | ✅ In-kernel (not tested on real hardware by us) | |
| Windows | Not tested by us | Official driver from ALFA |
| Raspberry Pi / Jetson | Not tested by us | In-kernel driver; only the GX10 was tested |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Not in `lsusb` | Power / cable | Different port / powered hub — [troubleshooting](/alfa-network/troubleshooting/) |
| No interface | Driver not loaded (rare) | `sudo modprobe mt76x0u` |
| Lower throughput than 2×2 cards | 1×1 hardware (AC600 class) | Not a bug; we did not benchmark throughput |
| Injection fails | Empty channel | `sudo iw $IF set channel 6` |
| iPhone cannot join your AP ("wrong password") | 802.11n enabled | Use pure `hw_mode=g` / `hw_mode=a` |
| iPhone 7 Plus cannot join WPA3 AP | `sae_pwe=2` | Set `sae_pwe=0` |

## Related resources

- [MT7610U driver page](/alfa-network/drivers/mt7610u/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/) and [Kali setup guide](/alfa-network/linux-setup-kali/)
- [AWUS036ACM](/alfa-network/products/awus036acm/) — the faster sibling
- [Adapter comparison](/alfa-network/wifi-adapter-comparison/)
