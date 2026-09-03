# DIY Sim Racing Wheel & Gear-Driven Pedals (Raspberry Pi Pico 2 + Adafruit AS5600)

A high-precision, zero-friction USB Sim Racing Steering Wheel and Accelerator Pedal set built using a **Raspberry Pi Pico 2WH** (RP2350 microcontroller), an **Adafruit AS5600** magnetic rotary encoder over I2C, a 10k potentiometer throttle pedal with a 4:1 gear ratio, custom tactile buttons, and a T8 CNC lead-screw shaft assembly.

This project reads 12-bit contactless Hall-Effect rotational steering data (0 to 4095) and 16-bit analog potentiometer pedal data, mapping them down to clean, unsigned 8-bit HID Gamepad axes (0 to 255) running at a 100Hz polling rate in CircuitPython.

---

## Features

* **Contactless Precision Steering:** Uses the Adafruit AS5600 magnetic sensor to track a diametrically magnetized magnet with zero physical wear.
* **4:1 Gear-Driven Accelerator Pedal:** Stepped-up gear ratio assembly (80T pedal gear to 20T pot gear) provides smooth, high-resolution pedal modulation.
* **RP2350 Microcontroller:** Powered by the Raspberry Pi Pico 2WH running CircuitPython.
* **8 Integrated Inputs:** Support for 8 tactile push buttons or paddle shifters using internal pull-up resistors.
* **Auto-Inverting Pedal Calibration:** Robust calibration math handles custom potentiometer mechanical sweep directions (whether voltage sweeps up or down) automatically.
* **Modular RJ45 Cabling:** Floor pedal signals route up to the steering base through a standard Cat5e Ethernet patch cable and RJ45 breakout modules.
* **Plug-and-Play USB HID:** Enumerates directly as a standard USB Gamepad recognized by games like RaceRoom, Assetto Corsa, and iRacing without third-party software.

---

## Hardware Bill of Materials (BOM)

| Component | Quantity | Description / Notes |
| :--- | :---: | :--- |
| **Raspberry Pi Pico 2WH** | 1 | RP2350 microcontroller running CircuitPython |
| **Adafruit AS5600 Breakout** | 1 | 12-bit I2C Magnetic Rotary Encoder |
| **Diametric Magnet** | 1 | Neodymium disc magnet (**Must be diametrically magnetized**) |
| **300mm T8 Shaft & Bearing Kit** | 1 | Lead screw, pillow-block bearings, and shaft coupler |
| **10k Linear Potentiometer (B10K)** | 1 | Accelerator pedal sensor |
| **Tactile Buttons / Switches** | 8 | Inputs for wheel buttons and paddle shifters |
| **RJ45 Breakout Modules** | 2 | Modular connection for floor pedals to wheel base |
| **Cat5e / Cat6 Patch Cable** | 1 | Umbilical cable connecting pedals to steering wheel housing |
| **3D Printed Mechanical Parts** | Set | STL/SVG pedal files (see `CAD/` folder) |
| **Breadboard / Custom PCB** | 1 | Circuit interconnects |

---

## Pinout and Wiring

### 1. Steering & Pedal Connections

| Sensor / Component | Module Pin | Pico 2 Pin | Function |
| :--- | :--- | :--- | :--- |
| **AS5600 Steering** | VIN | 3.3V (Pin 36) | Power Rail |
| **AS5600 Steering** | GND | GND (Pin 38) | Ground Rail |
| **AS5600 Steering** | SDA | GP0 (Pin 1) | I2C Data |
| **AS5600 Steering** | SCL | GP1 (Pin 2) | I2C Clock |
| **Throttle Potentiometer** | Pin 1 (Outer) | 3.3V (Pin 36) | Power Rail |
| **Throttle Potentiometer** | Pin 2 (Center) | GP26 (Pin 31) | ADC0 Analog Input |
| **Throttle Potentiometer** | Pin 3 (Outer) | GND (Pin 38) | Ground Rail |

### 2. Modular Pedal Extension (RJ45 / Cat5e)

| RJ45 Pin | Pico 2 / Wheel Base | Floor Pedal Box | Function |
| :---: | :--- | :--- | :--- |
| **Pin 1** | 3.3V (Pin 36) | Potentiometer Pin 1 | Power Rail |
| **Pin 2** | GND (Pin 38) | Potentiometer Pin 3 | Ground Rail |
| **Pin 3** | GP26 (ADC0) | Potentiometer Pin 2 | Throttle Signal Line |
| **Pin 4** | GP27 (ADC1) | Reserved | Future Brake Line |

### 3. Button Wiring (Active-LOW)

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

## 3D Printed Parts & CAD Models

The repository includes ready-to-print 3D assets and 2D vector files located in the `CAD/` folder:

* **`PedalFinal.svg`:** Vector profile for laser-cutting or CNC milling the pedal plates.
* **`80T Gear Pedal Adapter.stl`:** Large 80-tooth drive gear mounted directly to the pedal pivot shaft.
* **`Small Gear 10k pot.stl`:** Small 20-tooth driven gear pressed onto the 10k potentiometer wiper shaft (4:1 step-up ratio).
* **`8mm Rod T Adapter Final.stl`:** T-Adapter mounting block for securing the guide rod and spring assembly.

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

## Pedal Calibration

Because custom gear-driven potentiometers vary by build, calibrate your pedal limits in `code.py`:

1. Run a basic analog read script to measure the raw ADC value at **Rest** and **Floored**.
2. Update the constants in `code.py`:
   ```python
   # Measured calibration limits (includes small safety buffer)
   THROTTLE_REST = 27700     # Raw value when pedal is at rest
   THROTTLE_FLOORED = 8900   # Raw value when pedal is pressed flat
