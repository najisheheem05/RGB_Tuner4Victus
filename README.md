# Victus RGB (Linux)

Control the keyboard RGB lighting on **HP Victus laptops** directly from Linux by writing RGB values to the Embedded Controller (EC).

This project was created after reverse-engineering how the lighting values are stored in EC memory. It allows you to change keyboard colors without using Windows or OMEN Gaming Hub.

---

## Features

- Change keyboard RGB color directly from Linux
- No Windows or proprietary software required
- Simple command line interface
- Lightweight (single Python script)

---

## How it works

The keyboard lighting values are stored in EC registers.
The RGB triplet appears starting at **offset `0x08`** inside the EC memory.

Example EC values discovered during testing:

| Color | EC Bytes   |
| ----- | ---------- |
| Red   | `e4 00 00` |
| Green | `00 e4 00` |
| Blue  | `00 00 e4` |

These values were observed in EC dumps when changing colors in OMEN software.

The program writes the RGB bytes directly to:

```
/sys/kernel/debug/ec/ec0/io
```

---

## Preset Colors

The program also supports several predefined colors.

You can use the color name instead of RGB values.

### Available colors

| Color  | Command                  |
| ------ | ------------------------ |
| Red    | `sudo victus-rgb red`    |
| Green  | `sudo victus-rgb green`  |
| Blue   | `sudo victus-rgb blue`   |
| Yellow | `sudo victus-rgb yellow` |
| Cyan   | `sudo victus-rgb cyan`   |
| Purple | `sudo victus-rgb purple` |
| White  | `sudo victus-rgb white`  |
| Off    | `sudo victus-rgb off`    |

### Example

Set keyboard to purple:

```
sudo victus-rgb purple
```

Set keyboard to cyan:

```
sudo victus-rgb cyan
```

Turn off the keyboard lighting:

```
sudo victus-rgb off
```

To inspect rgb values of current lighting:

```
sudo victus-rgb current
```

### Equivalent RGB values

| Color  | RGB         |
| ------ | ----------- |
| Red    | 255 0 0     |
| Green  | 0 255 0     |
| Blue   | 0 0 255     |
| Yellow | 255 255 0   |
| Cyan   | 0 255 255   |
| Purple | 100 12 223  |
| White  | 255 255 255 |
| Off    | 0 0 0       |

---

## Requirements

- Linux
- Root access
- `ec_sys` kernel module with write support
- Python 3

---

## Enable EC write access

Load the EC module with write support:

```bash
sudo modprobe ec_sys write_support=1
```

You may also need to mount debugfs:

```bash
sudo mount -t debugfs none /sys/kernel/debug
```

---

## Installation

Clone or download this repository.

Make the script executable:

```bash
chmod +x victus-rgb.py
```

Optional: install globally

```bash
sudo mv victus-rgb.py /usr/local/bin/victus-rgb
```

---

## Usage

Run with root privileges.

```
sudo victus-rgb R G B
```

Where:

- `R` = red value (0–255)
- `G` = green value (0–255)
- `B` = blue value (0–255)

### Examples

Red

```
sudo victus-rgb 255 0 0
```

Green

```
sudo victus-rgb 0 255 0
```

Blue

```
sudo victus-rgb 0 0 255
```

---

## Supported hardware

Tested on:

- HP Victus 16

Other Victus models may work if they use the same EC RGB layout.

---

## Warning

This tool writes directly to EC registers.

Incorrect values may:

- freeze the keyboard controller
- crash the EC
- require a hard reboot

Use at your own risk.

---

## Future improvements

- brightness control
- color presets
- animation effects
- integration with OpenRGB
- GUI interface

---

## License

MIT License
