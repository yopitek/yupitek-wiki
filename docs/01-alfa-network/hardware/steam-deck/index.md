---
id: alfa-hardware-steam-deck
title: Steam Deck & UP Squared Pro × ALFA Network Integration Guide
sidebar_label: Steam Deck / UP Squared
sidebar_position: 9
description: Reference architecture (not tested by Yupitek) for a UP Squared Pro onboard computer and Steam Deck ground station with ALFA AWUS036ACH over a 5.745GHz wfb-ng long-range video/telemetry link.
tags: [steam-deck, steamos, up-squared, alfa, awus036ach, rtl8812au, wfb-ng, uav]
keywords: [Steam Deck, UP Squared Pro, AWUS036ACH, RTL8812AU, wfb-ng, UAS, SteamOS readonly]
---

# Steam Deck & UP Squared Pro × ALFA Network Integration Guide

> **Quick Summary**: A commonly described Unmanned Aerial System (UAS) setup uses the **UP Squared Pro** as the airborne real-time vision computer and the **Valve Steam Deck (SteamOS)** as the handheld Ground Control Station (GCS), with **ALFA AWUS036ACH** adapters at both ends over `wfb-ng` (Wi-Fi Broadcast Next Generation) on 5.745 GHz for a long-range, low-latency unidirectional broadcast link. This guide covers setup, SteamOS immutable filesystem handling, and partition recovery.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **Steam Deck, UP Squared Pro and wfb-ng have not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. The ACH in-kernel driver (`rtw88_8812au`, kernel 6.13+) was exercised on the GX10 only for monitor mode and injection (100% on 2.4 and 5 GHz), not for wfb-ng; whether you need the DKMS driver below depends on the SteamOS kernel version. Only test networks you own or are authorized to test.

## Is This Guide for You?

- **Difficulty**: Advanced (Linux terminal, kernel headers, SteamOS immutable filesystem).
- **Estimated Time**: 25–40 minutes.
- **Skills Used**: DKMS compilation, SteamOS system unlock, wfb-ng broadcast configuration.
- **What You Will Achieve**:
  1. Understand the architecture of unidirectional Wi-Fi broadcast links (`wfb-ng`).
  2. Temporarily unlock the SteamOS read-only root filesystem and compile the injection-capable RTL8812AU DKMS driver.
  3. Create an automated driver rebuild script to protect against SteamOS A/B partition updates.

---

## UAS Wireless Link Architecture

```mermaid
flowchart LR
    subgraph Drone["Airborne Node (UAV / Drone)"]
        Camera["HD Digital Camera"]
        UPSquared["UP Squared Pro Edge PC<br/>(Intel x86 / Ubuntu 22.04)"]
        AirALFA["ALFA AWUS036ACH<br/>(RTL8812AU / Dual Antennas)"]
        Camera --> UPSquared
        UPSquared -->|wfb-ng Unidirectional Broadcast| AirALFA
    end

    RFLink((5.745 GHz RF Broadcast Link<br/>wfb-ng Wireless Packet Injection))

    subgraph GCS["Ground Control Station (GCS)"]
        GroundALFA["ALFA AWUS036ACH<br/>(APA-M25 Directional Panel Antenna)"]
        SteamDeck["Valve Steam Deck<br/>(SteamOS / QGroundControl)"]
        Display["Real-time FPV Video & Telemetry"]
        GroundALFA -->|Monitor Frame Reception| SteamDeck
        SteamDeck --> Display
    end

    AirALFA --> RFLink
    RFLink --> GroundALFA
```

---

## Why the AWUS036ACH Is the Commonly Cited Choice

In `wfb-ng` long-range FPV links, the **Realtek RTL8812AU driver** supports customized frame injection parameters, disables ACK retransmissions, and enforces operation on specific 5 GHz channels (e.g. 5.745 GHz / Channel 149). The ALFA AWUS036ACH incorporates dual hardware power amplifiers (PA/LNA) and dual RP-SMA ports, which is why it is the card most often cited in community `wfb-ng` setups.

> **Strict Scope Disclaimer**: Yupitek has not tested `wfb-ng`, the Steam Deck, or the UP Squared Pro. Other models (such as AXML / ACM) have not been benchmarked under `wfb-ng` and are not endorsed in this document. On the GX10 test platform the AXML failed packet injection, so it should not be used for injection-based links.

---

## Steam Deck (SteamOS) Driver Installation

SteamOS uses an immutable (read-only) root filesystem by default. Disabling the lock is necessary before building DKMS kernel modules:

```bash
# 1. Switch to Steam Deck Desktop Mode and launch Konsole

# 2. Set administrator password if not set
passwd

# 3. Temporarily disable SteamOS read-only rootfs
sudo steamos-readonly disable

# 4. Initialize Pacman keyring
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman -Sy --needed base-devel linux-neptune-headers git dkms

# 5. Clone and build the injection-capable RTL8812AU driver
git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh

# 6. Re-enable read-only filesystem protection
sudo steamos-readonly enable
```

---

## SteamOS System Update Recovery Script

- **A/B Partitioning Caveat**: SteamOS major updates overwrite the system partition, wiping kernel modules in `/usr/lib/modules/`.
- **Recommended Practice**: Store an automated rebuild script at `/home/deck/scripts/rebuild_alfa.sh` to quickly restore driver functionality after system updates.
