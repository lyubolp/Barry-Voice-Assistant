# daemon must be started in order to install the actions

python3 daemon/barryd.py add weather actions/weather/weather.py
chmod +x actions/weather/weather.py

python3 daemon/barryd.py add joke actions/joke/joke.py
chmod +x actions/joke/joke.py

python3 daemon/barryd.py add what_is actions/whatIs/what_is.py
chmod +x actions/whatIs/what_is.py

python3 daemon/barryd.py add time actions/time/time.py
chmod +x actions/time/time.py

python3 daemon/barryd.py add news actions/news/news.py
chmod +x actions/news/news.py

python3 daemon/barryd.py add todo actions/todo/todo.py
chmod +x actions/todo/todo.py

python3 daemon/barryd.py add alarm actions/alarm/alarm.py
chmod +x actions/alarm/alarm.py

python3 daemon/barryd.py add reminder actions/reminder/reminder.py
chmod +x actions/reminder/reminder.py

python3 daemon/barryd.py add timer actions/timer/timer.py
chmod +x actions/timer/timer.py