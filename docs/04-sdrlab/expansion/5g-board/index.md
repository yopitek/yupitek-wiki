---
title: Flipper Zero 5G Expansion Board — Complete Guide
source_url: https://doc.yupitek.com/sdrlab/expansion/5g-board/
revision: 2026-10-03
status: Draft pending sign-off (audit log kept separately in audit_wiki.md, not included here)
translated_from: flipper_board_wiki_manual_zhtw.md
---

# Flipper Zero 5G Expansion Board — Complete Guide

> **In short**: The 5G expansion board brings dual-band **2.4GHz + 5GHz Wi-Fi** tools to your Flipper Zero — an ESP32-C5 running Marauder firmware, plus a GPS receiver, a 2.8" screen, and a built-in battery, all in one compact module.

---

## Spec Overview

| Item | Spec |
|---|---|
| **Wi-Fi module** | **ESP32-C5** (2.4GHz + 5GHz), ships pre-flashed with Marauder 5G firmware, dual-band 2.4GHz / 5GHz |
| **Sub-GHz** | **433MHz** A07 RF module, **10 dBm** output (must be set to External on the Flipper) |
| **GPS** | Built-in GPS module, powered either from the Flipper or from the board's battery |
| **Screen** | **2.8" color TFT**, built-in Marauder UI |
| **Battery** | **800 mAh** battery; the charging indicator light turns off when fully charged |
| **Antennas** | SMA connectors; included: dual-band Wi-Fi antenna (3 dBi), GPS antenna (20 dBi), 433MHz antenna (3 dBi) |
| **microSD** | **FAT32 format** — captures saved as `.pcap`, wardrive logs saved as `wardrive_*.csv` |
| **Protection** | All pins gold-plated, each signal pin has a **TVS** protection device |
| **Flashing** | USB-C port (front-left); hold the rear button while plugging in USB to enter flash mode |
| **Apps** | Flipper Zero apps: `[ESP32] WiFiMarauder`, `GPS` |
| **Connector** | Flipper Zero GPIO header |
| **Bluetooth** | BLE (Bluetooth LE) ⚠️ Bluetooth Classic is not supported |

### Antennas

The board uses SMA antenna connectors. The vendor lists three included antennas: a dual-band Wi-Fi antenna (3 dBi, no need to distinguish frequencies), a GPS antenna (20 dBi) and a 433MHz antenna (3 dBi). Match each antenna to its labeled port on the board.

---

## What This Board Is For

The ESP32-C5 is the Wi-Fi workhorse: paired with **Marauder firmware**, it scans APs and stations, sniffs beacons and probe requests, runs deauth and PMKID capture tests, and logs Wi-Fi activity — **now including 5GHz networks, which older ESP32 boards can't see**.

The GPS module turns your wardrive logs into geotagged data. The built-in battery means the Wi-Fi side doesn't have to draw entirely from the Flipper, and the module can also run standalone, detached from the Flipper.

The 433MHz Sub-GHz module lets you work with 433MHz signals directly from the Flipper Zero's Sub-GHz menu — particularly useful where the Flipper's built-in receiver is weak.

> **Use only on your own networks and devices.** Deauth and probe sniffing interfere with others and are regulated in most countries. This is an experimentation/education tool.

---

## Before You Start

- The Flipper needs **custom firmware with WiFi Marauder and GPS apps** — such as **Momentum**. (See the [Flipper Zero section](/flipper-zero/) for firmware basics.)
- **This board already includes** the 433MHz Sub-GHz module, the 2.8" Marauder screen, and the 800mAh battery.
- Prepare a microSD card formatted as **FAT32**.

---

## Setup: GPIO Pins (Momentum Firmware)

On **Momentum**:

1. Open `Protocol Settings → GPIO Pin Settings`
2. Set **GPS Pin** to **13** or **14** (UART pins)
3. Set **ESP32 Pin** to **15, 16** (the UART that talks to the ESP32-C5)
4. Exit settings and reboot the Flipper

> ⚠️ **GPS and ESP32 use two separate UART pin groups.**
> This board ships configured as: GPS = 13/14, ESP32 = 15/16.
> **Do not set both to the same pins** — if you do, neither GPS nor Wi-Fi will respond.
> If you're using a different firmware, the setup path may differ — check that firmware's own GPIO settings menu.

---

## Using the Board

### WiFi Marauder

1. With the board installed, open `Apps → GPIO → [ESP32] WiFiMarauder`
2. Run **Scan AP**: nearby APs will show SSID, channel, RSSI, and encryption type
3. Run **Packet Monitor** or **Beacon Sniff** to watch beacon/probe traffic
4. **Wardrive** (paired with GPS) exports logs as CSV for later analysis

Example scan output (**illustrative format only, not actual captured data**):

```
SSID              CH  RSSI  ENC     AUTH
yupitek-lab       6   -55   WPA2    PSK
Campus_Guest      11  -72   OPEN
```

### GPS

1. Attach the GPS antenna and position it facing open sky (near a window works, outdoors is better)
2. Open `Apps → GPIO → GPS` and wait — **the first fix can take several minutes (cold start)**
3. Once a satellite fix is acquired, position data starts coming in. Combine with Marauder to get geotagged Wi-Fi logs

> ℹ️ GPS time is always reported as **UTC+0**. For local time, add your UTC offset manually — the firmware menu has no timezone setting.

### 433MHz Sub-GHz

1. `Flipper Zero → Sub-GHz → Advanced Settings → Module`
2. Change to **External**
3. Use the 433MHz band from the Sub-GHz menu

> Without this step, the Flipper keeps using its built-in CC1101 chip and the board's 433MHz module is never activated.

### microSD Logging

1. Format the microSD as **FAT32** (**exFAT/NTFS are not supported**)
2. Insert it into the card slot on the board
3. In the module, confirm **PCAP saving is enabled** under `Device → Settings`
4. Captures are saved as `.pcap` files (open with [Wireshark](https://www.wireshark.org)); wardrive logs are saved separately as `wardrive_*.csv`

---

## Updating ESP32-C5 Firmware

This board **ships pre-flashed with Marauder 5G** and normally doesn't need to be reflashed.

If you do need to update it, get the **board-specific** firmware file and version from the manufacturer or distributor first — whether the generic ESP32-C5 build from the open-source Marauder release page is fully compatible with this board's screen, SD card, GPS, and pin configuration hasn't been confirmed by the manufacturer yet. Don't flash an unconfirmed generic build, as it may leave the device unable to boot.

### Entering Flash Mode (USB-C)

1. Hold down the button on the back
2. While still holding it, plug in the USB-C cable (front-left flashing port)
3. Flash firmware using a tool confirmed to support **ESP32-C5**
4. Unplug and reboot the Flipper Zero

> ⚠️ Before flashing, confirm your tool supports the ESP32-C5 chip; when in doubt, follow guidance from the manufacturer or distributor.

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| App shows "no module" | GPIO pins not configured | Recheck `GPIO Pin Settings`; reboot the Flipper |
| No networks found at all | Wrong UART pins for ESP32 | Set ESP32 Pin to **15, 16**; reboot |
| 5GHz networks missing or scans unstable | Possibly a firmware-version-related limitation | Favor scanning/monitoring; check the [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) for the current state of your firmware version |
| 5GHz deauth has no effect | Known firmware limitation | 2.4GHz is more mature and stable — prefer it |
| GPS never gets a fix | Antenna not connected / indoors / fix time not met | Connect the GPS antenna, face it toward open sky, go outdoors or near a window, and allow several minutes for a cold start |
| Module has power but Flipper shows nothing | Flipper firmware lacks the matching app | Install a custom firmware that includes the WiFi Marauder / GPS apps (e.g., Momentum) |
| SD card not recognized | Wrong format or capacity | Must be FAT32; reformat |
| No PCAP files produced | PCAP saving not enabled | Enable PCAP saving under `Device → Settings` |
| Module unresponsive at boot | GPIO connector not fully seated | Press down firmly until flush; confirm the battery has charge or USB-C is connected |

For more help, see the [SDRLAB Troubleshooting Center](/sdrlab/troubleshooting/).

---

## Known Limitations

- **5GHz deauth reliability depends on firmware version.** Open-source Marauder firmware support for 5GHz deauth on the ESP32-C5 is still being actively improved. Prefer **2.4GHz** for deauth testing; use **5GHz** mainly for scanning, signal monitoring, and wardrive logging. Check the [ESP32 Marauder GitHub](https://github.com/justcallmekoko/ESP32Marauder) for the current state of your firmware version before relying on it.
- **5GHz PMKID/EAPOL support is not yet confirmed.** Test on your own hardware before relying on it.
- **microSD supports FAT32 only.** exFAT and NTFS are not supported.
- **Bluetooth is BLE only.** The ESP32-C5 has no Bluetooth Classic (BR/EDR) hardware.
- **The two USB-C ports serve different functions** — the top-front port is the charging port; the front-left port is the ESP32-C5 programming port.

---

## Related Pages

- [WiFi multiboard (ESP32-S2)](/sdrlab/expansion/wifi-multiboard/) — the 2.4GHz-only little sibling
- [NRF24 module](/sdrlab/expansion/nrf24/) — 2.4GHz packet radio sniffing
- [Flipper Zero section](/flipper-zero/) — firmware and device basics

**Tags**: `sdrlab` · `flipper-zero` · `5g-board` · `esp32-c5` · `marauder` · `gps`
