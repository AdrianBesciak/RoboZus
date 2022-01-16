import time
from arduino import *
import time
import board
from adafruit_motorkit import MotorKit

import speech_recognition as sr



# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        aud = recognizer.recognize_google(audio,language='pl-PL').lower()
        if aud!='Google Speech Recognition could not understand audio':
            print(aud)
            if "bułka" in aud:
                print("!!!!!")
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback,phrase_time_limit=10)


def wall_follower_main():
    arduino = Arduino('ttyUSB0')
    print(arduino.get_distances())

    kit = MotorKit(i2c=board.I2C())

    motor_left = kit.motor2
    motor_right = kit.motor1

    s0 = 0.0
    s1 = 0.05
    s2 = 0.07

    time.sleep(0.5)
    kit.motor1.throttle = 0

    right_measurement = 500
    front_measurement = 10000

    while True:
        distances = arduino.get_distances()
        for key, val in distances.items():
            if key == 'front':
                front_measurement = val
            elif key == 'right':
                right_measurement = val

        if front_measurement < 3000:
            motor_left.throttle = s1
            motor_right.throttle = s0
        elif right_measurement < 1500:
            motor_right.throttle = s2
            motor_left.throttle = s1
        else:
            motor_right.throttle = s1
            motor_left.throttle = s2


def stop_motors():
    kit = MotorKit(i2c=board.I2C())
    motor_left = kit.motor1
    motor_right = kit.motor2
    motor_left.throttle = 0.0
    motor_right.throttle = 0.0


if __name__ == '__main__':
    wall_follower_main()
