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


engine = IntentDeterminationEngine()

register_weather_intent(engine)
register_joke_intent(engine)
register_what_is_intent(engine)
register_time_intent(engine)


def determine_intent(text: str):
    res_intent = None
    best_confidence = 0

    for intent in engine.determine_intent(text):
        if intent.get('confidence') > best_confidence:
            best_confidence = intent.get('confidence')
            res_intent = intent

    return res_intent
