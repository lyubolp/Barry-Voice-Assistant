#!/usr/bin/python3
import datetime
import inflect
import json


def execute_action():
    time = datetime.datetime.now().time()
    hour = time.hour
    minutes = time.minute

    p = inflect.engine()
    time_words = p.number_to_words(hour) + " " + p.number_to_words(minutes)
    message = "The time is " + time_words
    time_numeric = str(hour) + ':' + str(minutes)
    return json.dumps({'message': ''.join(message), 'details': {'time_numeric': time_numeric, 'time_words': time_words}})

if __name__ == '__main__':
    print(execute_action())
