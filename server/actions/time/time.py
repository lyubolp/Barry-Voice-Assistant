#!/usr/bin/python3
import datetime
import inflect
import json
import sys
from pytz import timezone


def execute_action(timezone_str):
    try:
        local_timezone = timezone(timezone_str)
        time = datetime.datetime.now(local_timezone).time()
    except:
        return json.dumps({'error': 'Invalid timezone ' + timezone_str})
        
    hours = time.hour
    minutes = time.minute

    p = inflect.engine()
    time_words = p.number_to_words(hours) + " " + p.number_to_words(minutes)
    message = "The time is " + time_words

    hours = str(hours)
    if len(hours) == 1:
        hours = '0' + hours
    minutes = str(minutes)
    if len(minutes) == 1:
        minutes = '0' + minutes
    time_numeric = hours + ':' + minutes

    return json.dumps({'message': ''.join(message), 'details': {'time_numeric': time_numeric, 'time_words': time_words}})

if __name__ == '__main__':
    timezone_str = 'UTC'
    if len(sys.argv) == 2:
        timezone_str = sys.argv[1]
    print(execute_action(timezone_str))
