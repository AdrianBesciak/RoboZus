from RPi import GPIO
from time import sleep


class MotorDriver:
    def __init__(self, pwm_pin, forward_pin, reversed_pin):
        self.__pwm_pin = pwm_pin         # ENx - H-bridge enable pin
        self.__forward_pin = forward_pin     # IN1 - Forward Drive
        self.__reversed_pin = reversed_pin    # IN2 - Reverse Drive
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)    #standby pin
        GPIO.output(26, GPIO.HIGH)
        GPIO.setup(self.__pwm_pin, GPIO.OUT)
        GPIO.setup(self.__forward_pin, GPIO.OUT)
        GPIO.setup(self.__reversed_pin, GPIO.OUT)
        GPIO.output(self.__forward_pin, GPIO.LOW)
        GPIO.output(self.__reversed_pin, GPIO.LOW)
        self.__pwm_channel = GPIO.PWM(self.__pwm_pin, 1000)

    # negative speed value means driving back
    def spin(self, speed):
        if speed < 0:
            GPIO.output(self.__forward_pin, GPIO.LOW)
            GPIO.output(self.__reversed_pin, GPIO.HIGH)
            self.__pwm_channel.start(-1 * speed)
        else:
            GPIO.output(self.__forward_pin, GPIO.HIGH)
            GPIO.output(self.__reversed_pin, GPIO.LOW)
            self.__pwm_channel.start(speed)

    def brake(self):
        GPIO.output(self.__forward_pin, GPIO.HIGH)
        GPIO.output(self.__reversed_pin, GPIO.HIGH)
        self.__pwm_channel.stop()

    def stop(self):
        GPIO.output(self.__forward_pin, GPIO.LOW)
        GPIO.output(self.__reversed_pin, GPIO.LOW)
        self.__pwm_channel.stop()
