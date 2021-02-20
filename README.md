# Barry voice assistant

![Logo](https://raw.githubusercontent.com/lyubolp/Barry-Voice-Assistant/master/logo.png)

​	Barry is a voice assistant which can help you with your everyday tasks. It's focus is on privacy, usability and extensibility. It is written in Python, and it's modular architecture allows for the user to write his own actions, in order to customize Barry according to his personal needs. The voice assistant can run headless on a Raspberry Pi board (hence the name - Barry). 

[Demo](https://youtu.be/Amy10VUfTcE)

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

1. Set up a (MongoDB)[https://www.mongodb.com/] cluster. You will need the credentials to access this server, which we'll call `MONGODB_URI`. Create a database `barry` and inside create a `users` collection(table). The `users` collection needs to have 3 fields:
    - email (create an index on this field)
    - password
    - config
2. Check the credentials section below to acquire the necessary keys. The keys you will need are:
    - `GOOGLE_KEY` from (Google)[https://console.cloud.google.com/apis/library/speech.googleapis.com] cloud for text-to-speech and speech-to-text
    - `WEATHER_API_KEY` from (Openweather)[https://openweathermap.org/]
    - `NEWS_API_KEY` from (NewsAPI)[https://newsapi.org/]
3. Clone this repository - `git clone https://github.com/lyubolp/Barry-Voice-Assistant.git`
4. Replace the placeholders for `<--MONGODB_URI-->`, `<--WEATHER_API_KEY-->`, `<--NEWS_API_KEY-->` inside server/Dockerfile with the keys you acquired in step 2.
5. Run the server docker container and get its IP, which we'll call `SERVER_URL`.
6. Replace the placeholders for `<--SERVER_URL-->`, `<--GOOGLE_KEY-->` inside frontend/Dockerfile with the keys you acquired in step 2 and the IP address you acquired from step 5.
7. Run the frontend docker container and you should be able to access the Barry website with the container's IP.

## Credentials:

Some service require credentials or API keys in order for them to be used:

- Google Speech-to-text (here)[https://console.cloud.google.com/apis/library/speech.googleapis.com] - enable the API, then click `Manage`, then `Credentials`, then create a `Service account`. Save the credentials as `google_credentials.json` in the directory `<project_folder>/speech_to_text`
- Weather API - (here)[https://openweathermap.org/]. After you get the key, place it in a file called `api_key` in the following directory: `<project_folder>/actions/weather`
- News API - (here)[https://newsapi.org/] After you get the key, place it in a file called `api_key` in the following directory: `<project_folder>/actions/news`
- Google Calendar - (here)[https://developers.google.com/calendar/quickstart/python] - copy the file `credentials.json` to the following directories `<project_folder>/actions/googleCalendarAddEvent` and `<project_folder>/actions/googleCalendarGetAgenda`

## How to run:

- Run `python3 voice_assistant.py` for a single voice command
- Compile `mouseClickHandler.c` and run the executable for a voice command on every left mouse button click
