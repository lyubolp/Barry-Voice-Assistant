FROM debian:buster
RUN apt-get -y update && apt-get upgrade -y
RUN apt-get -y install sudo git python3 python3-pip pkg-config libcairo2-dev libjpeg-dev libgif-dev libapt-pkg-dev python3-distutils-extra unattended-upgrades python-dnspython
COPY ./requirements.txt /barry-voice-assistant/server/requirements.txt
WORKDIR /barry-voice-assistant/server
RUN pip3 install -r /barry-voice-assistant/server/requirements.txt
COPY . /barry-voice-assistant/server
RUN echo 'mongodb_key=<--MONGODB_URI-->\njwt_secret=mysecretfortokens' > /barry-voice-assistant/server/server.conf
RUN echo 'city=Londontemperature=Celsius\ndefault_response=Sorry, I could not understand\nweather_api_key=<--WEATHER_API_KEY-->\nnews_api_key=<--NEWS_API_KEY-->' > /barry-voice-assistant/server/defaults.conf
EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["/barry-voice-assistant/server/server.py"]
