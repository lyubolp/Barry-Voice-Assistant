from intents import determine_intent
from typing import Dict, List
from configs import ACTIONS
import os
import subprocess
import json

def execute_command(text: str, args: Dict[str, str]):
    if text is None:
        raise Exception("Invalid command")

    # The daemon has to be started in order to execute a command
    intent = determine_intent(text)

    if intent is None:
        raise Exception("Could not recognize command")

    intent_type = intent.get('intent_type')
    if intent_type == 'WeatherIntent':
        return execute_weather_action(intent, args)
    elif intent_type == 'JokeIntent':
        return execute_joke_action()
    elif intent_type == 'WhatIsIntent':
        return execute_what_is_action(intent)
    elif intent_type == 'TimeIntent':
        return execute_time_action()
    elif intent_type == 'NewsIntent':
        return execute_news_action(intent, args)
    elif intent_type == 'TodoIntent':
        return execute_todo_action(intent)
    elif intent_type == 'AlarmIntent':
        return execute_alarm_action(intent)
    elif intent_type == 'ReminderIntent':
        return execute_reminder_action(intent)
    elif intent_type == 'TimerIntent':
        return execute_timer_action(intent)
    elif intent.get('intent_type') == 'AgendaIntent':
        return execute_agenda_action(intent)
    elif intent.get('intent_type') == 'AddEventIntent':
        return execute_add_event_action(text)


def _execute(action, args: List[str] = [], named_args: Dict[str, str] = {}) -> str:

    # TODO Handle arguments

    if action in ACTIONS:
        path = ACTIONS[action]['path']
    else:
        raise KeyError('Action not found')

    current_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
    full_path = current_dir + 'actions/' + path

    fileStat = os.stat(full_path)
    sudo = ['sudo', '-u', '#' + str(fileStat.st_uid)]
    executable = [full_path] + args
    out = subprocess.Popen(sudo + executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    stdout = stdout.decode('utf-8').strip()

    try:
        response = json.loads(stdout)
    except:
        return stdout, {}, action

    if 'error' in response:
        raise Exception(response['error'])
    elif 'message' in response and 'details' in response:
        return response['message'], response['details'], action
    else:
        raise Exception("Invalid response from action")


def execute_weather_action(weather_intent, args):
    if 'weather_api_key' not in args:
        raise Exception("You do not have a weather API key")
    weather_api_key = args['weather_api_key']

    city = weather_intent.get('Location')
    if city is None and 'city' not in args:
        raise Exception("No location is specified")
    if city is None:
        city = args['city']

    return _execute('weather', [weather_api_key, city])


def execute_joke_action():
    return _execute('joke')


def execute_what_is_action(what_is_intent):
    subject = what_is_intent.get('Subject')
    if subject is None:
        raise Exception("No subject specified")

    return _execute('what_is', [subject])


def execute_time_action():
    return _execute('time')


def execute_news_action(news_intent, args):
    if 'news_api_key' not in args:
        raise Exception("You do not have a news API key")
    news_api_key = args['news_api_key']

    topic = news_intent.get('Topic')
    if topic is None and 'topic' not in args:
        raise Exception("No topic is specified")
    if topic is None:
        topic = args['topic']

    return _execute('news', [news_api_key, topic])


def execute_todo_action(todo_intent):
    action = todo_intent.get('TodoCommand')
    list_type = todo_intent.get('ListType')

    storage_path = os.getcwd() + "/actions/todo/lists.json"
    if action == 'add' or action == 'remove':
        item = todo_intent.get('Item')

        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', action, list_type, item, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    elif action == 'get' or action == 'tell me':
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', 'get', list_type, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    elif action == 'clear':
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'todo', action, list_type, storage_path],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    else:
        speak("Unknown action")


def execute_alarm_action(alarm_intent):
    time = alarm_intent.get('Time')
    weekday = alarm_intent.get('Weekday')

    pattern = re.compile(r'(\d\d?)[: ](\d\d)')
    match = pattern.search(time)
    if match is None:
        speak("Please specify time and day for the alarm")
        return

    hours = match.group(1)
    minutes = match.group(2)

    if weekday is None:
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'alarm', hours, minutes],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)
    else:
        process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'alarm', hours, minutes, weekday],
                                 stdout=subprocess.PIPE)
        output = process.stdout.decode('utf-8').rstrip()
        speak(output)


def execute_reminder_action(reminder_intent):
    action = reminder_intent.get('Action')

    tokens = reminder_intent.get('Time').split(' ')
    seconds, minutes, days, hours = '0', '0', '0', '0'

    for i, token in enumerate(tokens):
        if token == 'seconds':
            seconds = tokens[i - 1]
        elif token == 'minutes':
            minutes = tokens[i - 1]
        elif token == 'hours':
            hours = tokens[i - 1]
        elif token == 'days':
            days = tokens[i - 1]

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'reminder', seconds, minutes, hours, days, action],
                             stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()
    speak(output)


def execute_timer_action(timer_intent):
    tokens = timer_intent.get('Time').split(' ')
    seconds, minutes, days, hours = '0', '0', '0', '0'

    for i, token in enumerate(tokens):
        if token == 'seconds':
            seconds = tokens[i - 1]
        elif token == 'minutes':
            minutes = tokens[i - 1]
        elif token == 'hours':
            hours = tokens[i - 1]
        elif token == 'days':
            days = tokens[i - 1]

    process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'timer', seconds, minutes, hours, days],
                             stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()
    speak(output)


def execute_agenda_action(agenda_intent) -> bool:
    process = subprocess.run(['python3', 'daemon/barryd.py',
                              'exec', 'read-google-calendar'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True


def execute_add_event_action(input) -> bool:
    event_name_re = re.search(
        'called (?P<event_name>.+?)(?=from|to|at|on|until)', input)
    location_re = re.search(
        'at (?P<location>[a-zA-Z0-9 ]+?)(?=from|to|at|on|until)', input)
    start_date_re = re.search(
        '(on the)(?<!until the) ((?P<start_date>\d+?)(?=st|nd|rd|th))', input)
    start_time_re = re.search(
        'at (?P<start_time>([0-9]{1,4}:?[0-9]{0,2} ?(p\.m\.|a\.m\.)?)).*', input)
    end_date_re = re.search(
        '(until the) ((?P<end_date>\d+?)(?=st|nd|rd|th))', input)
    end_time_re = re.search(
        '(?<=until the \d{2}(st|nd|rd|th) of) \w*? at (?P<end_time>([0-9]{1,4}:?[0-9]{0,2} ?(p\.m\.|a\.m\.)?))', input)

    event_name = event_name_re.groupdict()['event_name']

    if location_re.groupdict()['location'] is not None:
        location = location_re.groupdict()['location']
        start_date = start_date_re.groupdict()['start_date']
        end_date = end_date_re.groupdict()['end_date']
        if start_time_re.groupdict()['start_time'] is not None:
            start_time = start_time_re.groupdict()['start_time']
            end_time = end_time_re.groupdict()['end_time']
            process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'add-event', event_name, location,
                                      start_date, start_time, end_date, end_time],
                                     stdout=subprocess.PIPE)
        else:
            process = subprocess.run(
                ['python3', 'daemon/barryd.py', 'exec', 'add-event', event_name, location, start_date,
                 end_date],
                stdout=subprocess.PIPE)
    else:
        start_date = start_date_re.groupdict()['start_date']
        end_date = end_date_re.groupdict()['end_date']
        if start_time_re.groupdict()['start_time'] is not None:
            start_time = start_time_re.groupdict()['start_time']
            end_time = end_time_re.groupdict()['end_time']
            process = subprocess.run(['python3', 'daemon/barryd.py', 'exec', 'add-event', event_name,
                                      start_date, start_time, end_date, end_time],
                                     stdout=subprocess.PIPE)
        else:
            process = subprocess.run(
                ['python3', 'daemon/barryd.py', 'exec', 'add-event', event_name, start_date,
                 end_date],
                stdout=subprocess.PIPE)

    output = process.stdout.decode('utf-8').rstrip()

    speak(output)
    return True
