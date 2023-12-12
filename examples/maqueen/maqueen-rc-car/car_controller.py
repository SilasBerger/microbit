from microbit import *
from maqueen import *
from helper import *
import radio

# If this is set to True, no motor speed updates be applied
failsafe_engaged = False

def engage_failsafe():
    global failsafe_engaged
    stop_motors()
    failsafe_engaged = True

def update_motor_speeds(command):
    # If the failsafe is engaged, we don't do anything here
    if failsafe_engaged:
        return

    # Split the message at the ':' and set the motor speeds
    (speed_left, speed_right) = command.split(':')
    print('motor left = ' + speed_left + ', motor right = ' + speed_right)
    motor_run(Motor.LEFT, int(speed_left))
    motor_run(Motor.RIGHT, int(speed_right))

def read_next_command():
    # Look for a new radio message - return if nothing available
    command = radio.receive()
    if not command:
        return

    # This looks like a speed command, use it to update the motor speeds
    if ':' in command:
        update_motor_speeds(command)
    # This is the init command, run the init routine
    elif command == 'init':
        car_controller_initialize()
    # We don't know this command - something's off, engage failsafe!
    else:
        engage_failsafe()
        print('Unexpected command: ' + command)
        play_system_error_alarm()

def car_controller_process_command():
    try:
        read_next_command()
    except Exception as e:
        engage_failsafe()
        print(e)
        play_system_error_alarm()

def stop_motors():
    motor_stop(Motor.ALL)

def car_controller_initialize():
    global failsafe_engaged
    stop_motors()
    failsafe_engaged = False
    has_radio_messages = True
    while has_radio_messages:
        msg = radio.receive()
        has_radio_messages = msg
