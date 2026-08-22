---
slug: driver-registry
id: admin-driver-registry
title: Driver Registry
sidebar_position: 2
description: Map of every wireless chipset documented in the wiki to its supported ALFA adapters, driver type, and in-kernel status.
---

# Driver Registry

The Driver Registry maps each **wireless chipset** to the ALFA adapters that use it, the **driver type**, and the **in-kernel status** on modern Linux kernels. This mirrors the [`linux-compatibility-matrix`](/alfa-network/linux-compatibility-matrix/) and the per-chip driver guides under [`/alfa-network/drivers/`](/alfa-network/drivers/).

## Chipset Table

| Chipset | Adapters | Driver binding | In-kernel? | Driver guide |
|---------|----------|----------------|------------|--------------|
| MT7612U | AWUS036ACM | `mt76x2u` | ✅ In-kernel | [Guide](/alfa-network/drivers/mt7612u/) |
| MT7610U | AWUS036ACHM | `mt76x0u` | ✅ In-kernel | [Guide](/alfa-network/drivers/mt7610u/) |
| MT7921AUN | AWUS036AXM, AWUS036AXML | `mt7921u` | ✅ In-kernel | [Guide](/alfa-network/drivers/mt7921aun/) |
| RTL8812AU | AWUS036ACH | Out-of-tree / DKMS | ❌ Not in-kernel | [Guide](/alfa-network/drivers/rtl8812au/) |
| RTL8811AU | AWUS036ACS | Out-of-tree / DKMS | ❌ Not in-kernel | [Guide](/alfa-network/drivers/rtl8811au/) |
| RTL8832BU | AWUS036AX, AWUS036AXER | Out-of-tree / DKMS | ❌ Not in-kernel | [Guide](/alfa-network/drivers/rtl8832bu/) |
| RTL8821CU | AWUS036EACS | Out-of-tree / DKMS | ❌ Not in-kernel | [Guide](/alfa-network/drivers/rtl8821cu/) |

## Driver Types

- **In-kernel (mainline)** — Included in the Linux kernel; the adapter typically works out of the box on a current kernel with no extra installation. MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) adapters fall into this category.
- **Out-of-tree / DKMS** — The driver source is maintained outside the kernel. It must be compiled and installed, ideally via DKMS so it survives kernel updates. All Realtek chipsets in this registry fall into this category.

## Kernel Updates

For out-of-tree drivers, the single most common failure is a **kernel update** breaking the module because the pre-built module no longer matches the running kernel.

```bash
# Rebuild DKMS modules for the currently running kernel
sudo dkms autoinstall

# Or, for a convenient apt-managed rebuild on Debian/Ubuntu
sudo apt install --reinstall linux-headers-$(uname -r)
```

See also the [FAQ](/getting-started/faq/) and [`troubleshooting`](/alfa-network/troubleshooting/).

## Driver Setup Guides

- [`ubuntu`](/alfa-network/linux-setup-ubuntu/), [`kali`](/alfa-network/linux-setup-kali/), and [`nethunter`](/alfa-network/linux-setup-nethunter/) cover full system setup.
- The [`shared ALFA Linux guide`](/sdrlab/shared/alfa-linux-guide/) is referenced from SDRLAB where ALFA driver knowledge is reused.

## Maintenance

Keep this registry in sync whenever a driver guide, adapter product page, or the compatibility matrix is edited, so the cross-references never drift.
