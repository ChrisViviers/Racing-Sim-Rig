# DIY Sim Racing Wheel & Gear-Driven Pedals (Raspberry Pi Pico 2 + Adafruit AS5600)

A high-precision, zero-friction USB Sim Racing Steering Wheel and Pedal set built using a **Raspberry Pi Pico 2WH** (RP2350 microcontroller), an **Adafruit AS5600** magnetic rotary encoder over I2C, gear-driven potentiometer pedals, custom tactile buttons, and a laser-cut/3D-printed rig frame.

This project reads 12-bit contactless magnetic steering data (0–4095) and 16-bit analog potentiometer pedal data, mapping them down to clean, unsigned 8-bit HID Gamepad axes (0–255) in CircuitPython.

## Table of Contents

- [Features](#features)
- [Hardware Bill of Materials](#hardware-bill-of-materials-bom)
- [3D Printed & Laser Cut Parts](#3d-printed--laser-cut-parts)
- [Pinout and Wiring](#pinout-and-wiring)
- [Software Setup](#software-setup)
- [Pedal Calibration](#pedal-calibration)

---

## Features

- **Contactless Precision Steering:** Uses the Adafruit AS5600 magnetic sensor to track a diametrically magnetized magnet with zero physical wear.
- **Gear-Driven Pedal:** Stepped-up gear ratio assembly (80T pedal gear to 20T pot gear, connected by a timing belt) provides smooth, high-resolution pedal modulation.
- **RP2350 Microcontroller:** Powered by the Raspberry Pi Pico 2WH running CircuitPython.
- **8 Integrated Inputs:** Support for 8 tactile push buttons or paddle shifters using internal pull-up resistors.
- **Auto-Inverting Pedal Calibration:** Robust calibration math handles custom potentiometer mechanical sweep directions (whether voltage sweeps up or down) automatically.
- **Modular RJ45 Cabling:** Floor pedal signals route up to the steering base through a standard Cat5e Ethernet patch cable and RJ45 breakout modules.
- **Plug-and-Play USB HID:** Enumerates directly as a standard USB Gamepad recognized by games like RaceRoom, Assetto Corsa, and iRacing without third-party software.

---

## Hardware Bill of Materials (BOM)

| Component                           | Quantity | Description / Notes                                          |
| ------------------------------------ | -------- | -------------------------------------------------------------- |
| **Raspberry Pi Pico 2WH**            | 1        | RP2350 microcontroller running CircuitPython                   |
| **Adafruit AS5600 Breakout**         | 1        | 12-bit I2C Magnetic Rotary Encoder                              |
| **Diametric Magnet**                 | 1        | Neodymium disc magnet (**must be diametrically magnetized**)   |
| **10k Linear Potentiometers (B10K)** | 2        | Throttle and brake pedal sensors                                |
| **Tactile Buttons / Switches**       | 8        | Inputs for wheel buttons and paddle shifters                    |
| **Timing Belt & Pulleys**            | 1 set    | Drives the 20T potentiometer gear from the 80T pedal gear        |
| **RJ45 Breakout Modules**            | 2        | Modular connection for floor pedals to wheel base                |
| **Cat5e / Cat6 Patch Cable**         | 1        | Umbilical cable connecting pedals to steering wheel housing     |
| **8mm Steel Rod & Bearings**         | Set      | Shaft stock used across the pedal, steering, and shifter parts  |
| **Laser Cut / 3D Printed Parts**     | Set      | See [3D Printed & Laser Cut Parts](#3d-printed--laser-cut-parts) |
| **Breadboard / Custom PCB**          | 1        | Circuit interconnects                                            |
| **M5x35 Nuts & Bolts**          | 20        | Connecting Laser Cuts                                            |

---

## 3D Printed & Laser Cut Parts

All CAD source files are in the repository root:

| File | Description |
| ---- | ------------ |
| [`racingSimPotFullLaser6mm.svg`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/racingSimPotFullLaser6mm.svg) | Laser cut template for the entire rig frame (6mm material). |
| [`Racing Wheel.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/Racing%20Wheel.stl) | 3D printable racing wheel. |
| [`8mmRodTAdapterPedal.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/8mmRodTAdapterPedal.stl) | T-adapter for the pedal that attaches a rod perpendicular to another rod in the pedal assembly. |
| [`80TGearPedalAdapter.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/80TGearPedalAdapter.stl) | 80-tooth gear that attaches to the pedal. |
| [`20TGear10kPotAdapter.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/20TGear10kPotAdapter.stl) | 20-tooth gear that attaches to the potentiometers; connected to the 80T pedal gear via a timing belt. |
| [`8mmRodMagnetAdapter.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/8mmRodMagnetAdapter.stl) | Attaches the steering wheel's AS5600 magnet to an 8mm shaft. |
| [`ShifterLaserToShaftAdapter.stl`](https://github.com/ChrisViviers/Racing-Sim-Rig/blob/main/ShifterLaserToShaftAdapter.stl) | Adapts the laser-cut design to an 8mm shaft for the sequential shifter. |

---

## Pinout and Wiring

### 1. Steering & Pedal Connections

| Sensor / Component         | Module Pin     | Pico 2 Pin    | Function          |
| --------------------------- | -------------- | ------------- | ------------------ |
| **AS5600 Steering**         | VIN            | 3.3V (Pin 36) | Power Rail          |
| **AS5600 Steering**         | GND            | GND (Pin 38)  | Ground Rail         |
| **AS5600 Steering**         | SDA            | GP0 (Pin 1)   | I2C Data            |
| **AS5600 Steering**         | SCL            | GP1 (Pin 2)   | I2C Clock           |
| **Throttle Potentiometer**  | Pin 1 (Outer)  | 3.3V (Pin 36) | Power Rail          |
| **Throttle Potentiometer**  | Pin 2 (Center) | GP26 (Pin 31) | ADC0 Analog Input   |
| **Throttle Potentiometer**  | Pin 3 (Outer)  | GND (Pin 38)  | Ground Rail         |
| **Brake Potentiometer**     | Pin 1 (Outer)  | 3.3V (Pin 36) | Power Rail          |
| **Brake Potentiometer**     | Pin 2 (Center) | GP27 (Pin 32) | ADC1 Analog Input   |
| **Brake Potentiometer**     | Pin 3 (Outer)  | GND (Pin 38)  | Ground Rail         |

### 2. Modular Pedal Extension (RJ45 / Cat5e)

| RJ45 Pin  | Pico 2 / Wheel Base | Floor Pedal Box     | Function             |
| ---------- | -------------------- | -------------------- | ---------------------- |
| **Pin 1** | 3.3V (Pin 36)        | Potentiometer Pin 1   | Power Rail             |
| **Pin 2** | GND (Pin 38)         | Potentiometer Pin 3   | Ground Rail            |
| **Pin 3** | GP26 (ADC0)          | Potentiometer Pin 2   | Throttle Signal Line   |
| **Pin 4** | GP27 (ADC1)          | Potentiometer Pin 2   | Brake Signal Line      |

### 3. Button Wiring (Active-LOW)

All buttons connect between their designated GPIO pin and GND (using the Pico's internal pull-up resistors):

- **Button 1:** GP6 -> Switch -> GND
- **Button 2:** GP7 -> Switch -> GND
- **Button 3:** GP8 -> Switch -> GND
- **Button 4:** GP9 -> Switch -> GND
- **Button 5 (Left Shifter):** GP10 -> Switch -> GND
- **Button 6 (Right Shifter):** GP11 -> Switch -> GND
- **Button 7:** GP12 -> Switch -> GND
- **Button 8:** GP13 -> Switch -> GND

---

## Software Setup

### Prerequisites

1. Download the latest CircuitPython `.uf2` firmware for the **Raspberry Pi Pico 2**.
2. Download the official **Adafruit CircuitPython Library Bundle**.

### Installation

1. **Flash CircuitPython:** Hold down the `BOOTSEL` button on your Pico 2, connect it to your PC via USB, and drop the downloaded `.uf2` file onto the `RPI-RP2` drive.
2. **Install Libraries:** Copy `adafruit_as5600.mpy` from the Adafruit bundle into the `lib/` directory on your `CIRCUITPY` drive.
3. **Add Project Files:** Copy `boot.py`, `code.py`, and `hid_gamepad.py` from this repository directly to the root of your `CIRCUITPY` drive.
4. **Reboot:** Eject the drive safely and reconnect the Pico 2 to initialize the new USB device profile.

---

## Pedal Calibration

Because custom gear-driven potentiometers vary by build, calibrate your pedal limits in `code.py`:

1. Run a basic analog read script to measure the raw ADC value at **Rest** and **Floored** for each pedal.
2. Update the constants in `code.py`:

\`\`\`python
#### Measured calibration limits
THROTTLE_REST    = 800
THROTTLE_FLOORED = 23300
BRAKE_REST       = 3400
BRAKE_FLOORED    = 24000
\`\`\`

The mapping function handles both increasing and inverted potentiometer sweep directions automatically, so it doesn't matter which end of the pedal's travel reads the higher raw value.
