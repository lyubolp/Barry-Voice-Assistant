from flask import Flask, render_template, flash, redirect

from alarm import SendAlarmData
from config import Config

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
def login():
    form = SendAlarmData()
    if form.validate_on_submit():
        print(form.alarm_time.data)
        return redirect('/')
    return render_template('alarm.html', title='Alarm', alarm=alarm, form=form)
if __name__ == '__main__':
    app.run()
