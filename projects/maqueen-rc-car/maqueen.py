'''
Version: 2.0.1
@see https://github.com/DFRobot/pxt-DFRobot_MaqueenPlus_v20/blob/master/maqueenPlusV2.ts
'''
from micropython import const
from microbit import i2c, display, Image, pin13, pin14, pin15, accelerometer, compass
from machine import time_pulse_us
from time import sleep_ms

class Motor:
    LEFT = 0
    RIGHT = 1
    ALL = 2

class Direction:
    FORWARD = 0
    BACKWARD = 1

I2C_ADDR = const(0x10)
ADC0_REGISTER = const(0X1E)
ADC1_REGISTER = const(0X20)
ADC2_REGISTER = const(0X22)
ADC3_REGISTER = const(0X24)
ADC4_REGISTER = const(0X26)
LEFT_LED_REGISTER = const(0X0B)
RIGHT_LED_REGISTER = const(0X0C)
LEFT_MOTOR_REGISTER = const(0X00)
RIGHT_MOTOR_REGISTER = const(0X02)
LINE_STATE_REGISTER = const(0X1D)
VERSION_CNT_REGISTER = const(0X32)
VERSION_DATA_REGISTER = const(0X33)

_ULTRASONIC_PULSE_LENGTH_US = const(500*58)

_motor_calibration = [[], []]

def I2CInit():
    version_v = 0
    i2c.write(I2C_ADDR, bytearray([VERSION_CNT_REGISTER]))
    version_v = i2c.read(I2C_ADDR, 1) # read 1 byte
    while not version_v:
        display.show(Image('90009:09090:00900:09090:90009'))
        sleep_ms(500)
        display.clear()
        i2c.write(I2C_ADDR, bytearray([VERSION_CNT_REGISTER]))
        version_v = i2c.read(I2C_ADDR, 1) # read 1 byte
    display.show(Image('00000:00009:00090:90900:09000'))
    sleep_ms(500)
    display.clear()

def motor_calibration(motor: int, speed_factors: list):
    '''
    Maqueen robots tend to have different motor speeds.
    You can provide factors for different speeds to inter/extrapolate
    new speeds.
    ```
    motor_calibration(Motor.Right, [(20, 1.28), (200, 1.22)])
    ```
    '''
    if motor > 1:
        print('No motor index', motor, 'found. Calibration is ignored')
        return
    _motor_calibration[motor] = sorted(speed_factors, key=lambda x: x[0])

def motor_get_calibration(motor: int):
    '''
    Returns a copy of the calibration data for the given motor.
    ```
    motor_get_calibration(Motor.RIGHT) # => [(20, 1.28), (200, 1.22)]
    ```
    '''
    return [s for s in _motor_calibration[motor]]

def _get_speed(motor: int, speed: int):
    num_calibs = len(_motor_calibration[motor])
    if motor > 1 or num_calibs == 0:
        return speed
    elif num_calibs == 1:
        return int(_motor_calibration[motor][0][1] * speed)
    elif num_calibs == 2:
        calibs = _motor_calibration[motor]
        x1 = calibs[0][0]
        y1 = calibs[0][1]
        x2 = calibs[1][0]
        y2 = calibs[1][1]
        m = (y2 - y1) / (x2 - x1)
        factor = y1 + (speed - x1) * m
        return int(factor * speed)
    else:
        calibs = _motor_calibration[motor]
        bigger = [x for x in calibs if x[0] > speed]
        if len(bigger) > 0:
            cal2 = bigger[0]
        else:
            cal2 = calibs[-1]
        idx_cal2 = calibs.index(cal2)
        if idx_cal2 > 0:
            cal1 = calibs[idx_cal2 - 1]
        else:
            cal1 = cal2
            cal2 = calibs[idx_cal2 + 1]
        x1 = cal1[0]
        y1 = cal1[1]
        x2 = cal2[0]
        y2 = cal2[1]
        m = (y2 - y1) / (x2 - x1)
        factor = y1 + (speed - x1) * m
        return int(factor * speed)

def motor_run(motor: int, speed: int, dir: int = Direction.FORWARD):
    '''
    Run the motor on the given speed.
    speed: 0-255
    ```
    motor_run(Motor.ALL, speed=100, dir=Direction.Forward)
    ```
    '''
    if speed < 0:
        speed = -speed
        dir = Direction.FORWARD if dir == Direction.BACKWARD else Direction.BACKWARD

    if motor == Motor.LEFT:
        i2c.write(I2C_ADDR, bytearray([LEFT_MOTOR_REGISTER, dir, _get_speed(motor, speed)]))
    elif motor == Motor.RIGHT:
        i2c.write(I2C_ADDR, bytearray([RIGHT_MOTOR_REGISTER, dir, _get_speed(motor, speed)]))
    else:
        i2c.write(I2C_ADDR, bytearray([LEFT_MOTOR_REGISTER, dir, _get_speed(Motor.LEFT, speed), dir, _get_speed(Motor.RIGHT, speed)]))

def motor_stop(motor: int = Motor.ALL):
    '''
    Stop the motor.
    ```
    motor_stop() # => stop both motors
    motor_stop(Motor.LEFT) # => stop the left motor
    ```
    '''
    motor_run(motor, 0, 0)

def ultrasonic(trig = pin13, echo = pin14):
    '''
    Read the ultrasonic sensor.
    ```
    ultrasonic()
    ```
    '''
    trig.write_digital(1)
    sleep_ms(1)
    trig.write_digital(0)
    if echo.read_digital() == 0:
        trig.write_digital(0)
        trig.write_digital(1)
        sleep_ms(20)
        trig.write_digital(0)
        data = time_pulse_us(echo, 1, _ULTRASONIC_PULSE_LENGTH_US)
    else:
        trig.write_digital(1)
        trig.write_digital(0)
        sleep_ms(20)
        trig.write_digital(0)
        data = time_pulse_us(echo, 1, _ULTRASONIC_PULSE_LENGTH_US)
    data = data / 59
    if data <= 0:
        return 0
    elif data >= 500:
        return 500
    return round(data)

def version():
    '''
    Read the version of the board.
    ```
    version() # => string like 'MBT0021-EN-2.1'
    ```
    '''
    i2c.write(I2C_ADDR, bytearray([VERSION_CNT_REGISTER]))
    bytes_to_read = int(i2c.read(I2C_ADDR, 1)[0])
    i2c.write(I2C_ADDR, bytearray([VERSION_DATA_REGISTER]))
    version = i2c.read(I2C_ADDR, bytes_to_read)
    return version.decode('utf-8')
