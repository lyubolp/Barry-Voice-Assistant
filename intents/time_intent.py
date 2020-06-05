from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_time_intent(engine: IntentDeterminationEngine):
    time_keywords = [
        "time"
    ]

    for tk in time_keywords:
        engine.register_entity(tk, "TimeKeyword")

    time_intent = IntentBuilder("TimeIntent")\
        .require("TimeKeyword")\
        .build()

    engine.register_intent_parser(time_intent)
