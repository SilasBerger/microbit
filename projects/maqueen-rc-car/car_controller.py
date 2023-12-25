from microbit import *
from maqueen import *
from helper import play_system_error_alarm, play_driver_error_alarm
from config import OBSTACLE_DETECTION_ENABLED, SAFETY_DISTANCE_CM, MAX_SUBSEQUENT_SAFETY_DISTANCE_VIOLATIONS
import radio

# If this is set to True, no motor speed updates be applied.
_failsafe_engaged = False

# If we see more than this many too-close readings in a row,
# we trigger need the obstacle detection protocol (if enabled).
_safety_distance_violation_count = 0

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
    global _safety_distance_violation_count
    print('[CAR] Initializing...')
    _stop_motors()
    _failsafe_engaged = False
    _safety_distance_violation_count = 0
    has_radio_messages = True
    while has_radio_messages:
        msg = radio.receive()
        has_radio_messages = msg

# Check ultrasonic sensor against safety distance, engage
# failsafe if an obstacle is too close
def car_controller_verify_no_obstacles():
    global _safety_distance_violation_count

    # If obstacle detection is not enabled, or if we already are in failsafe mode,
    # do nothing here.
    if not OBSTACLE_DETECTION_ENABLED or _failsafe_engaged:
        return

    # Get the current distance reading.
    distance_cm = ultrasonic(trig = pin1, echo = pin2)

    # If we have a safe distance, reset subsequent violation count and return.
    if distance_cm >= SAFETY_DISTANCE_CM:
        _safety_distance_violation_count = 0
        return

    # We don't have a safe distance. Increment the subsequent violation count.
    # If the count surpasses a threshold, trigger obstacle detection.
    _safety_distance_violation_count += 1
    if (_safety_distance_violation_count > MAX_SUBSEQUENT_SAFETY_DISTANCE_VIOLATIONS):
        _engage_failsafe()
        _safety_distance_violation_count
        print('[CAR] Obstacle detected: ' + str(distance_cm) + 'cm')
        play_driver_error_alarm()

