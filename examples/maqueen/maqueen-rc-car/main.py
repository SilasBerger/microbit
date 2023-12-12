from microbit import *
from remote_control import *
from car_controller import *
from helper import *
import radio

# Configure radio
radio.on()
radio.config(group=23, power=5)

# Set this Microbit to mode "remote control: parking" by default
mode = Mode.REMOTE_CONTROL_PARKING
display_indicate_remote_control_parking()

# Define a function that toggles between car controller and remote control mode
def toggle_operation_mode():
    global mode
    # We were in remote control mode, switch to car control
    if mode == Mode.REMOTE_CONTROL_PARKING or mode == Mode.REMOTE_CONTROL_DRIVING:
        mode = Mode.CAR_CONTROLLER
        car_controller_initialize()
        display_indicate_car_controller_mode()
    # We were in car controller mode, switch to "remote control: parking"
    elif mode == Mode.CAR_CONTROLLER:
        mode = Mode.REMOTE_CONTROL_PARKING
        display_indicate_remote_control_parking()

# Define a function that toggles the remote control between "parking" and "driving"
def remote_control_toggle_parking_and_driving():
    global mode
    # We were in parking mode, switch to driving
    if mode == Mode.REMOTE_CONTROL_PARKING:
        mode = Mode.REMOTE_CONTROL_DRIVING
        display_indicate_remote_control_driving()
    # We were in driving mode, send stop command and switch to parking
    elif mode == Mode.REMOTE_CONTROL_DRIVING:
        mode = Mode.REMOTE_CONTROL_PARKING
        remote_control_send_stop_command()
        display_indicate_remote_control_parking()

# Continuously read the sensors and send an updated speed command
while True:
    # Button A was pressed, toggle the operation mode
    if button_a.was_pressed():
        toggle_operation_mode()

    # Button B was pressed, toggle remote between "paring" and "driving"
    if button_b.was_pressed():
        remote_control_toggle_parking_and_driving()

    # This microbit is in remote control mode, send speed update if "driving"
    if mode == Mode.REMOTE_CONTROL_PARKING or mode == Mode.REMOTE_CONTROL_DRIVING:
        remote_control_send_update(mode)

    # This microbit is in car controller mode, process speed command
    elif mode == Mode.CAR_CONTROLLER:
        car_controller_process_speed_command()

    # Something went wrong, we don't know that mode...
    else:
        raise Exception('[MAIN] Undefined mode: ' + str(mode))
