from flask_wtf import FlaskForm
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired


class SendAlarmData(FlaskForm):
    alarm_time = TimeField('Alarm time')
