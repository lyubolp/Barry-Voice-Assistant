#!/usr/bin/python3
import subprocess
import pathlib
import sys
import datetime
import time

# Expected order of arguments HH:MM WEEKDAY


def set_alarm(sleep_seconds: int):
    currentPath = str(pathlib.Path(__file__).parent.absolute())

    # Run in background
    subprocess.Popen([currentPath + '/timeout.sh', str(sleep_seconds)],
                     cwd="/",
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)


def calcualte_sleep(alarm_time):
    return (int)((alarm_time - datetime.datetime.now()).total_seconds())


def get_day_offset_from_today(day: str):
    difference = time.strptime(day, '%A').tm_wday - time.localtime().tm_wday
    if difference >= 0:
        return difference
    else:
        return 7 - abs(difference)


def calculate_alarm_time(weekday_offset: int, alarm_hour: int, alarm_minute: int):
    now = datetime.datetime.now()
    alarm_time = now.replace(hour=alarm_hour, minute=alarm_minute, second=0)
    alarm_time = alarm_time + datetime.timedelta(days=weekday_offset_days)
    if alarm_time < now:
        alarm_time = alarm_time + datetime.timedelta(days=7)
    return alarm_time


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Invalid arguments")
        exit(1)

    hourminutes = sys.argv[1]
    if len(sys.argv) >= 3:
        day = sys.argv[2]
    else:
        day = datetime.datetime.now().strftime('%A')

    try:
        datetime.datetime.strptime(day + " " + hourminutes, '%A %H:%M')
    except Exception:
        print("Invalid input")
        exit(1)

    weekday_offset_days = get_day_offset_from_today(day)

    hourminutes = hourminutes.split(':')
    hours = int(hourminutes[0])
    minutes = int(hourminutes[1])

    alarm_time = calculate_alarm_time(weekday_offset_days, hours, minutes)
    sleep_seconds = calcualte_sleep(alarm_time)

    set_alarm(sleep_seconds)
    print("Alarm set for " + day + " " + str(hours) + ":" + str(minutes))
