from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_joke_intent(engine: IntentDeterminationEngine):
    # create and register joke vocabulary
    joke_keywords = [
        "joke",
        "make me laugh"
    ]

    for jk in joke_keywords:
        engine.register_entity(jk, "JokeKeyword")

    # structure intent
    weather_intent = IntentBuilder("JokeIntent")\
        .require("JokeKeyword")\
        .build()

    engine.register_intent_parser(weather_intent)
