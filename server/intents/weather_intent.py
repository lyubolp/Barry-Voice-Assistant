from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_weather_intent(engine: IntentDeterminationEngine):
    # create and register weather vocabulary
    weather_keyword = [
        "weather"
    ]

    for wk in weather_keyword:
        engine.register_entity(wk, "WeatherKeyword")

    # create regex to parse out locations
    engine.register_regex_entity("in (?P<Location>.*)")

    # structure intent
    weather_intent = IntentBuilder("WeatherIntent")\
        .require("WeatherKeyword")\
        .optionally("Location")\
        .build()

    engine.register_intent_parser(weather_intent)
