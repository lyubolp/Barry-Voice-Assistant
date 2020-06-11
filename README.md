# Barry voice assistant

![Logo](https://raw.githubusercontent.com/lyubolp/Barry-Voice-Assistant/master/logo.png)

​	Barry is a voice assistant which can help you with your everyday tasks. It's focus is on privacy, usability and extensibility. It is written in Python, and it's modular architecture allows for the user to write his own actions, in order to customize Barry according to his personal needs. The voice assistant can run headless on a Raspberry Pi board (hence the name - Barry). 

​	Barry is built on the following technologies:

- (Google Speech-To-Text)[https://cloud.google.com/speech-to-text] (for speech recognition)
- [Adapt Intent Parser](https://github.com/MycroftAI/adapt) (used for linking voice commands with actions)
- [Mimic1 Text-To-Speech engine](https://github.com/MycroftAI/mimic1) (the voice of Barry)

## Examples for voice commands

- `weather in Sofia ` (requires an API key from https://openweathermap.org)
- `weather` (if you have configured your location)
- `tell me a joke`
- `what is Ferrari`
- `tell me the latest news about Bulgaria` (requires an API key from https://newsapi.org/)
- `what time is it`
- `add milk to my shopping list` (remove works as well)
- `tell me my shopping list`
- `clear my shopping list`
- `set an alarm for 8:30`
- `set an alarm for 8:30 on Monday`
- `remind me to stop the oven in 10 minutes ` 
- `set a timer for 30 seconds` 


## How to setup:
- Clone this repository - `git clone https://github.com/lyubolp/Barry-Voice-Assistant.git`
- Go into the Barry-Voice-Assistant directory
- Run `requirements.sh` with root privileges 
- Create a virtual environment: `virtualenv -p python3 .env `
- Activate the virtual environment: `source .env/bin/activate `
- Install python dependencies: `pip install -r requirements.txt `
- Install `systemd` as global python dependency `sudo pip3 install systemd`
- Run `install.sh` with root privileges

## Credentials:

Some service require credentials or API keys in order for them to be used:

- Google Speech-to-text (here)[https://console.cloud.google.com/apis/library/speech.googleapis.com] - enable the API, then click `Manage`, then `Credentials`, then create a `Service account`. Save the credentials as `google_credentials.json` in the directory `<project_folder>/speech_to_text`
- Weather API - (here)[https://openweathermap.org/]. After you get the key, place it in a file called `api_key` in the following directory: `<project_folder>/actions/weather`
- News API - (here)[https://newsapi.org/] After you get the key, place it in a file called `api_key` in the following directory: `<project_folder>/actions/news`
- Google Calendar - (here)[https://developers.google.com/calendar/quickstart/python] - copy the file `credentials.json` to the following directories `<project_folder>/actions/googleCalendarAddEvent` and `<project_folder>/actions/googleCalendarGetAgenda`

## How to run:

- Run `python3 voice_assistant.py` for a single voice command
- Compile `mouseClickHandler.c` and run the executable for a voice command on every left mouse button click