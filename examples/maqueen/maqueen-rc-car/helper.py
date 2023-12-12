from microbit import *

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
