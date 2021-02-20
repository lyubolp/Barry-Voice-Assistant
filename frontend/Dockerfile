FROM debian:buster
RUN apt-get -y update && apt-get upgrade -y
RUN apt-get -y install sudo git python3 python3-pip
COPY ./requirements.txt /barry-voice-assistant/frontend/requirements.txt
WORKDIR /barry-voice-assistant
RUN pip3 install -r /barry-voice-assistant/frontend/requirements.txt
COPY . /barry-voice-assistant/frontend
RUN echo 'server_url=<--SERVER_URL-->' > frontend/client/client.conf
RUN echo 'import os' > ./frontend/config.py
RUN echo '\n' >> ./frontend/config.py
RUN echo "class Config(object):" >> ./frontend/config.py
RUN echo "\tSECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'" >> ./frontend/config.py
RUN echo "\t<--GOOGLE_KEY--> = r'keys/stunning-crane-297410-39248a86fcd0.json'" >> ./frontend/config.py
RUN mkdir ./frontend/keys
RUN echo '{' > ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"type": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"project_id": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"private_key_id": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"private_key": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"client_email": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"client_id": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"auth_uri": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"token_uri": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"auth_provider_x509_cert_url": "<--GOOGLE_KEY-->",' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '"client_x509_cert_url": "<--GOOGLE_KEY-->"' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN echo '}' >> ./frontend/keys/stunning-crane-297410-39248a86fcd0.json
RUN mkdir ./frontend/static/audio
WORKDIR /barry-voice-assistant/frontend
ENV FLASK_APP=app
ENV FLASK_ENV=development
EXPOSE 80
ENTRYPOINT ["python3"]
CMD ["app.py"]
