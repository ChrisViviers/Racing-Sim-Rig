import board
import busio
import digitalio
import analogio
import time
import usb_hid
import adafruit_as5600

# ==========================================
# 1. HARDWARE SETUP
# ==========================================
# Steering Wheel: I2C connection to AS5600 (SCL -> GP1, SDA -> GP0)
i2c = busio.I2C(board.GP1, board.GP0)
as5600 = adafruit_as5600.AS5600(i2c)

# Accelerator Pedal: 10k Potentiometer Wiper on GP26 (ADC0)
throttle_adc = analogio.AnalogIn(board.GP26)

def setup_btn(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

# 8 Button Layout (GP6 through GP13)
buttons = [
    setup_btn(board.GP6),   # Button 1
    setup_btn(board.GP7),   # Button 2
    setup_btn(board.GP8),   # Button 3
    setup_btn(board.GP9),   # Button 4
    setup_btn(board.GP10),  # Shifter Left
    setup_btn(board.GP11),  # Shifter Right
    setup_btn(board.GP12),  # Button 7
    setup_btn(board.GP13)   # Button 8
]

# ==========================================
# 2. CALIBRATION CONSTANTS (YOUR MEASURED DATA)
# ==========================================
# Rest is around 28,000 | Floored is around 8,700
# We add a small 300-point buffer so the pedal cleanly hits 0% and 100%
THROTTLE_REST    = 27700  # Map to 0 byte (Released)
THROTTLE_FLOORED = 8900   # Map to 255 byte (Full Throttle)

def scale_wheel(val):
    """Scales 12-bit AS5600 reading (0-4095) down to 8-bit HID (0-255)."""
    REVERSED = False 
    wheel_offset = 2048  # Physical center alignment point
    
    calibrated_val = (val - wheel_offset) % 4096
    if REVERSED:
        calibrated_val = 4095 - calibrated_val
        
    s = int((calibrated_val / 4095) * 255)
    return max(0, min(255, s))

def scale_pedal_calibrated(raw_val, rest_val, floored_val):
    """
    Directly converts a reverse-sweeping ADC signal (High rest, Low floored)
    into a clean 0 to 255 forward byte array.
    """
    # 1. Clamp raw reading within physical boundaries
    if raw_val > rest_val: 
        raw_val = rest_val
    if raw_val < floored_val: 
        raw_val = floored_val
    
    # 2. Reverse scaling math: High raw = 0 (Rest), Low raw = 255 (Floored)
    scaled = int(((rest_val - raw_val) / (rest_val - floored_val)) * 255)
    
    return max(0, min(255, scaled))

# Locate USB Gamepad Interface
gamepad_dev = None
for device in usb_hid.devices:
    if device.usage == 0x05:
        gamepad_dev = device
        break

print("✅ Calibrated Rig Active: Steering (AS5600) + Accelerator (GP26) + 8 Buttons")

# ==========================================
# 3. MAIN RUNTIME LOOP (100Hz)
# ==========================================
while True:
    if gamepad_dev:
        # 1. Process Steering (X-Axis)
        raw_angle = as5600.angle
        if raw_angle < 10: raw_angle = 0
        if raw_angle > 4085: raw_angle = 4095
        x_wheel = scale_wheel(raw_angle)
        
        # 2. Process Accelerator Pedal (Y-Axis)
        y_throttle = scale_pedal_calibrated(
            throttle_adc.value, 
            THROTTLE_REST, 
            THROTTLE_FLOORED
        )
        
        # 3. Zero-out unused axis channels (Brake / Rz) to prevent in-game telemetry noise
        z_brake = 0
        rz_unused = 0
        
        # 4. Pack Buttons into bitwise byte array
        b_low = 0
        for idx, btn in enumerate(buttons):
            if not btn.value:  # Active LOW (pressed)
                b_low |= (1 << idx)
        b_high = 0

        # 5. Dispatch USB Report: [Buttons_Low, Buttons_High, Steering, Throttle, Brake, Unused]
        report = bytearray([b_low, b_high, x_wheel, y_throttle, z_brake, rz_unused])
        
        try:
            gamepad_dev.send_report(report)
        except Exception:
            pass

    time.sleep(0.01)  # Locked 100Hz Polling Rate
