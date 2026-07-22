# DIY Sim Racing Wheel (Raspberry Pi Pico 2 + Adafruit AS5600)

A high-precision, zero-friction USB Sim Racing Steering Wheel built using a Raspberry Pi Pico 2WH (RP2350 microcontroller), an Adafruit AS5600 magnetic rotary encoder over I2C, custom tactile buttons, and a T8 CNC lead-screw shaft assembly.

This project reads 12-bit contactless Hall-Effect rotational data (0 to 4095) from the AS5600 and maps it to a clean, unsigned 8-bit HID Gamepad axis (0 to 255) running at 100Hz using CircuitPython.

---

## Features

* **Contactless Precision:** Uses the Adafruit AS5600 magnetic sensor to track a diametrically magnetized magnet with zero physical wear.
* **4,096 Steps of Resolution:** Provides 360-degree rotational tracking mapped directly to an unsigned USB HID axis.
* **RP2350 Microcontroller:** Powered by the Raspberry Pi Pico 2WH running CircuitPython.
* **8 Integrated Inputs:** Includes support for 8 tactile push buttons or paddle shifters using internal pull-up resistors.
* **Plug-and-Play USB HID:** Enumerates directly as a standard USB Gamepad recognized by games like RaceRoom, Assetto Corsa, and iRacing without third-party software.

---

## Hardware Bill of Materials (BOM)

| Component | Quantity | Description / Notes |
| :--- | :---: | :--- |
| **Raspberry Pi Pico 2WH** | 1 | RP2350 microcontroller running CircuitPython |
| **Adafruit AS5600 Breakout** | 1 | 12-bit I2C Magnetic Rotary Encoder |
| **Diametric Magnet** | 1 | Neodymium disc magnet (**Must be diametrically magnetized**) |
| **300mm T8 Shaft & Bearing Kit** | 1 | Lead screw, pillow-block bearings, and shaft coupler |
| **Tactile Buttons / Switches** | 8 | Inputs for wheel buttons and paddle shifters |
| **Breadboard / Custom PCB** | 1 | Circuit interconnects |

---

## Pinout and Wiring

### 1. Adafruit AS5600 (I2C) Connection

| AS5600 Pin | Pico 2 Pin | Function |
| :--- | :--- | :--- |
| **VIN** | 3.3V (Pin 36) | Power Rail |
| **GND** | GND (Pin 38) | Ground Rail |
| **SDA** | GP0 (Pin 1) | I2C Data |
| **SCL** | GP1 (Pin 2) | I2C Clock |

### 2. Button Wiring (Active-LOW)

All buttons connect between their designated GPIO pin and GND (using the Pico's internal pull-up resistors):

* **Button 1:** GP6 -> Switch -> GND
* **Button 2:** GP7 -> Switch -> GND
* **Button 3:** GP8 -> Switch -> GND
* **Button 4:** GP9 -> Switch -> GND
* **Button 5 (Left Shifter):** GP10 -> Switch -> GND
* **Button 6 (Right Shifter):** GP11 -> Switch -> GND
* **Button 7:** GP12 -> Switch -> GND
* **Button 8:** GP13 -> Switch -> GND

---

## Software Setup

### Prerequisites

1. Download the latest CircuitPython `.uf2` firmware for the **Raspberry Pi Pico 2**.
2. Download the official **Adafruit CircuitPython Library Bundle**.

### Installation

1. **Flash CircuitPython:** Hold down the `BOOTSEL` button on your Pico 2, connect it to your PC via USB, and drop the downloaded `.uf2` file onto the `RPI-RP2` drive.
2. **Install Libraries:** Copy `adafruit_as5600.mpy` from the Adafruit bundle into the `lib/` directory on your `CIRCUITPY` drive.
3. **Add Project Files:** Copy `boot.py` and `code.py` from this repository directly to the root of your `CIRCUITPY` drive.
4. **Reboot:** Eject the drive safely and reconnect the Pico 2 to initialize the new USB device profile.

---

## Repository Structure

```text
├── lib/
│   └── adafruit_as5600.mpy   # Adafruit AS5600 CircuitPython Driver
├── boot.py                   # Custom USB HID Gamepad Descriptor
├── code.py                   # Main 100Hz Sensor Scaling & Input Loop
└── README.md                 # Project Documentation
