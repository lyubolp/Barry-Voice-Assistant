#!/bin/bash

# Input is <seconds-to-timeout> <message>

tts="$(dirname $0)/../../text-to-speech/relative-tts.py"

seconds="$1"

now="$(date '+%A, %d %B %H:%M')"

sleep $seconds && python3 $tts "Reminder. $2" &
