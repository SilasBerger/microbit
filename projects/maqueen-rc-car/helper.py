from microbit import *
import music

def display_indicate_remote_control_parking():
    display.show('P')

def display_indicate_remote_control_driving():
    display.show('D')

def display_indicate_car_controller_mode():
    display.show('C')

# Define the possible operation modes
class Mode:
    REMOTE_CONTROL_PARKING = 0
    REMOTE_CONTROL_DRIVING = 1
    CAR_CONTROLLER = 2

def play_system_error_alarm():
    music.set_tempo(bpm=140)
    music.play(['c', 'f#', 'c', 'f#', 'c', 'f#'])

def play_driver_error_alarm():
    music.set_tempo(bpm=240)
    music.play([
        'c5:1', 'd5:1', 'e5:1', 'f5:1', '_:4',
        'c5:1', 'd5:1', 'e5:1', 'f5:1', '_:4',
        'c5:1', 'd5:1', 'e5:1', 'f5:1'
    ])
