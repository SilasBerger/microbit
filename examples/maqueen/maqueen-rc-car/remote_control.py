from math import *
from microbit import *

# Define allowed max speed (0-255)
MAX_SPEED = 100

# Wait this many seconds between sensor reading cycles
POLL_DELAY = 1000

def calculate_speed_command():
    # Get x and z acceleration
    (acc_x, acc_z) = (
        min(accelerometer.get_x(), 1024)/1024,
        min(accelerometer.get_z(), 1024)/1024,
    )

    # Calculate tilt angle along x and z axes
    deg_x = atan(acc_x)*(180/pi)
    deg_z = atan(acc_z)*(180/pi)

    # Transform tilt along z axis to range [0, 45]° and map to speed range
    tilt_z_norm = min(45, -1 * min(0, deg_z)) / 45
    base_motor_speed = tilt_z_norm * MAX_SPEED

    # Transform tilt along x axis to range [-45, 45]°
    deg_x_norm = min(45, max(-45, deg_x)) / 45

    # Calculate steering factors:
    #   if tilt = 1: run motor left at base speed, motor right 0
    #   if tilt = -1: run motor right at base speed, motor left 0
    #   if tilt = 0: run both motors at base speed
    factor_left = min(1, deg_x_norm + 1)
    factor_right = min(1, 1-deg_x_norm)

    # Apply steering factors
    speed_left = round(base_motor_speed * factor_left)
    speed_right = round(base_motor_speed * factor_right)

    return str(speed_left) + ':' + str(speed_right) + ';'
