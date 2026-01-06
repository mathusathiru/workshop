from machine import Pin
import time

leds = {
    "red": Pin(18, Pin.OUT),
    "yellow": Pin(19, Pin.OUT),
    "green": Pin(20, Pin.OUT),
    }

red_time = 5
red_amber_time = 2
amber_time = 3
green_time = 5


def all_off():
    for led in leds.values():
        led.value(0)


def all_on():
    for led in leds.values():
        led.value(1)


all_off()

print("Traffic Light Controller")
print("+-+-+-+-+-+-+-+-+-+-+-+-")
print("Press Ctrl+C to quit\n")

cycles = 0

try:
    while True:
        cycles += 1
        print("Cycle:", cycles)

        print("Red")
        all_off()
        leds["red"].value(1)
        time.sleep(red_time)

        print("Amber")
        all_off()
        leds["red"].value(1)
        leds["yellow"].value(1)
        time.sleep(red_amber_time)

        print("Green")
        all_off()
        leds["green"].value(1)
        time.sleep(green_time)

        all_off()
        leds["yellow"].value(1)
        time.sleep(amber_time)
        
        print()
except KeyboardInterrupt:
    print("Shutting down traffic light controller...")
