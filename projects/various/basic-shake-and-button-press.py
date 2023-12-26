# ----------------------------------------------------------------------------------------
# Shake the Microbit to show the skull logo and play a sound. Press button A to reset.
# See also: makecode-basic-shake-and-button-press.md
# ----------------------------------------------------------------------------------------

# Imports go at the top
from microbit import *
import music

# Show heart image on start
display.show(Image.HEART)

# Code in a 'while True:' loop repeats forever
while True:
    if accelerometer.was_gesture('shake'):
        music.set_tempo(bpm=80)
        music.play(['b3:1', 'f4:1', ':1', 'f4:1', 'f4:1', 'e4:1', 'd4:1', 'c4:3'])
        display.show(Image.SKULL)

    if button_a.was_pressed():
        display.show(Image.HEART)
