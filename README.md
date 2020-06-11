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
- Clone this repo
- Run `requirements.sh`
- Run `install.sh`
- Create a virtual environment: `virtualenv -p python3 .env `
- Activate the virtual environment: `source .env/bin/activate `
- Install python dependencies: `pip install -r requirements.txt `

## How to run:

- Run `python3 voice_assistant.py` for a single voice command
- Compile `mouseClickHandler.c` and run the executable for a voice command on every left mouse button click