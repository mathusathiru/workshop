from machine import Pin
from utime import sleep

led = Pin("LED", Pin.OUT)

# emergency SOS message in morse code
while True:
    # short dot pulses for S
    for i in range(1, 4):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)
    # time sleep between S and O
    sleep(0.4)
    # long dash pulses for O
    for i in range(1, 4):
        led.on()
        sleep(0.6)
        led.off()
        sleep(0.6)
