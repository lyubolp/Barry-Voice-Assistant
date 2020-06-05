#!/usr/bin/python3
import datetime
import inflect


def execute_action():
    time = datetime.datetime.now().time()
    hour = time.hour
    minutes = time.minute

    p = inflect.engine()
    return "The time is " + p.number_to_words(hour) + " " + p.number_to_words(minutes)


if __name__ == '__main__':
    print(execute_action())
