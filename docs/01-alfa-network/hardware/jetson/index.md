---
id: alfa-hardware-jetson
title: ALFA Adapters on NVIDIA Jetson (Orin Nano / NX)
sidebar_label: NVIDIA Jetson
sidebar_position: 1
description: Complete guide to using ALFA Wi-Fi adapters on NVIDIA Jetson Orin Nano and Orin NX — 6 GHz Wi-Fi 6E video streaming for robotics, monitor mode, and JetPack L4T kernel configuration.
tags: [alfa, jetson, nvidia, robotics, wifi-6e, monitor-mode]
keywords: [Jetson Orin ALFA, Jetson Wi-Fi 6E, AWUS036AXML Jetson, robotics wireless, JetPack L4T driver]
---

# ALFA Adapters on NVIDIA Jetson (Orin Nano / NX)

> **Quick Summary**: NVIDIA Jetson Orin Nano and NX developer kits are designed as vision and AI compute modules, meaning their default wireless capability is often basic 2.4/5 GHz with internal PCB antennas. Adding an external ALFA Wi-Fi adapter unlocks **6 GHz (Wi-Fi 6E) low-latency camera streaming for robotics**, high-gain external antenna range, and wireless packet auditing on JetPack.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **NVIDIA Jetson has not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. Only test networks you own or are authorized to test.

## Is This Guide for You?

- **Difficulty**: Intermediate (familiarity with terminal commands and Linux kernel concepts).
- **Estimated Time**: 15–25 minutes.
- **Skills Used**: Linux command line, package installation, DKMS module management.
- **What You Will Achieve**:
  1. Determine whether your JetPack version supports in-kernel plug-and-play or requires DKMS drivers.
  2. Configure the **AWUS036AXML** for clean 6 GHz Wi-Fi 6E video streaming and telemetry.
  3. Verify physical RF link throughput and enable monitor mode.

---

## Architectural Concepts: Why Jetson Needs an External Wi-Fi Adapter

Jetson Orin carrier boards typically include modest integrated Wi-Fi radios sufficient only for routine package downloads. High-performance robotics, autonomous navigation (ROS 2), and real-time computer vision require substantially more:

1. **6 GHz Wi-Fi 6E (Empty Spectrum)**: Standard carrier radios operate on congested 2.4 GHz and 5 GHz bands. The 6 GHz spectrum provides wide 80/160 MHz channels with near-zero lab interference—ideal for streaming 4K RTSP camera feeds and 3D LiDAR point clouds.
2. **High-Gain External Antennas**: High-gain ALFA antennas (such as the ARS-NT5B7 omni antenna or the APA-M25 panel antenna) paired with your adapter penetrate obstacles and maintain line-of-sight telemetry over 100+ meters.
3. **Dedicated Monitor Mode**: Enables passive wireless sniffing and spectrum analysis directly on robot development platforms.

### JetPack & L4T Kernel Compatibility Matrix

Jetson runs NVIDIA Linux for Tegra (L4T) kernels rather than generic Ubuntu desktop kernels. Compatibility depends on your installed JetPack release:

| JetPack Version | L4T Kernel Version | MediaTek MT7921AUN (AWUS036AXML), `mt7921u` since 5.18 | MediaTek MT7612U (AWUS036ACM), `mt76x2u` since 4.19 | Realtek RTL8812AU (AWUS036ACH), `rtw88_8812au` since 6.13 |
|---|---|---|---|---|
| **JetPack 6.x** | Linux 5.15 (check `uname -r`) | In-kernel only if the kernel is 5.18 or newer; on 5.15 it needs a backport / DKMS | ✅ In-kernel | In-kernel only if the kernel is 6.13 or newer; otherwise DKMS |
| **JetPack 5.x** | Linux 5.10 | ⚠️ Kernel older than 5.18: needs a backport / out-of-tree driver | ✅ In-kernel | ⚠️ DKMS required (kernel older than 6.13) |
| **JetPack 4.x** | Linux 4.9 | ❌ Kernel older than 5.18: out-of-tree driver only | ⚠️ Kernel older than 4.19: manual driver compile | ⚠️ DKMS required (kernel older than 6.13) |

This matrix is **inferred from kernel versions, not tested on Jetson**. Other Realtek models reached mainline in EACS 6.2 and AX / AXER 6.17; below those versions they need DKMS or a newer kernel. Where the platform kernel is not listed, the answer depends on the platform kernel version.

---

## Prerequisites & Checklist

- [ ] NVIDIA Jetson Orin Nano / Orin NX / AGX Orin running JetPack 5.x or 6.x.
- [ ] ALFA USB adapter: **AWUS036AXML** (Top Pick for Wi-Fi 6E) or **AWUS036ACM** (Best Value for 5 GHz).
- [ ] 5V/3A+ dedicated power supply for the Jetson board to prevent USB current drops.
- [ ] Active internet connection for initial package installation.

---

## Step-by-Step Configuration

### Step 1: Connect Hardware & Check USB Detection

Plug the ALFA adapter into a blue USB 3.0 Type-A port on your Jetson carrier board. Open the terminal and verify USB detection:

```bash
lsusb
```

**Expected Output**:
- For **AWUS036AXML**: `ID 0e8d:7961 MediaTek Inc. Wireless_Device`
- For **AWUS036ACM**: `ID 0e8d:7612 MediaTek Inc. MT7612U`

### Step 2: Check Kernel Module & Firmware

```bash
# Check dmesg logs for driver initialization
dmesg | grep -E "mt7921|mt76"
```

**Expected Output (AWUS036AXML)**:
```text
mt7921u 1-1:1.0: ASIC revision: 79610000
mt7921u 1-1:1.0: firmware: mediatek/WIFI_MT7961_patch_mcu_1_2_tv.bin loaded
mt7921u 1-1:1.0: firmware: mediatek/WIFI_RAM_CODE_MT7961_1_2.bin loaded
```

If firmware is missing on JetPack 5.x, install the latest linux-firmware package:
```bash
sudo apt update && sudo apt install -y linux-firmware
```

### Step 3: Verify Wireless Interface & 6 GHz Capabilities

```bash
# Check network interface
iw dev

# Inspect 6 GHz frequency band support
iw phy | grep -A 10 "Band 4"
```

**Expected Output**: `Band 4` lists available 6 GHz HE channels (Channels 1–233).

### Step 4: Configure Wi-Fi Connection or Monitor Mode

Connect to a Wi-Fi 6E network via NetworkManager:
```bash
nmcli device wifi connect "Your_6GHz_SSID" password "YourPassword"
```

Or enable monitor mode for wireless research (on the GX10 test platform the AWUS036AXML showed weak monitor mode and failed packet injection; use the AWUS036ACM when you need injection):
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

---

## Troubleshooting & FAQ

### Q1: Adapter lights don't turn on or Jetson reboots when transmitting?
- **Root Cause**: Jetson USB power brownout. Jetson dev kits throttle USB ports if system power supply is below 15W.
- **Solution**: Use a dedicated 19V DC barrel jack supply or 5V/4A USB-C PD power adapter.

### Q2: `lsusb` shows device, but `iw dev` shows no interface on JetPack 5.x?
- **Root Cause**: On kernels older than 5.18 (for example JetPack 5.x on 5.10) the `mt7921u` driver is not in the kernel at all, so the interface cannot appear. If the kernel is 5.18 or newer, the cause is usually missing MediaTek firmware binaries in `/lib/firmware/mediatek/`.
- **Solution**: Use a kernel with `mt7921u` (or an out-of-tree backport); if the driver is present, download the firmware files from the kernel git repository:
  ```bash
  sudo wget -P /lib/firmware/mediatek https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mediatek/WIFI_MT7961_patch_mcu_1_2_tv.bin
  sudo wget -P /lib/firmware/mediatek https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mediatek/WIFI_RAM_CODE_MT7961_1_2.bin
  sudo reboot
  ```
