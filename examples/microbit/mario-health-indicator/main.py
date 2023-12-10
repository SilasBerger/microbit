# Imports go at the top
from microbit import *
from sounds import play_hit_sound, play_death_sound
from health_indiciator import show_health, HealthLevel

# We start with full health, and we show that on the screen.
health = HealthLevel.FULL
show_health(health)

# Define a function which handles a "hit".
def handle_hit():
    # We were hit. Decrease the health by 1, update the screen.
    global health
    health = health - 1
    show_health(health)

    # Play the hit or death sound, depending on whether
    # the remaining health is greater than HealthLevel.DEAD.
    if health == HealthLevel.DEAD:
        play_death_sound()
    else:
        play_hit_sound()

# Define a function that resets health and screen.
def reset():
    global health
    health = 5
    show_health(health)

# Code in a 'while True:' loop repeats forever
while True:
    # If the sensor registered a shake gesture (and we are not dead yet),
    # we call that a hit.
    if accelerometer.was_gesture('shake') and health > HealthLevel.DEAD:
        handle_hit()

    # Press the A button to reset everything.
    if button_a.was_pressed():
        reset()
