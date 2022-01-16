import time

import speech_recognition as sr

import cv2

import random

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

init()

cap = cv2.VideoCapture(0)

def save_frame():
    ret,frame=cap.read()
    cv2.imwrite('saved/delikwent.png',frame)

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    print("Listening")
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        aud = recognizer.recognize_google(audio,language='pl-PL').lower()
        if aud!='Google Speech Recognition could not understand audio':
            print(aud)
            if ("mama" in aud) or ("bułka" in aud):
                print("!!!!!")
                save_frame()
                publish()
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    r = sr.Recognizer()
    m = sr.Microphone(2)
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback,phrase_time_limit=5)

    while True:
        ret,frame=cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
    cap.release()
    stop_listening(wait_for_stop=False)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
