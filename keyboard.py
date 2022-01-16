from pynput import keyboard
import board
from adafruit_motorkit import MotorKit


import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "pl/bitehack/nc"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
client = None

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish():
    msg_count = 0
    msg = "1"
    result = client.publish(topic, msg)
    #result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1


def init():
    global client
    client = connect_mqtt()
    client.loop_start()
    # publish(client)

kit = MotorKit(i2c=board.I2C())

motor_left = kit.motor2
motor_right = kit.motor1

init()

def on_press(key):
    try:
        print('Alphanumeric key pressed: {0} '.format(
            key.char))
    except AttributeError:
        print('special key pressed: {0}'.format(
            key))
    if key == keyboard.Key.down:
        motor_left.throttle = -1.0
        motor_right.throttle = -1.0
    elif key == keyboard.Key.up:
        motor_left.throttle = 1.0
        motor_right.throttle = 1.0
    elif key == keyboard.Key.left:
        motor_left.throttle = 1.0
        motor_right.throttle = 0.0
    elif key == keyboard.Key.right:
        motor_left.throttle = 0.0
        motor_right.throttle = 1.0
    elif key == keyboard.Key.media_play_pause:
        publish()




def on_release(key):
    motor_left.throttle = 0.0
    motor_right.throttle = 0.0
    print('Key released: {0}'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()