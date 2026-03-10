#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import colorsys

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8

PRESET_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "purple": (255, 0, 255),
    "neon-purple": (100, 12, 223),
    "white": (255, 255, 255),
    "off": (0, 0, 0),
}


def require_root():
    if os.geteuid() != 0:
        print("Run with sudo.")
        sys.exit(1)


def ensure_ec_access():
    if not os.path.exists("/sys/kernel/debug"):
        subprocess.run(
            ["mount", "-t", "debugfs", "none", "/sys/kernel/debug"], check=True
        )

    if not os.path.exists(EC_PATH):
        subprocess.run(["modprobe", "ec_sys", "write_support=1"], check=True)

    if not os.path.exists(EC_PATH):
        print("EC interface not available.")
        sys.exit(1)


def read_current():
    with open(EC_PATH, "rb") as f:
        f.seek(OFFSET)
        r, g, b = f.read(3)

    print(f"Current RGB: {r} {g} {b}")


def write_rgb(r, g, b):
    data = bytes([r, g, b])

    with open(EC_PATH, "r+b", buffering=0) as f:
        f.seek(OFFSET)
        f.write(data)


# --------------------------
# EFFECTS
# --------------------------


def rainbow():
    colors = [
        (255, 0, 0),
        (255, 127, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 0, 255),
        (75, 0, 130),
        (148, 0, 211),
    ]

    while True:
        for c in colors:
            write_rgb(*c)
            time.sleep(0.5)


def smooth_rainbow(speed=0.02):
    hue = 0

    while True:
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

        write_rgb(int(r * 255), int(g * 255), int(b * 255))

        hue += 0.002
        if hue >= 1:
            hue = 0

        time.sleep(speed)


def breathing(color, speed=0.02):
    r, g, b = color

    while True:
        for i in range(0, 256, 3):
            write_rgb(r * i // 255, g * i // 255, b * i // 255)
            time.sleep(speed)

        for i in range(255, -1, -3):
            write_rgb(r * i // 255, g * i // 255, b * i // 255)
            time.sleep(speed)


def scale_brightness(color, percent):
    r, g, b = color
    factor = percent / 100

    return (
        int(r * factor),
        int(g * factor),
        int(b * factor),
    )


# --------------------------
# CLI
# --------------------------


def usage():
    print("Usage:")
    print("  victus-rgb red")
    print("  victus-rgb neon-purple")
    print("  victus-rgb 255 0 0")
    print("  victus-rgb current")
    print("  victus-rgb rainbow")
    print("  victus-rgb smooth-rainbow")
    print("  victus-rgb breathe red")
    print("  victus-rgb breathe red 0.01")
    print("  victus-rgb brightness red 50")
    sys.exit(1)


def main():
    require_root()
    ensure_ec_access()

    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()

        if arg == "current":
            read_current()
            return

        if arg == "rainbow":
            rainbow()
            return

        if arg == "smooth-rainbow":
            smooth_rainbow()
            return

        if arg in PRESET_COLORS:
            write_rgb(*PRESET_COLORS[arg])
            return

        usage()

    elif len(sys.argv) == 3:
        cmd = sys.argv[1]
        color = sys.argv[2]

        if cmd == "breathe" and color in PRESET_COLORS:
            breathing(PRESET_COLORS[color])
            return

        usage()

    elif len(sys.argv) == 4:
        if sys.argv[1] == "brightness":
            color = sys.argv[2]
            percent = int(sys.argv[3])

            if color not in PRESET_COLORS:
                usage()

            write_rgb(*scale_brightness(PRESET_COLORS[color], percent))
            return

        if sys.argv[1] == "breathe":
            color = sys.argv[2]
            speed = float(sys.argv[3])

            if color not in PRESET_COLORS:
                usage()

            breathing(PRESET_COLORS[color], speed)
            return

        try:
            r = int(sys.argv[1])
            g = int(sys.argv[2])
            b = int(sys.argv[3])
        except ValueError:
            usage()

        write_rgb(r, g, b)
        return

    else:
        usage()


if __name__ == "__main__":
    main()
