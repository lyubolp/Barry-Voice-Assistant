from flask import Flask, render_template, flash, redirect, request

from alarm import SendAlarmData
from config import Config
from client import client

from news import News
from whatIs import WhatIs

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
    user = {
        'username': 'lyubolp',
        'name': 'Lyubo'
    }
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


if __name__ == '__main__':
    app.run()
