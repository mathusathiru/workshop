from machine import Pin
from utime import sleep
from random import randint

led = Pin("LED", Pin.OUT)

def blink(times, delay):
    for i in range(times):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)

print("Press Enter to roll dice or 'q' to quit: ")

while True:
    command = input()
    if command.lower() == "q":
        print("Thank you for playing!")
        break
    elif command != "":
        print("Error: Invalid input - press Enter to roll, or 'q' to quit")
    else:
        dice_throw = randint(1, 6)
        print("You rolled a", dice_throw)
        blink(dice_throw, 0.2)