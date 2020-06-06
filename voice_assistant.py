import subprocess

from intents import determine_intent
from speech_to_text import speech_to_text

DEFAULT_TEXT_TO_SAY = "Sorry, I could not understand"


def speak(output: str):
    subprocess.run(['python3', 'text-to-speech/tts.py', output])


def execute_weather_action(weather_intent) -> bool:
    process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'weather_api_key'],
                             stdout=subprocess.PIPE)
    weather_api_key = process.stdout.decode('utf-8').rstrip()
    if weather_api_key == '':
        try:
            with open('actions/weather/api_key') as f:
                weather_api_key = f.read()
        except FileNotFoundError:
            speak("You do not have a weather API key")
            return True

    city = weather_intent.get('Location')
    if city is None:
        process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'city'],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        if output != '':
            city = output
        else:
            speak("No location is specified")
            return True

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'weather', weather_api_key, city],
                             stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True


def execute_joke_action() -> bool:
    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'joke'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True


def execute_what_is_action(what_is_intent) -> bool:
    subject = what_is_intent.get('Subject')
    if subject is None:
        return False

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'what_is', subject], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True


def execute_time_action() -> bool:
    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'time'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True


def execute_news_action(news_intent) -> bool:
    process = subprocess.run(['python3', 'daemon/barryd.py', 'config', 'get', 'news_api_key'],
                             stdout=subprocess.PIPE)
    news_api_key = process.stdout.decode('utf-8').rstrip()
    if news_api_key == '':
        try:
            with open('actions/news/api_key') as f:
                news_api_key = f.read()
        except FileNotFoundError:
            speak("You do not have a news API key")
            return True

    topic = news_intent.get('Topic')
    if topic is not None:

        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'news', news_api_key, topic],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()

        speak(output)
        return True
    else:
        speak('Please provide a topic')
        return True


if __name__ == "__main__":
    text = speech_to_text.recognize(speech_to_text.get_audio(save=False))
    print(text)
    if text is None:
        speak(DEFAULT_TEXT_TO_SAY)
        exit(0)

    # The daemon has to be started in order to execute a command
    intent = determine_intent(text)
    success = False
    if intent is None:
        pass
    elif intent.get('intent_type') == 'WeatherIntent':
        success = execute_weather_action(intent)
    elif intent.get('intent_type') == 'JokeIntent':
        success = execute_joke_action()
    elif intent.get('intent_type') == 'WhatIsIntent':
        success = execute_what_is_action(intent)
    elif intent.get('intent_type') == 'TimeIntent':
        success = execute_time_action()
    elif intent.get('intent_type') == 'NewsIntent':
        success = execute_news_action(intent)

    if not success:
        speak(DEFAULT_TEXT_TO_SAY)
