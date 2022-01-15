import time

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


if __name__ == '__main__':
    main()
