from hashlib import sha256

from flask import Flask, render_template, flash, redirect, request, url_for, make_response
from flask_login import LoginManager, current_user, login_user

from alarm import SendAlarmData
from client.client import register, login
from config import Config
from client import client

from news import News
from user import User
from whatIs import WhatIs

app = Flask(__name__)
app.config.from_object(Config)


def isUserLoggedIn() -> bool:
    return request.cookies.get('userToken') is None

@app.route('/')
@app.route('/index')
def index():
    if not request.cookies.get('userToken') is None:
        token = request.cookies.get('userToken')
        user = {
            'username': request.cookies.get('username')
        }
    else:
        user = None

    return render_template('index.html', title='Home', user=user)


@app.route('/alarm')
def alarm():
    alarm = {
        'ring': False,
        'time': '08:30',
    }
    form = SendAlarmData()
    return render_template('alarm.html', title='Alarm', alarm=alarm, form=form)


@app.route('/submit-alarm', methods=['GET', 'POST'])
def submit_alarm():
    form = SendAlarmData()
    if form.validate_on_submit():
        print(form.alarm_time.data)
        return redirect('/')
    return render_template('alarm.html', title='Alarm', alarm=alarm, form=form)


@app.route('/news')
def news():
    try:
        token = client.login('luchevz@gmail.com', '123123')
        # Execute command
        try:
            response = client.execute_command(token, "news about tech")
            news_objects = []
            for news_piece in response['details']:
                print(news_piece)
                author = news_piece['author']
                content = news_piece['content']
                description = news_piece['description']
                published_at = news_piece['publishedAt']
                source = (news_piece['source']['id'], news_piece['source']['name'])
                title = news_piece['title']
                url = news_piece['url']
                url_image = news_piece['urlToImage']

                news_objects.append(News(author, content, description, published_at, source, title, url, url_image))

        except Exception as err:
            print("Failed to execute command :(")
            print(err)

    except Exception as err:
        print("Failed to login :(")
        print(err)

    return render_template('news.html', title='News', news=news_objects)


@app.route('/what-is')
def what_is():
    try:
        token = client.login('luchevz@gmail.com', '123123')
        # Execute command
        try:
            response = client.execute_command(token, "what is " + request.args['article'])
            article = WhatIs(response['details']['title'], response['details']['content'], response['details']['image_url'])
        except Exception as err:
            print("Failed to execute command :(")
            print(err)

        print()
    except Exception as err:
        print("Failed to login :(")
        print(err)

    return render_template('what-is.html', title='What is ?', article=article)


@app.route('/login')
def loginPath():
    if isUserLoggedIn():
        return redirect('/')
    else:
        return render_template("login.html")


@app.route('/handle-login', methods=['POST'])
def handle_login():
    try:
        username = request.form['username']
        password = request.form['password']
        # token = login('luchevz@gmail.com', '123123')
        print(username, password)
        token = login(username, password)

        resp = make_response(redirect('/'))
        resp.set_cookie('userToken', token)
        resp.set_cookie('username', username)
        return resp

    except Exception as err:
        print("Failed to register user :(")
        print(err)
        print()

        return err


@app.route('/register')
def registerPath():
    if request.cookies.get('userToken') is None:
        return render_template("register.html")
    else:
        return redirect('/')


@app.route('/handle-register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    password_repeat = request.form['passwordRepeat']

    if password == password_repeat:
        try:
            token = register(username, password)
        except Exception as err:
            return render_template('register.html', errors=err.args)

        resp = make_response(redirect('/'))
        resp.set_cookie('userToken', token)
        resp.set_cookie('username', username)
        return resp
    else:
        return render_template('register.html', errors=['Passwords don\'t match'])


if __name__ == '__main__':
    app.run()
