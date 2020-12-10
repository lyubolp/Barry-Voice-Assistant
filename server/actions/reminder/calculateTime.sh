#!/bin/bash

# Input is SECONDS MINUTES HOURS DAYS

tts="$(dirname $0)/../../text-to-speech/relative-tts.py"

seconds=0
timeStr=""

if [ $(echo "$1" | grep -P "^\d+$" -c) -eq 1 ]; then
    seconds="$(($seconds + $1))"
    if [ "$1" == "1" ]; then
        timeStr="$1 second"
    elif [ "$1" != "0" ]; then
        timeStr="$1 seconds"
    fi
fi

if [ $(echo "$2" | grep -P "^\d+$" -c) -eq 1 ]; then
    seconds="$(($seconds + $2 * 60))"
    if [ "$2" == "1" ]; then
        timeStr="$2 minute $timeStr"
    elif [ "$2" != "0" ]; then
        timeStr="$2 minutes $timeStr"
    fi
fi

if [ $(echo "$3" | grep -P "^\d+$" -c) -eq 1 ]; then
    seconds="$(($seconds + $3 * 60 * 60))"
    if [ "$3" == "1" ]; then
        timeStr="$3 hour $timeStr"
    elif [ "$3" != "0" ]; then
        timeStr="$3 hours $timeStr"
    fi
fi

if [ $(echo "$4" | grep -P "^\d+$" -c) -eq 1 ]; then
    seconds="$(($seconds + $4 * 60 * 60 * 24))"
    if [ "$4" == "1" ]; then
        timeStr="$4 day $timeStr"
    elif [ "$4" != "0" ]; then
        timeStr="$4 days $timeStr"
    fi
fi

if [ "$timeStr" ]; then
    echo "$seconds:Reminder set for $timeStr"
else
    echo "Invalid reminder parameters"
    exit 1
fi
