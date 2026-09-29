"""Main driver API for Logitech Apex Pro keyboard support."""

from __future__ import annotations

from .device import LogitechDevice, enumerate_logitech_devices
from .protocol import LightingMode, LightingRequest, ProfileSlot, RGBColor


class LogitechApexProDriver:
    """Best-effort driver scaffold for Logitech Apex Pro keyboards.

    This class is intentionally written as a user-space abstraction for HID-based
    interaction. It provides method names and state management similar to a real
    driver, but the protocol mapping is a placeholder and should be refined against
    actual hardware reports and firmware documentation.
    """

    def __init__(self, device: LogitechDevice | None = None):
        self.device = device
        self.profile_index = 0
        self.backlight_enabled = True
        self.current_color = RGBColor(255, 0, 255)
        self.current_mode = LightingMode.STATIC
        self.current_speed = 3

    @classmethod
    def discover(cls) -> list["LogitechApexProDriver"]:
        devices = enumerate_logitech_devices()
        return [cls(device=d) for d in devices]

    def connect(self, device: LogitechDevice) -> None:
        self.device = device

    def disconnect(self) -> None:
        if self.device is not None:
            self.device.close()
        self.device = None

    def set_profile(self, slot: int | ProfileSlot) -> None:
        if isinstance(slot, int):
            slot = ProfileSlot(slot)
        self.profile_index = int(slot)
        if self.device is not None:
            from .protocol import build_profile_switch_report

            self.device.write_feature(build_profile_switch_report(slot))

    def set_brightness(self, level: int) -> None:
        """Set brightness in 0..100."""
        safe_level = max(0, min(100, int(level)))
        self.backlight_enabled = safe_level > 0
        self.current_speed = max(1, min(10, round(safe_level / 10)))

    def set_lighting_mode(self, mode: LightingMode, color: RGBColor | None = None, speed: int | None = None, zone: int = 0) -> None:
        self.current_mode = mode
        if color is not None:
            self.current_color = color
        if speed is not None:
            self.current_speed = max(0, min(20, int(speed)))

        request = LightingRequest(
            mode=mode,
            color=self.current_color,
            speed=self.current_speed,
            zone=zone,
        )

        if self.device is not None:
            self.device.write_feature(request.build())

    def set_static_color(self, color: RGBColor) -> None:
        self.set_lighting_mode(LightingMode.STATIC, color=color)

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        self.set_static_color(RGBColor(red, green, blue))

    def set_macro(self, key: int, macro_id: int) -> None:
        if self.device is not None:
            from .protocol import build_macro_report

            self.device.write_feature(build_macro_report(key, macro_id))

    def get_status(self) -> dict:
        return {
            "profile_index": self.profile_index,
            "backlight_enabled": self.backlight_enabled,
            "mode": self.current_mode.name,
            "color": {
                "red": self.current_color.red,
                "green": self.current_color.green,
                "blue": self.current_color.blue,
            },
            "speed": self.current_speed,
        }

    def reset(self) -> None:
        from .protocol import build_reset_report

        if self.device is not None:
            self.device.write_feature(build_reset_report())
"},{