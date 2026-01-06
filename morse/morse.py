from machine import Pin
from utime import sleep

led = Pin("LED", Pin.OUT)

codes = {
    "a": ".-", "b": "-...",  "c": "-.-.",
    "d": "-..", "e": ".", "f": "..-.",
    "g": "--.", "h": "....", "i": "..",
    "j": ".---", "k": "-.-", "l": ".-..",
    "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-",
    "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..",
    "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
    "0": "-----",
}

dot_duration = 0.2
dash_duration = dot_duration * 3
word_gap = dot_duration * 7


def send_pulse(dot_or_dash):
    if dot_or_dash == ".":
        delay = dot_duration
    else:
        delay = dash_duration
    led.on()
    sleep(delay)
    led.off()
    sleep(delay)


def send_morse_for(character):
    if character == " ":
        sleep(word_gap)
    else:
        pattern = codes.get(character.lower())
        if pattern:
            print(character + " " + pattern)
            for pulse in pattern:
                send_pulse(pulse)
                sleep(dash_duration)
        else:
            print("unknown character: " + character)


print("Morse Messenger")
print("+-+-+-+-+-+-+-+")
print("Messenger is ready. Press Ctrl+C to quit.\n")

try:
    while True:
        text = input("Message: ")
        for character in text:
            send_morse_for(character)
except KeyboardInterrupt:
    print("\nStopping Messenger...")
