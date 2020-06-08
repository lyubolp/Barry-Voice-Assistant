"""
Useful links for building intents:
https://github.com/MycroftAI/adapt
https://mycroft-ai.gitbook.io/docs/mycroft-technologies/adapt
https://mycroft-ai.gitbook.io/docs/mycroft-technologies/adapt/adapt-examples
"""
from adapt.engine import IntentDeterminationEngine

from intents.weather_intent import register_weather_intent
from intents.joke_intent import register_joke_intent
from intents.what_is_intent import register_what_is_intent
from intents.time_intent import register_time_intent
from intents.news_intent import register_news_intent
from intents.todo_intent import register_todo_intent
from intents.alarm_intent import register_alarm_intent
from intents.reminder_intent import register_reminder_intent
from intents.timer_intent import register_timer_intent


engine = IntentDeterminationEngine()

register_weather_intent(engine)
register_joke_intent(engine)
register_what_is_intent(engine)
register_time_intent(engine)
register_news_intent(engine)
register_todo_intent(engine)
register_alarm_intent(engine)
register_reminder_intent(engine)
register_timer_intent(engine)


def determine_intent(text: str):
    res_intent = None
    best_confidence = 0

    for intent in engine.determine_intent(text):
        if intent.get('confidence') > best_confidence:
            best_confidence = intent.get('confidence')
            res_intent = intent

    return res_intent
