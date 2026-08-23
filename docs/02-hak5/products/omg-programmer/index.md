---
id: hak5-product-omg-programmer
title: O.MG Programmer
sidebar_position: 13
description: The universal programmer for all O.MG devices — activate, upgrade firmware, recover from self-destruct, and make forensic backups.
tags: [hak5, omg, omg-programmer, firmware, setup, activation]
keywords: [O.MG Programmer, WebFlasher, activate O.MG, firmware upgrade, forensic backup, self-destruct recovery]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-programmer
category: product
difficulty: intermediate
toc: true
---

# O.MG Programmer — The Complete Guide

> **Quick Summary**: The O.MG Programmer is the dedicated interface for provisioning and maintaining all O.MG hardware—providing initial flashing, firmware updates, factory recovery, and forensic backups.

Every O.MG device ships **deactivated** for legal reasons. Before it can do anything, it must be activated — and that's what the **O.MG Programmer** is for. It's a small USB dongle you plug between your computer and any O.MG device, paired with a browser-based **WebFlasher** utility. One Programmer serves the *entire* O.MG lineup, so you never buy per-device hardware.

Beyond first-time activation, it's your management tool: firmware upgrades, recovery after an accidental self-destruct, and forensic backups before you hand a device to someone else.

> **Why "deactivated"?** O.MG implants are so capable that regulations require them to ship inert. The Programmer is both the legal gate and your everyday control panel.

---

## Specs at a glance

| Item | Specification |
|---|---|
| Form factor | USB dongle (computer ↔ O.MG device) |
| Compatibility | O.MG Cable, O.MG Plug, O.MG Adapter, O.MG UnBlocker |
| Interface | USB-A to your computer; hosts the connected O.MG device |
| Control utility | WebFlasher in a WebSerial browser (Chrome / Edge); Python flasher alternative |
| Operations | Activate, firmware upgrade, self-destruct recovery, forensic backup/dump, batch install |
| Official docs | https://o.mg.lol/setup/ |

## What it can do

| Operation | What happens |
|---|---|
| **Activation** | Initial 3-step setup that makes a dormant O.MG device operational |
| **Firmware upgrade** | Free updates; Elite devices gain future capabilities without new hardware |
| **Self-destruct recovery** | Restore a device you remotely wiped (e.g. accidental geofence fire) |
| **Forensic dump/backup** | Pull an image of any compatible O.MG device's memory |
| **Batch install** | Flash many units at once for bulk deployments |

---

## Activation workflow

```mermaid
%% name: hak5-product-omg-programmer-activation
flowchart TD
    A[Connect O.MG device to Programmer] --> B[Connect Programmer to a Chrome/Edge computer]
    B --> C[Open WebFlasher at o.mg.lol/setup]
    C --> D[Select your O.MG model]
    D --> E[Step 1: detect device (WebSerial prompt)]
    E --> F[Step 2: optionally forensic backup]
    F --> G[Step 3: flash firmware & activate]
    G --> H[Boot device — WebUI now available over WiFi]
```

### Step 1 — Physical setup
1. Insert the O.MG device into the Programmer.
2. Insert the Programmer into a computer running **Chrome or Edge** (these support WebSerial; Firefox/Safari do not).
3. **Keep the O.MG device unplugged from the Programmer until the wizard asks.** The bootloader detection expects a clean connect.

### Step 2 — Open WebFlasher
Browse to **https://o.mg.lol/setup/** and select your device model (Cable, Plug, Adapter, or UnBlocker).

### Step 3 — Follow the wizard
- The browser prompts you to **select the serial port** — choose the Programmer.
- (Recommended) take the optional **forensic backup** first — a safety net.
- Start the flash. It installs the latest firmware and activates the device.

Expected outcome:

```text
[+] Device detected
[+] Backup complete (optional)
[+] Firmware flashed successfully
[+] Device activated — connecting to WiFi...
```

### Step 4 — Verify
Join the O.MG device's WiFi, open its WebUI, and confirm the firmware version. It's now operational.

> **Python flasher alternative:** the O.MG firmware repo ships a Python flasher for users without a WebSerial browser. Check the O.MG firmware docs.

---

## Advanced

| Capability | How |
|---|---|
| Self-destruct recovery | Re-attach device → WebFlasher → reflash to restore from a wipe |
| Forensic forensics | Backup any O.MG device; use dumps for malware/training analysis |
| Bulk provisioning | Batch-flash a fleet of O.MG devices for a red-team lab or training class |
| Firmware access to Beta | Elite owners install Beta firmware to get upcoming features |

> **You might be asking:** *"Do I need the Programmer if I only have one O.MG cable?"* Yes — it's the only supported way to activate any O.MG device, and one Programmer covers all of them. It's not optional.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| WebFlasher says "No device found" | Device not properly connected, or wrong browser | Use Chrome/Edge; connect device only when prompted |
| Browser chooses the wrong serial port | Multiple USB-serial devices | Disconnect others; pick the serial port the wizard highlights |
| Activation stuck at "detecting" | Device not in bootloader mode | Power-cycle; re-connect cleanly at the prompt |
| Device shows old version | Firmware step skipped | Re-run WebFlasher and finish the firmware step |
| Python flasher errors | Driver / permissions | Run with appropriate privileges; see O.MG firmware docs for OS notes |

---

## Related resources

- [O.MG Cable](/hak5/products/omg-cable/) — the flagship implant this Programmer serves
- [O.MG Plug](/hak5/products/omg-plug/) / [O.MG Adapter](/hak5/products/omg-adapter/) / [O.MG UnBlocker](/hak5/products/omg-unblocker/)
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — defensive counterpart
- [Firmware & Downloads](/hak5/firmware-downloads/) — O.MG firmware & WebFlasher links
- [Troubleshooting Index](/hak5/troubleshooting-index/)
- [Hak5 overview](/hak5/)
