import json

import speech_recognition as sr

GOOGLE_CREDENTIALS_PATH = "speech-to-text/google_credentials.json"


def get_google_credentials():
    with open(GOOGLE_CREDENTIALS_PATH) as google_credentials:
        credentials = json.load(google_credentials)

    return credentials


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, 5, 5)

    return audio


def recognize(audio):
    r = sr.Recognizer()

    credentials = get_google_credentials()

    try:
        print("Google Cloud Speech thinks you said " +
              r.recognize_google_cloud(audio, credentials_json=json.dumps(credentials)))
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))


if __name__ == '__main__':
    audio = get_audio()
    recognize(audio)