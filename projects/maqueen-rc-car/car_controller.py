from microbit import *
from mockueen import * # TODO: Change this back to the regular library.
from helper import play_system_error_alarm, play_driver_error_alarm
from config import OBSTACLE_DETECTION_ENABLED, SAFETY_DISTANCE_CM
import radio

# If this is set to True, no motor speed updates be applied
_failsafe_engaged = False

def _stop_motors():
    motor_stop(Motor.ALL)

def _engage_failsafe():
    global _failsafe_engaged
    _stop_motors()
    _failsafe_engaged = True

def _update_motor_speeds(command):
    # If the failsafe is engaged, we don't do anything here
    if _failsafe_engaged:
        return

    # Split the message at the ':' and set the motor speeds
    (speed_left, speed_right) = command.split(':')
    print('[CAR] motor left = ' + speed_left + ', motor right = ' + speed_right)
    motor_run(Motor.LEFT, int(speed_left))
    motor_run(Motor.RIGHT, int(speed_right))

def _read_next_command():
    # Look for a new radio message - return if nothing available
    command = radio.receive()
    if not command:
        return

    # This looks like a speed command, use it to update the motor speeds
    if ':' in command:
        _update_motor_speeds(command)
    # This is the init command, run the init routine
    elif command == 'init':
        car_controller_initialize()
    # We don't know this command - something's off, engage failsafe!
    else:
        _engage_failsafe()
        print('[CAR] Unexpected command: ' + command)
        play_system_error_alarm()

# Try reading and processing the next command,
# engage failsafe if something goes wrong
def car_controller_process_command():
    try:
        _read_next_command()
    except Exception as e:
        _engage_failsafe()
        print(e)
        play_system_error_alarm()

# Stop motors, reset failsafe, purge buffered radio messages
def car_controller_initialize():
    global _failsafe_engaged
    print('[CAR] Initializing...')
    _stop_motors()
    _failsafe_engaged = False
    has_radio_messages = True
    while has_radio_messages:
        msg = radio.receive()
        has_radio_messages = msg

# Check ultrasonic sensor against safety distance, engage
# failsafe if an obstacle is too close
def car_controller_verify_no_obstacles():
    if not OBSTACLE_DETECTION_ENABLED:
        return

    distance_cm = ultrasonic()
    if distance_cm < SAFETY_DISTANCE_CM:
        _engage_failsafe()
        print('[CAR] Obstacle detected: ' + str(distance_cm) + 'cm')
        play_driver_error_alarm()

