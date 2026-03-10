#!/usr/bin/env python3

import os
import sys

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8

PRESET_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "purple": (255, 0, 255),
    "white": (255, 255, 255),
    "off": (0, 0, 0),
}


def require_root():
    if os.geteuid() != 0:
        print("Please run with sudo.")
        sys.exit(1)


def parse_args():
    if len(sys.argv) == 2:
        color = sys.argv[1].lower()
        if color in PRESET_COLORS:
            return PRESET_COLORS[color]
        else:
            print("Unknown color.")
            print("Available colors:", ", ".join(PRESET_COLORS.keys()))
            sys.exit(1)

    elif len(sys.argv) == 4:
        try:
            r = int(sys.argv[1])
            g = int(sys.argv[2])
            b = int(sys.argv[3])
        except ValueError:
            print("RGB values must be numbers.")
            sys.exit(1)

        for v in (r, g, b):
            if v < 0 or v > 255:
                print("RGB values must be between 0 and 255.")
                sys.exit(1)

        return (r, g, b)

    else:
        print("Usage:")
        print("  victus-rgb red")
        print("  victus-rgb 255 0 0")
        sys.exit(1)


def write_rgb(r, g, b):
    data = bytes([r, g, b])

    try:
        with open(EC_PATH, "r+b", buffering=0) as f:
            f.seek(OFFSET)
            f.write(data)
    except Exception as e:
        print("Failed to write EC registers:", e)
        sys.exit(1)


def main():
    require_root()

    r, g, b = parse_args()

    write_rgb(r, g, b)

    print(f"Keyboard color set to: {r} {g} {b}")


if __name__ == "__main__":
    main()
