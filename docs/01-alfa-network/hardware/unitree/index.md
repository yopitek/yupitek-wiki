---
id: alfa-hardware-unitree
title: ALFA Adapters on Unitree Quadruped Robots
sidebar_label: Unitree Quadruped
sidebar_position: 3
description: Integration guide for ALFA high-power Wi-Fi adapters on Unitree Go2 and B2 quadruped robots — overcoming RF attenuation and motor EMI for ultra-low-latency vision streaming.
tags: [alfa, unitree, robotics, quadruped, wifi-6e, telemetry]
keywords: [Unitree ALFA, Unitree quadruped Wi-Fi, Go2 telemetry, AWUS036AXML Unitree, robotics 5GHz streaming]
---

# ALFA Adapters on Unitree Quadruped Robots

> **Quick Summary**: Unitree quadruped robots (such as the Go2 and B2) rely on high-bandwidth telemetry and low-latency video streaming between the onboard computer (NVIDIA Jetson / x86 PC) and the remote operator. Replacing the default internal Wi-Fi with an **ALFA AWUS036AXML (Wi-Fi 6E)** or **AWUS036ACM (5 GHz)** can give a more reliable control link than the default internal Wi-Fi, and 5 / 6 GHz operation avoids the 2.4 GHz band where motor electromagnetic interference (EMI) is most significant.

> **Test scope**: Yupitek's ALFA compatibility testing was done only on ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17. **Unitree robots have not been tested.** Statements on this page about driver availability are inferred from the platform's kernel version and the kernel release in which each driver reached mainline (ACM / ACHM 4.19, AXM / AXML 5.18, EACS 6.2, ACH / ACS 6.13, AX / AXER 6.17), not verified on the hardware. Range and latency on the robot have not been measured. Only test networks you own or are authorized to test.

## Is This Guide for You?

- **Difficulty**: Intermediate (robotics networking and onboard computer configuration).
- **Estimated Time**: 20–30 minutes.
- **Skills Used**: Linux networking, antenna mounting, ROS 2 telemetry optimization.
- **What You Will Achieve**:
  1. Overcome RF attenuation and motor EMI on robot platforms.
  2. Connect and configure an external ALFA adapter on the Unitree onboard Jetson/Linux PC.
  3. Optimize RTSP / WebRTC camera feeds and ROS 2 DDS communication over 5 GHz and 6 GHz.

---

## Why Robot Dogs Need External High-Power Wi-Fi

Quadruped robots are dynamic mobile sensor arrays. The onboard computing module must stream LiDAR, multi-camera feeds, and IMU state data in real time:

1. **Motor EMI Suppression**: High-torque BLDC joint motors generate significant electromagnetic noise on 2.4 GHz. Switching to 5 GHz or 6 GHz avoids the 2.4 GHz band where motor noise is most significant.
2. **Body Chassis Obstruction**: Carbon fiber and aluminum robot chassis attenuate signals from internal PCB antennas. Elevated RP-SMA external antennas maintain uninterrupted line of sight.
3. **Wi-Fi 6E and the 6 GHz band**: AWUS036AXML adds the 6 GHz band (6 GHz was tested working on the GX10 test platform). Latency for ROS 2 command topics on a Unitree robot has not been measured.

---

## Installation & Antenna Mounting Architecture

```
[Unitree Onboard Jetson / PC] === (USB 3.0) === [ALFA AWUS036AXML]
                                                    ├── [Antenna 1 (Elevated Top Mount)]
                                                    └── [Antenna 2 (Elevated Top Mount)]
```

### Best Practices for Antenna Mounting:
- Mount antennas at the highest point of the robot payload deck.
- Keep RF cables away from high-current motor power distribution buses.
- Use 2× **ALFA ARS-NT5B7** omnidirectional antennas for 360° roaming coverage.

---

## Onboard Configuration

```bash
# 1. Verify USB identification
lsusb

# 2. Check wireless interface status
iw dev

# 3. Configure connection to the field control station
sudo nmcli device wifi connect "Robot_GCS_5G" password "ControlPassword"
```
