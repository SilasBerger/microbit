from microbit import *
from remote_control import *
from car_controller import *
from helper import *
import radio

# Configure radio
radio.on()
radio.config(group=23, power=5)

# Set this Microbit to mode "remote control: parking" by default
_mode = Mode.REMOTE_CONTROL_PARKING
display_indicate_remote_control_parking()

# Define a function that toggles between car controller and remote control mode
def _toggle_operation_mode():
    global _mode
    # We were in remote control mode, switch to car control
    if _mode == Mode.REMOTE_CONTROL_PARKING or _mode == Mode.REMOTE_CONTROL_DRIVING:
        _mode = Mode.CAR_CONTROLLER
        car_controller_initialize()
        display_indicate_car_controller_mode()
    # We were in car controller mode, switch to "remote control: parking"
    elif _mode == Mode.CAR_CONTROLLER:
        _mode = Mode.REMOTE_CONTROL_PARKING
        remote_control_send_init_command()
        display_indicate_remote_control_parking()

# Define a function that toggles the remote control between "parking" and "driving"
def _toggle_parking_and_driving():
    global _mode
    # We were in parking mode, switch to driving
    if _mode == Mode.REMOTE_CONTROL_PARKING:
        _mode = Mode.REMOTE_CONTROL_DRIVING
        remote_control_send_init_command()
        display_indicate_remote_control_driving()
    # We were in driving mode, send stop command and switch to parking
    elif _mode == Mode.REMOTE_CONTROL_DRIVING:
        _mode = Mode.REMOTE_CONTROL_PARKING
        remote_control_send_stop_command()
        display_indicate_remote_control_parking()

# Continuously read the sensors and send an updated speed command
while True:
    # Button A was pressed, toggle the operation mode
    if button_a.was_pressed():
        _toggle_operation_mode()

    # Button B was pressed, toggle remote between "paring" and "driving"
    if button_b.was_pressed():
        _toggle_parking_and_driving()

    # This microbit is in remote control mode, send speed update if "driving"
    if _mode == Mode.REMOTE_CONTROL_PARKING or _mode == Mode.REMOTE_CONTROL_DRIVING:
        remote_control_send_update(_mode)

    # This microbit is in car controller mode, process speed command
    elif _mode == Mode.CAR_CONTROLLER:
        car_controller_verify_no_obstacles()
        car_controller_process_command()

    # Something went wrong, we don't know that mode...
    else:
        raise Exception('[MAIN] Undefined mode: ' + str(_mode))
