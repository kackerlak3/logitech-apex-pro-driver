# Logitech Apex Pro Driver

A best-effort starter project for Logitech Apex Pro keyboard support. This repository is intentionally structured as a driver skeleton for HID-based Logitech keyboard interaction, with placeholder protocol definitions and a user-space API you can extend.

This is not a vendor-validated, production-grade driver and should be treated as a research / engineering scaffold.

## Features

- device discovery for Logitech HID keyboards
- symbolic protocol constants and report builder helpers
- backlight configuration interfaces
- profile and macro abstraction stubs
- example usage and extension points

## Project layout

- `src/logitech_apex_pro/driver.py` - main driver API
- `src/logitech_apex_pro/protocol.py` - protocol and HID report constants
- `src/logitech_apex_pro/device.py` - device abstraction and discovery
- `example_usage.py` - sample script

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install hidapi
python example_usage.py
```

## Notes

- The Logitech Apex Pro uses vendor-specific HID feature reports. Hardware-specific packet layouts vary by model revision and firmware.
- A real implementation typically requires:
  - device enumeration by USB VID/PID
  - feature report writes using hidapi or OS-specific HID APIs
  - firmware-specific packet decoding
  - calibration and keymap validation on the target OS

## License

MIT
