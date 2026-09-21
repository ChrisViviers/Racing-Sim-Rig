import usb_hid

gamepad_descriptor = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop Controls)
    0x09, 0x05,        # Usage (Gamepad)
    0xa1, 0x01,        # Collection (Application)
    0x85, 0x05,        #   REPORT ID (5) <-- Forces Windows Registry Refresh!
    # 16 Digital Buttons
    0x05, 0x09,        #   Usage Page (Button)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x10,        #   Usage Maximum (Button 16)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1)
    0x95, 0x10,        #   Report Count (16)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    # Steering: X (Signed -127 to 127)
    0x05, 0x01,        #   Usage Page (Generic Desktop Controls)
    0x09, 0x30,        #   Usage (X - Steering)
    0x15, 0x81,        #   Logical Minimum (-127)
    0x25, 0x7F,        #   Logical Maximum (127)
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    # Pedals: Y (Throttle) & Z (Brake) (Unsigned 0 to 255)
    0x09, 0x31,        #   Usage (Y - Throttle)
    0x09, 0x32,        #   Usage (Z - Brake)
    0x09, 0x35,        #   Usage (Rz - Unused)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0xFF,        #   Logical Maximum (255)
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x03,        #   Report Count (3)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0xc0               # End Collection
))

my_gamepad = usb_hid.Device(
    report_descriptor=gamepad_descriptor,
    usage_page=0x01,
    usage=0x05,
    report_ids=(5,),      # Updated to Report ID 5
    in_report_lengths=(6,),
    out_report_lengths=(0,),
)

usb_hid.enable((my_gamepad,))
