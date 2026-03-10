#!/usr/bin/env python3

import os
import sys
import subprocess

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8

PRESET_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "purple": (100, 12, 223),
    "white": (255, 255, 255),
    "off": (0, 0, 0),
}


def require_root():
    if os.geteuid() != 0:
        print("Please run with sudo.")
        sys.exit(1)


def ensure_ec_access():
    # mount debugfs if needed
    if not os.path.exists("/sys/kernel/debug"):
        subprocess.run(
            ["mount", "-t", "debugfs", "none", "/sys/kernel/debug"], check=True
        )

    # load EC module if needed
    if not os.path.exists(EC_PATH):
        subprocess.run(["modprobe", "ec_sys", "write_support=1"], check=True)

    if not os.path.exists(EC_PATH):
        print("EC interface not found.")
        sys.exit(1)


def read_current():
    try:
        with open(EC_PATH, "rb") as f:
            f.seek(OFFSET)
            data = f.read(3)
    except Exception as e:
        print("Failed to read EC:", e)
        sys.exit(1)

    r, g, b = data[0], data[1], data[2]
    print(f"Current RGB: {r} {g} {b}")


def write_rgb(r, g, b):
    data = bytes([r, g, b])

    try:
        with open(EC_PATH, "r+b", buffering=0) as f:
            f.seek(OFFSET)
            f.write(data)
    except Exception as e:
        print("Failed to write EC:", e)
        sys.exit(1)

    print(f"Keyboard color set to: {r} {g} {b}")


def parse_args():
    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()

        if arg == "current":
            read_current()
            sys.exit(0)

        if arg in PRESET_COLORS:
            return PRESET_COLORS[arg]

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
        print("  victus-rgb current")
        sys.exit(1)


def main():
    require_root()
    ensure_ec_access()

    result = parse_args()

    if result:
        r, g, b = result
        write_rgb(r, g, b)


if __name__ == "__main__":
    main()
