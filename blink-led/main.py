from machine import Pin
from utime import sleep

''' 
Microcontroller PIN number for the built-in LED
Specific PIN number unused so the code is compatabile with multiple Pico boards
'''
led = Pin("LED", Pin.OUT)

while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
