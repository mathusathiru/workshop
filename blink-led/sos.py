from machine import Pin
from utime import sleep

led = Pin("LED", Pin.OUT)


def blink(times, delay):
    # counts from 0 to 3
    for i in range(times):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)


# emergency SOS message in morse code
while True:
    # short dot pulses for S
    blink(3, 0.2)
    # time sleep between S and O
    sleep(0.4)
    # long dash pulses for O, and time sleep between O and S
    blink(3, 0.6)