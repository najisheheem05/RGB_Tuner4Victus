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


# --------------------------
# SYSTEM
# --------------------------


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


# --------------------------
# EC ACCESS
# --------------------------


def write_rgb(r, g, b):

    data = bytes([r, g, b])

    with open(EC_PATH, "r+b", buffering=0) as f:
        f.seek(OFFSET)
        f.write(data)


def read_current():

    with open(EC_PATH, "rb") as f:
        f.seek(OFFSET)
        r, g, b = f.read(3)

    print(f"Current RGB: {r} {g} {b}")


# --------------------------
# HELPERS
# --------------------------


def speed_delay(speed):

    speed = max(1, min(speed, 10))

    return 0.12 - speed * 0.01


def hsv_to_rgb(h, s, v):

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))


def kill_previous():

    subprocess.run(
        ["pkill", "-f", "victus-rgb.*--worker"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def run_background():

    kill_previous()

    subprocess.Popen(
        [sys.executable] + sys.argv + ["--worker"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Effect started in background.")
    sys.exit(0)


# --------------------------
# EFFECTS
# --------------------------


def rainbow(speed=5):

    delay = speed_delay(speed)
    hue = 0

    while True:
        write_rgb(*hsv_to_rgb(hue, 1, 1))

        hue += 0.003
        if hue >= 1:
            hue = 0

        time.sleep(delay)


def breathe(color, speed=5):

    delay = speed_delay(speed)

    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    while True:
        for i in range(0, 101, 2):
            write_rgb(*hsv_to_rgb(h, s, i / 100))
            time.sleep(delay)

        for i in range(100, -1, -2):
            write_rgb(*hsv_to_rgb(h, s, i / 100))
            time.sleep(delay)


def alternate(c1, c2, speed=5):

    delay = speed_delay(speed)

    while True:
        write_rgb(*c1)
        time.sleep(delay * 6)

        write_rgb(*c2)
        time.sleep(delay * 6)


def fade(c1, c2, speed=5):

    delay = speed_delay(speed)

    r1, g1, b1 = c1
    r2, g2, b2 = c2

    while True:
        for i in range(0, 101, 2):
            r = int(r1 + (r2 - r1) * (i / 100))
            g = int(g1 + (g2 - g1) * (i / 100))
            b = int(b1 + (b2 - b1) * (i / 100))

            write_rgb(r, g, b)
            time.sleep(delay)

        for i in range(100, -1, -2):
            r = int(r1 + (r2 - r1) * (i / 100))
            g = int(g1 + (g2 - g1) * (i / 100))
            b = int(b1 + (b2 - b1) * (i / 100))

            write_rgb(r, g, b)
            time.sleep(delay)


# --------------------------
# CLI
# --------------------------


def usage():

    print("Usage:")
    print("victus-rgb red")
    print("victus-rgb 255 0 0")
    print("victus-rgb current")
    print("victus-rgb rainbow")
    print("victus-rgb rainbow 8")
    print("victus-rgb breathe red")
    print("victus-rgb breathe red 7")
    print("victus-rgb alternate red blue")
    print("victus-rgb fade red blue")
    print("victus-rgb stop")

    sys.exit(1)


def main():

    require_root()
    ensure_ec_access()

    worker = "--worker" in sys.argv

    args = [a for a in sys.argv[1:] if a != "--worker"]

    if len(args) == 1:
        arg = args[0].lower()

        if arg == "current":
            read_current()
            return

        if arg == "stop":
            kill_previous()
            print("Effects stopped.")
            return

        if arg == "rainbow":
            if not worker:
                run_background()

            rainbow()
            return

        if arg in PRESET_COLORS:
            kill_previous()
            write_rgb(*PRESET_COLORS[arg])
            return

        usage()

    elif len(args) == 2:
        if args[0] == "rainbow":
            if not worker:
                run_background()

            rainbow(int(args[1]))
            return

        if args[0] == "breathe":
            color = args[1]

            if color not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            breathe(PRESET_COLORS[color])
            return

        usage()

    elif len(args) == 3:
        if args[0] == "breathe":
            color = args[1]
            speed = int(args[2])

            if color not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            breathe(PRESET_COLORS[color], speed)
            return

        if args[0] == "alternate":
            c1 = args[1]
            c2 = args[2]

            if c1 not in PRESET_COLORS or c2 not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            alternate(PRESET_COLORS[c1], PRESET_COLORS[c2])
            return

        if args[0] == "fade":
            c1 = args[1]
            c2 = args[2]

            if c1 not in PRESET_COLORS or c2 not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            fade(PRESET_COLORS[c1], PRESET_COLORS[c2])
            return

        try:
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])

        except:
            usage()

        kill_previous()
        write_rgb(r, g, b)
        return

    elif len(args) == 4:
        if args[0] == "alternate":
            c1 = args[1]
            c2 = args[2]
            speed = int(args[3])

            if c1 not in PRESET_COLORS or c2 not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            alternate(PRESET_COLORS[c1], PRESET_COLORS[c2], speed)
            return

        if args[0] == "fade":
            c1 = args[1]
            c2 = args[2]
            speed = int(args[3])

            if c1 not in PRESET_COLORS or c2 not in PRESET_COLORS:
                usage()

            if not worker:
                run_background()

            fade(PRESET_COLORS[c1], PRESET_COLORS[c2], speed)
            return

        usage()

    else:
        usage()


if __name__ == "__main__":
    main()
