from hashlib import sha256

from flask import Flask, render_template, flash, redirect, request, url_for, make_response, send_file
from flask_login import LoginManager, current_user, login_user

from client.client import register, login, execute_command
from config import Config
from client import client

from news import News
from user import User
from weather import Weather
from whatIs import WhatIs

import os
import random
import string
from google.cloud import speech
from google.cloud import texttospeech
import requests
import json


app = Flask(__name__)
app.config.from_object(Config)


def isUserLoggedIn() -> bool:
    return not request.cookies.get('userToken') is None and request.cookies.get('userToken') != 'None'


@app.route('/')
@app.route('/index')
def index():
    if isUserLoggedIn():
        token = request.cookies.get('userToken')
        user = {
            'username': request.cookies.get('username')
        }
    else:
        user = None

    return render_template('index.html', title='Home', user=user)


@app.route('/audio/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_file('static/audio/' + filename)


@app.route('/speech_to_text/', methods=['POST'])
def speech_to_text():
    try:
        # move to config file?
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config['GOOGLE_KEY']

        try:
            file = request.files['audio_data']
            content = file.read()

            client = speech.SpeechClient()

            audio = speech.RecognitionAudio(content = content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code="en-US",
            )

            response = client.recognize(config = config, audio = audio)

            for result in response.results:
                result = result.alternatives[0].transcript
                print("Transcript: {}".format(result))
                return result

            return "ERROR: Google failed to transcribe!"

        except Exception as err:
            print("Failed to transcribe audio:")
            print(err)

    except Exception as err:
        print("Failed to get google api credentials:")
        print(err)

def text_to_speech(text: str) -> str:
    try:
        # move to config file?
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config['GOOGLE_KEY']

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text = text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        filename = "audio/output" + rand + ".mp3"

        with open("static/" + filename, "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file: ' + filename)

    except Exception as err:
        print("Failed to get google api credentials:")
        print(err)
        
    return filename


@app.route('/action_handler', methods=["POST"])
def action_handler():
    try:
        if isUserLoggedIn():
            token = request.cookies.get('userToken')
        else:
            return redirect(url_for(login))

        transcribed_text = request.form["recognized_string"]

        if transcribed_text == "ERROR: Google failed to transcribe!":
            return redirect('/')

        # transcribed_text = "news about sports"

        response = client.execute_command(token, transcribed_text)
        
        target_url = response['action']

        # For local testing, 127.0.0.1:5000
        return requests.post('https://0.0.0.0:80/' + target_url, json = response).text

    except Exception as err:
        print(err)
        return redirect('/')


@app.route('/news', methods=['POST'])
def news():

    response = request.json['details']
    news_objects = []
    for news_piece in response:
        news_objects.append(News(news_piece))

    audio_file = text_to_speech(request.json['message'])
    return render_template('news.html', title='News', news=news_objects, audio_file = audio_file)


@app.route('/what_is', methods=['POST'])
def what_is():
    response = request.json['details']
    article = WhatIs(response)

    audio_file = text_to_speech(response['content'])
    return render_template('what-is.html', title='What is ?', article=article, audio_file = audio_file)


@app.route('/login')
def loginPath():
    if isUserLoggedIn():
        return redirect('/')
    else:
        return render_template("login.html")


@app.route('/handle-login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    try:
        token = login(username, password)
    except Exception as err:
        user_friendly_errors = [error for error_list in err.args for error in error_list]
        return render_template('login.html', errors=user_friendly_errors)

    resp = make_response(redirect('/'))
    resp.set_cookie('userToken', token)
    resp.set_cookie('username', username)
    return resp


@app.route('/register')
def registerPath():
    if isUserLoggedIn():
        return redirect('/')
    else:
        return render_template("register.html")


@app.route('/logout')
def logout():
    if request.cookies.get('userToken') is not None:
        resp = make_response(redirect('/'))
        resp.set_cookie('userToken', "None", expires=0)

    return resp


@app.route('/handle-register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    password_repeat = request.form['passwordRepeat']

    if password == password_repeat:
        try:
            token = register(username, password)
        except Exception as err:
            user_friendly_errors = [error for error_list in err.args for error in error_list]
            return render_template('register.html', errors=user_friendly_errors)

        resp = make_response(redirect('/'))
        resp.set_cookie('userToken', token)
        resp.set_cookie('username', username)
        return resp
    else:
        return render_template('register.html', errors=['Passwords don\'t match'])


@app.route('/weather', methods=['POST'])
def weather():
    response = request.json['details']
    weather = Weather(response)
    print(request.json)
    audio_file = text_to_speech(request.json['message'])
    return render_template("weather.html", weather=weather, audio_file=audio_file)


@app.route('/joke', methods=['POST'])
def joke():
    response = request.json['message']
    audio_file = text_to_speech(response)
    return render_template("joke.html", joke=response, audio_file=audio_file)


@app.route('/time', methods=['POST'])
def time():
    response = request.json['details']['time_numeric']
    # response = '12:33'
    audio_file = text_to_speech(request.json['message'])
    print(request.json)
    return render_template("time.html", time=response, audio_file=audio_file)


if __name__ == '__main__':
    # app.run()
    # Uncomment this to run at port 80, and comment the line above
    app.run(host='0.0.0.0', port=80, ssl_context='adhoc')
