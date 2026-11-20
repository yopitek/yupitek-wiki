---
id: alfa-hardware-orange-pi
title: Orange Pi & Rockchip RK3588 SBC × ALFA Network Integration Guide
sidebar_label: Orange Pi / RK3588
sidebar_position: 8
description: Integration guide for Orange Pi 5 / 5B / 5 Plus and Rockchip RK3588 SBCs with ALFA adapters, kernel differences, Armbian mainline deployment, and power optimization.
tags: [orange-pi, rk3588, armbian, rockchip, alfa, awus036axml, awus036acm, sbc]
keywords: [Orange Pi 5, RK3588, Armbian mainline, vendor BSP, AWUS036AXML, AWUS036ACM, mt76]
---

# Orange Pi & Rockchip RK3588 SBC × ALFA Network Integration Guide

> **Quick Summary**: Single-board computers powered by the Rockchip RK3588 SoC (such as Orange Pi 5 / 5B / 5 Plus, Radxa ROCK 5B) deliver exceptional compute power for edge gateways and wireless sensing. When connecting ALFA USB adapters, the **OS Kernel Architecture (Vendor BSP vs. Armbian Mainline)** determines whether the adapter works plug-and-play.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **Orange Pi / RK3588 boards have not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. Only test networks you own or are authorized to test.

## Is This Guide for You?

- **Difficulty**: Intermediate.
- **Estimated Time**: 15–25 minutes.
- **Skills Used**: Terminal commands, image flashing, driver verification.
- **What You Will Achieve**:
  1. Understand why stock Vendor BSP (Debian 5.10) fails to recognize adapters, while Armbian Mainline works out of the box.
  2. Select the optimal ALFA adapter model and configure plug-and-play drivers on Armbian.
  3. Manage power budgets (5V/4A) to ensure stability under heavy RF transmission.

---

## Core Difference: Vendor BSP vs. Armbian Mainline

Many developers find ALFA adapters unacknowledged on stock Orange Pi Debian images. This is a software kernel packaging issue, not a hardware defect:

```mermaid
flowchart TD
    subgraph SBC["Orange Pi 5 (RK3588S SBC)"]
        Hardware["RK3588S 8-Core CPU<br/>USB 3.0 / USB 2.0 Ports"]
    end

    subgraph Vendor["Vendor BSP OS (Debian 5.10-rockchip)"]
        VCore["Linux 5.10 Legacy Kernel Branch"]
        VDrviers["❌ mt7921u is absent (in mainline since 5.18)<br/>⚠️ mt76 modules / MediaTek firmware may be missing"]
        VResult["Requires manual header install and DKMS build"]
    end

    subgraph Armbian["Community Armbian Mainline (Kernel ≥ 6.x)"]
        ACore["Linux 6.1 / 6.6+ Mainline Kernel"]
        ADrivers["✅ Full in-tree mt76 driver suite enabled<br/>✅ Complete linux-firmware package included"]
        AResult["ALFA AXML / ACM / ACHM Plug-and-Play!"]
    end

    Hardware --> Vendor
    Hardware --> Armbian
```

---

## Compatibility Matrix on RK3588

| ALFA Model | Chipset | Armbian (Kernel ≥6.x) | Stock Debian (Kernel 5.10) | Engineering Notes |
|---|---|---|---|---|
| **AWUS036AXML** | MT7921AUN (Wi-Fi 6E) | ✅ Plug & Play (`mt7921u`, kernel 5.18+) | ⚠️ Kernel 5.10 is older than 5.18: needs a backport / out-of-tree driver | 2.4G/5G/6G; injection failed on the GX10 test platform |
| **AWUS036ACM** | MT7612U (802.11ac) | ✅ Plug & Play | ⚠️ Requires manual module load (`mt76x2u`, in mainline since 4.19) | Injection works (63-83% on 2.4 GHz in GX10 tests; EACS / ACH / ACS scored higher) |
| **AWUS036ACHM** | MT7610U (802.11ac) | ✅ Plug & Play | ⚠️ Requires manual module load (`mt76x0u`, in mainline since 4.19) | Compact single-antenna (1T1R) monitoring |
| **AWUS036ACH** | RTL8812AU | ⚠️ DKMS build unless the kernel is 6.13+ (`rtw88_8812au`) | ⚠️ Requires DKMS build | Requires `linux-headers` package |

---

## Armbian Mainline Setup (Recommended)

1. Flash the latest **Armbian Linux (Kernel 6.x Mainline)** image onto your Orange Pi 5 microSD / NVMe.
2. Plug the ALFA AWUS036AXML into a **blue USB 3.0 Type-A port**.
3. Verify driver binding:

```bash
# Check dmesg logs
dmesg | grep -i "mt7921"
# Expected: mt7921u: firmware: mediatek/WIFI_MT7961_patch_mcu_1_2_tv.bin loaded

# Verify interface
iw dev
```

---

## Power & Thermal Guidelines

- **Power Supply**: RK3588 boards draw 10W~15W under full load. Adding an ALFA high-power adapter (2W~4W) requires a dedicated **5V/4A (20W) USB-C power supply**.
- **Port Allocation**: Connect the adapter directly to the primary USB 3.0 controller port, avoiding shared unpowered USB hubs.
