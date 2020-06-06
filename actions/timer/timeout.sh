#!/bin/bash

# Input is <seconds-to-timeout>

tts="$(dirname $0)/../../text-to-speech/relative-tts.py"

seconds="$1"

now="$(date '+%A, %d %B %H:%M')"

nohup sleep $seconds && python3 $tts "Timer from $now o'clock ran out" &!
