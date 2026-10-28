from machine import Pin
from utime import sleep
from random import randint

led = Pin("LED", Pin.OUT)


def throw_dice(num_dice):
    total = 0
    for i in range(num_dice):
        total += randint(1, 6)
    return total


def blink(times, delay):
    for i in range(times):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)


while True:
    try:
        dice = int(input("Choose number of dice to roll with (1 to 5): "))
        if dice > 5:
            print("Too many dice - enter a number from 1 to 5\n")
        else:
            break
    except ValueError:
        print("Error: invalid input - enter a number from 1 to 5\n")

print("Type 'r' to roll dice or 'q' to quit: ")

while True:
    command = input()
    if command.lower() == "q":
        print("Thank you for playing!")
        break
    elif command.lower() == "r":
        dice_throw = throw_dice(dice)
        print("You rolled a", dice_throw)
        blink(dice_throw, 0.2)
    else:
        print("Error: Invalid input - type 'r' to roll or 'q' to quit")
