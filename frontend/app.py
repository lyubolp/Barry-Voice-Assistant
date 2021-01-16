from hashlib import sha256

from flask import Flask, render_template, flash, redirect, request, url_for, make_response
from flask_login import LoginManager, current_user, login_user

from client.client import register, login
from config import Config
from client import client

from news import News
from user import User
from whatIs import WhatIs

app = Flask(__name__)
app.config.from_object(Config)


def isUserLoggedIn() -> bool:
    return not request.cookies.get('userToken') is None and request.cookies.get('userToken') is not 'None'


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


@app.route('/news', methods=['POST'])
def news():

    response = request.form['command-response']
    news_objects = []
    for news_piece in response:
        news_objects.append(News(news_piece))

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


if __name__ == '__main__':
    app.run()
