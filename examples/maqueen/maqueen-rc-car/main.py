from microbit import *
from remote_control import calculate_speed_command, POLL_DELAY
import radio

# Configure radio
radio.on()
radio.config(group=23, power=5)

# Continuously read the sensors and send an updated speed command
while True:
    # TODO: Choose op mode (RC or car control)
    speed_command = calculate_speed_command()
    print(speed_command)
    radio.send(speed_command)
    sleep(POLL_DELAY)
