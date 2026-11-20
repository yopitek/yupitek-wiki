---
id: alfa-driver-mt7610u
title: MT7610U Driver Guide (AWUS036ACHM)
sidebar_position: 2
description: MT7610U chipset deep-dive — the in-kernel mt76x0u driver used by the AWUS036ACHM, with monitor mode, verify steps and troubleshooting.
tags: [alfa, drivers, mt7610u, monitor-mode, kernel]
keywords: [MT7610U driver, AWUS036ACHM, mt76x0u, monitor mode Linux]
---

# MT7610U Driver Guide (AWUS036ACHM)

> **Quick Summary**: The **MediaTek MT7610U** is the 1T1R (one stream) dual-band chipset inside the **AWUS036ACHM** — a budget-friendly AC600 (150 + 433 Mbps) adapter whose `mt76x0u` driver is **in the Linux kernel since 4.19**. Like its big brother the MT7612U, it is plug-and-play on any modern Linux.

> **Tested platform**: ASUS Ascent GX10 (NVIDIA GB10), Ubuntu 24.04 LTS ARM64, kernel `6.17.0-1014-nvidia` (2026-11-16 to 2026-11-19). The in-kernel `mt76x0u` driver bound automatically (USB ID `0e8d:7610`, firmware `mt7610u.bin`); no DKMS was needed. Monitor works on 2.4/5 GHz, injection on 2.4 GHz reached 96–100 % (5 GHz: broadcast only), AP and WPA3-SAE work. For an AP use pure 802.11g (2.4 GHz) / pure 802.11a (5 GHz), and for WPA3 set `sae_pwe=0` (with `sae_pwe=2` an iPhone 7 Plus could not connect).

## Concept: the "little brother" chipset

Where the MT7612U is a 2×2 radio, the MT7610U is a **1×1** — one spatial stream, so 433 Mbps max on 5 GHz instead of 867. That is exactly the AC600 (150 + 433 Mbps) spec of the AWUS036ACHM. What you lose in speed you gain in simplicity and price: it is the cheapest ALFA adapter that still gives you **in-kernel driver + dual-band + working monitor mode**.

The driver lives in the same mainline `mt76` family (`drivers/net/wireless/mediatek/mt76/mt76x0/`), so the experience is identical to the MT7612U:

- Plug in → interface appears. No installation.
- No DKMS → nothing to maintain across kernel updates.
- Monitor mode + injection via standard `mac80211` tooling.

```mermaid
flowchart LR
    A["AWUS036ACHM plugged in"] --> B["USB core sees 0e8d:7610"]
    B --> C["mt76x0u driver binds (in-kernel)"]
    C --> D["wlan0 appears"]
    D --> E["Managed mode: connect to AP"]
    E --> F["airmon-ng start wlan0 → wlan0mon"]
```

## Prerequisites

- [ ] Linux with kernel **4.19 or newer**
- [ ] `sudo` access
- [ ] AWUS036ACHM (or any MT7610U dongle)

## Step 1: Verify the driver

```bash
lsusb | grep 0e8d:7610
sudo dmesg | grep mt76x0u | tail -3
```

**Expected output** (measured on the GX10; bus/device numbers and the `wlx` MAC differ on your machine):

```text
Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi
mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

If `lsusb` sees the device but there is no `mt76x0u` line: `sudo modprobe mt76x0u`.

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

## Step 3: Connect

```bash
nmcli device wifi connect "MySSID" password "my-passphrase"
```

**Expected output**: `Device 'wlan0' successfully activated with 'MySSID'.`

> Expect roughly **half the throughput** of an AWUS036ACM at the same distance — that is the 1×1 radio. For class exercises, note-taking, and light captures it is completely fine.

## Step 4: Monitor mode

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
iw dev
```

> On a GX10 or any desktop where NetworkManager provides your network, **do not run `airmon-ng check kill`**; use `iw` on the adapter's `wlx...` interface only.

**Expected output**: `type monitor`. Or use Aircrack-ng's helper:

```bash
sudo airmon-ng start wlan0
```

Injection check:

```bash
sudo aireplay-ng --test wlan0mon
```

**Expected output**: `Injection is working!` (measured on the GX10: 96–100 % on 2.4 GHz; 5 GHz per-client response rate was not measured, broadcast injection works)

## Step 5: Back to normal

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Not in `lsusb` | Power / cable | Different port, powered hub — [troubleshooting index](/alfa-network/troubleshooting/) |
| No interface | Driver not loaded | `sudo modprobe mt76x0u`; check `dmesg \| grep mt76` |
| Throughput caps at ~150 Mbps on 5 GHz | That is the 1×1 hardware limit | Not a bug — the 5 GHz link rate is at most 433 Mbps; ~150–250 Mbps real-world |
| Monitor mode refused | Kernel < 4.19 | Upgrade kernel / OS |
| Injection test fails | Dead channel / RF zone | `sudo iw wlan0mon set channel 6`, test near an AP |

## References

- [AWUS036ACHM product page](/alfa-network/products/awus036achm/)
- [Ubuntu setup guide](/alfa-network/linux-setup-ubuntu/) and [Kali setup guide](/alfa-network/linux-setup-kali/)
- [Compatibility matrix](/alfa-network/linux-compatibility-matrix/)
- Mainline driver source: `drivers/net/wireless/mediatek/mt76/mt76x0/` in the Linux kernel tree
