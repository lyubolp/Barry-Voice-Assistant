from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_timer_intent(engine: IntentDeterminationEngine):
    timer_keywords = [
        "timer"
    ]

    for tk in timer_keywords:
        engine.register_entity(tk, "TimerKeyword")

    engine.register_regex_entity("for (?P<Time>.*)")

    # structure intent
    timer_intent = IntentBuilder("TimerIntent")\
        .require("TimerKeyword")\
        .optionally("Time")\
        .build()

    engine.register_intent_parser(timer_intent)
