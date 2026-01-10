from machine import Pin, SPI, PWM
import framebuf
import time

# colour constants for RGB565 format
RED = 0x00F8
GREEN = 0xC006
BLUE = 0x1F00
YELLOW = 0xE0FF
WHITE = 0xFFFF
BLACK = 0x0000


class LCD_0inch96(framebuf.FrameBuffer):
    def __init__(self):

        # LCD dimensions
        self.width = 160
        self.height = 80

        # pin configuration for the display
        self.cs = Pin(9, Pin.OUT)  # chip select
        self.rst = Pin(12, Pin.OUT)  # output for RESET line on hardware
        self.cs(1)  # deselect the display

        # SPI bus configuration to map Pico pins to LCD pins
        self.spi = SPI(1,
                       10000_000,
                       polarity=0,
                       phase=0,
                       sck=Pin(10),
                       mosi=Pin(11),
                       miso=None)
        self.dc = Pin(8, Pin.OUT)
        self.dc(1)

        # frame buffer for the display
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.Init()

        # set the full display area as the drawing window
        self.SetWindows(0, 0, self.width-1, self.height-1)

    def reset(self):
        # hardware reset sequence for the display
        self.rst(1)
        time.sleep(0.2)
        self.rst(0)
        time.sleep(0.2)
        self.rst(1)
        time.sleep(0.2)

    def write_cmd(self, cmd):
        # send a  single command byte to the display
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        # send a single data byte to the display
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def backlight(self, value):
        # set the backlight brightness using PWM on pin 13
        pwm = PWM(Pin(13))
        pwm.freq(1000)
        if value >= 1000:
            value = 1000
        data = int(value * 65536 / 1000)
        pwm.duty_u16(data)

    def Init(self):
        # initialise the display with a sequence of commands and data
        self.reset()
        # turn on the backlight at full brightness
        self.backlight(10000)

        # initialisation sequence
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x21)
        self.write_cmd(0x21)

        self.write_cmd(0xB1)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB2)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB3)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB4)
        self.write_data(0x03)

        self.write_cmd(0xC0)
        self.write_data(0x62)
        self.write_data(0x02)
        self.write_data(0x04)

        self.write_cmd(0xC1)
        self.write_data(0xC0)

        self.write_cmd(0xC2)
        self.write_data(0x0D)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8D)
        self.write_data(0x6A)

        self.write_cmd(0xC4)
        self.write_data(0x8D)
        self.write_data(0xEE)

        self.write_cmd(0xC5)
        self.write_data(0x0E)

        # postive and negative voltage gamma control
        self.write_cmd(0xE0)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x02)
        self.write_data(0x03)
        self.write_data(0x0E)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x12)
        self.write_data(0x27)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x03)
        self.write_data(0x03)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x02)
        self.write_data(0x08)
        self.write_data(0x0A)
        self.write_data(0x13)
        self.write_data(0x26)
        self.write_data(0x36)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0x36)
        self.write_data(0xA8)

        self.write_cmd(0x29)

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        # set drawing window on display, adjust coordinates for panel offset
        Xstart = Xstart + 1
        Xend = Xend + 1
        Ystart = Ystart + 26
        Yend = Yend + 26
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)

        self.write_cmd(0x2C)

    def display(self):
        # updates the display with the contents of the frame buffer
        self.SetWindows(0, 0, self.width-1, self.height-1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


class Canvas:
    # creates a simple pixel art canvas application for the LCD display
    def __init__(self, lcd):
        self.lcd = lcd
        self.grid_size = 10  # size of each grid cell in pixels
        self.cols = 16  # number of columns in the canvas
        self.rows = 8  # number of rows in the canvas
        self.canvas = {}  # dictionary to store filled pixels
        # initial brush position
        self.brush_x = 8
        self.brush_y = 4
        # set brush colours
        self.brush_color = RED
        self.color_index = 0
        self.colors = [RED, YELLOW, GREEN, BLUE]

    def draw_grid(self):
        # draw the grid lines on the canvas
        self.lcd.fill(WHITE)
        for i in range(0, self.lcd.height+1, self.grid_size):
            self.lcd.hline(0, i, self.lcd.width, BLACK)
        for i in range(0, self.lcd.width+1, self.grid_size):
            self.lcd.vline(i, 0, self.lcd.height, BLACK)

    def draw_canvas(self):
        # draws filled cells onto the canvas
        for pos, color in self.canvas.items():
            x, y = pos
            # leave a 1 pixel border for grid lines
            self.lcd.fill_rect(
                x * self.grid_size + 1,
                y * self.grid_size + 1,
                self.grid_size - 1,
                self.grid_size - 1,
                color,
            )

    def draw_brush(self):
        # computes pixel position of brush and draws inset rectangular outline
        x = self.brush_x * self.grid_size
        y = self.brush_y * self.grid_size
        self.lcd.rect(x + 1,
                      y + 1,
                      self.grid_size - 1,
                      self.grid_size - 1,
                      self.brush_color
                      )

    def refresh_display(self):
        # refreshes the entire display
        self.draw_grid()
        self.draw_canvas()
        self.draw_brush()
        self.lcd.display()

    def move_brush(self, dx, dy):
        # movees the brush cursor, wrapping around the canvas edges
        self.brush_x = (self.brush_x + dx) % self.cols
        self.brush_y = (self.brush_y + dy) % self.rows
        self.refresh_display()

    def change_color(self):
        # cycles through the brush colors
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.brush_color = self.colors[self.color_index]
        self.refresh_display()

    def fill_current(self):
        # fill the current brush position with the selected color
        self.canvas[(self.brush_x, self.brush_y)] = self.brush_color
        self.refresh_display()

    def clear_canvas(self):
        # clear the entire canvas
        self.canvas.clear()
        self.refresh_display()


if __name__ == '__main__':
    # startup message wth instructions
    lcd = LCD_0inch96()
    lcd.fill(WHITE)
    lcd.text("Pixel Canvas", 28, 8, BLACK)
    lcd.hline(10, 20, 140, BLACK)
    lcd.text("Arrows: Move", 20, 30, BLACK)
    lcd.text("CTRL: Color", 20, 42, BLACK)
    lcd.text("A: Fill", 20, 54, BLACK)
    lcd.text("B: Clear", 20, 66, BLACK)
    lcd.display()
    time.sleep(5)

    # initialises the canvas
    canvas = Canvas(lcd)
    canvas.refresh_display()

    # setup buttons for input
    KEY_UP = Pin(2, Pin.IN, Pin.PULL_UP)
    KEY_DOWN = Pin(18, Pin.IN, Pin.PULL_UP)
    KEY_LEFT = Pin(16, Pin.IN, Pin.PULL_UP)
    KEY_RIGHT = Pin(20, Pin.IN, Pin.PULL_UP)
    KEY_CTRL = Pin(3, Pin.IN, Pin.PULL_UP)
    KEY_A = Pin(15, Pin.IN, Pin.PULL_UP)
    KEY_B = Pin(17, Pin.IN, Pin.PULL_UP)

    while True:
        any_key_pressed = False

        # move brush based on directional inputs
        if KEY_UP.value() == 0:
            canvas.move_brush(0, -1)
            any_key_pressed = True
        elif KEY_DOWN.value() == 0:
            canvas.move_brush(0, 1)
            any_key_pressed = True
        elif KEY_LEFT.value() == 0:
            canvas.move_brush(-1, 0)
            any_key_pressed = True
        elif KEY_RIGHT.value() == 0:
            canvas.move_brush(1, 0)
            any_key_pressed = True

        # change color on CTRL press
        if KEY_CTRL.value() == 0:
            canvas.change_color()
            time.sleep(0.2)
            any_key_pressed = True

        # fill current pixel on A press
        if KEY_A.value() == 0:
            canvas.fill_current()
            any_key_pressed = True

        # clear canvas on B press
        if KEY_B.value() == 0:
            canvas.clear_canvas()
            time.sleep(0.2)
            any_key_pressed = True

        # small delay to reduce CPU usage
        if any_key_pressed:
            time.sleep(0.08)
        else:
            time.sleep(0.01)
