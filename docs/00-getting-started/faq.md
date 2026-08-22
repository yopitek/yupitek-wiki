---
slug: faq
id: getting-started-faq
title: FAQ
sidebar_position: 3
description: Frequently asked questions about Yupitek products, Linux driver support and downloads.
---

# FAQ

Answers to the most common questions about Yupitek products, Linux support and downloads.

## Does my Wi-Fi adapter work out of the box on Linux?

It depends on the chipset. Adapters using **MediaTek** chipsets (`mt7612u`, `mt7610u`, `mt7921aun`) have **in-kernel** drivers — they work on recent Ubuntu, Kali and Fedora without installing anything. Adapters using **Realtek** chipsets (`rtl8812au`, `rtl8811au`, `rtl8832bu`, `rtl8821cu`) usually need an out-of-tree DKMS driver. See the [Linux Compatibility Matrix](/alfa-network/linux-compatibility-matrix/) for the full breakdown.

## Where do I download drivers and firmware?

Product firmware and drivers are hosted on our Cloudflare R2 download server at **dl.yupitek.com**. Each product page links the exact driver and firmware it needs, and driver pages under [ALFA Network](/alfa-network/) group files by chipset. Always download from the official Yupitek links rather than third-party mirrors to avoid tampered firmware.

## Which operating systems are supported?

**ALFA Network** adapters are supported on **Kali Linux**, **Ubuntu** and **Android NetHunter**, plus Windows and macOS where noted. For hardware integration, ALFA adapters are documented with **NVIDIA Jetson**, **Raspberry Pi 3/4/5** and **Unitree** robots. See the [Linux Setup](/alfa-network/linux-setup-ubuntu/) guides for step-by-step instructions.

## What is monitor mode and how do I enable it?

Monitor mode lets a wireless adapter capture and inject raw 802.11 frames without associating to a network. It is required for auditing with `airmon-ng` and `airodump-ng`. Not every chipset supports it well. Our [monitor mode](/alfa-network/linux-setup-kali/) guides cover the supported chipsets step by step.

## How do I know if my chipset supports packet injection?

Chipset support varies. MediaTek and Realtek chipsets used in ALFA adapters generally support monitor mode and packet injection, but the exact behaviour depends on the driver in use. Always test with a quick `aireplay-ng --test` before starting an engagement.

## My driver stopped working after a kernel update

Realtek out-of-tree DKMS drivers occasionally break after a kernel upgrade. The fix is usually to rebuild the module:

```bash
sudo dkms autoinstall
sudo modprobe <chipset-module>
```

See the specific [chipset driver](/alfa-network/drivers/) guide for your adapter for exact module names.

## Do HAK5 tools require the Hak5 cloud (o.mg.lol)?

**No.** You can configure and run most HAK5 devices fully offline. However, the **O.MG** product family is tied to the `o.mg.lol` cloud platform: every O.MG device must be activated with an **O.MG Programmer** and registered to an `o.mg.lol` account before first use. See the [HAK5 section](/hak5/) for device-specific setup.

## Is the Flipper Zero legal to use?

The Flipper Zero is a legitimate tool for learning, research and radio testing. Whether a specific use is legal depends on your local laws and whether you have permission for the signals you are transmitting or receiving. We encourage responsible, ethical use.

## Can I use the ACS reader for web-based NFC?

- **ACR1252U**: works with the **Web NFC API** in Chrome on Android, and with desktop browsers through a PC/SC + WebUSB bridge.
- **ACR122U** and **ACR1552U**: use the **PC/SC** framework (and libnfc for the ACR122U).

See the [ACS section](/acs/) for reader-specific guidance.

## Do you host the SDRLAB TRX-duo SD image?

The TRX-duo is a Red Pitaya–compatible board. Its SD-card images are maintained by the upstream open-source projects, so we link to the **official** downloads (trx-duo.com and the Red Pitaya community repos) rather than hosting a potentially outdated copy. Everything else we host on **dl.yupitek.com**.

## Where can I get more help?

- Search this wiki — the top navigation search covers all brands.
- Check the brand **Troubleshooting** page (for example [ALFA troubleshooting](/alfa-network/troubleshooting/)).
- Visit the [Yupitek official website](https://www.yupitek.com) for contact and sales support.
