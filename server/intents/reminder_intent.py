from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_reminder_intent(engine: IntentDeterminationEngine):
    reminder_keywords = [
        "remind"
    ]

    for rk in reminder_keywords:
        engine.register_entity(rk, "ReminderKeyword")

    engine.register_regex_entity("to (?P<Action>.*) in")
    engine.register_regex_entity("in (?P<Time>.*)")

    # structure intent
    reminder_intent = IntentBuilder("ReminderIntent")\
        .require("ReminderKeyword")\
        .require("Action") \
        .require("Time") \
        .build()

    engine.register_intent_parser(reminder_intent)
