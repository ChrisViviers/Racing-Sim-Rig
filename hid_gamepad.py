import struct
import usb_hid


class Gamepad:
    def __init__(self, devices):
        self._gamepad_device = None
        for dev in devices:
            if dev.usage == 0x05 and dev.usage_page == 0x01:
                self._gamepad_device = dev
                break
        if not self._gamepad_device:
            raise RuntimeError("Gamepad HID device not found in usb_hid.devices")

        self._buttons = 0
        self._x = 0     # Steering center (0)
        self._y = 0     # Throttle rest (0)
        self._z = 0     # Brake rest (0)
        self._rz = 0    # Unused (0)
        self._report = bytearray(6)

    # --- Kept for compatibility / interactive use, but each call sends
    # its own report. For the main loop, prefer report() below so only
    # one HID report goes out per iteration. ---
    def press_buttons(self, *button_numbers):
        for btn in button_numbers:
            self._buttons |= (1 << (btn - 1))
        self._send()

    def release_buttons(self, *button_numbers):
        for btn in button_numbers:
            self._buttons &= ~(1 << (btn - 1))
        self._send()

    def move_joysticks(self, x=0, y=0, z=0, rz=0):
        self._x = max(-127, min(127, int(x)))
        self._y = max(0, min(255, int(y)))
        self._z = max(0, min(255, int(z)))
        self._rz = max(0, min(255, int(rz)))
        self._send()

    def report(self, buttons=0, x=0, y=0, z=0, rz=0):
        """Set buttons + all axes and send exactly one HID report.

        buttons: 16-bit mask, bit 0 = button 1 ... bit 15 = button 16.
        """
        self._buttons = buttons & 0xFFFF
        self._x = max(-127, min(127, int(x)))
        self._y = max(0, min(255, int(y)))
        self._z = max(0, min(255, int(z)))
        self._rz = max(0, min(255, int(rz)))
        self._send()

    def _send(self):
        # Pack 16 buttons (H), 1 signed byte for X (b), 3 unsigned bytes for Y, Z, Rz (3B)
        struct.pack_into("<Hb3B", self._report, 0, self._buttons, self._x, self._y, self._z, self._rz)
        self._gamepad_device.send_report(self._report, 5)  # Sent to Report ID 5
