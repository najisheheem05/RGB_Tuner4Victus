# Victus RGB (Linux)

Control the keyboard RGB lighting on **HP Victus laptops** directly from Linux by writing RGB values to the Embedded Controller (EC).

This project was created after reverse-engineering how the lighting values are stored in EC memory. It allows you to change keyboard colors and run lighting effects without Windows or OMEN Gaming Hub.

---

## Features

- Change keyboard RGB color directly from Linux
- No Windows or proprietary software required
- Simple command line interface
- Lightweight (single Python script)
- Automatic EC access setup
- Background lighting effects
- Automatic replacement of running effects

Supported lighting modes:

- Static colors
- Custom RGB
- Rainbow
- Breathing effect
- Alternate between two colors
- Fade between two colors

---

## How It Works

The keyboard lighting values are stored in EC registers.

The RGB values are written starting at **offset `0x08`** inside EC memory.

Example values discovered during testing:

| Color | EC Bytes   |
| ----- | ---------- |
| Red   | `e4 00 00` |
| Green | `00 e4 00` |
| Blue  | `00 00 e4` |

The program writes RGB values directly to:

```

/sys/kernel/debug/ec/ec0/io

```

---

## Requirements

- Linux
- Python 3
- Root access
- `ec_sys` kernel module

The program automatically loads the module when needed.

---

## Installation

Clone or download the repository.

Make the script executable:

```bash
chmod +x victus-rgb.py
```

Optional: install globally

```bash
sudo mv victus-rgb.py /usr/local/bin/victus-rgb
```

Then run commands like:

```bash
sudo victus-rgb red
```

---

## Preset Colors

| Color       | Command                       |
| ----------- | ----------------------------- |
| red         | `sudo victus-rgb red`         |
| green       | `sudo victus-rgb green`       |
| blue        | `sudo victus-rgb blue`        |
| yellow      | `sudo victus-rgb yellow`      |
| cyan        | `sudo victus-rgb cyan`        |
| purple      | `sudo victus-rgb purple`      |
| neon-purple | `sudo victus-rgb neon-purple` |
| white       | `sudo victus-rgb white`       |
| off         | `sudo victus-rgb off`         |

Example:

```bash
sudo victus-rgb neon-purple
```

---

## Custom RGB

You can set any RGB color.

```
sudo victus-rgb R G B
```

Example:

```bash
sudo victus-rgb 120 40 255
```

---

## Read Current Color

Display the RGB value currently stored in the EC.

```bash
sudo victus-rgb current
```

Example output:

```
Current RGB: 255 0 0
```

---

## Lighting Effects

All lighting effects run **in the background** and continue even after the terminal closes.

Starting a new effect **automatically stops the previous one**.

---

### Rainbow

Cycle through all colors smoothly.

```bash
sudo victus-rgb rainbow
```

Adjust speed:

```bash
sudo victus-rgb rainbow 8
```

---

### Breathing Effect

Fade brightness in and out.

```bash
sudo victus-rgb breathe red
```

Adjust speed:

```bash
sudo victus-rgb breathe neon-purple 7
```

---

### Alternate Between Two Colors

Switch between two colors repeatedly.

```bash
sudo victus-rgb alternate red blue
```

Adjust speed:

```bash
sudo victus-rgb alternate red blue 8
```

---

### Fade Between Two Colors

Smooth transition between two colors.

```bash
sudo victus-rgb fade red blue
```

Adjust speed:

```bash
sudo victus-rgb fade neon-purple cyan 7
```

---

All of these effects can be run using RGB values as well ("R G B R G B" if there are 2 colors : else R G B)

```bash
sudo victus-rgb fade 255 0 0 0 255 0
```

---

## Stop Effects

Stop all running lighting effects.

```bash
sudo victus-rgb stop
```

---

## Supported Hardware

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

## License

MIT Licence
