#!/usr/bin/env python3

import os
import sys

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8

if os.geteuid() != 0:
    print("Run with sudo.")
    sys.exit(1)

if len(sys.argv) != 4:
    print("Usage: victus-rgb R G B")
    sys.exit(1)

r = int(sys.argv[1])
g = int(sys.argv[2])
b = int(sys.argv[3])

for v in (r, g, b):
    if v < 0 or v > 255:
        print("Values must be 0–255")
        sys.exit(1)

data = bytes([r, g, b])

with open(EC_PATH, "r+b", buffering=0) as f:
    f.seek(OFFSET)
    f.write(data)

print(f"Set keyboard color to: {r} {g} {b}")
