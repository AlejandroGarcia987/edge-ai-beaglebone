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
- NumPy
- scikit-learn (training and inference)
- joblib (model serialization)
- Git + GitHub for version control
- VS Code with Remote SSH

---

## System Architecture and Design Decisions

This project follows a simple edge AI pipeline, designed to reflect
constraints found in embedded Linux systems.

The processing flow is:

1. Sensor acquisition (ADXL345 via I2C)
2. Fixed-rate sampling under Linux
3. Block-based buffering
4. Feature extraction on-device
5. Lightweight ML inference

### Sampling strategy

Instead of relying on per-sample real-time guarantees (which are difficult to
achieve under standard Linux), the system uses:

- Fixed target sampling rate
- Block-based acquisition (time windows)
- Timing measurement and jitter analysis

This approach prioritizes statistical stability at the block level rather
than strict real-time behavior per sample.

### Feature-first approach

Rather than streaming raw data to a model, the system extracts simple,
interpretable time-domain features (RMS, mean, standard deviation, magnitude).

This keeps the inference stage:
- Lightweight
- Explainable
- Suitable for edge devices with limited resources


## Edge ML Workflow

A simple binary classifier (idle vs vibration) is used to validate the complete
Edge AI pipeline.

### Dataset generation

- Data is collected directly on the BeagleBone AI
- Each sample corresponds to a feature vector extracted from one block
- Labels are assigned manually during acquisition:
  - `0`: idle (sensor static)
  - `1`: vibration (sensor in motion)

The dataset is intentionally small and clean, as the goal is to:
- Validate the pipeline
- Ensure reproducibility
- Avoid unnecessary complexity at this stage

### Training and inference

- Training is performed off-device (PC)
- A lightweight model (logistic regression) is used
- The trained model is deployed back to the BeagleBone AI
- Inference runs fully on-device using live sensor data

High classification accuracy is expected due to:
- Clear separation between classes
- Low-noise features
- Controlled experimental setup

This is considered a baseline, not a final model.

---

## Current Status

### Implemented (v1.0)

- ADXL345 I2C driver with device validation
- Sensor configuration (output data rate, measurement range, measurement mode)
- Fixed-rate sampling under standard Linux
- Block-based buffering strategy
- Timing and jitter measurement and analysis
- On-device time-domain feature extraction
- Dataset recording directly on the BeagleBone AI
- Off-device model training
- On-device inference using a lightweight classifier
- Continuous, real-time inference loop on live sensor data

This version closes the full edge AI loop:
**sensor → features → model → on-device prediction**.

### Planned

- Frequency-domain feature extraction (FFT-based)
- DC component handling and filtering strategies
- More diverse datasets and operating conditions
- Alternative lightweight models
- Performance and resource usage analysis
- Further reduction of dependencies for constrained environments

## Scope and Disclaimer

This is a personal learning project focused on embedded systems and Edge AI concepts.  
The goal is not to build a production-ready solution, but to explore realistic design constraints and trade-offs found in real embedded systems.

