import json

from flask import Flask, render_template, flash, redirect

from alarm import SendAlarmData
from config import Config
from client import client
from types import SimpleNamespace

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
            response = client.execute_command(token, "news about sport")

            news_objects = []

            print("Response: ", response)

            for news_piece in response['details']:
                print(news_piece)
                news_objects.append(json.loads(news_piece))
            # x = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
            # print(x.name, x.hometown.name, x.hometown.id)
        except Exception as err:
            print("Failed to execute command :(")
            print(err)

        print()
    except Exception as err:
        print("Failed to login :(")
        print(err)

    return render_template('news.html', title='News')


if __name__ == '__main__':
    app.run()
