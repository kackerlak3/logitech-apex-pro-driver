from logitech_apex_pro import LogitechApexProDriver
from logitech_apex_pro.protocol import RGBColor, LightingMode


def main() -> None:
    driver = LogitechApexProDriver()

    driver.set_profile(0)
    driver.set_brightness(70)
    driver.set_lighting_mode(LightingMode.STATIC, color=RGBColor(0, 255, 255), speed=4)
    driver.set_macro(10, 1)

    print(driver.get_status())


if __name__ == "__main__":
    main()

