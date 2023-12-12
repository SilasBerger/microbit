# Maqueen RC Car
This project combines two Microbits and a Maqueen robot into an RC car setup with a gyroscopic remote control.

One Microbit acts as a car controller and is installed into the Maqueen robot, while the other one is used as the remote
control. The driver controls the throttle and steers the car by tilting the remote control forward and sideways,
respectively. The car controller receives the remote's speed commands via the radio module and uses them to control 
the speed of Maqueen's two motors. If it detects something having gone wrong, the car controller stops the motors,
enters a failsafe mode, and sounds and alarm.

## Usage
### Installation and setup
- Load the program in the [Python editor](https://python.microbit.org/v/3/project), e.g. by importing the hex file.
- Flash it onto **two** Microbits.
- Disable the motors on the Maqueen robot (toggle switch on the side) and turn it on. 
- Connect one Microbit to the Maqueen robot - this Microbit is now the _car controller_.
- Use the `A` button on the car controller to set it into `car controller` mode, indicated by a `C` on the screen.
- Connect the other Microbit to a battery pack (or leave it plugged into a USB port). This Microbit is now the _remote control_.
- Use the `A` button to set the remote control into `remote control: parking` mode, indicated by a `P` on the screen.
  - **Caution:** If the screen is showing a `D` instead of a `P`, press the `B` button once to switch from `driving` into `parking` mode.
- Enable the motors on the Maqueen robot (toggle switch on the side).

### Driving
After completing the installation and setup steps, the Maqueen RC car is now ready for driving.
- Hold the remote control upright, in landscape orientation, with the Microbit logo facing toward you. Tilt slightly toward yourself.
- Press the `B` button on the remote to switch from `parking` to `driving` mode, indicated by a `D` on the screen.
- Start tilting the remote control away from yourself to let the Maqueen drive forward. Tilt sideways to steer.

## Troubleshooting
### Failsafe
The car controller has a built-in failsafe mode, which is triggered whenever there is a problem. Engaging the failsafe
mode stops all motors and causes all speed update commands to be ignored, until the init routine is run again.

To exit the failsafe mode, use the `B` button on the remote to first switch to `parking` mode (`P`) and then back to
`driving` mode (`D`). 

### Alarms
If something goes wrong, the car controller sounds an alarm, usually indicating that the failsafe mode has been
engaged. This section discusses the possible alarm tones and their meaning.

**System error,** _marked by a siren of six tones in three pairs of tritones_. Think of it as a 5xx-class HTTP status
code: if that happens, blame the developer. Possible reasons could be that the remote sent an unrecognized command, that
a command was interpreted as a speed update but didn't match the required format, or that some other exception has
ocurred.

**Driver error,** _marked by three ascending warning tones_. Think of it as a 4xx-class HTTP status code: if that
happens, blame the driver.
