from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_alarm_intent(engine: IntentDeterminationEngine):
    alarm_keywords = [
        "alarm"
    ]

    for ak in alarm_keywords:
        engine.register_entity(ak, "AlarmKeyword")

    engine.register_regex_entity("(for|at) (?P<Time>.*)")

    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    for w in weekdays:
        engine.register_entity(w, "Weekday")

    # structure intent
    alarm_intent = IntentBuilder("AlarmIntent")\
        .require("AlarmKeyword")\
        .require("Time")\
        .optionally("Weekday")\
        .build()

    engine.register_intent_parser(alarm_intent)
