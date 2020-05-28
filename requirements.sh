# apt-installs

apt-get install gcc make pkg-config automake libtool libasound2-dev git curl python3 pip3 -y;

# add scripts to the daemon

python3 daemon/barryd.py start

python3 daemon/barryd.py add weather actions/weather/weather.py
chmod +x actions/weather/weather.py

python3 daemon/barryd.py add joke actions/joke/joke.py
chmod +x actions/joke/joke.py

python3 daemon/barryd.py add what_is actions/whatIs/what_is.py
chmod +x actions/whatIs/what_is.py

python3 daemon/barryd.py stop