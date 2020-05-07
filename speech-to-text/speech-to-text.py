import speech_recognition as sr

from datetime import datetime

AUDIO_SAVE_DIR = "speech-to-text/audio"
GOOGLE_CREDENTIALS_PATH = "speech-to-text/google_credentials.json"


def get_google_credentials():
    with open(GOOGLE_CREDENTIALS_PATH) as f:
        credentials = f.read()

    return credentials


def get_audio(timeout=5, phrase_time_limit=5):
    """
    Records audio and returns it as an instance of type AudioData.
    Saves the recorded audio locally in directory AUDIO_SAVE_DIR.

    :param int timeout: The maximum number of seconds that this will wait for a phrase to start before giving up.
    :param int phrase_time_limit: The maximum number of seconds that this will allow a phrase to continue before
    stopping and returning the part of the phrase processed before the time limit was reached.

    :return: The audio data or None if there was a problem while listening.

    This operation will always complete within timeout + phrase_time_limit seconds.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout, phrase_time_limit)
        except sr.WaitTimeoutError as e:
            print("Failed to record audio: {0}".format(e))
            return None

    file_name = datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ".wav"

    # Write the recorded audio to a file
    with open(AUDIO_SAVE_DIR + "/" + file_name, "wb") as f:
        f.write(audio.get_wav_data())

    return audio


def recognize(audio):
    r = sr.Recognizer()

    credentials = get_google_credentials()

    try:
        return r.recognize_google_cloud(audio, credentials_json=credentials)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return None


if __name__ == '__main__':
    result = recognize(get_audio())

    if result is not None:
        print("Google Cloud Speech thinks you said " + result)
