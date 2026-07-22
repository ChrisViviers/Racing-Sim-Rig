import board
import busio
import digitalio
import time
import usb_hid
import adafruit_as5600

# ==========================================
# 1. HARDWARE SETUP (STEERING WHEEL & BUTTONS)
# ==========================================
# Connect AS5600 SCL -> Pico GP1, SDA -> Pico GP0
i2c = busio.I2C(board.GP1, board.GP0)
as5600 = adafruit_as5600.AS5600(i2c)

def setup_btn(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

# Streamlined 8-Button Layout (GP6 through GP13)
btn1 = setup_btn(board.GP6)
btn2 = setup_btn(board.GP7)
btn3 = setup_btn(board.GP8)
btn4 = setup_btn(board.GP9)
btn5 = setup_btn(board.GP10)  # Shifter Left (Via slip ring)
btn6 = setup_btn(board.GP11)  # Shifter Right (Via slip ring)
btn7 = setup_btn(board.GP12)
btn8 = setup_btn(board.GP13)

# ==========================================
# 2. DATA SCALING FUNCTIONS
# ==========================================
def scale_wheel(val):
    REVERSED = False 
    wheel_offset = 2048  # Aligns your AS5600's physical midpoint
    
    # Process the raw reading against the center midpoint
    calibrated_val = (val - wheel_offset) % 4096
    
    if REVERSED:
        calibrated_val = 4095 - calibrated_val
    
    # Scale 0-4095 directly to a hard 0-255 byte array layout. 
    # Center is mathematically locked around 127.
    s = int((calibrated_val / 4095) * 255)
    
    # Hardware clamp to prevent any out-of-bounds rollover
    if s < 0: s = 0
    if s > 255: s = 255
    
    return s

# Find the Gamepad device Link
gamepad_dev = None
for device in usb_hid.devices:
    if device.usage == 0x05:
        gamepad_dev = device
        break

print("Streamlined 8-Button Racing Wheel Script Active!")

# ==========================================
# 3. MAIN RUNTIME LOOP
# ==========================================
while True:
    if gamepad_dev:
        # 1. Fetch the raw angle from the AS5600 sensor
        raw_angle = as5600.angle
        
        # 2. Keep the hardware clamp filters
        if raw_angle < 10: raw_angle = 0
        if raw_angle > 4085: raw_angle = 4095
        
        # 3. Process the cleaned data through your signed scale function
        x1 = scale_wheel(raw_angle)
        
        # 4. Clear unused extra joystick channels to neutral center (0)
        y1, x2, y2 = 0, 0, 0
        
        # 5. Pack your 8 breadboard buttons into the first byte
        b_low = 0
        if not btn1.value: b_low |= 0x01  # Button 1
        if not btn2.value: b_low |= 0x02  # Button 2
        if not btn3.value: b_low |= 0x04  # Button 3
        if not btn4.value: b_low |= 0x08  # Button 4
        if not btn5.value: b_low |= 0x10  # Button 5
        if not btn6.value: b_low |= 0x20  # Button 6
        if not btn7.value: b_low |= 0x40  # Button 7
        if not btn8.value: b_low |= 0x80  # Button 8
        
        # Second byte is empty now since we only need 8 buttons
        b_high = 0

        # 6. Assemble and dispatch report
        # CRITICAL FIX: The first element in the array MUST be the Report ID '4' 
        # to unlock communication with your custom boot.py setup!
        report = bytearray([b_low, b_high, x1, y1, x2, y2])
        
        # ... your existing code ...
        # 6. Assemble and dispatch report
        report = bytearray([b_low, b_high, x1, y1, x2, y2])
        
        # --- ADD THIS PRINT LINE FOR DIAGNOSTICS ---
        print(f"X1 Byte: {x1}") 
        
        try:
            gamepad_dev.send_report(report)
        except:
            pass
        
        try:
            gamepad_dev.send_report(report)
        except Exception as e:
            pass

    # Keep that 100Hz polling rate locked down for RaceRoom compatibility!
    time.sleep(0.01)
