# Imports go at the top
from microbit import *
import speech

# Code in a 'while True:' loop repeats forever
while True:
    if accelerometer.was_gesture('shake'):
        speech.say('Ouch!')

    if microphone.sound_level() > 100:
        speech.say('Quiet, please.')
