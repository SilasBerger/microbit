from microbit import *
from maqueen import *
import radio
import music

def read_message_and_set_motor_speeds():
    # Look for a new radio message - return if nothing available
    msg = radio.receive()
    if not msg:
        return

    # Split the message at the ':' and set the motor speeds
    (speed_left, speed_right) = msg.split(':')
    print('motor left = ' + speed_left + ', motor right = ' + speed_right)
    motor_run(Motor.LEFT, int(speed_left))
    motor_run(Motor.RIGHT, int(speed_right))

def play_error_alarm_sound():
    music.play(['c', 'f#', 'c', 'f#', 'c', 'f#'])

def car_controller_process_speed_command():
    try:
        read_message_and_set_motor_speeds()
    except Exception as e:
        stop_motors()
        print(e)
        play_error_alarm_sound()

def stop_motors():
    motor_stop(Motor.ALL)

def car_controller_initialize():
    stop_motors()
    has_radio_messages = True
    while has_radio_messages:
        msg = radio.receive()
        has_radio_messages = msg
