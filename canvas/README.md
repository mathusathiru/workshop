
# Pixel Canvas

This is a simple pixel art drawing application for the Waveshare Pico LCD 0.96 display and the Raspberry Pi Pico. This builds on the demo code from Waveshare that fixes small bugs and includes a new colour. 

## Hardware Requirements

- Raspberry Pi Pico with soldered headers
- 0.96" LCD display (ST7735 controller)

## Software Requirements

- MicroPython on Raspberry Pi Pico
- Thonny IDE (this guide uses Thonny but you can use any compatible IDE of choice with the Raspberry Pi Pico)

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move brush cursor |
| CTRL | Cycle through colors |
| A | Fill current cell |
| B | Clear entire canvas |

## Usage

1. Slot the Waveshare Pico LCD into the Raspberry Pi Pico at the headers, observing the USB markings on each board to ensure correct alignment. You can use the images in the [Waveshare Pico LCD documentation](https://www.waveshare.com/wiki/Pico-LCD-0.96) as a reference to check the alignment. 

2. Connect the Raspberry Pi Pico to your desktop via USB.  

3. Open Thonny and ensure the interpreter is set to MicroPython on Raspberry Pi Pico. [This guide](https://thepihut.com/blogs/raspberry-pi-tutorials/raspberry-pi-pico-getting-started-guide) is useful for setting up Thonny, and MicroPython. 

4. Open `canvas.py` in the editor and run the program by clicking the Run button. The application will start on the LCD display, and will display instructions for you.