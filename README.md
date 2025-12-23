# Edge AI on BeagleBone AI  
**ADXL345-based vibration sensing, feature extraction and on-device inference**

---

## Project Overview

This repository contains an **end-to-end Edge AI project built on a BeagleBone AI**, using a real accelerometer (ADXL345) as the data source.

The goal of the project is **not** to build a large or complex ML system, but to focus on what actually matters in embedded and industrial edge environments:

- Reliable sensor acquisition  
- Deterministic sampling  
- Feature extraction on-device  
- Lightweight inference suitable for constrained hardware  

This project is intentionally designed to be **hardware-first**, progressively building from low-level drivers up to simple Edge AI inference.

---

## Motivation and Context

This is my **first complete project using a BeagleBone AI**.

Coming from Raspberry Pi–based projects, I deliberately chose the BeagleBone AI to:

- Work with a **more industrial-oriented Linux platform**
- Move away from “just works” abstractions and better understand the system underneath
- Build a stronger foundation for **embedded ML / Edge AI** beyond hobbyist setups

### Early challenges (and learning)

The initial setup was not as straightforward as with a Raspberry Pi, especially regarding:

- Network configuration (USB networking vs Wi-Fi, static IPs, routing)
- SSH access and development workflow
- Understanding the default BeagleBone Linux layout and services
- I2C bus selection and pin mapping

These issues were solved step by step and are part of the learning process.  
This repository reflects that journey: **from bare hardware access to a structured Edge AI pipeline**.

---

## Hardware

- **Board:** BeagleBone AI  
- **Sensor:** ADXL345 (3-axis accelerometer)  
- **Interface:** I2C (Bus 2)  
- **Power:** On-board 3.3 V supply  
- **Cooling:** Small external fan (manual wiring)

---

## Software Stack

- Debian GNU/Linux (BeagleBone AI)
- Python 3.11
- `smbus2` for I2C communication
- NumPy (planned)
- SciPy / lightweight DSP utilities (planned)
- Git + GitHub for version control
- VS Code with Remote SSH

---

## Current Status

### Implemented
- ADXL345 I2C driver with device validation
- Sensor configuration (output data rate, measurement range, FIFO)
- Stable raw XYZ acceleration readings
- Clean Python package structure
- Remote development using VS Code over SSH

### In progress
- Fixed-rate sampling with deterministic timing
- Window-based buffering
- Feature extraction pipeline

### Planned
- Time-domain features (RMS, variance, peak-to-peak, energy)
- Frequency-domain features (FFT-based)
- Lightweight classifier suitable for edge inference
- Off-device training, on-device inference
- Basic performance and resource usage analysis

---

## Scope and Disclaimer

This is a personal learning project focused on embedded systems and Edge AI concepts.  
The goal is not to build a production-ready solution, but to explore realistic design constraints and trade-offs found in real embedded systems.
