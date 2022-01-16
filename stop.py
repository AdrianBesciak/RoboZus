import board
from adafruit_motorkit import MotorKit

if __name__ == '__main__':
    kit = MotorKit(i2c=board.I2C())

    motor_left = kit.motor1
    motor_right = kit.motor2

    motor_left.throttle = 0.0
    motor_right.throttle = 0.0
