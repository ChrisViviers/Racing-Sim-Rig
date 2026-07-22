import usb_hid

gamepad_descriptor = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop Controls)
    0x09, 0x05,        # Usage (Gamepad)
    0xa1, 0x01,        # Collection (Application)
    0x85, 0x04,        #   Report ID (4)
    0x05, 0x09,        #   Usage Page (Button)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x10,        #   Usage Maximum (Button 16)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1)
    0x95, 0x10,        #   Report Count (16)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0x05, 0x01,        #   Usage Page (Generic Desktop Controls)
    0x09, 0x30,        #   Usage (X)
    0x09, 0x31,        #   Usage (Y)
    0x09, 0x32,        #   Usage (Z)
    0x09, 0x35,        #   Usage (Rz)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0xFF,        #   Logical Maximum (255) <-- Force pure 0-255 scale
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x04,        #   Report Count (4)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0xc0               # End Collection
))

my_gamepad = usb_hid.Device(
    report_descriptor=gamepad_descriptor,
    usage_page=0x01,
    usage=0x05,
    report_ids=(4,),
    in_report_lengths=(6,),
    out_report_lengths=(0,),
)

usb_hid.enable((my_gamepad,))
