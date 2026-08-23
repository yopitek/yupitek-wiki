---
id: hak5-product-omg-cable
title: O.MG Cable
sidebar_position: 10
description: A malicious USB cable with a hidden WiFi implant — covert keystroke injection, DuckyScript over WiFi, self-destruct and geofencing.
tags: [hak5, omg, omg-cable, malicious-cable, remote-access, duckyscript]
keywords: [O.MG Cable, malicious USB cable, keystroke injection over WiFi, DuckyScript, self-destruct, geofencing, ESP32]
authors: yupitek
date: 2026-08-21
last_updated: 2026-08-21
product: omg-cable
category: product
difficulty: advanced
toc: true
---

# O.MG Cable — The Complete Guide

> **Quick Summary**: The O.MG Cable looks and functions identically to an OEM charging and data cable, while housing a covert wireless implant microcontroller for remote Wi-Fi payload triggering and keystroke injection.

What if the charging cable you just picked up at a conference was actually a computer with a Wi-Fi radio? That's the O.MG Cable. Until tools like this existed, an implant of this class (think the NSA's COTTONMOUTH) cost tens of thousands of dollars. O.MG put it in a mass-produced, hand-made USB cable.

The cable looks and acts like a normal USB 2.0 cable — 5V charging, 480 Mbps data — but inside sits an implant that stays **dormant** (invisible on the data lines) until you trigger it over Wi-Fi. Then it deploys DuckyScript payloads, injects keystrokes, or pivots into the target's network, all controllable from a browser.

> **⚠️ Authorised testing only — and this one is special.** O.MG devices are legally *required to ship deactivated* because they are so powerful. Use them solely for authorized red-team work, teaching, and testing your own detection — and see [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) for the defensive counterpart.

---

## Specs at a glance

| Item | Specification |
|---|---|
| Form factor | Hand-made USB 2.0 cable (1 m standard; custom 2 m available) |
| Implant | WiFi-enabled wireless HID chip (WebUI + 802.11 radio on board) |
| Payload language | DuckyScript 3.0 (Elite) / DuckyScript 2.0 (Basic) |
| Remote control | Any web browser over WiFi |
| Activation | Required via [O.MG Programmer](/hak5/products/omg-programmer/) (ships deactivated) |
| Distinctive features | Self-destruct, geofencing, WiFi triggers, spoofed VID/PID/MAC |
| Elite extras | Encrypted C², HIDX StealthLink, hardware keylogger, extended WiFi range |
| Data passthrough | Normal USB 2.0 charging + data while dormant |
| Official docs | https://docs.hak5.org/omg-cable |

## Basic vs Elite (hardware tiers)

| Feature | Basic (Gen 1) | Elite (Gen 3) |
|---|---|---|
| Keystroke injection | DuckyScript 2 | DuckyScript 3 |
| Payload slots | 8 | 50–300 |
| Max payload size | ~4,000 keystrokes | ~1,500,000 keystrokes |
| Max speed | 120 keys/sec | 890 keys/sec |
| Self-destruct / geofence / WiFi trigger | ✅ | ✅ |
| FullSpeed hardware keylogger | — | ✅ |
| HIDX StealthLink / encrypted C² / extended range | — | ✅ |

---

## How the attack works

```mermaid
%% name: hak5-product-omg-cable-attack
sequenceDiagram
    participant A as Attacker (browser)
    participant C as O.MG Cable (dormant)
    participant T as Target computer
    A->>C: joins cable's WiFi, opens WebUI
    A->>C: deploys payload / triggers
    C->>T: re-enumerates as HID "keyboard"
    C->>T: injects keystrokes / exfiltrates
    T-->>C: (USB 2.0 data passthrough still works)
    A->>C: commands; optional self-destruct
```

The key insight: while *dormant*, the cable is just a cable. It only becomes a keyboard when you tell it to — which is exactly why it's so hard to detect without the right tools.

---

## Quickstart — activation & first payload

O.MG devices ship **deactivated** (legal requirement). You must activate with the Programmer:

### Step 1 — Activate with the O.MG Programmer
1. Insert the O.MG Cable's micro USB side into the [O.MG Programmer](/hak5/products/omg-programmer/).
2. Plug the Programmer into a computer running **Chrome or Edge** (WebSerial).
3. Open the WebFlasher (https://o.mg.lol/setup/), select the model, follow the 3-step wizard. The wizard optionally performs a forensic backup first.

### Step 2 — Connect to the cable's WiFi
After activation, the cable broadcasts its own WiFi. Join it from your browser.

### Step 3 — Deploy a DuckyScript payload
Open the cable's WebUI and paste/launch a payload — no recompiling to the specific device needed; DuckyScript runs directly.

```text
REM Example: open notepad and type a proof-of-concept
DELAY 1000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 800
STRING Hello from an O.MG Cable!
ENTER
```

Click **Run** in the WebUI. Within moments the target machine shows the typed text.

---

## Stealth features

| Feature | What it does |
|---|---|
| Port Stealthing | Implant stays dormant (no USB enumeration) until a payload deploys |
| Spoofable identity | Clone any VID/PID, extended USB ID, and MAC address |
| No logs / no detections | Nothing on the data lines while dormant |
| Self-destruct | Remote command wipes payloads + loot, renders cable inert (recoverable via Programmer) |
| Geofencing | Auto-trigger/self-destruct based on location — keeps the tool in scope |
| WiFi triggers | Fire a payload long-range with a single beacon |
| Encrypted C² (Elite) | Encrypted control channel; can disable the onboard WebUI if wanted |

> **You might be asking:** *"Can anything catch this cable?"* The [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) exists precisely because these are hard to catch by eye or by data-line sniffing — it uses **side-channel power analysis** to see the implant. Defense exists, but it has to be purposeful.

---

## Advanced

| Capability | How |
|---|---|
| Mouse injection | Inject cursor movement/clicks (Elite+) |
| Hardware keylogger (Elite) | FullSpeed USB keylogger add-on (with extra storage) |
| Encrypted network C² | Reach the cable from anywhere via an encrypted tunnel to your own server |
| HIDX StealthLink (Elite) | Bidirectional tunnel: Target ↔ O.MG ↔ control machine |
| Recover self-destruct | Re-attach to the Programmer to restore |
| Batch firmware | Programmer supports bulk firmware installs |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No WebUI appears | Device not activated | Activate with the Programmer first |
| WebFlasher finds nothing | Browser not WebSerial-capable / device not in bootloader | Use Chrome/Edge; keep cable unplugged until wizard asks |
| Keystrokes slow / garbled | Wrong keyboard layout or DuckyScript version | Compile/reload with correct layout; check Basic vs Elite version |
| Can't find cable's WiFi | Dormant / not in setup mode | Re-trigger via Programmer or press the onboard button sequence |
| Accidental self-destruct | Payload/geofence rule fired | Recover with the Programmer (full reset). Review geofence scope |

---

## Related resources

- [O.MG Plug](/hak5/products/omg-plug/) — same implant as a keychain USB plug
- [O.MG Adapter](/hak5/products/omg-adapter/) — the implant in a USB-A-to-C adapter
- [O.MG UnBlocker](/hak5/products/omg-unblocker/) — the implant inside a "safe" data blocker
- [O.MG Programmer](/hak5/products/omg-programmer/) — required to activate/update O.MG devices
- [Malicious Cable Detector](/hak5/products/malicious-cable-detector/) — the defensive detection tool
- [USB Rubber Ducky](/hak5/products/usb-rubber-ducky/) — DuckyScript language reference
- [Firmware & Downloads](/hak5/firmware-downloads/) — O.MG firmware & WebFlasher
- [Troubleshooting Index](/hak5/troubleshooting-index/)
- [Hak5 overview](/hak5/)
